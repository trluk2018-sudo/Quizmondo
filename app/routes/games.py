"""Single-player mini games.

A self-contained blueprint: the hub lists every game, each game gets its own
route and template, and all gameplay runs in vanilla JS in the page. Nothing
here touches Arena matches or Pub League scoring — a mini game only ever adds
XP and coins to the player's profile, the same way finishing a duel round does.
"""
import random
from datetime import date, datetime, timedelta

from flask import (Blueprint, abort, flash, jsonify, redirect, render_template,
                   request, session, url_for)

from ..models import db, PlayerProfile, SiteSetting
from ..models_games import MiniGameScore, DailyChallengeScore
from ..utils import game_data as gd
from .arena import get_current_player, AVATAR_LOOKUP
from .public import inject_global_data

games_bp = Blueprint('games', __name__, url_prefix='/games')


@games_bp.context_processor
def inject_games_global_data():
    data = inject_global_data()
    data['avatar_lookup'] = AVATAR_LOOKUP
    return data


# ---------------------------------------------------------------------------
# Guests
#
# A guest may play every mini game. What they may not do is leave a trail: no
# profile row, no score row, nothing to tidy up after them. Their scores ride
# along in the signed session cookie instead, which means they can see their
# best for the afternoon and lose it when they close the browser.
#
# The cookie is also the carrot. "You scored 840 and it is not saved" is the
# best argument for an account there is, and the moment they make one those
# scores are moved into the table rather than thrown away.
# ---------------------------------------------------------------------------

GUEST_SCORES = 'qm_guest_scores'


def _has_account() -> bool:
    return bool(session.get('user_id'))


def _guests_recorded() -> bool:
    """Whether an operator has asked for guest rows in the table after all."""
    return SiteSetting.get('guest_scores_saved') == '1'


def _guest_bests() -> dict:
    scores = session.get(GUEST_SCORES)
    return scores if isinstance(scores, dict) else {}


def _remember_guest_score(key, score):
    """Hold one guest score in the cookie. Returns (best, improved, plays)."""
    scores = dict(_guest_bests())
    entry = scores.get(key) or {}
    best = int(entry.get('best') or 0)
    plays = int(entry.get('plays') or 0) + 1
    improved = score > best
    scores[key] = {'best': max(best, score), 'last': score, 'plays': plays}
    session[GUEST_SCORES] = scores
    session.modified = True
    return scores[key]['best'], improved, plays


@games_bp.before_app_request
def adopt_guest_scores():
    """Move a cookie's worth of guest scores into the table once they sign up.

    Runs app wide rather than at registration, because the registration route
    belongs to the Arena. The common case costs one dictionary lookup, since
    there is nothing to do unless the cookie holds scores and the visitor now
    has an account.
    """
    if not session.get(GUEST_SCORES) or not _has_account():
        return
    scores = _guest_bests()
    session.pop(GUEST_SCORES, None)
    session.modified = True
    try:
        player = get_current_player()
        if not player:
            return
        for key, entry in scores.items():
            if key not in GAME_BY_KEY:
                continue
            score = int(entry.get('best') or 0)
            row = MiniGameScore.query.filter_by(
                player_session=player.session_key, game_key=key).first()
            if row is None:
                row = MiniGameScore(player_session=player.session_key, game_key=key,
                                    best_score=0, plays=0)
                db.session.add(row)
            row.display_name = player.display_name
            row.avatar_key = player.avatar_key
            row.plays = (row.plays or 0) + int(entry.get('plays') or 1)
            row.last_score = int(entry.get('last') or score)
            row.last_played_at = datetime.utcnow()
            if score > (row.best_score or 0):
                row.best_score = score
                row.best_at = datetime.utcnow()
        db.session.commit()
    except Exception:
        # Carrying scores over is a courtesy. It must never be the reason a
        # newly registered player cannot load a page.
        db.session.rollback()


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
# xp_rate turns a game's own score into XP. Mini games are meant to top up a
# player's level between duels, not replace them, so each rate is tuned to land
# a good run somewhere around 60-180 XP, under the XP_CAP below.

XP_CAP = 220

GROUPS = [
    ('word', 'Word Games', '🔤', 'Letters, clues and quick thinking'),
    ('puzzle', 'Puzzles & Tiles', '🧩', 'Slide, swap and solve'),
    ('memory', 'Memory & Reflex', '🧠', 'How much can you hold in your head?'),
]

GAMES = [
    # ---- Word games -------------------------------------------------------
    {
        'key': 'word-search', 'title': 'Word Search', 'icon': '🔍', 'group': 'word',
        'blurb': 'Hunt eight hidden words in the letter grid before the clock runs out.',
        'accent': 'from-purple-600 to-indigo-700', 'border': 'border-purple-500/40',
        'xp_rate': 0.09, 'score_unit': 'pts',
        'how': 'Drag or tap-and-tap across a run of letters to claim a word. Words go in any direction, backwards included.',
    },
    {
        'key': 'anagrams', 'title': 'Anagram Attack', 'icon': '🔀', 'group': 'word',
        'blurb': 'Unscramble as many words as you can in ninety seconds.',
        'accent': 'from-cyan-500 to-blue-700', 'border': 'border-cyan-500/40',
        'xp_rate': 0.12, 'score_unit': 'pts',
        'how': 'Type the unscrambled word and hit enter. Each correct answer adds time; a wrong one costs you nothing but the clock.',
    },
    {
        'key': 'word-ladder', 'title': 'Word Ladder', 'icon': '🪜', 'group': 'word',
        'blurb': 'Turn one word into another, changing a single letter at a time.',
        'accent': 'from-emerald-500 to-teal-700', 'border': 'border-emerald-500/40',
        'xp_rate': 0.14, 'score_unit': 'pts',
        'how': 'Every rung must be a real four-letter word and may differ from the one above it by exactly one letter.',
    },
    {
        'key': 'crossword', 'title': 'Trivia Crossword', 'icon': '✏️', 'group': 'word',
        'blurb': 'A compact crossword built live from real Quizmondo questions.',
        'accent': 'from-amber-500 to-orange-600', 'border': 'border-amber-500/40',
        'xp_rate': 0.11, 'score_unit': 'pts',
        'how': 'Tap a square, read the clue underneath and type the answer. Every clue is a genuine trivia question from the Arena.',
    },
    {
        'key': 'hangman', 'title': 'Gallows', 'icon': '💀', 'group': 'word',
        'blurb': 'Guess the hidden phrase one letter at a time. Six lives.',
        'accent': 'from-rose-600 to-slate-800', 'border': 'border-rose-500/40',
        'xp_rate': 0.16, 'score_unit': 'pts',
        'how': 'Pick letters from the keyboard. Every miss costs a life; clear the phrase to bank the round and move on.',
    },
    {
        'key': 'word-chain', 'title': 'Word Chain', 'icon': '⛓️', 'group': 'word',
        'blurb': 'Each word must start with the letter the last one ended on.',
        'accent': 'from-violet-600 to-fuchsia-700', 'border': 'border-violet-500/40',
        'xp_rate': 0.13, 'score_unit': 'pts',
        'how': 'Four letters or longer, no repeats, and the clock keeps ticking. Longer words score far more.',
    },
    {
        'key': 'boggle', 'title': 'Letter Shake', 'icon': '🎲', 'group': 'word',
        'blurb': 'Find every word you can in a shaken four-by-four letter grid.',
        'accent': 'from-sky-500 to-indigo-700', 'border': 'border-sky-500/40',
        'xp_rate': 0.10, 'score_unit': 'pts',
        'how': 'Tap neighbouring letters to build a word — across, down or diagonally. Three letters minimum.',
    },
    {
        'key': 'word-wheel', 'title': 'Word Wheel', 'icon': '🎯', 'group': 'word',
        'blurb': 'Nine letters, one compulsory centre. How many words can you see?',
        'accent': 'from-teal-500 to-emerald-700', 'border': 'border-teal-500/40',
        'xp_rate': 0.11, 'score_unit': 'pts',
        'how': 'Every word must use the centre letter and may use each outer letter once. Find the nine-letter word for a big bonus.',
    },
    {
        'key': 'missing-vowels', 'title': 'Missing Vowels', 'icon': '✂️', 'group': 'word',
        'blurb': 'The vowels are gone and the spaces have moved. Name the answer.',
        'accent': 'from-fuchsia-600 to-purple-800', 'border': 'border-fuchsia-500/40',
        'xp_rate': 0.14, 'score_unit': 'pts',
        'how': 'Read the mangled letters aloud in your head — it is the fastest way in. Type what you think it says.',
    },
    {
        'key': 'five-guess', 'title': 'Quizmondo Five', 'icon': '🟩', 'group': 'word',
        'blurb': 'Six goes to crack a five-letter word. Green means right, amber means close.',
        'accent': 'from-lime-500 to-emerald-700', 'border': 'border-lime-500/40',
        'xp_rate': 0.18, 'score_unit': 'pts',
        'how': 'Guess a real five-letter word. Green is the right letter in the right place, amber is right letter wrong place.',
    },
    {
        'key': 'emoji-riddles', 'title': 'Emoji Riddles', 'icon': '🧐', 'group': 'word',
        'blurb': 'Films, food, sayings and landmarks, told entirely in emoji.',
        'accent': 'from-orange-500 to-rose-600', 'border': 'border-orange-500/40',
        'xp_rate': 0.15, 'score_unit': 'pts',
        'how': 'Read the emoji, type the answer. Stuck? Burn a hint to reveal a letter — it costs you points, not the round.',
    },
    {
        'key': 'sort-it', 'title': 'Sort It', 'icon': '🗂️', 'group': 'word',
        'blurb': 'Twelve things, two or three boxes, one ticking clock.',
        'accent': 'from-blue-500 to-violet-700', 'border': 'border-blue-500/40',
        'xp_rate': 0.13, 'score_unit': 'pts',
        'how': 'Tap the box each item belongs in. Get it right and the streak multiplier climbs.',
    },
    # ---- Puzzles ----------------------------------------------------------
    {
        'key': 'slide-image', 'title': 'Picture Slide', 'icon': '🖼️', 'group': 'puzzle',
        'blurb': 'A flag, badge or logo, cut into tiles and shuffled. Slide it back.',
        'accent': 'from-indigo-500 to-purple-700', 'border': 'border-indigo-500/40',
        'xp_rate': 0.16, 'score_unit': 'pts',
        'how': 'Tap any tile next to the gap to slide it. Fewer moves and less time means a far better score.',
    },
    {
        'key': 'slide-word', 'title': 'Word Slide', 'icon': '🔡', 'group': 'puzzle',
        'blurb': 'The same sliding puzzle, but the tiles spell a word.',
        'accent': 'from-cyan-500 to-teal-700', 'border': 'border-cyan-500/40',
        'xp_rate': 0.16, 'score_unit': 'pts',
        'how': 'Slide the lettered tiles until the word reads correctly, left to right, top to bottom.',
    },
    {
        'key': 'pic-swap', 'title': 'Picture Swap', 'icon': '🔄', 'group': 'puzzle',
        'blurb': 'No gap to slide into — tap two tiles to swap them instead.',
        'accent': 'from-pink-500 to-rose-700', 'border': 'border-pink-500/40',
        'xp_rate': 0.16, 'score_unit': 'pts',
        'how': 'Tap one tile, then tap another to trade their places. Rebuild the picture in as few swaps as you can.',
    },
    # ---- Memory -----------------------------------------------------------
    {
        'key': 'pairs', 'title': 'Memory Pairs', 'icon': '🃏', 'group': 'memory',
        'blurb': 'Classic concentration, played with flags, badges and logos.',
        'accent': 'from-emerald-500 to-cyan-700', 'border': 'border-emerald-500/40',
        'xp_rate': 0.15, 'score_unit': 'pts',
        'how': 'Turn two cards over. A match stays up, a miss flips back. Clear the board before the clock beats you.',
    },
    {
        'key': 'sequence', 'title': 'Sequence Recall', 'icon': '🔔', 'group': 'memory',
        'blurb': 'Watch the pads light up, then repeat the pattern back.',
        'accent': 'from-amber-500 to-rose-600', 'border': 'border-amber-500/40',
        'xp_rate': 0.20, 'score_unit': 'pts',
        'how': 'The sequence grows by one every round. Each pad has its own note, so listen as well as watch.',
    },
    {
        'key': 'spot-difference', 'title': 'Spot The Odd One', 'icon': '👀', 'group': 'memory',
        'blurb': 'One tile in the grid is not quite like the others. Find it, fast.',
        'accent': 'from-rose-500 to-orange-600', 'border': 'border-rose-500/40',
        'xp_rate': 0.14, 'score_unit': 'pts',
        'how': 'The grid grows and the difference shrinks every round. Tap the odd one out before the timer empties.',
    },
    {
        'key': 'flag-flash', 'title': 'Flag Flash', 'icon': '⚡', 'group': 'memory',
        'blurb': 'An image flashes up for a second. Pick it out of the line-up.',
        'accent': 'from-violet-500 to-blue-700', 'border': 'border-violet-500/40',
        'xp_rate': 0.17, 'score_unit': 'pts',
        'how': 'Study the flash, then find the same flag, badge or logo among the choices. The flash gets shorter as you go.',
    },
    {
        'key': 'grid-recall', 'title': 'Pattern Recall', 'icon': '🔢', 'group': 'memory',
        'blurb': 'Tiles light up for a moment. Tap exactly those tiles back.',
        'accent': 'from-purple-500 to-cyan-700', 'border': 'border-purple-500/40',
        'xp_rate': 0.19, 'score_unit': 'pts',
        'how': 'Order does not matter, but a wrong tile costs a life. The pattern gains a tile every round you survive.',
    },
    {
        'key': 'digit-span', 'title': 'Digit Span', 'icon': '🧮', 'group': 'memory',
        'blurb': 'A number appears, then vanishes. Type it back from memory.',
        'accent': 'from-slate-500 to-purple-800', 'border': 'border-slate-500/40',
        'xp_rate': 0.22, 'score_unit': 'pts',
        'how': 'One extra digit every round. Most people stall somewhere between seven and nine — see where you land.',
    },
]

GAME_BY_KEY = {g['key']: g for g in GAMES}


def built_games():
    """Only the games whose template actually exists.

    The registry is written ahead of the templates, so a game that has not been
    built yet is simply left off the hub instead of handing a player a 500.
    """
    from flask import current_app

    out = []
    for g in GAMES:
        try:
            current_app.jinja_env.get_template('themes/quizhub/games/%s.html' % g['key'])
        except Exception:
            continue
        out.append(g)
    return out


# ---------------------------------------------------------------------------
# Score helpers
# ---------------------------------------------------------------------------

class _GuestBest:
    """A guest's cookie score, shaped like a MiniGameScore row.

    The hub and the game shell read best_score and plays off whatever they are
    given, so a guest's figures can go through the same templates.
    """
    __slots__ = ('game_key', 'best_score', 'last_score', 'plays', 'saved')

    def __init__(self, game_key, entry):
        self.game_key = game_key
        self.best_score = int(entry.get('best') or 0)
        self.last_score = int(entry.get('last') or 0)
        self.plays = int(entry.get('plays') or 0)
        self.saved = False


def _score_rows(session_key=None):
    """Everyone's own figures, from the table or from the cookie."""
    if not _has_account() and not _guests_recorded():
        return {key: _GuestBest(key, entry) for key, entry in _guest_bests().items()}
    if not session_key:
        return {}
    rows = MiniGameScore.query.filter_by(player_session=session_key).all()
    return {r.game_key: r for r in rows}


def _leaderboard(game_key, limit=10):
    return MiniGameScore.query.filter(
        MiniGameScore.game_key == game_key,
        MiniGameScore.best_score > 0,
    ).order_by(MiniGameScore.best_score.desc(), MiniGameScore.best_at.asc()).limit(limit).all()


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

@games_bp.route('/')
def hub():
    player = get_current_player(persist=False)
    bests = _score_rows(player.session_key if player else None)

    total_plays = sum((r.plays or 0) for r in bests.values())
    played_count = sum(1 for r in bests.values() if (r.plays or 0) > 0)

    today = date.today()
    today_spec = gd.daily_spec(today)
    daily_done = bool(player and DailyChallengeScore.query.filter_by(
        player_session=player.session_key, challenge_key=today_spec['key']
    ).first())

    return render_template(
        'themes/quizhub/games/hub.html',
        player=player,
        daily_spec=today_spec,
        daily_done=daily_done,
        games=built_games(),
        groups=GROUPS,
        bests=bests,
        total_plays=total_plays,
        played_count=played_count,
    )


def _render_game(key, **payload):
    meta = GAME_BY_KEY.get(key)
    if not meta:
        abort(404)
    from flask import current_app
    try:
        current_app.jinja_env.get_template(f'themes/quizhub/games/{key}.html')
    except Exception:
        abort(404)  # registered but not built yet
    player = get_current_player(persist=False)
    row = _score_rows(player.session_key if player else None).get(key)
    return render_template(
        f'themes/quizhub/games/{key}.html',
        game=meta,
        games=built_games(),
        player=player,
        scores_saved=_has_account() or _guests_recorded(),
        best=(row.best_score if row else 0),
        plays=(row.plays if row else 0),
        leaderboard=_leaderboard(key),
        **payload,
    )


@games_bp.route('/word-search')
def word_search():
    rng = random.Random()
    theme = rng.choice(gd.WORD_SEARCH_THEMES)
    return _render_game('word-search', themes=gd.WORD_SEARCH_THEMES, theme=theme)


@games_bp.route('/anagrams')
def anagrams():
    rng = random.Random()
    bank = gd.shuffled(gd.ANAGRAM_BANK, rng)[:40]
    return _render_game('anagrams', bank=[{'word': w, 'hint': h} for w, h in bank])


@games_bp.route('/word-ladder')
def word_ladder():
    rng = random.Random()
    puzzles = []
    for steps in (3, 4, 4, 5, 5):
        pz = gd.word_ladder(rng, steps=steps)
        if pz:
            puzzles.append(pz)
    # Rungs are checked over the API against the full dictionary.
    return _render_game('word-ladder', puzzles=puzzles)


@games_bp.route('/crossword')
def crossword():
    rng = random.Random()
    puzzle = gd.crossword_puzzle(rng)
    return _render_game('crossword', puzzle=puzzle)


@games_bp.route('/hangman')
def hangman():
    rng = random.Random()
    bank = gd.shuffled(gd.HANGMAN_BANK, rng)[:12]
    return _render_game('hangman', bank=[{'phrase': p, 'category': c} for p, c in bank])


@games_bp.route('/word-chain')
def word_chain():
    return _render_game('word-chain')


@games_bp.route('/boggle')
def boggle():
    rng = random.Random()
    return _render_game('boggle', letters=gd.roll_boggle(rng))


@games_bp.route('/word-wheel')
def word_wheel():
    rng = random.Random()
    return _render_game('word-wheel', puzzle=gd.wheel_puzzle(rng))


@games_bp.route('/missing-vowels')
def missing_vowels():
    rng = random.Random()
    return _render_game('missing-vowels', sets=gd.shuffled(gd.MISSING_VOWELS, rng)[:6])


@games_bp.route('/five-guess')
def five_guess():
    rng = random.Random()
    # Answers come from the harvested common-word list, so nobody is asked to
    # guess something obscure. Guesses are checked against every five-letter
    # word in the dictionary, which is small enough to send with the page.
    # Guesses are checked against the full dictionary over the API rather than
    # inlined: 16,000 five-letter words would quadruple the size of the page.
    answers = gd.shuffled([w.upper() for w in gd.words_of_length(5)], rng)[:400]
    return _render_game('five-guess', answers=answers)


@games_bp.route('/emoji-riddles')
def emoji_riddles():
    rng = random.Random()
    return _render_game('emoji-riddles', bank=gd.shuffled(gd.EMOJI_RIDDLES, rng)[:20])


@games_bp.route('/sort-it')
def sort_it():
    rng = random.Random()
    sets = []
    for s in gd.shuffled(gd.SORT_SETS, rng)[:4]:
        sets.append({
            'title': s['title'],
            'buckets': s['buckets'],
            'items': [{'label': lbl, 'bucket': b} for lbl, b in gd.shuffled(s['items'], rng)],
        })
    return _render_game('sort-it', sets=sets)


@games_bp.route('/slide-image')
def slide_image():
    rng = random.Random()
    pics = gd.image_pairs(limit=80)
    rng.shuffle(pics)
    return _render_game('slide-image', pics=pics[:20])


@games_bp.route('/slide-word')
def slide_word():
    rng = random.Random()
    pool = [w.upper() for w in gd.words_of_length(8) if w.isalpha()]
    words = gd.shuffled(pool, rng)[:30]
    return _render_game('slide-word', words=words)


@games_bp.route('/pic-swap')
def pic_swap():
    rng = random.Random()
    pics = gd.image_pairs(limit=80)
    rng.shuffle(pics)
    return _render_game('pic-swap', pics=pics[:20])


@games_bp.route('/pairs')
def pairs():
    rng = random.Random()
    pics = gd.image_pairs(limit=120)
    rng.shuffle(pics)
    return _render_game('pairs', pics=pics[:40])


@games_bp.route('/sequence')
def sequence():
    return _render_game('sequence')


@games_bp.route('/spot-difference')
def spot_difference():
    return _render_game('spot-difference')


@games_bp.route('/flag-flash')
def flag_flash():
    rng = random.Random()
    pics = gd.image_pairs(limit=160)
    rng.shuffle(pics)
    return _render_game('flag-flash', pics=pics[:60])


@games_bp.route('/grid-recall')
def grid_recall():
    return _render_game('grid-recall')


@games_bp.route('/digit-span')
def digit_span():
    return _render_game('digit-span')


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------

@games_bp.route('/api/score', methods=['POST'])
def submit_score():
    data = request.get_json(silent=True) or {}
    key = str(data.get('game') or '')
    meta = GAME_BY_KEY.get(key)
    if not meta:
        return jsonify({'ok': False, 'error': 'unknown game'}), 400

    try:
        score = int(data.get('score') or 0)
    except (TypeError, ValueError):
        score = 0
    score = max(0, min(score, 100000))

    if not _has_account() and not _guests_recorded():
        # Nothing is written anywhere. The score lives in the cookie until
        # they either make an account or close the browser.
        best, improved, plays = _remember_guest_score(key, score)
        return jsonify({
            'ok': True,
            'guest': True,
            'score': score,
            'best': best,
            'improved': improved,
            'xp': 0,
            'coins': 0,
            'plays': plays,
            'signup_url': url_for('arena.player_register'),
            'note': 'Not saved — make an account to keep it.',
        })

    player = get_current_player()  # a submitted score is worth saving a profile for
    row = MiniGameScore.query.filter_by(player_session=player.session_key, game_key=key).first()
    if not row:
        row = MiniGameScore(player_session=player.session_key, game_key=key, best_score=0, plays=0)
        db.session.add(row)

    improved = score > (row.best_score or 0)
    row.display_name = player.display_name
    row.avatar_key = player.avatar_key
    row.last_score = score
    row.plays = (row.plays or 0) + 1
    row.last_played_at = datetime.utcnow()
    if improved:
        row.best_score = score
        row.best_at = datetime.utcnow()

    xp = min(XP_CAP, int(score * meta.get('xp_rate', 0.1)))
    coins = xp // 10
    if xp > 0 and player.id:
        player.add_xp(xp)
        player.coins = (player.coins or 0) + coins
        player.last_active_at = datetime.utcnow()

    db.session.commit()

    rank = MiniGameScore.query.filter(
        MiniGameScore.game_key == key,
        MiniGameScore.best_score > (row.best_score or 0),
    ).count() + 1

    return jsonify({
        'ok': True,
        'score': score,
        'best': row.best_score or 0,
        'improved': improved,
        'xp': xp,
        'coins': coins,
        'level': player.level,
        'rank': rank,
        'plays': row.plays,
    })


# ---------------------------------------------------------------------------
# The daily crossword
# ---------------------------------------------------------------------------

DAILY_CHAMPION_COINS = 250


def _daily_board(challenge_key, limit=20):
    return DailyChallengeScore.query.filter_by(challenge_key=challenge_key).order_by(
        DailyChallengeScore.score.desc(), DailyChallengeScore.seconds_taken.asc()
    ).limit(limit).all()


def _settle_champion(day):
    """Award the previous day's winner, once.

    There is no scheduler in this app, so a finished day is settled the next
    time anybody opens the page. A flag in site settings records that it has
    been paid, which keeps it to one award however many people look.
    """
    key = 'crossword-%s' % day.isoformat()
    flag = 'daily_champion_paid_%s' % day.isoformat()
    champion = DailyChallengeScore.query.filter_by(challenge_key=key).order_by(
        DailyChallengeScore.score.desc(), DailyChallengeScore.seconds_taken.asc()
    ).first()
    if not champion:
        return None

    if not SiteSetting.get(flag):
        winner = PlayerProfile.query.filter_by(session_key=champion.player_session).first()
        if winner:
            winner.coins = (winner.coins or 0) + DAILY_CHAMPION_COINS
            winner.add_xp(100)
        SiteSetting.set(flag, '1')
        db.session.commit()
    return champion


@games_bp.route('/daily')
def daily():
    if not _has_account():
        # Everybody gets the same grid, so a daily leaderboard made of
        # throwaway identities would be meaningless: clear the cookies, replay
        # the grid, post a better time. An account is the whole mechanism.
        flash('The Daily Crossword needs an account — that is how scores and the '
              'champion award are tracked. Mini games are open to everyone.', 'error')
        return redirect(url_for('arena.player_register', next=url_for('games.daily')))

    today = date.today()
    spec, puzzle = gd.daily_crossword(today)
    player = get_current_player(persist=False)

    mine = None
    if player:
        mine = DailyChallengeScore.query.filter_by(
            player_session=player.session_key, challenge_key=spec['key']
        ).first()

    champion = _settle_champion(today - timedelta(days=1))

    return render_template(
        'themes/quizhub/games/daily.html',
        # An empty key stops the shared shell posting to the ordinary score
        # endpoint; the daily has its own, with its own one-go-a-day rule.
        game={'key': '', 'title': 'Daily Crossword', 'icon': '🗓️',
              'how': 'One grid a day, the same for everyone. It builds through the week '
                     'and starts fresh on Monday. You get a single attempt, so take your time.'},
        games=built_games(),
        player=player,
        spec=spec,
        puzzle=puzzle,
        mine=mine,
        best=(mine.score if mine else 0),
        leaderboard=_daily_board(spec['key']),
        champion=champion,
        champion_day=(today - timedelta(days=1)),
        ladder=[gd.DAILY_LADDER[i] for i in range(7)],
        today_weekday=today.weekday(),
    )


@games_bp.route('/api/daily-score', methods=['POST'])
def submit_daily_score():
    data = request.get_json(silent=True) or {}
    today = date.today()
    spec = gd.daily_spec(today)

    # Checked before the day, so a guest is told what is actually wrong.
    if not _has_account():
        return jsonify({'ok': False, 'error': 'The Daily Crossword needs an account.',
                        'signup_url': url_for('arena.player_register')}), 403

    if str(data.get('key') or '') != spec['key']:
        # The day rolled over while they were playing, or the key was fiddled
        return jsonify({'ok': False, 'error': 'That puzzle is no longer today\'s.'}), 400

    try:
        score = max(0, min(int(data.get('score') or 0), 100000))
        seconds = max(0, min(int(data.get('seconds') or 0), 86400))
    except (TypeError, ValueError):
        score, seconds = 0, 0

    player = get_current_player()
    existing = DailyChallengeScore.query.filter_by(
        player_session=player.session_key, challenge_key=spec['key']
    ).first()
    # Everyone gets the same grid, so a replay would just be a memory test.
    if existing:
        return jsonify({'ok': True, 'already': True, 'score': existing.score,
                        'rank': _daily_rank(spec['key'], existing)})

    row = DailyChallengeScore(
        player_session=player.session_key,
        challenge_key=spec['key'],
        challenge_date=today,
        display_name=player.display_name,
        avatar_key=player.avatar_key,
        score=score,
        seconds_taken=seconds,
        solved=bool(data.get('solved')),
    )
    db.session.add(row)

    xp = min(XP_CAP, int(score * 0.12))
    if xp > 0 and player.id:
        player.add_xp(xp)
        player.coins = (player.coins or 0) + xp // 10
        player.last_active_at = datetime.utcnow()
    db.session.commit()

    return jsonify({'ok': True, 'already': False, 'score': score, 'xp': xp,
                    'coins': xp // 10, 'rank': _daily_rank(spec['key'], row),
                    'players': DailyChallengeScore.query.filter_by(challenge_key=spec['key']).count()})


def _daily_rank(challenge_key, row):
    return DailyChallengeScore.query.filter(
        DailyChallengeScore.challenge_key == challenge_key,
        db.or_(
            DailyChallengeScore.score > (row.score or 0),
            db.and_(DailyChallengeScore.score == (row.score or 0),
                    DailyChallengeScore.seconds_taken < (row.seconds_taken or 0)),
        ),
    ).count() + 1


@games_bp.route('/api/check-word', methods=['POST'])
def check_word():
    """Is this a real word?

    The page carries a small common-word list and answers most guesses itself;
    this is only called for a word it does not recognise. The dictionary is one
    read-only set held in the process, so every game and every player checks
    against the same copy without touching the database.
    """
    data = request.get_json(silent=True) or {}
    word = str(data.get('word') or '')[:40]
    return jsonify({'ok': True, 'word': word.upper(), 'valid': gd.is_word(word)})


@games_bp.route('/api/leaderboard/<game_key>')
def leaderboard_api(game_key):
    if game_key not in GAME_BY_KEY:
        return jsonify({'ok': False, 'error': 'unknown game'}), 404
    rows = _leaderboard(game_key, limit=15)
    return jsonify({'ok': True, 'rows': [r.to_dict() for r in rows]})
