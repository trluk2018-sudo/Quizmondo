# -*- coding: utf-8 -*-
"""Choosing which ad to show, and deciding whether it is fit to show at all.

Quizmondo is played by children, so the rule here is strict and deliberately
dull: an ad runs only once a human has ticked the family-safe box in admin.
Everything in this module exists to make that human's decision an informed one
rather than a reflex — the automated check flags what it can and refuses to be
the final word on anything.
"""
import json
import random
import re
import urllib.parse
import urllib.request
from datetime import datetime

from ..models import Advertisement, AD_SLOTS


# Words that have no business on a children's quiz site. Matched on word
# boundaries against the headline, body, alt text, link and video title.
# This list is a tripwire, not a filter: it catches the obvious and the lazy,
# and the admin still has to look.
BLOCKED_TERMS = [
    'casino', 'betting', 'bet365', 'bookmaker', 'poker', 'roulette', 'slots',
    'bingo', 'gamble', 'gambling', 'odds boost', 'free spins', 'no deposit',
    'porn', 'xxx', 'adult only', 'adults only', 'escort', 'hookup', 'nsfw',
    'onlyfans', 'strip club', 'sex',
    'vape', 'vaping', 'e-cigarette', 'cigarette', 'tobacco', 'nicotine',
    'beer', 'lager', 'vodka', 'whisky', 'whiskey', 'gin', 'rum', 'cocktail',
    'alcohol', 'booze', 'brewery', 'off licence',
    'cbd', 'cannabis', 'weed', 'vaporizer',
    'loan', 'payday', 'quick cash', 'crypto', 'bitcoin', 'forex', 'trading signals',
    'weight loss', 'diet pill', 'slimming',
    'dating', 'singles near you', 'meet women', 'meet men',
]

# Whole domains that are never acceptable, however the copy is worded.
BLOCKED_DOMAINS = [
    'bet365.com', 'williamhill.com', 'paddypower.com', 'ladbrokes.com',
    'coral.co.uk', 'skybet.com', 'betfair.com', 'unibet.co.uk', '888casino.com',
    'pornhub.com', 'onlyfans.com', 'xvideos.com', 'xhamster.com',
    'tinder.com', 'ashleymadison.com',
]

# A pub league is a real part of this site, so the drink words above would
# flag every venue ad. These phrases pardon that specific case.
PUB_CONTEXT = [
    'pub quiz', 'quiz night', 'quiz league', 'venue', 'function room',
    'family pub', 'carvery', 'sunday roast',
]


def _haystack(ad):
    parts = [
        ad.name, ad.headline, ad.body_text, ad.alt_text,
        ad.link_url, ad.video_title, ad.advertiser,
    ]
    return ' '.join(p for p in parts if p).lower()


def _domain(url):
    try:
        host = urllib.parse.urlparse(url if '//' in (url or '') else '//' + (url or '')).netloc
    except Exception:
        return ''
    return host.lower().lstrip('www.')


def fetch_youtube_title(video_id, timeout=8):
    """The video's real title, via oEmbed, which needs no API key.

    Worth having because the pasted URL tells you nothing: a link called
    'our new advert' can point at anything at all.
    """
    if not video_id:
        return ''
    url = ('https://www.youtube.com/oembed?format=json&url='
           + urllib.parse.quote('https://www.youtube.com/watch?v=' + video_id, safe=''))
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Quizmondo/1.0'})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode('utf-8', 'replace'))
        title = (data.get('title') or '').strip()
        author = (data.get('author_name') or '').strip()
        return ('%s — %s' % (title, author)).strip(' —')
    except Exception:
        return ''


def check_family_safe(ad):
    """Look over an ad and report what is wrong with it.

    Returns (looks_ok, notes). A False never means 'blocked for good' and a
    True never means 'approved' — only the admin's tick does that. This is
    here so nobody has to spot 'FREE SPINS' in a 300-character body field at
    half past eleven at night.
    """
    notes = []
    text = _haystack(ad)

    pub_ok = any(phrase in text for phrase in PUB_CONTEXT)
    drink_words = {'beer', 'lager', 'vodka', 'whisky', 'whiskey', 'gin', 'rum',
                   'cocktail', 'alcohol', 'booze', 'brewery', 'off licence'}

    for term in BLOCKED_TERMS:
        if re.search(r'(?<!\w)%s(?!\w)' % re.escape(term), text):
            if term in drink_words and pub_ok:
                notes.append('Mentions "%s", but reads like a pub venue ad. Check it is '
                             'promoting the quiz night and not the drink.' % term)
            else:
                notes.append('Contains "%s", which is not suitable for an all-ages site.' % term)

    for url in (ad.link_url, ad.image_url, ad.video_url):
        host = _domain(url)
        if not host:
            continue
        for bad in BLOCKED_DOMAINS:
            if host == bad or host.endswith('.' + bad):
                notes.append('Links to %s, which is blocked outright.' % host)

    if ad.kind == 'image':
        if not ad.image_url:
            notes.append('No image set.')
        if not ad.alt_text:
            notes.append('No alt text. Needed for screen readers, and it makes the '
                         'advertiser say in words what the picture shows.')
    if ad.kind == 'youtube':
        if not ad.youtube_id():
            notes.append('The video URL is not a YouTube link we recognise.')
        elif not ad.video_title:
            notes.append('Could not read the video title from YouTube. Watch it before approving.')
    if ad.kind == 'adsense' and not ad.adsense_slot_id:
        notes.append('No AdSense slot id.')

    # Column defaults only apply once a row is saved, so everything read here
    # has to cope with None on an ad that is still being typed in.
    link = (ad.link_url or '').strip()
    if link and not link.startswith(('http://', 'https://', '/')):
        notes.append('The click-through link is not a full URL.')
    if link.startswith('http://'):
        notes.append('Click-through is plain http, not https.')

    blocking = [n for n in notes if 'not suitable' in n or 'blocked outright' in n]
    return (not blocking), notes


def refresh_video_title(ad):
    """Fill in the YouTube title so the safety check has something to read."""
    if ad.kind == 'youtube':
        vid = ad.youtube_id()
        if vid:
            ad.video_title = fetch_youtube_title(vid) or ad.video_title
    return ad.video_title


def pick_ads(slot, limit=1, now=None):
    """The ads to show in a slot, best first.

    Paid work comes first: a direct-sold image or video is what somebody is
    being invoiced for. AdSense fills what is unsold. A house ad fills what is
    left, so a quiet week shows our own games instead of a gap.
    """
    now = now or datetime.utcnow()
    candidates = Advertisement.query.filter(
        Advertisement.slot == slot,
        Advertisement.is_active.is_(True),
        Advertisement.approved_family.is_(True),
    ).all()
    live = [a for a in candidates if a.is_live(now)]

    tiers = (
        [a for a in live if a.kind in ('image', 'youtube')],
        [a for a in live if a.kind == 'adsense'],
        [a for a in live if a.kind == 'house'],
    )

    chosen = []
    for tier in tiers:
        if len(chosen) >= limit:
            break
        pool = list(tier)
        while pool and len(chosen) < limit:
            weights = [max(1, int(a.weight or 1)) for a in pool]
            pick = random.choices(pool, weights=weights, k=1)[0]
            chosen.append(pick)
            pool.remove(pick)
    return chosen


def slot_choices():
    return list(AD_SLOTS)
