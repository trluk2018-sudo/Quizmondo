# -*- coding: utf-8 -*-
"""Counting what the ads actually did.

Two numbers an advertiser will ask about, and both are recorded here rather
than guessed at:

* an impression is counted when the ad is really on screen, not when the page
  that holds it is sent. A banner nobody scrolled to has not been seen, and
  billing for it is how a site loses an advertiser.
* a click is counted on the way out, by sending the visitor through here
  before the advertiser's site.

Totals live on the ad for the quick view, and a row per ad per day gives the
run of it. Nothing about the visitor is stored: no id, no address, no profile.
"""
from datetime import datetime

from flask import Blueprint, abort, jsonify, redirect, request, session

from ..models import AdStat, Advertisement, db

ads_bp = Blueprint('ads', __name__, url_prefix='/ads')


def _bump(ad, field, amount=1):
    """Add to today's row and to the running total, in one go."""
    today = datetime.utcnow().date()
    row = AdStat.query.filter_by(ad_id=ad.id, day=today).first()
    if not row:
        row = AdStat(ad_id=ad.id, day=today, impressions=0, clicks=0)
        db.session.add(row)
    setattr(row, field, (getattr(row, field) or 0) + amount)
    setattr(ad, field, (getattr(ad, field) or 0) + amount)


@ads_bp.route('/<int:ad_id>/seen', methods=['POST'])
def ad_seen(ad_id):
    """The ad came into view. Counted once per ad per page view.

    The page sends a nonce it generated on load; we remember the nonces this
    session has already counted, so a visitor scrolling up and down past the
    same banner does not bill the advertiser five times over.
    """
    ad = Advertisement.query.get(ad_id)
    if not ad or not ad.is_live():
        return jsonify({'ok': False}), 404

    nonce = (request.form.get('n') or request.json.get('n') if request.is_json else None) \
        or request.form.get('n') or ''
    key = '%s:%s' % (ad_id, nonce)
    seen = session.get('ads_seen') or []
    if not nonce or key in seen:
        return jsonify({'ok': True, 'counted': False})

    _bump(ad, 'impressions')
    db.session.commit()

    # Keep the list short; it only has to cover the page in front of them.
    seen.append(key)
    session['ads_seen'] = seen[-40:]
    return jsonify({'ok': True, 'counted': True})


@ads_bp.route('/<int:ad_id>/click')
def ad_click(ad_id):
    """Count the click, then send them where the ad said."""
    ad = Advertisement.query.get_or_404(ad_id)
    _bump(ad, 'clicks')
    db.session.commit()

    target = (ad.link_url or '').strip()
    # Only ever leave for a real destination. An open redirect in an ad link is
    # exactly the hole somebody would come looking for.
    if not target or not target.startswith(('http://', 'https://', '/')):
        abort(404)
    return redirect(target, code=302)
