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
from ..models_challenge import (GameChallenge, GameChallengeScore,
                                GAMES_PER_CHALLENGE, new_challenge_code)
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
    ('trivia', 'Trivia Arcade', '🎯', 'Facts, timelines, connections and obscure picks'),
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
    # ---- Trivia Arcade ----------------------------------------------------
    {
        'key': 'higher-lower', 'title': 'Higher or Lower', 'icon': '📈', 'group': 'trivia',
        'blurb': 'Compare real-world heights, years, speeds and populations on a rising streak.',
        'accent': 'from-emerald-500 to-cyan-700', 'border': 'border-emerald-500/40',
        'xp_rate': 0.06, 'score_unit': 'pts',
        'how': 'Guess whether the second card is higher or lower than the first. Consecutive hits climb your multiplier up to 4×.',
    },
    {
        'key': 'timeline-sort', 'title': 'Timeline Sort', 'icon': '⏳', 'group': 'trivia',
        'blurb': 'Arrange four historical events, albums or inventions from earliest to latest.',
        'accent': 'from-cyan-500 to-indigo-700', 'border': 'border-cyan-500/40',
        'xp_rate': 0.08, 'score_unit': 'pts',
        'how': 'Tap any two cards to swap their positions, then lock in your order to reveal the exact dates.',
    },
    {
        'key': 'four-clues', 'title': '4 Clues, 1 Link', 'icon': '🔗', 'group': 'trivia',
        'blurb': 'Clues reveal one by one — buzz in early for 500 pts before it gets obvious.',
        'accent': 'from-fuchsia-500 to-purple-700', 'border': 'border-fuchsia-500/40',
        'xp_rate': 0.07, 'score_unit': 'pts',
        'how': 'Crack the link after Clue 1 for 500 points, or reveal more clues at lower value.',
    },
    {
        'key': 'rare-answer', 'title': 'Beat the Crowd', 'icon': '🎯', 'group': 'trivia',
        'blurb': 'Pick the most obscure valid answer for 100 pts — and dodge the fake trap!',
        'accent': 'from-amber-500 to-rose-700', 'border': 'border-amber-500/40',
        'xp_rate': 0.22, 'score_unit': 'pts',
        'how': 'Common answers score low, obscure answers score up to 100 (Pointless!), and the decoy scores zero.',
    },
    {
        'key': 'card-ladder', 'title': 'Card Ladder', 'icon': '🃏', 'group': 'trivia',
        'blurb': 'Three rows of five cards with a live host — call Higher or Lower to clear the ladder!',
        'accent': 'from-rose-500 to-indigo-700', 'border': 'border-rose-500/40',
        'xp_rate': 0.04, 'score_unit': 'pts',
        'how': 'Clear all three rows of five cards. You get 1 free base-card swap per row; a wrong call resets your current row and drops its multiplier.',
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

    # Challenges you are in, so one opened and then forgotten is findable
    # again. Without this the link was the only way back to it.
    my_key = player.session_key if player else None
    challenges = []
    for ch in _live_challenges(my_key):
        table = ch.standings()
        is_creator = (my_key == ch.creator_key)
        done = len(ch.scores_for(my_key))
        challenges.append({
            'code': ch.code,
            'opponent': (ch.opponent_name if is_creator else ch.creator_name),
            'waiting': not ch.opponent_key,
            'can_cancel': is_creator and not ch.opponent_key,
            'played': done,
            'total': len(ch.games()),
            'you': table['creator_wins'] if is_creator else table['opponent_wins'],
            'them': table['opponent_wins'] if is_creator else table['creator_wins'],
            'days_left': ch.days_left(),
        })

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
        challenges=challenges,
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


@games_bp.route('/higher-lower')
def higher_lower():
    rng = random.Random()
    return _render_game('higher-lower', deck=gd.higher_lower_deck(rng, count=14))


@games_bp.route('/timeline-sort')
def timeline_sort():
    rng = random.Random()
    return _render_game('timeline-sort', rounds=gd.timeline_sort_rounds(rng, count=5))


@games_bp.route('/four-clues')
def four_clues():
    rng = random.Random()
    return _render_game('four-clues', rounds=gd.four_clues_rounds(rng, count=6))


@games_bp.route('/rare-answer')
def rare_answer():
    rng = random.Random()
    return _render_game('rare-answer', rounds=gd.rare_answer_rounds(rng, count=6))


@games_bp.route('/card-ladder')
def card_ladder():
    return _render_game('card-ladder')


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
    raw_coins = min(4, max(1, xp // 25)) if xp > 0 else 0
    # Ad-backed Coin Economy (1,000 Coins = £1.00): cap daily Arcade coins at 20/day
    today_iso = datetime.utcnow().date().isoformat()
    if session.get('arcade_coin_date') != today_iso:
        session['arcade_coin_date'] = today_iso
        session['arcade_coins_today'] = 0
    earned_today = int(session.get('arcade_coins_today') or 0)
    ARCADE_DAILY_COIN_CAP = 20
    coins = max(0, min(raw_coins, ARCADE_DAILY_COIN_CAP - earned_today))
    if xp > 0 and player.id:
        player.add_xp(xp)
        if coins > 0:
            player.coins = (player.coins or 0) + coins
            session['arcade_coins_today'] = earned_today + coins
        player.last_active_at = datetime.utcnow()

    db.session.commit()

    # If this game belongs to a challenge they are in, that run is their go at
    # it. Recorded off the ordinary score submission rather than a separate
    # endpoint, so a challenge game is played exactly like any other.
    challenge_note = _record_challenge_run(player.session_key, key, score)

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
        'challenge': challenge_note,
    })


# ---------------------------------------------------------------------------
# Games Challenge: five games, two players, one week
# ---------------------------------------------------------------------------

def _live_challenges(player_key):
    """Challenges this player is in that are still running."""
    if not player_key:
        return []
    rows = GameChallenge.query.filter(
        GameChallenge.status != 'complete',
        db.or_(GameChallenge.creator_key == player_key,
               GameChallenge.opponent_key == player_key),
    ).order_by(GameChallenge.created_at.desc()).all()
    return [c for c in rows if not c.expired]


def _record_challenge_run(player_key, game_key, score):
    """Put this run against every live challenge that wants it.

    Returns something for the end-of-game overlay to show, or None. A player
    can be in more than one challenge at once, and the same game can be in
    both, so this is a loop rather than a lookup.
    """
    noted = None
    for ch in _live_challenges(player_key):
        if game_key not in ch.games():
            continue
        if not GameChallengeScore.record(ch, player_key, game_key, score):
            continue        # already had their go at this one
        table = ch.standings()
        if ch.opponent_key and table['rows'] and all(r['played_by_both'] for r in table['rows']):
            ch.status = 'complete'
            db.session.commit()
            _settle_challenge_pot(ch, {g['key']: g.get('xp_rate', 0.1) for g in GAMES})
        mine_wins = table['creator_wins'] if player_key == ch.creator_key else table['opponent_wins']
        their_wins = table['opponent_wins'] if player_key == ch.creator_key else table['creator_wins']
        done = len(ch.scores_for(player_key))
        noted = {
            'code': ch.code,
            'url': url_for('games.challenge', code=ch.code),
            'played': done,
            'total': len(ch.games()),
            'you': mine_wins,
            'them': their_wins,
            'opponent': (ch.opponent_name if player_key == ch.creator_key else ch.creator_name) or 'your opponent',
        }
    return noted


def _settle_challenge_pot(ch, rates):
    """Credit the coin pot once a wagered challenge completes."""
    wager = int(ch.wager_coins or 0)
    if wager <= 0 or ch.pot_settled or ch.status != 'complete':
        return
    winner_side = ch.leader(rates)
    if winner_side == 'creator':
        p = PlayerProfile.query.filter_by(session_key=ch.creator_key).first()
        if p:
            p.coins = (p.coins or 0) + (wager * 2)
    elif winner_side == 'opponent' and ch.opponent_key:
        p = PlayerProfile.query.filter_by(session_key=ch.opponent_key).first()
        if p:
            p.coins = (p.coins or 0) + (wager * 2)
    else:
        # Dead heat: refund each player's stake
        for sk in (ch.creator_key, ch.opponent_key):
            if not sk:
                continue
            p = PlayerProfile.query.filter_by(session_key=sk).first()
            if p:
                p.coins = (p.coins or 0) + wager
    ch.pot_settled = True
    db.session.commit()


def _pick_challenge_games(mode='random', category_filter=None, custom_keys=None):
    """Select 5 games for a challenge while preserving Classic Random as default."""
    all_keys = [g['key'] for g in built_games()]
    if mode == 'custom' and custom_keys:
        valid = [k for k in custom_keys if k in GAME_BY_KEY]
        # Preserve order, deduplicate
        picked = list(dict.fromkeys(valid))[:GAMES_PER_CHALLENGE]
        if len(picked) < GAMES_PER_CHALLENGE:
            rem = [k for k in all_keys if k not in picked]
            random.shuffle(rem)
            picked.extend(rem[:GAMES_PER_CHALLENGE - len(picked)])
        return picked
    if mode == 'category' and category_filter:
        cat_keys = [g['key'] for g in built_games() if g.get('group') == category_filter]
        random.shuffle(cat_keys)
        picked = cat_keys[:GAMES_PER_CHALLENGE]
        if len(picked) < GAMES_PER_CHALLENGE:
            rem = [k for k in all_keys if k not in picked]
            random.shuffle(rem)
            picked.extend(rem[:GAMES_PER_CHALLENGE - len(picked)])
        return picked
    # Default Classic Random
    keys = list(all_keys)
    random.shuffle(keys)
    return keys[:GAMES_PER_CHALLENGE]


@games_bp.route('/challenge/<code>/cancel', methods=['POST'])
def challenge_cancel(code):
    """Call off a challenge nobody has taken up yet (refunds any wager stake)."""
    ch = GameChallenge.query.filter_by(code=code.upper()).first_or_404()
    player = get_current_player(persist=False)
    me = player.session_key if player else None

    if not me or me != ch.creator_key:
        flash('Only whoever opened that challenge can call it off.', 'error')
        return redirect(url_for('games.hub'))
    if ch.opponent_key:
        flash('Someone has already taken that challenge on, so it has to play out.', 'error')
        return redirect(url_for('games.challenge', code=ch.code))

    if (ch.wager_coins or 0) > 0 and not ch.pot_settled:
        creator_p = PlayerProfile.query.filter_by(session_key=ch.creator_key).first()
        if creator_p:
            creator_p.coins = (creator_p.coins or 0) + int(ch.wager_coins)

    GameChallengeScore.query.filter_by(challenge_id=ch.id).delete()
    db.session.delete(ch)
    db.session.commit()
    flash('Challenge called off (any staked coins refunded).', 'success')
    return redirect(url_for('games.hub'))


@games_bp.route('/challenge/new', methods=['POST'])
def challenge_new():
    """Open a challenge: Classic Random 5, Category Filter, or Custom Hand-Picked + optional Coin Wager."""
    if not _has_account():
        return redirect(url_for('arena.player_register', next=url_for('games.hub')))
    player = get_current_player()

    mode = (request.form.get('challenge_mode') or 'random').strip().lower()
    if mode not in ('random', 'category', 'custom'):
        mode = 'random'
    cat_filter = (request.form.get('category_filter') or '').strip().lower() or None
    custom_keys = request.form.getlist('custom_games')

    try:
        wager = int(request.form.get('wager_coins') or 0)
    except (TypeError, ValueError):
        wager = 0
    if wager not in (0, 25, 50, 100):
        wager = 0
    if wager > 0:
        if (player.coins or 0) < wager:
            flash(f'Not enough coins for a {wager}-coin wager — opened as a friendly challenge instead.', 'info')
            wager = 0
        else:
            player.coins = (player.coins or 0) - wager

    picked = _pick_challenge_games(mode=mode, category_filter=cat_filter, custom_keys=custom_keys)
    friend = (request.form.get('friend_name') or '').strip()[:30]

    challenge = GameChallenge(
        code=new_challenge_code(),
        status='waiting',
        creator_key=player.session_key,
        creator_name=player.display_name,
        creator_avatar=player.avatar_key,
        opponent_name=friend or None,
        challenge_mode=mode,
        category_filter=cat_filter if mode == 'category' else None,
        wager_coins=wager,
    )
    challenge.set_games(picked)
    db.session.add(challenge)
    db.session.commit()
    return redirect(url_for('games.challenge', code=challenge.code, share=1))


@games_bp.route('/challenge/<code>/double-down', methods=['POST'])
def challenge_double_down(code):
    """Activate a player's 1x Double Down (2x score) power-up on an unplayed game."""
    ch = GameChallenge.query.filter_by(code=code.upper()).first_or_404()
    if not _has_account():
        return redirect(url_for('arena.player_register', next=url_for('games.challenge', code=ch.code)))
    player = get_current_player()
    me = player.session_key
    if not ch.is_player(me) or ch.status == 'complete':
        flash('Double Down can only be used on an active challenge.', 'error')
        return redirect(url_for('games.challenge', code=ch.code))

    game_key = (request.form.get('game_key') or '').strip()
    if game_key not in ch.games():
        flash('That game is not in this challenge.', 'error')
        return redirect(url_for('games.challenge', code=ch.code))

    already_played = GameChallengeScore.query.filter_by(
        challenge_id=ch.id, player_key=me, game_key=game_key).first()
    if already_played:
        flash('You must activate Double Down BEFORE playing that game!', 'error')
        return redirect(url_for('games.challenge', code=ch.code))

    if me == ch.creator_key:
        if ch.creator_double_game:
            flash('You already used your Double Down power-up on this challenge.', 'info')
            return redirect(url_for('games.challenge', code=ch.code))
        ch.creator_double_game = game_key
    else:
        if ch.opponent_double_game:
            flash('You already used your Double Down power-up on this challenge.', 'info')
            return redirect(url_for('games.challenge', code=ch.code))
        ch.opponent_double_game = game_key

    db.session.commit()
    gmeta = GAME_BY_KEY.get(game_key, {})
    flash(f"⚡ Double Down armed on {gmeta.get('title', game_key)}! Your score will count 2×!", 'success')
    return redirect(url_for('games.challenge', code=ch.code))


@games_bp.route('/challenge/<code>/rematch', methods=['POST'])
def challenge_rematch(code):
    """1-click Rematch or Double-or-Nothing rematch from a completed challenge."""
    old = GameChallenge.query.filter_by(code=code.upper()).first_or_404()
    if not _has_account():
        return redirect(url_for('arena.player_register', next=url_for('games.challenge', code=old.code)))
    player = get_current_player()
    me = player.session_key

    double_pot = (request.form.get('double_pot') == '1')
    base_wager = int(old.wager_coins or 0)
    wager = min(100, base_wager * 2 if (double_pot and base_wager > 0) else (25 if double_pot else base_wager))
    if wager not in (0, 25, 50, 100):
        wager = 50 if wager > 25 else 0
    if wager > 0:
        if (player.coins or 0) < wager:
            wager = 0
        else:
            player.coins = (player.coins or 0) - wager

    other_name = old.opponent_name if me == old.creator_key else old.creator_name
    picked = _pick_challenge_games(mode=old.challenge_mode or 'random', category_filter=old.category_filter)

    new_ch = GameChallenge(
        code=new_challenge_code(),
        status='waiting',
        creator_key=me,
        creator_name=player.display_name,
        creator_avatar=player.avatar_key,
        opponent_name=other_name,
        challenge_mode=old.challenge_mode or 'random',
        category_filter=old.category_filter,
        wager_coins=wager,
    )
    new_ch.set_games(picked)
    db.session.add(new_ch)
    db.session.commit()
    return redirect(url_for('games.challenge', code=new_ch.code, share=1))


@games_bp.route('/challenge/<code>')
def challenge(code):
    """The challenge itself: who is winning, power-ups, coin pot, rivalry & games."""
    ch = GameChallenge.query.filter_by(code=code.upper()).first_or_404()
    player = get_current_player(persist=False)
    me = player.session_key if player else None

    # Whoever opens the link second and is not already in it takes the seat.
    if (_has_account() and me and not ch.opponent_key and me != ch.creator_key
            and not ch.expired):
        player = get_current_player()
        me = player.session_key
        wager = int(ch.wager_coins or 0)
        if wager > 0:
            if (player.coins or 0) >= wager:
                player.coins = (player.coins or 0) - wager
            else:
                # Refund creator and convert to friendly so nobody is blocked from playing
                creator_p = PlayerProfile.query.filter_by(session_key=ch.creator_key).first()
                if creator_p:
                    creator_p.coins = (creator_p.coins or 0) + wager
                ch.wager_coins = 0
                flash('Converted to a friendly challenge (not enough coins to match the pot).', 'info')
        ch.opponent_key = me
        ch.opponent_name = player.display_name
        ch.opponent_avatar = player.avatar_key
        ch.status = 'active'
        db.session.commit()

    if ch.expired and ch.status != 'complete':
        ch.status = 'complete'
        db.session.commit()

    rates = {g['key']: g.get('xp_rate', 0.1) for g in GAMES}
    if ch.status == 'complete':
        _settle_challenge_pot(ch, rates)

    table = ch.standings()
    for row in table['rows']:
        row['meta'] = GAME_BY_KEY.get(row['game_key'], {'title': row['game_key'], 'icon': '🎮'})

    leader_side = ch.leader(rates)
    is_creator = (me == ch.creator_key)
    my_double = ch.creator_double_game if is_creator else (ch.opponent_double_game if ch.is_player(me) else None)
    h2h = GameChallenge.h2h_record(
        me if ch.is_player(me) else ch.creator_key,
        (ch.opponent_key if is_creator else ch.creator_key) if ch.is_player(me) else ch.opponent_key,
        rates
    )
    badges = ch.badges(leader_side, table) if ch.status == 'complete' else []

    return render_template(
        'themes/quizhub/games/challenge.html',
        challenge=ch,
        table=table,
        leader=leader_side,
        me=me,
        is_creator=is_creator,
        is_player=ch.is_player(me),
        my_scores=ch.scores_for(me) if me else {},
        my_double=my_double,
        h2h=h2h,
        badges=badges,
        days_left=ch.days_left(),
        has_account=_has_account(),
    )


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
