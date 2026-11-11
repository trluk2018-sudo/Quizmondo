import json
import random
import secrets
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash, current_app, Response
from sqlalchemy.sql.expression import func
from ..models import db, User, PlayerProfile, MINIMUM_SIGNUP_AGE, age_gate_config, ArenaMatch, ArenaRound, QuizQuestion, QuizPack, PubLeague, PubLeagueResult, pub_season_label, SiteSetting, slugify, GroupGame, GroupPlayer, ClimberSeason, ClimberProgress, UserPostRead, Post, ClimberFact, UserClimberFactSeen
from ..models_quiz_memory import QuestionMemory, MEMORY_LIMIT
from ..utils.share_card import generate_duel_card_png, generate_pub_card_png

arena_bp = Blueprint('arena', __name__, url_prefix='/arena')

from .public import inject_global_data

@arena_bp.context_processor
def inject_arena_global_data():
    data = inject_global_data()
    data['avatar_lookup'] = AVATAR_LOOKUP
    # The signup form needs the age rule and the latest date of birth that
    # satisfies it, so the date picker will not even offer a younger one.
    gate = age_gate_config()
    data['age_gate_on'] = gate['enabled']
    data['minimum_age'] = gate['minimum']
    today = datetime.utcnow().date()
    try:
        data['max_dob'] = today.replace(year=today.year - gate['minimum']).isoformat()
    except ValueError:  # 29 February
        data['max_dob'] = today.replace(month=2, day=28, year=today.year - gate['minimum']).isoformat()
    return data

# 24 Player Avatars (Note: 'nova' is reserved exclusively for Cyber Bot Nova!)
AVATAR_PRESETS = [
    {'key': 'quizzy', 'name': 'Quizzy', 'badge': 'Hyper Star', 'emoji': '⭐', 'bg': 'from-purple-600 to-indigo-600', 'border': 'border-purple-400'},
    {'key': 'pixel', 'name': 'Pixel', 'badge': '8-Bit Robot', 'emoji': '👾', 'bg': 'from-emerald-500 to-teal-700', 'border': 'border-emerald-400'},
    {'key': 'sage', 'name': 'Sage', 'badge': 'Owl Scholar', 'emoji': '🦉', 'bg': 'from-amber-500 to-orange-600', 'border': 'border-amber-400'},
    {'key': 'astro', 'name': 'Astro', 'badge': 'Space Ranger', 'emoji': '🧑‍🚀', 'bg': 'from-cyan-500 to-blue-600', 'border': 'border-cyan-400'},
    {'key': 'blaze', 'name': 'Blaze', 'badge': 'Fire Phoenix', 'emoji': '🔥', 'bg': 'from-orange-500 to-rose-600', 'border': 'border-orange-400'},
    {'key': 'volt', 'name': 'Volt', 'badge': 'Thunder Bolt', 'emoji': '⚡', 'bg': 'from-yellow-400 to-amber-600', 'border': 'border-yellow-400'},
    {'key': 'shadow', 'name': 'Shadow', 'badge': 'Stealth Ninja', 'emoji': '🥷', 'bg': 'from-slate-700 to-purple-900', 'border': 'border-purple-400'},
    {'key': 'rex', 'name': 'Rex', 'badge': 'Dino King', 'emoji': '🦖', 'bg': 'from-lime-500 to-emerald-700', 'border': 'border-lime-400'},
    {'key': 'kitsune', 'name': 'Kitsune', 'badge': 'Cyber Fox', 'emoji': '🦊', 'bg': 'from-amber-500 to-red-600', 'border': 'border-amber-400'},
    {'key': 'titan', 'name': 'Titan', 'badge': 'Mecha Knight', 'emoji': '🛡️', 'bg': 'from-blue-600 to-indigo-800', 'border': 'border-blue-400'},
    {'key': 'vortex', 'name': 'Vortex', 'badge': 'Galaxy Dragon', 'emoji': '🐉', 'bg': 'from-emerald-600 to-cyan-700', 'border': 'border-emerald-400'},
    {'key': 'maverick', 'name': 'Maverick', 'badge': 'Ace Falcon', 'emoji': '🦅', 'bg': 'from-sky-500 to-blue-700', 'border': 'border-sky-400'},
    {'key': 'phantom', 'name': 'Phantom', 'badge': 'Cosmic Ghost', 'emoji': '👻', 'bg': 'from-indigo-500 to-purple-800', 'border': 'border-indigo-400'},
    {'key': 'apex', 'name': 'Apex', 'badge': 'Golden Lion', 'emoji': '🦁', 'bg': 'from-amber-400 to-orange-600', 'border': 'border-amber-300'},
    {'key': 'neptune', 'name': 'Neptune', 'badge': 'Ocean Shark', 'emoji': '🦈', 'bg': 'from-cyan-600 to-blue-800', 'border': 'border-cyan-400'},
    {'key': 'cobra', 'name': 'Cobra', 'badge': 'Venom Viper', 'emoji': '🐍', 'bg': 'from-green-500 to-emerald-800', 'border': 'border-green-400'},
    {'key': 'panda', 'name': 'Bamboozle', 'badge': 'Zen Panda', 'emoji': '🐼', 'bg': 'from-teal-500 to-slate-800', 'border': 'border-teal-400'},
    {'key': 'unicorn', 'name': 'Stardust', 'badge': 'Mythic Unicorn', 'emoji': '🦄', 'bg': 'from-pink-500 to-purple-600', 'border': 'border-pink-400'},
    {'key': 'viking', 'name': 'Valhalla', 'badge': 'Storm Raider', 'emoji': '⚔️', 'bg': 'from-rose-600 to-slate-800', 'border': 'border-rose-400'},
    {'key': 'wizard', 'name': 'Merlin', 'badge': 'Arcane Mage', 'emoji': '🧙‍♂️', 'bg': 'from-violet-600 to-indigo-900', 'border': 'border-violet-400'},
    {'key': 'pirate', 'name': 'Corsair', 'badge': 'Sky Captain', 'emoji': '🏴‍☠️', 'bg': 'from-slate-700 to-rose-900', 'border': 'border-rose-400'},
    {'key': 'panther', 'name': 'Onyx', 'badge': 'Night Panther', 'emoji': '🐆', 'bg': 'from-fuchsia-700 to-slate-900', 'border': 'border-fuchsia-400'},
    {'key': 'octo', 'name': 'Kraken', 'badge': 'Deep Mind', 'emoji': '🐙', 'bg': 'from-pink-600 to-rose-800', 'border': 'border-pink-400'},
    {'key': 'crown', 'name': 'Monarch', 'badge': 'Trivia Royalty', 'emoji': '👑', 'bg': 'from-yellow-500 to-amber-700', 'border': 'border-yellow-300'},
]

AVATAR_LOOKUP = {a['key']: a for a in AVATAR_PRESETS}
AVATAR_LOOKUP['nova'] = {'key': 'nova', 'name': 'Cyber Bot Nova', 'badge': 'AI Challenger', 'emoji': '🤖', 'bg': 'from-cyan-500 to-purple-700', 'border': 'border-cyan-400'}


VISUAL_PRIORITY_CATEGORIES = {
    'match-flags', 'football-badges', 'brand-logos', 'country-shapes', 'football-teams'
}


def playable_questions():
    """Only moderated questions are ever put in front of a player."""
    return QuizQuestion.query.filter(
        db.or_(QuizQuestion.status == 'approved', QuizQuestion.status.is_(None))
    )


# What this player has been asked lately, so the next game does not open with
# the same questions.
#
# A signed-in player gets a row in question_memory, so the list follows the
# account between devices. A guest keeps it in the session, because there is
# no account to hang a row on; it still works, but only in that browser.
RECENT_QIDS = 'qm_recent_qids'
RECENT_MEMORY = MEMORY_LIMIT


def _recent_qids():
    from flask import has_request_context
    if not has_request_context():
        return []
    user_id = session.get('user_id')
    if user_id:
        return QuestionMemory.recent(user_id)
    try:
        return [int(qid) for qid in (session.get(RECENT_QIDS) or [])]
    except (TypeError, ValueError):
        return []


@arena_bp.before_app_request
def adopt_guest_question_memory():
    """Carry a guest's recently-seen list onto their new account.

    Without this, making an account would hand you back the very questions you
    had just played as a guest -- the opposite of the reward signing up is
    supposed to be.
    """
    user_id = session.get('user_id')
    if not user_id or RECENT_QIDS not in session:
        return
    guest_ids = session.pop(RECENT_QIDS) or []
    if not guest_ids:
        return
    try:
        # Oldest first, so the newest end up at the front of the merged list.
        QuestionMemory.remember(user_id, list(reversed(guest_ids)), RECENT_MEMORY)
    except Exception:
        db.session.rollback()


def _remember_qids(ids):
    from flask import has_request_context
    if not has_request_context() or not ids:
        return
    user_id = session.get('user_id')
    if user_id:
        try:
            QuestionMemory.remember(user_id, ids, RECENT_MEMORY)
        except Exception:
            # Losing the memory means a repeat eventually, which is a far
            # smaller thing than losing the player's game.
            db.session.rollback()
        return
    recent = [qid for qid in _recent_qids() if qid not in ids]
    session[RECENT_QIDS] = (list(ids) + recent)[:RECENT_MEMORY]


def _dashboard_challenges(player_key):
    """Games Challenges, shaped for the duels dashboard.

    A challenge is a duel in every way that matters to somebody looking at
    this page -- somebody is waiting on somebody -- so it belongs in the same
    two lists rather than only on the mini games hub. Queried here rather than
    imported from the games blueprint, which imports from this one.
    """
    from ..models_challenge import GameChallenge
    if not player_key:
        return {'your_turn': [], 'waiting': []}

    rows = GameChallenge.query.filter(
        GameChallenge.status != 'complete',
        db.or_(GameChallenge.creator_key == player_key,
               GameChallenge.opponent_key == player_key),
    ).order_by(GameChallenge.created_at.desc()).all()

    your_turn, waiting = [], []
    for ch in rows:
        if ch.expired:
            continue
        is_creator = (player_key == ch.creator_key)
        table = ch.standings()
        played = len(ch.scores_for(player_key))
        total = len(ch.games())
        item = {
            'code': ch.code,
            'opponent': (ch.opponent_name if is_creator else ch.creator_name),
            'accepted': bool(ch.opponent_key),
            'played': played,
            'total': total,
            'you': table['creator_wins'] if is_creator else table['opponent_wins'],
            'them': table['opponent_wins'] if is_creator else table['creator_wins'],
            'days_left': ch.days_left(),
        }
        # Games of yours left to play means it is on you; otherwise you are
        # waiting, either for them to play or for anyone to accept at all.
        (your_turn if played < total else waiting).append(item)
    return {'your_turn': your_turn, 'waiting': waiting}


def _dashboard_completed(player):
    """Completed Battles & Duels across 5-Mini-Game Challenges and Arena Quiz Duels.

    Only displayed for authenticated (logged-in) players who have completed matches.
    The current player is ALWAYS positioned first on the left ('You') with their score
    leading, regardless of whether they created the match or joined as a challenger.
    """
    if not player or not session.get('user_id'):
        return None

    from ..models_challenge import GameChallenge
    completed_items = []

    # 1. Fetch completed 5x Mini-Game Challenges
    try:
        challenges = GameChallenge.query.filter(
            db.or_(GameChallenge.creator_key == player.session_key,
                   GameChallenge.opponent_key == player.session_key)
        ).order_by(GameChallenge.created_at.desc()).all()

        for ch in challenges:
            total_games = len(ch.games())
            played_creator = len(ch.scores_for(ch.creator_key))
            played_opponent = len(ch.scores_for(ch.opponent_key)) if ch.opponent_key else 0

            is_both_done = bool(ch.opponent_key and total_games > 0 and played_creator >= total_games and played_opponent >= total_games)
            is_expired_with_play = bool(ch.expired and (played_creator > 0 or played_opponent > 0))

            if not (ch.status == 'complete' or is_both_done or is_expired_with_play):
                continue

            if is_both_done and ch.status != 'complete':
                ch.status = 'complete'
                db.session.commit()

            is_creator = (player.session_key == ch.creator_key)
            table = ch.standings()

            opp_name = (ch.opponent_name if is_creator else ch.creator_name) or 'Challenger'
            opp_avatar = (ch.opponent_avatar if is_creator else ch.creator_avatar) or 'quizzy'
            opp_key = ch.opponent_key if is_creator else ch.creator_key

            you_score = table['creator_wins'] if is_creator else table['opponent_wins']
            opp_score = table['opponent_wins'] if is_creator else table['creator_wins']

            if you_score > opp_score:
                outcome = 'won'
            elif opp_score > you_score:
                outcome = 'lost'
            else:
                outcome = 'tie'

            sort_dt = getattr(ch, 'updated_at', None) or getattr(ch, 'created_at', None) or datetime.utcnow()

            completed_items.append({
                'type': 'games',
                'type_label': '5 x Mini-Game',
                'code': ch.code,
                'you_name': player.display_name or 'You',
                'you_avatar': player.avatar_key or 'quizzy',
                'opp_name': opp_name,
                'opp_avatar': opp_avatar,
                'opp_key': opp_key,
                'you_score': you_score,
                'opp_score': opp_score,
                'outcome': outcome,
                'summary': f"{total_games} Mini-Games",
                'date_str': sort_dt.strftime('%b %d') if sort_dt else 'Recent',
                'sort_date': sort_dt,
                'details_url': url_for('games.challenge', code=ch.code),
                'rematch_url': url_for('games.challenge_new', friend_name=opp_name),
            })
    except Exception:
        db.session.rollback()

    # 2. Fetch completed Quiz & Trivia Arena Matches
    try:
        finished_matches = ArenaMatch.query.filter(
            (ArenaMatch.player1_session == player.session_key) | (ArenaMatch.player2_session == player.session_key),
            ArenaMatch.status.in_(['completed', 'forfeited'])
        ).order_by(ArenaMatch.updated_at.desc()).all()

        for m in finished_matches:
            is_p1 = (m.player1_session == player.session_key)
            opp_name = (m.player2_name if is_p1 else m.player1_name) or ('Cyber Bot Nova' if m.is_bot else 'Opponent')
            opp_avatar = (m.player2_avatar if is_p1 else m.player1_avatar) or ('nova' if m.is_bot else 'quizzy')
            opp_session = m.player2_session if is_p1 else m.player1_session

            you_score = m.p1_total_score if is_p1 else m.p2_total_score
            opp_score = m.p2_total_score if is_p1 else m.p1_total_score

            if m.status == 'forfeited':
                if (m.winner == 1 and is_p1) or (m.winner == 2 and not is_p1):
                    outcome = 'won'
                else:
                    outcome = 'lost'
            else:
                if you_score > opp_score:
                    outcome = 'won'
                elif opp_score > you_score:
                    outcome = 'lost'
                else:
                    outcome = 'tie'

            sort_dt = m.updated_at or m.created_at or datetime.utcnow()

            if m.is_bot:
                rematch_url = url_for('arena.create_match', opponent_mode='bot')
            elif opp_session and opp_session not in ('pending_invite', 'online_matchmaking'):
                rematch_url = url_for('arena.challenge_fresh', target_session=opp_session)
            else:
                rematch_url = url_for('arena.match_lobby', match_code=m.match_code)

            completed_items.append({
                'type': 'quiz',
                'type_label': 'Quiz & Trivia',
                'code': m.match_code,
                'you_name': player.display_name or 'You',
                'you_avatar': player.avatar_key or 'quizzy',
                'opp_name': opp_name,
                'opp_avatar': opp_avatar,
                'opp_key': opp_session,
                'you_score': you_score,
                'opp_score': opp_score,
                'outcome': outcome,
                'summary': "6-Round Arena Duel" if m.current_round >= 6 else "Arena Quiz Duel",
                'date_str': sort_dt.strftime('%b %d') if sort_dt else 'Recent',
                'sort_date': sort_dt,
                'details_url': url_for('arena.match_lobby', match_code=m.match_code),
                'rematch_url': rematch_url,
            })
    except Exception:
        db.session.rollback()

    if not completed_items:
        return None

    # Chronological sort: newest completed first
    completed_items.sort(key=lambda x: x['sort_date'] or datetime.min, reverse=True)

    total = len(completed_items)
    wins = sum(1 for item in completed_items if item['outcome'] == 'won')
    losses = sum(1 for item in completed_items if item['outcome'] == 'lost')
    ties = sum(1 for item in completed_items if item['outcome'] == 'tie')
    win_rate_pct = round((wins / total) * 100) if total > 0 else 0
    recent_form = [item['outcome'][0].upper() for item in completed_items[:5]]

    return {
        'total': total,
        'wins': wins,
        'losses': losses,
        'ties': ties,
        'win_rate_pct': win_rate_pct,
        'recent_form': recent_form,
        'duels': completed_items,
    }


def get_random_questions(category_slug=None, count=3, exclude_ids=None, difficulty=None):
    """Questions for duels, pub leagues and rounds, avoiding recent repeats.

    Picking at random is not enough on its own. Ten categories hold only a
    dozen approved questions each, so a three-question duel in one of them
    draws from twelve, and nothing used to stop the same ones coming back the
    very next game: exclude_ids only ever covered the match in progress.

    So this skips what the player has seen lately as well. The memory is a
    preference, not a rule -- a thin category would otherwise run dry and
    hand back nothing -- so anything still missing is topped up from the full
    pool afterwards.
    """
    hard_exclude = list(exclude_ids or [])
    recent = _recent_qids()

    questions = _select_questions(category_slug, count, hard_exclude + recent, difficulty)
    if len(questions) < count:
        seen = [q.id for q in questions]
        questions += _select_questions(category_slug, count - len(questions),
                                       hard_exclude + seen, difficulty)

    random.shuffle(questions)
    _remember_qids([q.id for q in questions])
    return questions


def _select_questions(category_slug=None, count=3, exclude_ids=None, difficulty=None):
    """One pass of the selection, with no memory of earlier games.

    For visual categories (flags, badges, logos, country shapes), ALWAYS prioritize visual image matching questions first,
    and avoid Expert ('hard') text-only questions in standard rounds unless explicitly requested.
    """
    if count <= 0:
        return []
    base_query = playable_questions()
    if category_slug:
        base_query = base_query.filter_by(category_slug=category_slug)
    if exclude_ids:
        base_query = base_query.filter(~QuizQuestion.id.in_(exclude_ids))

    # A thin category cannot afford to hold its Expert questions back: sitting on them
    # means the same handful of easy/medium ones come round every single game.
    # count * 3 alone was far too generous -- a three-question duel cleared the
    # bar with nine, so the ten categories holding a dozen questions narrowed
    # to the same handful every time. Twenty is the floor now.
    spare_easy_medium = True
    if category_slug:
        easy_med_pool = playable_questions().filter(
            QuizQuestion.category_slug == category_slug,
            QuizQuestion.difficulty.in_(['easy', 'medium'])
        ).count()
        spare_easy_medium = easy_med_pool >= max(count * 3, 20)

    questions = []
    if category_slug in VISUAL_PRIORITY_CATEGORIES and difficulty != 'hard':
        # 1. Prioritize fun visual matching questions (question_type == 'image')
        visual_q = base_query.filter(
            QuizQuestion.question_type == 'image',
            QuizQuestion.media_url != '',
            QuizQuestion.media_url.isnot(None)
        ).order_by(func.random()).limit(count).all()
        questions.extend(visual_q)

        # 2. If more needed, prefer easy/medium questions before expert ('hard') questions
        if len(questions) < count:
            needed = count - len(questions)
            used_ids = [q.id for q in questions] + (exclude_ids or [])
            non_expert = playable_questions().filter(
                QuizQuestion.category_slug == category_slug,
                ~QuizQuestion.id.in_(used_ids)
            )
            if spare_easy_medium:
                non_expert = non_expert.filter(QuizQuestion.difficulty.in_(['easy', 'medium']))
            questions.extend(non_expert.order_by(func.random()).limit(needed).all())

    if len(questions) < count:
        needed = count - len(questions)
        used_ids = [q.id for q in questions] + (exclude_ids or [])
        q_filter = playable_questions().filter(~QuizQuestion.id.in_(used_ids))
        if category_slug:
            q_filter = q_filter.filter_by(category_slug=category_slug)
        if difficulty:
            q_filter = q_filter.filter_by(difficulty=difficulty)
        else:
            # Prefer easy/medium for fun gameplay, but only where there are enough to pick from
            pick = q_filter
            if spare_easy_medium:
                pick = pick.filter(QuizQuestion.difficulty.in_(['easy', 'medium']))
            questions.extend(pick.order_by(func.random()).limit(needed).all())
            needed = count - len(questions)
            if needed > 0:
                used_ids = [q.id for q in questions] + (exclude_ids or [])
                q_filter2 = playable_questions().filter(~QuizQuestion.id.in_(used_ids))
                if category_slug:
                    q_filter2 = q_filter2.filter_by(category_slug=category_slug)
                questions.extend(q_filter2.order_by(func.random()).limit(needed).all())
        if difficulty and needed > 0:
            questions.extend(q_filter.order_by(func.random()).limit(needed).all())

    if len(questions) < count:
        needed = count - len(questions)
        exclude_existing = [q.id for q in questions] + (exclude_ids or [])
        fallback = playable_questions().filter(~QuizQuestion.id.in_(exclude_existing)).order_by(func.random()).limit(needed).all()
        questions = list(questions) + list(fallback)

    # Shuffle, or the order gives the selection away: the visual picks would always lead
    # and the fill-ins always trail, so every round opens the same shape.
    questions = list(questions)
    random.shuffle(questions)
    return questions


SUPERHERO_PREFIXES = [
    'Captain', 'Nova', 'Cosmic', 'Shadow', 'Turbo', 'Quantum', 'Hyper', 'Cyber',
    'Solar', 'Thunder', 'Blaze', 'Phantom', 'Apex', 'Omega', 'Astro', 'Vortex',
    'Neon', 'Titan', 'Crimson', 'Doctor', 'Ultra', 'Starlight', 'Velocity', 'Mighty'
]
SUPERHERO_NOUNS = [
    'Quasar', 'Striker', 'Volt', 'Maverick', 'Falcon', 'Phoenix', 'Viper', 'Comet',
    'Knight', 'Pulsar', 'Blaster', 'Guardian', 'Dynamo', 'Ranger', 'Horizon', 'Spark',
    'Nebula', 'Panther', 'Vector', 'Sentinel', 'Hawk', 'Storm', 'Eclipse', 'Matrix'
]


def generate_unique_superhero_name() -> str:
    """Generate a cool, unique superhero-sounding player name."""
    for _ in range(30):
        candidate = f"{random.choice(SUPERHERO_PREFIXES)}{random.choice(SUPERHERO_NOUNS)}"
        if random.random() < 0.35:
            candidate = f"{candidate}{random.randint(10, 99)}"
        exists_user = User.query.filter(func.lower(User.username) == candidate.lower()).first()
        exists_prof = PlayerProfile.query.filter(func.lower(PlayerProfile.display_name) == candidate.lower()).first()
        if not exists_user and not exists_prof:
            return candidate
    return f"CaptainQuasar{random.randint(100, 999)}"


@arena_bp.route('/api/random-hero-name')
def api_random_hero_name():
    """Return a unique superhero player name for the 3-step onboarding wizard."""
    return jsonify({'success': True, 'name': generate_unique_superhero_name()})


@arena_bp.route('/api/check-username')
def api_check_username():
    """Check if a player name is available during Step 1 of setup."""
    u = (request.args.get('u') or '').strip()
    if len(u) < 3:
        return jsonify({'available': False, 'reason': 'too_short', 'suggestion': generate_unique_superhero_name()})
    existing = User.query.filter(func.lower(User.username) == u.lower()).first()
    if existing and existing.id != session.get('user_id'):
        return jsonify({'available': False, 'reason': 'taken', 'suggestion': generate_unique_superhero_name()})
    return jsonify({'available': True, 'name': u})


def generate_guest_name(seed_key: str) -> str:
    """Build a collision-proof guest name, derived from the visitor's session key.

    Deriving it from the key keeps the name stable across page views for a
    visitor who has no saved profile yet, and the 16.7M name space stops two
    guests sharing a name — which the self-duel guard in match_lobby() would
    otherwise mistake for one person duelling themselves.
    """
    rng = random.Random(seed_key)
    for _ in range(40):
        candidate = f"Challenger_{rng.randrange(16 ** 6):06x}"
        taken_profile = PlayerProfile.query.filter(func.lower(PlayerProfile.display_name) == candidate.lower()).first()
        taken_user = User.query.filter(func.lower(User.username) == candidate.lower()).first()
        if not taken_profile and not taken_user:
            return candidate
    return f"Challenger_{secrets.token_hex(5)}"


def get_current_player(persist=True):
    """Retrieve or initialize the active player profile using session cookie or user_id.

    With persist=False a visitor who has no profile yet gets a throwaway
    in-memory profile instead of a saved row, so simply browsing the Arena no
    longer leaves a guest account behind. Routes that actually start or change
    something keep the default, which saves the profile as before.
    """
    session.permanent = True
    user_id = session.get('user_id')
    profile = None
    if user_id:
        user = db.session.get(User, user_id)
        if user and user.is_active:
            session['username'] = user.username
            session['user_role'] = user.role or 'player'
            session['is_creator'] = user.role in ('super_admin', 'admin', 'quizmaster', 'creator')
            profile = PlayerProfile.query.filter_by(user_id=user.id).first()
            if profile:
                changed = False
                if profile.display_name != user.username:
                    profile.display_name = user.username
                    changed = True
                if profile.avatar_key == 'nova':
                    profile.avatar_key = 'astro'
                    changed = True
                if changed:
                    db.session.commit()
                session['qm_player_key'] = profile.session_key
                return profile

    player_key = session.get('qm_player_key')
    if player_key:
        profile = PlayerProfile.query.filter_by(session_key=player_key).first()

    if not profile:
        # Reuse the key already in the cookie where there is one, so a visitor who
        # browsed first keeps the same identity once their profile is finally saved.
        new_key = player_key or secrets.token_urlsafe(16)
        session['qm_player_key'] = new_key
        # Seeded from the key so a browsing guest sees the same avatar and name on every page.
        rand_avatar = random.Random(new_key).choice(AVATAR_PRESETS)['key']
        rand_name = session.get('username') or generate_guest_name(new_key)
        profile = PlayerProfile(
            user_id=user_id,
            session_key=new_key,
            display_name=rand_name,
            avatar_key=rand_avatar,
            level=1,
            xp=0,
            coins=250,
            streak_days=1,
            matches_played=0,
            matches_won=0
        )
        if persist:
            db.session.add(profile)
            db.session.commit()
    elif user_id and not profile.user_id:
        profile.user_id = user_id
        if session.get('username'):
            profile.display_name = session.get('username')
        db.session.commit()

    return profile


def _get_friends_and_group_challenges(player: PlayerProfile) -> tuple:
    """Build the player's Friends Roster (past opponents + registered players) and Open Group Challenges."""
    # 1. Gather session keys of past & current human opponents
    all_my_matches = ArenaMatch.query.filter(
        (ArenaMatch.player1_session == player.session_key) | (ArenaMatch.player2_session == player.session_key)
    ).order_by(ArenaMatch.updated_at.desc()).limit(60).all()

    friend_sessions = set()
    active_by_opponent = {}
    last_completed_by_opponent = {}
    h2h_wins = {}
    h2h_Played = {}

    for m in all_my_matches:
        is_p1 = (m.player1_session == player.session_key)
        opp_sess = m.player2_session if is_p1 else m.player1_session
        if not opp_sess or opp_sess in ('bot_quizmondo_ai', 'pending_invite', 'online_matchmaking', '', player.session_key):
            continue
        friend_sessions.add(opp_sess)
        if m.status in ('waiting', 'in_progress') and opp_sess not in active_by_opponent:
            exp_t = m.expected_turn()
            if m.current_turn != exp_t:
                m.current_turn = exp_t
                db.session.commit()
            my_turn = (m.current_turn == 1 and is_p1) or (m.current_turn == 2 and not is_p1)
            active_by_opponent[opp_sess] = {
                'match_code': m.match_code,
                'current_round': m.current_round,
                'my_turn': my_turn,
                'my_score': m.p1_total_score if is_p1 else m.p2_total_score,
                'opp_score': m.p2_total_score if is_p1 else m.p1_total_score
            }
        elif m.status == 'completed':
            if opp_sess not in last_completed_by_opponent:
                last_completed_by_opponent[opp_sess] = m.match_code
            h2h_Played[opp_sess] = h2h_Played.get(opp_sess, 0) + 1
            if (is_p1 and m.winner == 1) or (not is_p1 and m.winner == 2):
                h2h_wins[opp_sess] = h2h_wins.get(opp_sess, 0) + 1

    # Also include registered human players on Quizmondo so friends who signed up appear in the roster
    registered_profiles = PlayerProfile.query.filter(
        PlayerProfile.user_id.isnot(None),
        PlayerProfile.session_key != player.session_key
    ).order_by(PlayerProfile.last_active_at.desc()).limit(20).all()
    for rp in registered_profiles:
        if rp.display_name and rp.display_name.strip().lower() != player.display_name.strip().lower():
            friend_sessions.add(rp.session_key)

    friends_roster = []
    if friend_sessions:
        profiles = PlayerProfile.query.filter(PlayerProfile.session_key.in_(list(friend_sessions))).all()
        seen_names = set()
        for fp in profiles:
            norm_name = (fp.display_name or '').strip().lower()
            if not norm_name or norm_name == (player.display_name or '').strip().lower() or norm_name in seen_names:
                continue
            seen_names.add(norm_name)
            act = active_by_opponent.get(fp.session_key)
            av_key = fp.avatar_key if (fp.avatar_key and fp.avatar_key != 'nova') else 'quizzy'
            av_meta = AVATAR_LOOKUP.get(av_key, AVATAR_LOOKUP['quizzy'])
            friends_roster.append({
                'session_key': fp.session_key,
                'display_name': fp.display_name,
                'avatar_key': av_key,
                'avatar': av_meta['emoji'],
                'level': fp.level or 1,
                'xp': fp.xp or 0,
                'is_registered': bool(fp.user_id),
                'wins': h2h_wins.get(fp.session_key, 0) or (fp.matches_won or 0),
                'wins_against': h2h_wins.get(fp.session_key, 0),
                'played_against': h2h_Played.get(fp.session_key, 0),
                'played_before': (h2h_Played.get(fp.session_key, 0) > 0) or bool(act),
                'active_match': act,
                'active_match_code': act['match_code'] if act else None,
                'active_round': act['current_round'] if act else None,
                'active_my_turn': act['my_turn'] if act else False,
                'last_completed_match_code': last_completed_by_opponent.get(fp.session_key)
            })

    # Sort: friends with an active match (especially your turn) first, then registered friends by XP
    friends_roster.sort(
        key=lambda f: (
            1 if (f['active_match'] and f['active_match']['my_turn']) else (0 if f['active_match'] else -1),
            1 if f['is_registered'] else 0,
            f['xp']
        ),
        reverse=True
    )

    # 2. Open Group Challenges: waiting matches created by other human players that anyone can accept!
    open_matches_raw = ArenaMatch.query.filter(
        ArenaMatch.player1_session != player.session_key,
        ArenaMatch.player1_session != 'bot_quizmondo_ai',
        (ArenaMatch.player2_session.is_(None)) | (ArenaMatch.player2_session.in_(['pending_invite', 'online_matchmaking', ''])),
        ArenaMatch.current_round == 1,
        ArenaMatch.status.in_(['waiting', 'in_progress'])
    ).order_by(ArenaMatch.created_at.desc()).limit(8).all()

    open_group_challenges = []
    for om in open_matches_raw:
        if om.player1_name and om.player1_name.strip().lower() == (player.display_name or '').strip().lower():
            continue
        r1 = om.rounds.filter_by(round_number=1).first()
        p1_sum = r1.get_p1_summary() if r1 else {}
        open_group_challenges.append({
            'match_code': om.match_code,
            'challenger_name': om.player1_name,
            'challenger_avatar': om.player1_avatar or 'quizzy',
            'category_name': r1.category_name if r1 else 'General Trivia',
            'p1_done': bool(p1_sum.get('done')),
            'p1_score': p1_sum.get('score', 0),
            'p1_correct': p1_sum.get('correct_count', 0),
            'p1_time': p1_sum.get('total_time_sec', 0)
        })

    return friends_roster, open_group_challenges


@arena_bp.route('/api/notifications')
def api_notifications():
    """Lightweight live notification endpoint for mobile & desktop: alerts when it's your turn, a friend challenged you, or a duel completed."""
    player = get_current_player(persist=False)
    active_matches = ArenaMatch.query.filter(
        (ArenaMatch.player1_session == player.session_key) | (ArenaMatch.player2_session == player.session_key),
        ArenaMatch.status.in_(['waiting', 'in_progress'])
    ).order_by(ArenaMatch.updated_at.desc()).limit(20).all()

    alerts = []
    active_match_states = {}
    for m in active_matches:
        exp_t = m.expected_turn()
        if m.current_turn != exp_t:
            m.current_turn = exp_t
            db.session.commit()

        is_p1 = (m.player1_session == player.session_key)
        opp_assigned = bool(m.player2_session and m.player2_session not in ('pending_invite', 'online_matchmaking', ''))
        my_turn = (m.current_turn == 1 and is_p1) or (m.current_turn == 2 and not is_p1)
        active_match_states[m.match_code] = {
            'my_turn': bool(my_turn),
            'current_round': m.current_round,
            'p1_total_score': m.p1_total_score,
            'p2_total_score': m.p2_total_score,
            # Oriented to whoever is asking, so the live refresh cannot undo the
            # card's "you first" score a few seconds after the page renders.
            'my_score': m.p1_total_score if is_p1 else m.p2_total_score,
            'their_score': m.p2_total_score if is_p1 else m.p1_total_score,
            'status': m.status
        }

        if m.is_bot or not opp_assigned:
            continue

        if my_turn:
            opp_name = m.player2_name if is_p1 else m.player1_name
            active_r = m.rounds.filter_by(round_number=m.current_round).first()
            cat_name = active_r.category_name if active_r else 'Trivia'
            is_new_challenge = (not is_p1 and m.current_round == 1 and m.p2_total_score == 0)
            alerts.append({
                'event_key': f"{m.match_code}_r{m.current_round}_t{m.current_turn}",
                'match_code': m.match_code,
                'opponent_name': opp_name,
                'round_number': m.current_round,
                'category_name': cat_name,
                'is_your_turn': True,
                'is_new_challenge': is_new_challenge,
                'title': f"⚔️ New Challenge from {opp_name}!" if is_new_challenge else f"🎉 {opp_name} finished their turn!",
                'message': f"{opp_name} challenged you to Round 1 ({cat_name})! Tap to play." if is_new_challenge else f"It's now YOUR TURN vs {opp_name} in Round {m.current_round} ({cat_name})!",
                'url': url_for('arena.match_lobby', match_code=m.match_code)
            })

    # Also check recently completed human duels so if an opponent finishes Round 6 while you're in another game, you get notified!
    recent_completed = ArenaMatch.query.filter(
        (ArenaMatch.player1_session == player.session_key) | (ArenaMatch.player2_session == player.session_key),
        ArenaMatch.status == 'completed'
    ).order_by(ArenaMatch.updated_at.desc()).limit(3).all()
    for cm in recent_completed:
        if cm.is_bot:
            continue
        is_p1 = (cm.player1_session == player.session_key)
        opp_name = cm.player2_name if is_p1 else cm.player1_name
        active_match_states[cm.match_code] = {
            'my_turn': False,
            'current_round': 6,
            'p1_total_score': cm.p1_total_score,
            'p2_total_score': cm.p2_total_score,
            'my_score': cm.p1_total_score if is_p1 else cm.p2_total_score,
            'their_score': cm.p2_total_score if is_p1 else cm.p1_total_score,
            'status': 'completed'
        }
        alerts.append({
            'event_key': f"{cm.match_code}_completed",
            'match_code': cm.match_code,
            'opponent_name': opp_name,
            'round_number': 6,
            'category_name': 'Final Results',
            'is_your_turn': False,
            'is_completed_event': True,
            'title': f"🏆 Duel Completed vs {opp_name}!",
            'message': f"{opp_name} finished Round 6! Final score: {cm.p1_total_score} - {cm.p2_total_score}. Tap to view results or Rematch!",
            'url': url_for('arena.match_lobby', match_code=cm.match_code)
        })

    your_turn_only_count = sum(1 for a in alerts if a.get('is_your_turn'))

    return jsonify({
        'success': True,
        'your_turn_count': your_turn_only_count,
        'alerts': alerts,
        'active_match_states': active_match_states
    })


def _live_matches_for(player):
    """Every duel of this player's still in play, with current_turn self-healed.

    Shared by the duels dashboard and the Hub overview so the two pages can
    never disagree about whose move it is.
    """
    raw_active = ArenaMatch.query.filter(
        (ArenaMatch.player1_session == player.session_key) | (ArenaMatch.player2_session == player.session_key),
        ArenaMatch.status.in_(['waiting', 'in_progress'])
    ).order_by(ArenaMatch.updated_at.desc()).all()

    dirty = False
    for m in raw_active:
        if m.current_round >= 6:
            r6 = m.rounds.filter_by(round_number=6).first()
            if r6 and r6.get_p1_answers() and r6.get_p2_answers():
                m.status = 'completed'
                if m.p1_total_score > m.p2_total_score:
                    m.winner = 1
                elif m.p2_total_score > m.p1_total_score:
                    m.winner = 2
                else:
                    m.winner = 0
                dirty = True
                continue
        exp_t = m.expected_turn()
        if m.current_turn != exp_t:
            m.current_turn = exp_t
            dirty = True
    if dirty:
        db.session.commit()

    return [m for m in raw_active if m.status in ('waiting', 'in_progress')]


def _annotate_match(m, player_key):
    """Attach the viewer's own side of a match, for the duel cards.

    Either player can appear in either list now, so a card can no longer work
    out who the opponent is from which list it was rendered in.
    """
    is_p1 = (m.player1_session == player_key)
    m.qm_i_created = is_p1
    m.qm_opponent_name = (m.player2_name if is_p1 else m.player1_name)
    m.qm_opponent_avatar = (m.player2_avatar if is_p1 else m.player1_avatar)
    m.qm_my_score = (m.p1_total_score if is_p1 else m.p2_total_score)
    m.qm_their_score = (m.p2_total_score if is_p1 else m.p1_total_score)
    m.qm_completed = (m.status == 'completed')
    m.qm_unaccepted = bool(
        is_p1
        and (not m.player2_session
             or m.player2_session in ('pending_invite', 'online_matchmaking', ''))
    )
    m.qm_my_turn = bool(
        not m.qm_completed
        and not m.qm_unaccepted
        and m.is_player_turn(player_key)
    )
    return m


@arena_bp.route('/')
def dashboard():
    """Arena Hub: Active duels, Completed Duels ready for Rematch, Friends & Group Challenges, leaderboards preview, and quick play."""
    player = get_current_player(persist=False)

    active_matches = _live_matches_for(player)

    # Finished matches
    history_matches = ArenaMatch.query.filter(
        (ArenaMatch.player1_session == player.session_key) | (ArenaMatch.player2_session == player.session_key),
        ArenaMatch.status.in_(['completed', 'forfeited'])
    ).order_by(ArenaMatch.updated_at.desc()).limit(8).all()

    # Include recent completed duels (that don't already have an active rematch) in active_matches so they show "COMPLETED • CLICK TO REMATCH"
    active_opp_sessions = set()
    for m in active_matches:
        opp_s = m.player2_session if m.player1_session == player.session_key else m.player1_session
        if opp_s:
            active_opp_sessions.add(opp_s)

    seen_completed_opps = set()
    for hm in history_matches:
        if hm.status != 'completed':
            continue
        opp_s = hm.player2_session if hm.player1_session == player.session_key else hm.player1_session
        if opp_s and opp_s not in active_opp_sessions and opp_s not in seen_completed_opps:
            if not hm.is_bot:
                seen_completed_opps.add(opp_s)
            active_matches.append(hm)
            if len(active_matches) >= 12:
                break

    # Categorize matches by WHOSE TURN IT IS, not by who created the duel.
    #
    # Splitting on creator looked right and was wrong in both directions: a duel
    # you started sat under "waiting on them" even on the rounds where it was
    # your move, and a duel you were challenged to sat under "your turn" even
    # while you were waiting. Wendy never saw a live round-3 duel she had
    # created, because "invites you sent" reads as "not accepted yet"; Amy saw
    # the same duel nagging her for a turn she had already taken.
    #
    # 1. Duels where it is your move
    your_move_matches = []
    # 2. Duels waiting on the other player, plus invites nobody has accepted yet
    waiting_matches = []
    # 3. Solo / Bot Nova training matches
    bot_matches = []

    for m in active_matches:
        _annotate_match(m, player.session_key)

        if m.is_bot:
            bot_matches.append(m)
        elif m.qm_my_turn:
            your_move_matches.append(m)
        else:
            waiting_matches.append(m)

    # Every in-flight card gets the animated ring; the card at the top of the
    # list -- the most recently played, since the query is newest first -- also
    # carries the travelling point of light.
    urgent_candidates = [m for m in (your_move_matches + bot_matches)
                         if not m.qm_completed and not m.qm_unaccepted]
    urgent_code = urgent_candidates[0].match_code if urgent_candidates else None

    # Live group lobbies, with enough detail for the dashboard to draw the seats
    group_lobbies = []
    for g in GroupGame.query.filter_by(status='lobby').order_by(GroupGame.created_at.desc()).limit(4).all():
        seats = list(g.players)
        group_lobbies.append({
            'code': g.code,
            'category_name': g.category_name,
            'filled': len(seats),
            'max_players': g.max_players or 6,
            'min_players': g.min_players or 3,
            'questions': g.total_questions,
            'seconds': g.seconds_per_question,
            'names': [p.display_name for p in seats][:6],
            'starting': bool(g.starts_at)
        })

    # Friends Roster & Open Group Challenges
    friends_roster, open_group_challenges = _get_friends_and_group_challenges(player)

    # Top leaderboards
    top_players = PlayerProfile.query.filter_by(is_paused=False).order_by(PlayerProfile.xp.desc()).limit(5).all()

    # Available Packs
    packs = QuizPack.query.order_by(QuizPack.created_at.desc()).limit(6).all()

    # Completed Battles & Duels Summary (Only for logged-in players with finished games)
    completed_battles_summary = _dashboard_completed(player)

    return render_template(
        'themes/quizhub/arena_dashboard.html',
        player=player,
        my_games_challenges=_dashboard_challenges(player.session_key),
        completed_battles_summary=completed_battles_summary,
        active_matches=active_matches,
        your_move_matches=your_move_matches,
        waiting_matches=waiting_matches,
        urgent_code=urgent_code,
        bot_matches=bot_matches,
        history_matches=history_matches,
        friends_roster=friends_roster,
        open_group_challenges=open_group_challenges,
        group_lobbies=group_lobbies,
        top_players=top_players,
        packs=packs,
        avatars=AVATAR_PRESETS
    )


@arena_bp.route('/hub')
def hub():
    """My Hub: who you are, what is in flight, and what you have finished.

    The duels page was doing three jobs at once -- identity, history and "what
    can I play next" -- which is why it read as cluttered. Identity and history
    moved here; the duels page keeps only the things you can act on. Anything
    in progress is summarised here and played from there, so the Hub is never
    the only route into a game already running.
    """
    player = get_current_player(persist=False)

    live = [_annotate_match(m, player.session_key) for m in _live_matches_for(player)]
    challenges = _dashboard_challenges(player.session_key)

    in_progress = []
    for m in live:
        if m.qm_unaccepted:
            continue  # nobody has taken the other seat, so nothing is in flight
        in_progress.append({
            'kind': 'duel',
            'kind_label': 'Bot practice' if m.is_bot else 'Quiz duel',
            'opponent': m.qm_opponent_name,
            'avatar': m.qm_opponent_avatar,
            'detail': 'Round %s of 6' % m.current_round,
            'score': '%s - %s' % (m.qm_my_score, m.qm_their_score),
            'pct': int(min(100, max(0, ((m.current_round - 1) / 6.0) * 100))),
            'my_turn': m.qm_my_turn,
            'url': url_for('arena.match_lobby', match_code=m.match_code),
            'code': m.match_code,
        })

    for bucket, mine in (('your_turn', True), ('waiting', False)):
        for ch in challenges[bucket]:
            if not ch['accepted']:
                continue
            in_progress.append({
                'kind': 'challenge',
                'kind_label': '5 mini games',
                'opponent': ch['opponent'],
                'avatar': None,
                'detail': '%s of %s played' % (ch['played'], ch['total']),
                'score': 'you %s-%s' % (ch['you'], ch['them']),
                'pct': int((ch['played'] / float(ch['total'])) * 100) if ch['total'] else 0,
                'my_turn': mine,
                'url': url_for('games.challenge', code=ch['code']),
                'code': ch['code'],
            })

    # Whatever needs you most goes first, and only that one breathes --
    # a marker on every card stops pointing at anything.
    in_progress.sort(key=lambda i: (not i['my_turn'], -i['pct']))
    urgent_code = in_progress[0]['code'] if in_progress else None

    return render_template(
        'themes/quizhub/arena_hub.html',
        player=player,
        in_progress=in_progress,
        urgent_code=urgent_code,
        your_turn_count=sum(1 for i in in_progress if i['my_turn']),
        completed_battles_summary=_dashboard_completed(player),
        avatars=AVATAR_PRESETS,
    )


@arena_bp.route('/new', methods=['GET', 'POST'])
def create_match():
    """Create a new head-to-head match or challenge (bot, friend, or online matchmaking)."""
    opponent_mode = request.form.get('opponent_mode') or request.args.get('opponent_mode', 'friend')  # 'friend', 'bot', 'online'
    category_slug = request.form.get('category_slug') or request.args.get('category_slug')
    friend_invite_name = (request.form.get('friend_name') or request.args.get('friend_name') or '').strip()

    if opponent_mode in ('friend', 'online'):
        gate = needs_account_to_challenge('challenge a friend to a duel')
        if gate:
            return gate

    player = get_current_player()

    # If opponent_mode is 'online', check if another player already has an open online_matchmaking duel waiting in Round 1!
    if opponent_mode == 'online':
        open_online_matches = ArenaMatch.query.filter(
            ArenaMatch.player2_session == 'online_matchmaking',
            ArenaMatch.player1_session != player.session_key,
            ArenaMatch.current_round == 1,
            ArenaMatch.status.in_(['waiting', 'in_progress'])
        ).order_by(ArenaMatch.created_at.desc()).limit(10).all()

        matched_duel = None
        if category_slug:
            for m in open_online_matches:
                r1 = m.rounds.filter_by(round_number=1).first()
                if r1 and r1.category_slug == category_slug:
                    matched_duel = m
                    break
        if not matched_duel and open_online_matches:
            matched_duel = open_online_matches[0]

        if matched_duel:
            matched_duel.player2_session = player.session_key
            matched_duel.player2_name = player.display_name
            matched_duel.player2_avatar = player.avatar_key
            matched_duel.status = 'in_progress'
            db.session.commit()
            flash(f"⚡ Online Challenger Found! Matched against {matched_duel.player1_name}!", "success")
            return redirect(url_for('arena.match_lobby', match_code=matched_duel.match_code))

    match_code = f"qm_{secrets.token_hex(4)}"

    # Pick 3 available categories
    available_cats = db.session.query(QuizQuestion.category_slug, QuizQuestion.category_name).distinct().all()
    if not available_cats:
        cat_slug, cat_name = 'science-cosmos', 'Science & Cosmos'
    elif category_slug:
        cat_match = next((c for c in available_cats if c[0] == category_slug), available_cats[0])
        cat_slug, cat_name = cat_match[0], cat_match[1]
    else:
        chosen = random.choice(available_cats)
        cat_slug, cat_name = chosen[0], chosen[1]

    # Pick 3 randomized questions for Round 1
    questions = get_random_questions(category_slug=cat_slug, count=3)
    if not questions:
        questions = QuizQuestion.query.order_by(func.random()).limit(3).all()
    q_ids = [q.id for q in questions]

    match = ArenaMatch(
        match_code=match_code,
        player1_session=player.session_key,
        player1_name=player.display_name,
        player1_avatar=player.avatar_key,
        player2_name=friend_invite_name if friend_invite_name else (
            'Searching Online Player...' if opponent_mode == 'online'
            else ('Awaiting Challenger...' if opponent_mode in ('open', 'random') else 'Invited Friend')
        ),
        status='waiting',
        current_round=1,
        current_turn=1,
        winner=0,
        p1_total_score=0,
        p2_total_score=0
    )

    if opponent_mode == 'bot':
        bot_avatar = 'nova' if player.avatar_key != 'nova' else 'pixel'
        match.player2_session = 'bot_quizmondo_ai'
        match.player2_name = 'Cyber Bot Nova'
        match.player2_avatar = bot_avatar
        match.status = 'in_progress'
    elif opponent_mode == 'online':
        match.player2_session = 'online_matchmaking'
        match.player2_name = 'Searching Online Player...'
        match.status = 'waiting'

    db.session.add(match)
    db.session.flush()

    # Create Round 1
    round_1 = ArenaRound(
        match_id=match.id,
        round_number=1,
        category_slug=cat_slug,
        category_name=cat_name,
        chosen_by=1,
        question_ids_json=json.dumps(q_ids),
        p1_score=0,
        p1_answers_json=json.dumps([]),
        p2_score=0,
        p2_answers_json=json.dumps([]),
        status='pending'
    )
    db.session.add(round_1)
    db.session.commit()

    # If starting a Friend Challenge without a setup profile yet, launch the quick 3-step setup first
    # and redirect straight into this match lobby so they can invite their friend & play Round 1!
    if opponent_mode == 'friend' and not session.get('user_id'):
        return redirect(url_for('arena.player_register', next=url_for('arena.match_lobby', match_code=match_code)))

    return redirect(url_for('arena.match_lobby', match_code=match_code))


def _build_round_comparison(r: ArenaRound) -> list:
    """Build question-by-question head-to-head comparison once BOTH players have completed a round."""
    p1_ans_map = {a.get('question_id'): a for a in r.get_p1_answers() if isinstance(a, dict)}
    p2_ans_map = {a.get('question_id'): a for a in r.get_p2_answers() if isinstance(a, dict)}
    q_ids = r.get_question_ids()
    questions = QuizQuestion.query.filter(QuizQuestion.id.in_(q_ids)).all() if q_ids else []
    q_map = {q.id: q for q in questions}

    comparison = []
    for idx, qid in enumerate(q_ids, start=1):
        q = q_map.get(qid)
        if not q:
            continue
        opts = q.get_options()
        a1 = p1_ans_map.get(qid, {})
        a2 = p2_ans_map.get(qid, {})
        c1 = a1.get('selected') or '—'
        c2 = a2.get('selected') or '—'
        t1 = a1.get('time_taken', round(max(0.5, (q.time_limit or 15) - float(a1.get('time_left', 10))), 1) if a1 else 0)
        t2 = a2.get('time_taken', round(max(0.5, (q.time_limit or 15) - float(a2.get('time_left', 10))), 1) if a2 else 0)
        comparison.append({
            'q_num': idx,
            'prompt': q.prompt,
            'correct_option': q.correct_option,
            'correct_text': opts.get(q.correct_option, q.correct_option),
            'p1_choice': c1,
            'p1_text': opts.get(c1, c1) if c1 in opts else ('Timed Out' if c1 == 'TIMEOUT' else c1),
            'p1_correct': bool(a1.get('is_correct')),
            'p1_points': a1.get('points_awarded', 0),
            'p1_time': t1,
            'p2_choice': c2,
            'p2_text': opts.get(c2, c2) if c2 in opts else ('Timed Out' if c2 == 'TIMEOUT' else ('Bot Correct' if a2.get('is_correct') else 'Bot Missed')),
            'p2_correct': bool(a2.get('is_correct')),
            'p2_points': a2.get('points_awarded', 0),
            'p2_time': t2,
        })
    return comparison


def _build_whatsapp_messages(match: ArenaMatch, player: PlayerProfile, is_player1: bool, base_url: str) -> tuple:
    """Generate rich WhatsApp invite and turn-nudge messages including round score, X/3 correct, and time in seconds."""
    lobby_url = f"{base_url}/arena/match/{match.match_code}"
    all_rounds = match.rounds.order_by(ArenaRound.round_number.asc()).all()
    active_round = match.rounds.filter_by(round_number=match.current_round).first()
    active_cat = active_round.category_name if active_round else "General Trivia"

    # Find the latest round this player has completed
    my_latest_round = None
    my_latest_summary = None
    for r in reversed(all_rounds):
        s = r.get_p1_summary() if is_player1 else r.get_p2_summary()
        if s.get('done'):
            my_latest_round = r
            my_latest_summary = s
            break

    opponent_assigned = bool(match.player2_session and match.player2_session not in ('pending_invite', 'online_matchmaking', '') and match.player2_session != match.player1_session)
    raw_opp_name = match.player2_name if is_player1 else match.player1_name
    if not opponent_assigned or not raw_opp_name or raw_opp_name.lower() in ('awaiting challenger...', 'searching online player...', player.display_name.lower()):
        target_nudgee = 'Friend'
    else:
        target_nudgee = raw_opp_name

    if my_latest_round and my_latest_summary:
        r_num = my_latest_round.round_number
        r_cat = my_latest_round.category_name
        r_score = my_latest_summary['score']
        r_corr = my_latest_summary['correct_count']
        r_total_q = my_latest_summary['total_questions']
        r_time = my_latest_summary['total_time_sec']

        whatsapp_text = (
            f"⚡ *QUIZMONDO CHALLENGE!* ⚡\n"
            f"🦸‍♂️ *{player.display_name}* challenged you to a 6-Round Trivia Duel!\n\n"
            f"🔥 *Round {r_num} ({r_cat}):*\n"
            f"✅ Got *{r_corr}/{r_total_q} correct* in *⏱️ {r_time}s*\n"
            f"🏆 Scored *{r_score} PTS* (Total: {match.p1_total_score if is_player1 else match.p2_total_score} PTS)\n\n"
            f"Think you can beat my score and time? Answers unlock after you play!\n"
            f"👇 *TAP TO ACCEPT CHALLENGE:* 👇\n"
            f"{lobby_url}"
        )

        if not opponent_assigned:
            whatsapp_nudge_text = whatsapp_text
        else:
            my_total = match.p1_total_score if is_player1 else match.p2_total_score
            opp_total = match.p2_total_score if is_player1 else match.p1_total_score
            whatsapp_nudge_text = (
                f"🔔 *QUIZMONDO TURN NUDGE • ROUND {match.current_round}* 🔔\n"
                f"⚔️ Hey *{target_nudgee}*! *{player.display_name}* just finished Round {r_num} ({r_cat})!\n\n"
                f"🎯 *{player.display_name}'s Round {r_num} Stats:*\n"
                f"• Score: *+{r_score} PTS*\n"
                f"• Accuracy: *{r_corr}/{r_total_q} Correct*\n"
                f"• Speed: *⏱️ {r_time}s*\n"
                f"📊 *Match Total:* {player.display_name} ({my_total} PTS) vs {target_nudgee} ({opp_total} PTS)\n\n"
                f"🔥 It's *YOUR TURN* to play Round {match.current_round} (and see the Round {r_num} answer comparison)!\n"
                f"👇 *TAP TO PLAY YOUR TURN:* 👇\n"
                f"{lobby_url}"
            )
    else:
        whatsapp_text = (
            f"⚡ *QUIZMONDO ARENA CHALLENGE!* ⚡\n"
            f"🦸‍♂️ *{player.display_name}* has challenged you to a 6-Round Head-to-Head Trivia Duel!\n"
            f"🔥 *Round 1 Category:* {active_cat}\n\n"
            f"👇 *TAP BELOW TO ACCEPT THE CHALLENGE:* 👇\n"
            f"{lobby_url}"
        )
        whatsapp_nudge_text = whatsapp_text

    return lobby_url, whatsapp_text, whatsapp_nudge_text


@arena_bp.route('/match/<match_code>')
def match_lobby(match_code):
    """Lobby, turn sync controller, and stage-gated round answer comparison for a match."""
    player = get_current_player(persist=False)
    match = ArenaMatch.query.filter_by(match_code=match_code).first_or_404()
    has_account = bool(session.get('user_id'))

    # 1. Self-duel protection & automatic cleanup if player1 was accidentally assigned to player2
    if not match.is_bot and match.player2_session:
        same_session = (match.player2_session == match.player1_session)
        same_name = bool(match.player1_name and match.player2_name and match.player1_name.strip().lower() == match.player2_name.strip().lower())
        if same_session or same_name:
            match.player2_session = None
            match.player2_name = 'Awaiting Challenger...'
            if match.current_round == 1:
                match.status = 'waiting'
            db.session.commit()

    # 2. Check if current visitor is Player 1 (by session_key or by logged-in username)
    is_player1 = (match.player1_session == player.session_key) or (
        has_account and match.player1_name and match.player1_name.strip().lower() == player.display_name.strip().lower()
    )
    if is_player1 and match.player1_session != player.session_key:
        match.player1_session = player.session_key
        match.player1_name = player.display_name
        db.session.commit()

    # 3. If visitor is NOT Player 1, and Player 2 slot is open on Round 1:
    # Only auto-bind Player 2 once they have completed the quick 3-step account setup (so their Superhero Name & PIN are saved!)
    if not is_player1 and not match.is_bot and (not match.player2_session or match.player2_session in ('pending_invite', 'online_matchmaking', '')) and match.current_round == 1:
        if has_account:
            match.player2_session = player.session_key
            match.player2_name = player.display_name
            match.player2_avatar = player.avatar_key
            match.status = 'in_progress'
            db.session.commit()

    is_player2 = (match.player2_session == player.session_key) or (
        not is_player1 and has_account and match.player2_name and match.player2_name.strip().lower() == player.display_name.strip().lower()
    )
    if is_player2 and match.player2_session != player.session_key:
        match.player2_session = player.session_key
        match.player2_name = player.display_name
        db.session.commit()

    is_online_matchmaking = (match.player2_session == 'online_matchmaking')
    # A guest challenger viewing an open Round 1 invite is an invited challenger ready to accept!
    is_invited_challenger = (not is_player1 and not is_player2 and not match.is_bot and (not match.player2_session or match.player2_session in ('pending_invite', 'online_matchmaking', '')) and match.current_round == 1)
    is_participant = is_player1 or is_player2 or is_invited_challenger

    # 4. Synchronize match.current_turn with deterministic Snake Turn Order
    if match.status in ('waiting', 'in_progress'):
        exp_turn = match.expected_turn()
        if match.current_turn != exp_turn:
            match.current_turn = exp_turn
            db.session.commit()

    active_round = match.rounds.filter_by(round_number=match.current_round).first()
    my_turn = False
    if match.status in ('waiting', 'in_progress'):
        if match.is_bot and is_player1:
            my_turn = True
        elif is_player1 and match.current_turn == 1:
            my_turn = True
        elif (is_player2 or is_invited_challenger) and match.current_turn == 2:
            my_turn = True

    opponent_assigned = bool(match.player2_session and match.player2_session not in ('pending_invite', 'online_matchmaking', ''))
    if is_player1:
        opponent_name = match.player2_name if opponent_assigned else ('Online Player' if is_online_matchmaking else 'Your Friend')
    else:
        opponent_name = match.player1_name

    base_url = current_app.config.get('APP_PUBLIC_URL', request.host_url.rstrip('/'))
    invite_url, whatsapp_text, whatsapp_nudge_text = _build_whatsapp_messages(match, player, is_player1, base_url)

    # 5. Build Stage-Gated Round Details (Exact answers ONLY included when both players have finished the round!)
    all_rounds = match.rounds.order_by(ArenaRound.round_number.asc()).all()
    rounds_detail = []
    opponent_active_summary = None
    my_active_summary = None

    for r in all_rounds:
        p1_sum = r.get_p1_summary()
        p2_sum = r.get_p2_summary()
        both_done = bool(p1_sum['done'] and p2_sum['done'])
        comparison = _build_round_comparison(r) if both_done else []
        rounds_detail.append({
            'round': r,
            'round_number': r.round_number,
            'category_name': r.category_name,
            'p1_summary': p1_sum,
            'p2_summary': p2_sum,
            'both_done': both_done,
            'comparison': comparison
        })
        if r.round_number == match.current_round:
            my_active_summary = p1_sum if is_player1 else p2_sum
            opponent_active_summary = p2_sum if is_player1 else p1_sum

    friends_roster, open_group_challenges = _get_friends_and_group_challenges(player)

    # Check if this match is completed and one of the two players already clicked "Rematch" to start a new active duel!
    active_rematch = None
    if match.status == 'completed' and not match.is_bot and opponent_assigned:
        active_rematch = ArenaMatch.query.filter(
            ArenaMatch.id != match.id,
            ((ArenaMatch.player1_session == match.player1_session) & (ArenaMatch.player2_session == match.player2_session)) |
            ((ArenaMatch.player1_session == match.player2_session) & (ArenaMatch.player2_session == match.player1_session)),
            ArenaMatch.status.in_(['waiting', 'in_progress'])
        ).order_by(ArenaMatch.created_at.desc()).first()

    return render_template(
        'themes/quizhub/arena_match.html',
        match=match,
        player=player,
        is_player1=is_player1,
        is_player2=is_player2,
        is_invited_challenger=is_invited_challenger,
        is_online_matchmaking=is_online_matchmaking,
        is_participant=is_participant,
        opponent_name=opponent_name,
        opponent_assigned=opponent_assigned,
        active_round=active_round,
        my_turn=my_turn,
        all_rounds=all_rounds,
        rounds_detail=rounds_detail,
        my_active_summary=my_active_summary,
        opponent_active_summary=opponent_active_summary,
        invite_url=invite_url,
        whatsapp_text=whatsapp_text,
        whatsapp_nudge_text=whatsapp_nudge_text,
        has_account=has_account,
        friends_roster=friends_roster,
        open_group_challenges=open_group_challenges,
        active_rematch=active_rematch
    )


@arena_bp.route('/match/<match_code>/convert-to-whatsapp', methods=['GET', 'POST'])
def convert_to_whatsapp(match_code):
    """Convert an online matchmaking duel into a WhatsApp Friend Challenge."""
    player = get_current_player()
    match = ArenaMatch.query.filter_by(match_code=match_code).first_or_404()
    if match.player1_session == player.session_key and not match.is_bot:
        match.player2_session = None
        match.player2_name = 'Invited Friend'
        db.session.commit()
        flash("📲 Converted to WhatsApp Friend Challenge! Invite your friend on WhatsApp below!", "success")
    return redirect(url_for('arena.match_lobby', match_code=match_code, open_whatsapp='1'))


@arena_bp.route('/match/<match_code>/status')
def match_status_poll(match_code):
    """Lightweight JSON status endpoint so waiting players auto-refresh when an opponent joins, completes a round, or starts a rematch."""
    player = get_current_player(persist=False)
    match = ArenaMatch.query.filter_by(match_code=match_code).first_or_404()
    if match.status in ('waiting', 'in_progress'):
        exp_t = match.expected_turn()
        if match.current_turn != exp_t:
            match.current_turn = exp_t
            db.session.commit()

    opponent_assigned = bool(match.player2_session and match.player2_session not in ('pending_invite', 'online_matchmaking', ''))
    is_p1 = (match.player1_session == player.session_key)
    my_turn = False
    if match.status in ('waiting', 'in_progress'):
        if match.is_bot and is_p1:
            my_turn = True
        elif is_p1 and match.current_turn == 1:
            my_turn = True
        elif not is_p1 and match.current_turn == 2:
            my_turn = True

    active_r = match.rounds.filter_by(round_number=match.current_round).first()
    rematch_code = None
    if match.status == 'completed' and not match.is_bot and opponent_assigned:
        rm = ArenaMatch.query.filter(
            ArenaMatch.id != match.id,
            ((ArenaMatch.player1_session == match.player1_session) & (ArenaMatch.player2_session == match.player2_session)) |
            ((ArenaMatch.player1_session == match.player2_session) & (ArenaMatch.player2_session == match.player1_session)),
            ArenaMatch.status.in_(['waiting', 'in_progress'])
        ).order_by(ArenaMatch.created_at.desc()).first()
        if rm:
            rematch_code = rm.match_code

    return jsonify({
        'status': match.status,
        'current_round': match.current_round,
        'current_turn': match.current_turn,
        'my_turn': my_turn,
        'active_category': active_r.category_name if active_r else 'Trivia',
        'opponent_assigned': opponent_assigned,
        'player2_name': match.player2_name,
        'p1_total_score': match.p1_total_score,
        'p2_total_score': match.p2_total_score,
        'rematch_code': rematch_code
    })


@arena_bp.route('/match/<match_code>/card.png')
def match_card_image(match_code):
    """Dynamic 1200x630 OpenGraph match preview card for WhatsApp and social sharing."""
    match = ArenaMatch.query.filter_by(match_code=match_code).first_or_404()
    active_r = match.rounds.filter_by(round_number=match.current_round).first()
    cat_name = active_r.category_name if active_r else "General Trivia"
    png_bytes = generate_duel_card_png(
        p1_name=match.player1_name or "Player 1",
        p2_name=match.player2_name or "Challenger",
        round_num=match.current_round,
        category_name=cat_name,
        p1_score=match.p1_total_score,
        p2_score=match.p2_total_score,
        match_code=match.match_code
    )
    resp = Response(png_bytes, mimetype='image/png')
    resp.headers['Cache-Control'] = 'public, max-age=60'
    return resp


@arena_bp.route('/match/<match_code>/nudge')
def match_nudge_redirect(match_code):
    """Deep link for WhatsApp nudge: auto-claims player 2 if open and sends directly into the playable questions!"""
    return redirect(url_for('arena.play_round', match_code=match_code))


@arena_bp.route('/match/<match_code>/play')
def play_round(match_code):
    """Live interactive round play screen with timer and mascot reaction."""
    player = get_current_player(persist=False)
    match = ArenaMatch.query.filter_by(match_code=match_code).first_or_404()
    has_account = bool(session.get('user_id'))

    is_player1 = (match.player1_session == player.session_key) or (
        has_account and match.player1_name and match.player1_name.strip().lower() == player.display_name.strip().lower()
    )
    if is_player1 and match.player1_session != player.session_key:
        match.player1_session = player.session_key
        match.player1_name = player.display_name
        db.session.commit()

    is_player2 = (match.player2_session == player.session_key) or (
        not is_player1 and has_account and match.player2_name and match.player2_name.strip().lower() == player.display_name.strip().lower()
    )
    if is_player2 and match.player2_session != player.session_key:
        match.player2_session = player.session_key
        match.player2_name = player.display_name
        db.session.commit()

    if not (is_player1 or is_player2):
        # Challenger accepting Round 1 invite: require quick 3-step setup first so their Superhero Name & PIN are saved!
        if not match.is_bot and match.current_round == 1 and (not match.player2_session or match.player2_session in ('pending_invite', 'online_matchmaking', '')):
            if not has_account:
                return redirect(url_for('arena.player_register', next=url_for('arena.play_round', match_code=match_code)))
            match.player2_session = player.session_key
            match.player2_name = player.display_name
            match.player2_avatar = player.avatar_key
            match.status = 'in_progress'
            db.session.commit()
            is_player2 = True
        else:
            flash(f"This duel is already locked between {match.player1_name} and {match.player2_name or 'another challenger'} (Round {match.current_round}).", "info")
            return redirect(url_for('arena.match_lobby', match_code=match_code))

    # Gating requirement: in human friend duels, players must have their 3-step account set up
    if not match.is_bot and not has_account and match.current_round > 1:
        return redirect(url_for('arena.player_register', next=url_for('arena.play_round', match_code=match_code)))

    # Synchronize & verify turn order
    exp_turn = match.expected_turn()
    if match.current_turn != exp_turn:
        match.current_turn = exp_turn
        db.session.commit()

    if not match.is_bot:
        if (is_player1 and match.current_turn != 1) or (is_player2 and match.current_turn != 2):
            flash("You have completed your turn for this round! Waiting for your opponent.", "info")
            return redirect(url_for('arena.match_lobby', match_code=match_code))

    active_round = match.rounds.filter_by(round_number=match.current_round).first()
    if not active_round or match.status not in ('waiting', 'in_progress'):
        return redirect(url_for('arena.match_lobby', match_code=match_code))

    # Fetch questions for this round
    q_ids = active_round.get_question_ids()
    questions = QuizQuestion.query.filter(QuizQuestion.id.in_(q_ids)).all()
    q_dict = {q.id: q for q in questions}
    ordered_questions = [q_dict[qid] for qid in q_ids if qid in q_dict]

    # Mask correct answers on client side initially
    client_questions = []
    for q in ordered_questions:
        client_questions.append({
            'id': q.id,
            'prompt': q.prompt,
            'question_type': q.question_type,
            'media_url': q.media_url,
            'options': q.get_options(),
            'category_name': q.category_name,
            'time_limit': q.time_limit or 15
        })

    return render_template(
        'themes/quizhub/arena_play.html',
        match=match,
        active_round=active_round,
        player=player,
        questions_json=json.dumps(client_questions),
        total_questions=len(client_questions)
    )


@arena_bp.route('/match/<match_code>/submit', methods=['POST'])
def submit_round(match_code):
    """Receive player round responses, compute score & time, enforce Snake Turn Sync, and return stage payload."""
    player = get_current_player()
    match = ArenaMatch.query.filter_by(match_code=match_code).first_or_404()
    has_account = bool(session.get('user_id'))

    is_player1 = (match.player1_session == player.session_key) or (
        has_account and match.player1_name and match.player1_name.strip().lower() == player.display_name.strip().lower()
    )
    is_player2 = (match.player2_session == player.session_key) or (
        not is_player1 and has_account and match.player2_name and match.player2_name.strip().lower() == player.display_name.strip().lower()
    )
    if not (is_player1 or is_player2):
        return jsonify({'error': 'Unauthorized participant'}), 403

    payload = request.get_json() or {}
    answers = payload.get('answers', [])  # list of { question_id, choice, time_left }

    active_round = match.rounds.filter_by(round_number=match.current_round).first()
    if not active_round:
        return jsonify({'error': 'Active round not found'}), 404

    completed_round_num = active_round.round_number
    completed_round_cat = active_round.category_name

    # Prevent duplicate submission of the same round by the same player
    already_done = bool(active_round.get_p1_answers()) if is_player1 else bool(active_round.get_p2_answers())
    if already_done:
        return jsonify({'redirect': url_for('arena.match_lobby', match_code=match_code)})

    q_ids = active_round.get_question_ids()
    questions = QuizQuestion.query.filter(QuizQuestion.id.in_(q_ids)).all()
    q_map = {q.id: q for q in questions}

    round_score = 0
    correct_count = 0
    total_time_sec = 0.0
    detailed_results = []

    for ans in answers:
        qid = ans.get('question_id')
        choice = (ans.get('choice') or '').strip().upper()
        time_left = max(0, int(ans.get('time_left', 0)))

        q = q_map.get(qid)
        if not q:
            continue

        q_limit = q.time_limit or 15
        time_taken = round(max(0.5, float(q_limit - time_left)), 1)
        total_time_sec = round(total_time_sec + time_taken, 1)

        is_correct = (choice == q.correct_option)
        points_awarded = 0
        if is_correct:
            correct_count += 1
            speed_bonus = time_left * 5
            points_awarded = q.points + speed_bonus
            round_score += points_awarded

        detailed_results.append({
            'question_id': q.id,
            'prompt': q.prompt,
            'selected': choice,
            'correct_option': q.correct_option,
            'is_correct': is_correct,
            'time_left': time_left,
            'time_taken': time_taken,
            'explanation': q.explanation,
            'points_awarded': points_awarded
        })

    # Record answers and update scores
    if is_player1:
        active_round.p1_score = round_score
        active_round.p1_answers_json = json.dumps(detailed_results)
        match.p1_total_score = (match.p1_total_score or 0) + round_score
    else:
        active_round.p2_score = round_score
        active_round.p2_answers_json = json.dumps(detailed_results)
        match.p2_total_score = (match.p2_total_score or 0) + round_score

    # Award player XP and coins
    player.add_xp(round_score)
    player.coins = (player.coins or 0) + (round_score // 10)
    player.last_active_at = datetime.utcnow()

    # ONLY simulate bot round if this match was explicitly created as a Bot Match (never overwrite a Friend Duel!)
    if match.is_bot and is_player1:
        bot_score = 0
        bot_detailed = []
        for q in questions:
            bot_correct = (random.random() < 0.65)
            bot_tl = random.randint(4, 12) if bot_correct else random.randint(1, 8)
            bot_pts = q.points + (bot_tl * 5) if bot_correct else 0
            bot_score += bot_pts
            # A miss has to land on an option that is actually wrong. This used to
            # be hard-coded to 'B', so whenever B was the right answer the results
            # screen showed the bot picking the correct line and marked it wrong.
            wrong_options = [k for k in (q.get_options() or {}) if k != q.correct_option]
            bot_choice = q.correct_option if bot_correct else (
                random.choice(wrong_options) if wrong_options else q.correct_option)
            bot_detailed.append({
                'question_id': q.id,
                'selected': bot_choice,
                'is_correct': bot_correct,
                'time_left': bot_tl,
                'time_taken': round(15.0 - bot_tl, 1),
                'points_awarded': bot_pts
            })
        active_round.p2_score = bot_score
        active_round.p2_answers_json = json.dumps(bot_detailed)
        match.p2_total_score = (match.p2_total_score or 0) + bot_score
        active_round.status = 'completed'

    # Check if both have completed this round
    has_p1_done = bool(active_round.p1_answers_json and active_round.p1_answers_json != '[]')
    has_p2_done = bool(active_round.p2_answers_json and active_round.p2_answers_json != '[]')
    both_completed_round = bool(has_p1_done and has_p2_done)

    opp_round_summary = active_round.get_p2_summary() if is_player1 else active_round.get_p1_summary()
    round_comparison = _build_round_comparison(active_round) if both_completed_round else []

    chosen_cat = None
    continue_next_round = False

    if both_completed_round:
        active_round.status = 'completed'
        if match.current_round >= 6:
            match.status = 'completed'
            if match.p1_total_score > match.p2_total_score:
                match.winner = 1
                if is_player1:
                    player.matches_won = (player.matches_won or 0) + 1
            elif match.p2_total_score > match.p1_total_score:
                match.winner = 2
                if is_player2:
                    player.matches_won = (player.matches_won or 0) + 1
            else:
                match.winner = 0
            player.matches_played = (player.matches_played or 0) + 1
        else:
            # Advance to next round!
            match.current_round += 1
            # SNAKE TURN SYNC:
            # The player who just caught up to complete Round R immediately leads off Round R + 1!
            if match.is_bot:
                next_turn = 1
            else:
                next_turn = 1 if is_player1 else 2
            match.current_turn = next_turn
            continue_next_round = True

            all_cats = db.session.query(QuizQuestion.category_slug, QuizQuestion.category_name).distinct().all()
            chosen_cat = random.choice(all_cats) if all_cats else ('general', 'General')
            existing_match_qids = [qid for r in match.rounds for qid in r.get_question_ids()]
            next_q = get_random_questions(category_slug=chosen_cat[0], count=3, exclude_ids=existing_match_qids)

            next_round = ArenaRound(
                match_id=match.id,
                round_number=match.current_round,
                category_slug=chosen_cat[0],
                category_name=chosen_cat[1],
                chosen_by=next_turn,
                question_ids_json=json.dumps([q.id for q in next_q]),
                p1_score=0,
                p2_score=0,
                status='pending'
            )
            db.session.add(next_round)
    else:
        # Only one player has finished this round -> flip turn to the opponent!
        active_round.status = 'p1_done' if has_p1_done else 'p2_done'
        match.current_turn = 2 if is_player1 else 1
        if match.player2_session:
            match.status = 'in_progress'

    db.session.commit()

    base_url = current_app.config.get('APP_PUBLIC_URL', request.host_url.rstrip('/'))
    invite_url, whatsapp_text, whatsapp_nudge_text = _build_whatsapp_messages(match, player, is_player1, base_url)
    opponent_assigned = bool(match.player2_session and match.player2_session not in ('pending_invite', 'online_matchmaking', ''))
    opp_display_name = (match.player2_name if opponent_assigned else 'Your Friend') if is_player1 else match.player1_name

    return jsonify({
        'success': True,
        'is_player1': is_player1,
        'round_score': round_score,
        'correct_count': correct_count,
        'total_questions': len(questions) or 3,
        'total_time_sec': total_time_sec,
        'bot_score': active_round.p2_score if match.is_bot else opp_round_summary.get('score', 0),
        'opponent_round_score': opp_round_summary.get('score', 0),
        'opponent_correct_count': opp_round_summary.get('correct_count', 0),
        'opponent_time_sec': opp_round_summary.get('total_time_sec', 0.0),
        'both_completed_round': both_completed_round,
        'continue_next_round': continue_next_round,
        'round_comparison': round_comparison,
        'detailed_results': detailed_results if both_completed_round else [],
        'player_level': player.level,
        'player_xp': player.xp,
        'my_total_score': match.p1_total_score if is_player1 else match.p2_total_score,
        'opponent_total_score': match.p2_total_score if is_player1 else match.p1_total_score,
        'p1_total_score': match.p1_total_score,
        'p2_total_score': match.p2_total_score,
        'match_status': match.status,
        'is_bot': match.is_bot,
        'opponent_assigned': opponent_assigned,
        'opponent_name': opp_display_name,
        'current_round': completed_round_num,
        'completed_round_cat': completed_round_cat,
        'next_round': match.current_round if match.status != 'completed' else None,
        'next_category_name': chosen_cat[1] if chosen_cat else '',
        'winner': match.winner,
        'has_account': has_account,
        'invite_url': invite_url,
        'whatsapp_nudge_text': whatsapp_nudge_text
    })


@arena_bp.route('/match/<match_code>/switch-to-bot', methods=['POST'])
def switch_to_bot(match_code):
    """Convert an existing match opponent to Cyber Bot Nova and simulate the bot's turn."""
    player = get_current_player()
    match = ArenaMatch.query.filter_by(match_code=match_code).first_or_404()

    is_player1 = (match.player1_session == player.session_key)
    is_player2 = (match.player2_session == player.session_key)

    if not (is_player1 or is_player2):
        flash("You are not a participant in this match.", "error")
        return redirect(url_for('arena.match_lobby', match_code=match_code))

    # Determine which slot becomes the bot
    if is_player1:
        match.player2_session = 'bot_quizmondo_ai'
        match.player2_name = 'Cyber Bot Nova'
        match.player2_avatar = 'nova'
    else:
        match.player1_session = 'bot_quizmondo_ai'
        match.player1_name = 'Cyber Bot Nova'
        match.player1_avatar = 'nova'

    match.status = 'in_progress'

    # If it is currently the bot's turn, simulate the bot's round immediately!
    active_round = match.rounds.filter_by(round_number=match.current_round).first()
    bot_turn = (is_player1 and match.current_turn == 2) or (is_player2 and match.current_turn == 1)

    if active_round and bot_turn:
        q_ids = active_round.get_question_ids()
        questions = QuizQuestion.query.filter(QuizQuestion.id.in_(q_ids)).all() if q_ids else []
        bot_score = 0
        bot_detailed = []
        for q in questions:
            bot_correct = (random.random() < 0.65)
            bot_pts = q.points + random.randint(20, 50) if bot_correct else 0
            bot_score += bot_pts
            bot_detailed.append({
                'question_id': q.id,
                'is_correct': bot_correct,
                'points_awarded': bot_pts
            })

        if is_player1:
            active_round.p2_score = bot_score
            active_round.p2_answers_json = json.dumps(bot_detailed)
            match.p2_total_score = (match.p2_total_score or 0) + bot_score
        else:
            active_round.p1_score = bot_score
            active_round.p1_answers_json = json.dumps(bot_detailed)
            match.p1_total_score = (match.p1_total_score or 0) + bot_score

        active_round.status = 'completed'

        if match.current_round >= 6:
            match.status = 'completed'
            if match.p1_total_score > match.p2_total_score:
                match.winner = 1
                if is_player1:
                    player.matches_won = (player.matches_won or 0) + 1
            elif match.p2_total_score > match.p1_total_score:
                match.winner = 2
                if is_player2:
                    player.matches_won = (player.matches_won or 0) + 1
            else:
                match.winner = 0
            player.matches_played = (player.matches_played or 0) + 1
        else:
            # Advance to next round!
            match.current_round += 1
            match.current_turn = 1 if is_player1 else 2  # Give turn back to human player!

            # Pick next round category and randomized questions (excluding questions already in this match)
            all_cats = db.session.query(QuizQuestion.category_slug, QuizQuestion.category_name).distinct().all()
            chosen_cat = random.choice(all_cats) if all_cats else ('general', 'General')
            existing_match_qids = [qid for r in match.rounds for qid in r.get_question_ids()]
            next_q = get_random_questions(category_slug=chosen_cat[0], count=3, exclude_ids=existing_match_qids)

            next_round = ArenaRound(
                match_id=match.id,
                round_number=match.current_round,
                category_slug=chosen_cat[0],
                category_name=chosen_cat[1],
                chosen_by=match.current_turn,
                question_ids_json=json.dumps([q.id for q in next_q]),
                p1_score=0,
                p2_score=0,
                status='pending'
            )
            db.session.add(next_round)

    db.session.commit()
    flash("Switched to Cyber Bot Nova! The bot has completed its turn—play your next round!", "success")
    return redirect(url_for('arena.match_lobby', match_code=match_code))


@arena_bp.route('/profile/update', methods=['POST'])
def update_profile():
    """Update active player avatar and display name."""
    player = get_current_player()
    payload = request.get_json(silent=True) or {}
    new_name = (request.form.get('display_name') or payload.get('display_name') or '').strip()
    new_avatar = (request.form.get('avatar_key') or payload.get('avatar_key') or '').strip()

    if new_name:
        player.display_name = new_name[:40]
    if new_avatar in [a['key'] for a in AVATAR_PRESETS]:
        player.avatar_key = new_avatar

    # Keep active & completed matches in sync with new mascot & display name
    ArenaMatch.query.filter_by(player1_session=player.session_key).update({
        'player1_name': player.display_name,
        'player1_avatar': player.avatar_key
    })
    ArenaMatch.query.filter_by(player2_session=player.session_key).update({
        'player2_name': player.display_name,
        'player2_avatar': player.avatar_key
    })
    if player.display_name:
        ArenaMatch.query.filter(func.lower(ArenaMatch.player1_name) == player.display_name.lower()).update({
            'player1_avatar': player.avatar_key
        }, synchronize_session=False)
        ArenaMatch.query.filter(func.lower(ArenaMatch.player2_name) == player.display_name.lower()).update({
            'player2_avatar': player.avatar_key
        }, synchronize_session=False)

    db.session.commit()
    if request.is_json or 'application/json' in (request.headers.get('Accept') or ''):
        return jsonify({
            'success': True,
            'display_name': player.display_name,
            'avatar_key': player.avatar_key
        })
    flash("Avatar & Profile updated successfully!", "success")
    return redirect(url_for('arena.dashboard'))


@arena_bp.route('/register', methods=['GET', 'POST'])
def player_register():
    """Quick 3-Step Player Challenge Setup (Unique/Superhero Name + Email + 6-Digit PIN)."""
    player = get_current_player()
    next_url = request.args.get('next') or request.form.get('next')
    if session.get('user_id'):
        if next_url and next_url.startswith('/'):
            return redirect(next_url)
        return redirect(url_for('arena.dashboard'))

    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        email = (request.form.get('email') or '').strip().lower()
        pin = (request.form.get('pin') or '').strip()
        password = pin or (request.form.get('password') or '')
        confirm_password = pin or (request.form.get('confirm_password') or password)

        if not username or len(username) < 3:
            flash("Player name must be at least 3 characters long.", "error")
            return render_template('themes/quizhub/arena_register.html', player=player)

        if not email or '@' not in email:
            flash("Please enter a valid email address.", "error")
            return render_template('themes/quizhub/arena_register.html', player=player)

        if len(password) < 6:
            flash("Please enter a 6-digit PIN (at least 6 characters).", "error")
            return render_template('themes/quizhub/arena_register.html', player=player)

        if password != confirm_password:
            flash("PIN / Passwords do not match.", "error")
            return render_template('themes/quizhub/arena_register.html', player=player)

        # Age gate, switchable in Settings > Security. On by default, because a
        # fresh install should not be open by accident. The date of birth is
        # asked for rather than a 'yes I am old enough' box, because a box tells
        # nobody anything afterwards and cannot be checked against.
        gate = age_gate_config()
        dob = None
        dob_raw = (request.form.get('date_of_birth') or '').strip()
        today = datetime.utcnow().date()

        if dob_raw:
            try:
                dob = datetime.strptime(dob_raw, '%Y-%m-%d').date()
            except ValueError:
                flash("That date of birth did not make sense. Use the date picker.", "error")
                return render_template('themes/quizhub/arena_register.html', player=player)
            if dob > today:
                flash("That date of birth is in the future.", "error")
                return render_template('themes/quizhub/arena_register.html', player=player)

        if gate['enabled']:
            if not dob:
                flash("Please enter your date of birth. You must be at least "
                      f"{gate['minimum']} to have a Quizmondo account.", "error")
                return render_template('themes/quizhub/arena_register.html', player=player)
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age > 120:
                flash("Please check your date of birth.", "error")
                return render_template('themes/quizhub/arena_register.html', player=player)
            if age < gate['minimum']:
                flash(f"Sorry — you need to be at least {gate['minimum']} to sign up for "
                      "Quizmondo. You can still play as a guest without an account.", "error")
                return render_template('themes/quizhub/arena_register.html', player=player)

        if User.query.filter(func.lower(User.username) == username.lower()).first():
            flash("That player name is already taken. Try picking a Superhero Name!", "error")
            return render_template('themes/quizhub/arena_register.html', player=player)

        if User.query.filter(func.lower(User.email) == email.lower()).first():
            flash("An account with that email already exists. Sign in with your 6-digit PIN instead!", "error")
            return render_template('themes/quizhub/arena_login.html', player=player)

        # Default role hierarchy: all newly registered users are strictly 'player'
        assigned_role = 'player'
        user = User(username=username, email=email, role=assigned_role)
        # With the gate off, a date of birth given anyway is still worth keeping.
        user.date_of_birth = dob
        user.age_confirmed_at = datetime.utcnow() if dob else None
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        player.user_id = user.id
        player.display_name = username
        # Update past match player names to permanently replace guest tag with real username (preventing self-duels)
        ArenaMatch.query.filter_by(player1_session=player.session_key).update({'player1_name': username})
        ArenaMatch.query.filter(
            ArenaMatch.player2_session == player.session_key,
            ArenaMatch.player1_session != player.session_key
        ).update({'player2_name': username})
        db.session.commit()

        session.permanent = True
        session['user_id'] = user.id
        session['username'] = user.username
        session['user_role'] = user.role
        session['is_creator'] = False
        session['qm_player_key'] = player.session_key

        # Send the confirmation now, while the address is fresh in their mind.
        # They are not made to act on it: confirmation_state leaves a brand new
        # account alone for the whole signup session, so this lands in the
        # inbox and the prompt waits until their next visit.
        try:
            from .account import send_confirmation as _send_confirm
            _send_confirm(user)
        except Exception:
            # No mail account set up yet, or the server refused it. Signing up
            # must not fail over an email nobody has asked for.
            db.session.rollback()

        flash(f"🎉 Welcome to Quizmondo, {username}! Your challenge profile and 6-digit PIN are set up!", "success")
        if next_url and next_url.startswith('/'):
            return redirect(next_url)
        return redirect(url_for('arena.dashboard'))

    return render_template('themes/quizhub/arena_register.html', player=player)


@arena_bp.route('/login', methods=['GET', 'POST'])
def player_login():
    """Sign in with Player Name/Email + 6-Digit PIN (or Password)."""
    next_url = request.args.get('next') or request.form.get('next')
    if session.get('user_id'):
        if next_url and next_url.startswith('/'):
            return redirect(next_url)
        return redirect(url_for('arena.dashboard'))

    if request.method == 'POST':
        login_id = (request.form.get('username') or '').strip()
        password = (request.form.get('password') or '').strip()

        user = User.query.filter(
            (func.lower(User.username) == login_id.lower()) | (func.lower(User.email) == login_id.lower())
        ).first()
        if user and user.check_password(password) and user.is_active:
            session.permanent = True
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_role'] = user.role or 'player'
            session['is_creator'] = user.role in ('super_admin', 'admin', 'quizmaster', 'creator')

            guest_key = session.get('qm_player_key')
            profile = PlayerProfile.query.filter_by(user_id=user.id).first()
            if profile:
                session['qm_player_key'] = profile.session_key
                profile.display_name = user.username
                profile.last_active_at = datetime.utcnow()
                if guest_key and guest_key != profile.session_key:
                    ArenaMatch.query.filter_by(player1_session=guest_key).update({
                        'player1_session': profile.session_key,
                        'player1_name': profile.display_name,
                        'player1_avatar': profile.avatar_key
                    })
                    ArenaMatch.query.filter(
                        ArenaMatch.player2_session == guest_key,
                        ArenaMatch.player1_session != profile.session_key
                    ).update({
                        'player2_session': profile.session_key,
                        'player2_name': profile.display_name,
                        'player2_avatar': profile.avatar_key
                    })
                db.session.commit()
            elif guest_key:
                guest_prof = PlayerProfile.query.filter_by(session_key=guest_key).first()
                if guest_prof:
                    guest_prof.user_id = user.id
                    guest_prof.display_name = user.username
                    db.session.commit()

            flash(f"Welcome back, {user.username}!", "success")
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect(url_for('arena.dashboard'))
        else:
            paused = User.query.filter(
                (func.lower(User.username) == login_id.lower()) | (func.lower(User.email) == login_id.lower())
            ).first()
            if paused and not paused.is_active and paused.check_password(password):
                return render_template('themes/quizhub/arena_login.html',
                                       player=get_current_player(persist=False),
                                       reactivate_id=login_id)
            flash("Invalid player name/email or 6-digit PIN.", "error")

    player = get_current_player(persist=False)
    return render_template('themes/quizhub/arena_login.html', player=player)


@arena_bp.route('/logout')
def player_logout():
    """Sign out of player account and revert to guest."""
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('user_role', None)
    session.pop('qm_player_key', None)
    flash("You have been signed out.", "info")
    return redirect(url_for('arena.dashboard'))


# =========================================================================
# Account control: pausing, and erasure
#
# Two deliberately different things. Pausing hides you and is reversible,
# because the account is still there. Erasure destroys the identity and
# cannot be undone - if it could be undone we would still be holding the
# link between you and the record, which is pseudonymisation, not erasure,
# and the privacy notice would be wrong.
# =========================================================================

def anonymised_display_name():
    """A randomised name in the same shape as any guest's.

    Not a label like "Former Player", which would mark the row out as a deleted
    account and still tell people something about it. This is indistinguishable
    from an ordinary guest name, which is the point of anonymising.
    """
    for _ in range(40):
        candidate = 'Challenger_%06x' % secrets.randbelow(16 ** 6)
        taken_profile = PlayerProfile.query.filter(
            func.lower(PlayerProfile.display_name) == candidate.lower()).first()
        taken_user = User.query.filter(func.lower(User.username) == candidate.lower()).first()
        if not taken_profile and not taken_user:
            return candidate
    return 'Challenger_%s' % secrets.token_hex(5)


def erase_player_identity(profile):
    """Irreversibly strip the identity, keeping only the score.

    Deletes the User row entirely (email, username, password hash), scrubs the
    profile's own identifying fields, and rotates the session key so the browser
    cookie that used to open this account cannot open it again. What is left -
    XP, matches played, level - is no longer personal data because nothing ties
    it to a person any more.
    """
    user = db.session.get(User, profile.user_id) if profile.user_id else None
    if user:
        db.session.delete(user)

    old_key = profile.session_key
    new_name = anonymised_display_name()

    # Scrub the name wherever it was copied, before the key it is found by changes
    ArenaMatch.query.filter_by(player1_session=old_key).update(
        {'player1_name': new_name}, synchronize_session=False)
    ArenaMatch.query.filter_by(player2_session=old_key).update(
        {'player2_name': new_name}, synchronize_session=False)
    GroupPlayer.query.filter_by(player_key=old_key).update(
        {'display_name': new_name}, synchronize_session=False)

    profile.user_id = None
    profile.display_name = new_name
    profile.session_key = secrets.token_urlsafe(16)
    profile.avatar_key = 'quizzy'
    profile.is_anonymised = True
    profile.is_paused = False
    return new_name


@arena_bp.route('/account')
def account_settings():
    """What a player can do with their own account and data."""
    if not session.get('user_id'):
        flash('Sign in to manage your account.', 'error')
        return redirect(url_for('arena.player_login', next='/arena/account'))
    player = get_current_player()
    user = db.session.get(User, session.get('user_id'))
    return render_template('themes/quizhub/arena_account.html', player=player, account=user)


@arena_bp.route('/account/pause', methods=['POST'])
def account_pause():
    """Hide the account and sign out. Signing back in brings it back."""
    if not session.get('user_id'):
        return redirect(url_for('arena.player_login'))
    player = get_current_player()
    user = db.session.get(User, session.get('user_id'))
    if user:
        user.is_active = False
    player.is_paused = True
    db.session.commit()
    for key in ('user_id', 'username', 'user_role', 'qm_player_key', 'is_creator'):
        session.pop(key, None)
    flash('Your account is paused and hidden. Sign in again whenever you want it back.', 'success')
    return redirect(url_for('arena.dashboard'))


@arena_bp.route('/account/delete', methods=['POST'])
def account_delete():
    """Erase the identity for good, keeping the score detached and anonymous."""
    if not session.get('user_id'):
        return redirect(url_for('arena.player_login'))
    if (request.form.get('confirm') or '').strip().upper() != 'DELETE':
        flash('Type DELETE in the box to confirm you want your account erased.', 'error')
        return redirect(url_for('arena.account_settings'))

    player = get_current_player()
    new_name = erase_player_identity(player)
    db.session.commit()
    for key in ('user_id', 'username', 'user_role', 'qm_player_key', 'is_creator'):
        session.pop(key, None)
    flash('Your account has been erased. Your email, player name and PIN are gone for good. '
          'Your score remains on the board as "%s" and can no longer be traced to you.' % new_name, 'success')
    return redirect(url_for('public.home'))


@arena_bp.route('/account/reactivate', methods=['POST'])
def account_reactivate():
    """Bring a paused account back, once the right PIN has been given."""
    login_id = (request.form.get('username') or '').strip()
    password = (request.form.get('password') or '').strip()
    user = User.query.filter(
        (func.lower(User.username) == login_id.lower()) | (func.lower(User.email) == login_id.lower())
    ).first()
    if not user or not user.check_password(password):
        flash('That player name or PIN did not match.', 'error')
        return redirect(url_for('arena.player_login'))

    user.is_active = True
    profile = PlayerProfile.query.filter_by(user_id=user.id).first()
    if profile:
        profile.is_paused = False
    db.session.commit()
    flash('Welcome back! Your account is live again, with your scores intact.', 'success')
    return redirect(url_for('arena.player_login'))


@arena_bp.route('/leaderboard')
def leaderboard():
    """Full global leaderboard ranking table."""
    player = get_current_player(persist=False)
    top_players = PlayerProfile.query.filter_by(is_paused=False).order_by(PlayerProfile.xp.desc()).limit(50).all()
    return render_template(
        'themes/quizhub/arena_leaderboard.html',
        player=player,
        top_players=top_players
    )


@arena_bp.route('/leagues')
def leagues():
    """Virtual & Pub Quiz Leagues directory."""
    player = get_current_player(persist=False)
    all_leagues = PubLeague.query.filter_by(is_active=True).order_by(PubLeague.created_at.desc()).all()
    return render_template(
        'themes/quizhub/arena_leagues.html',
        player=player,
        leagues=all_leagues
    )


@arena_bp.route('/leagues/join', methods=['POST'])
def league_join():
    """Validate venue room PIN code and redirect to venue lounge."""
    pin = (request.form.get('pin_code') or '').strip()
    if not pin:
        flash('Please enter a valid 4-digit venue PIN code.', 'error')
        return redirect(url_for('arena.leagues'))
        
    league = PubLeague.query.filter_by(pin_code=pin, is_active=True).first()
    if not league:
        flash(f'Room PIN "{pin}" not found. Please ask your venue quizmaster.', 'error')
        return redirect(url_for('arena.leagues'))

    session[f'pub_pin_{league.slug}'] = pin
    return redirect(url_for('arena.league_lounge', slug=league.slug))


@arena_bp.route('/leagues/<slug>')
def league_lounge(slug):
    """Pub League Venue Lounge: Squad registration, schedule, and TV mode."""
    player = get_current_player(persist=False)
    league = PubLeague.query.filter_by(slug=slug, is_active=True).first_or_404()
    state = league.get_state()
    apply_pub_auto_progression(league, state)
    is_virtual = league.is_virtual_league()
    # A finished night is not an in-play one: offering "reconnect your table" on a
    # quiz that ended on Thursday just bounces people off the closed room.
    night_over = pub_night_is_over(league, state)
    is_started = (not night_over) and (
        state.get('current_round', 1) > 1
        or state.get('round_status') in ('active', 'break', 'closed')
    )
    # Only display approved real teams on lounge scoreboard (no mock demo teams!)
    teams = [t for t in league.get_teams() if t.get('status') != 'pending']
    # Advertise the rounds this league actually plays, not a hardcoded 5-round venue card
    active_cfg = VIRTUAL_PUB_ROUNDS_CONFIG if is_virtual else PUB_ROUNDS_CONFIG
    total_rounds = int((state.get('config') or {}).get('total_rounds', 3 if is_virtual else 5))
    rounds_overview = []
    for r_num in range(1, min(total_rounds, len(active_cfg)) + 1):
        info = dict(active_cfg.get(r_num, {}))
        info['number'] = r_num
        info['name'] = (info.get('name') or f'Round {r_num}').split(': ', 1)[-1]
        rounds_overview.append(info)
    return render_template(
        'themes/quizhub/arena_league_lounge.html',
        player=player,
        league=league,
        state=state,
        is_virtual=is_virtual,
        is_started=is_started,
        night_over=night_over,
        next_pub_date=get_next_weekly_pub_date(),
        teams=teams,
        rounds_overview=rounds_overview
    )


@arena_bp.route('/leagues/<slug>/card.png')
def league_card_image(slug):
    """Dynamic 1200x630 OpenGraph pub quiz venue invite card for WhatsApp / social previews."""
    league = PubLeague.query.filter_by(slug=slug, is_active=True).first_or_404()
    state = league.get_state()
    cfg = state.get('config', {})
    png_bytes = generate_pub_card_png(
        venue_name=league.venue_name or league.name,
        pin_code="HOST GATED" if league.is_virtual_league() else "AT VENUE",
        schedule_day=league.schedule_day,
        first_prize=cfg.get('first_prize'),
        second_prize=cfg.get('second_prize')
    )
    resp = Response(png_bytes, mimetype='image/png')
    resp.headers['Cache-Control'] = 'public, max-age=120'
    return resp


def get_next_weekly_pub_date():
    """Calculate the next upcoming Thursday 20:00 GMT for the weekly pub quiz league."""
    now = datetime.utcnow()
    # Thursday is weekday 3 (Monday is 0)
    days_ahead = (3 - now.weekday()) % 7
    if days_ahead == 0 and now.hour >= 21:
        days_ahead = 7
    elif days_ahead == 0 and now.hour < 20:
        days_ahead = 0
    elif days_ahead == 0:
        days_ahead = 7
    next_date = now + timedelta(days=days_ahead)
    return next_date.strftime("%A, %d %B %Y at 20:00 GMT")


VIRTUAL_PUB_ROUNDS_CONFIG = {
    1: {'number': 1, 'name': 'Round 1: General Knowledge, Science & Lore', 'cat_slug': 'world-history', 'icon': '🌍', 'desc': 'Warm up your neurons with world history, science, and general news.'},
    2: {'number': 2, 'name': 'Round 2: Pop Culture, Cinema Titans & Music Legends', 'cat_slug': 'cinema-film-tv-radio', 'icon': '🎬', 'desc': 'Blockbuster cinema, chart-topping records, and modern pop icons.'},
    3: {'number': 3, 'name': 'Round 3: Championship Wipeout Lightning Sprint', 'cat_slug': 'gaming-esports', 'icon': '⚡', 'desc': 'High stakes finale! 1.5x score multiplier on all correct answers.'},
    4: {'number': 4, 'name': 'Round 4: World Geography & Flags', 'cat_slug': 'match-flags', 'icon': '🏳️', 'desc': 'Visual flags and global geography challenge.'},
    5: {'number': 5, 'name': 'Round 5: The Grand Finale Speed Wipeout', 'cat_slug': 'brand-logos', 'icon': '🏆', 'desc': 'Double points finale round!'},
}

PUB_ROUNDS_CONFIG = {
    1: {'number': 1, 'name': 'General Knowledge & News', 'cat_slug': 'uk-british', 'icon': '🧠', 'desc': 'Britain and beyond: monarchy, counties, telly, the pub and general knowledge.'},
    2: {'number': 2, 'name': 'Music, Audio & Waveforms', 'cat_slug': 'music-decades', 'icon': '🎵', 'desc': 'Iconic number one records, synthesizers, chiptunes, and rock anthems.'},
    3: {'number': 3, 'name': 'Cinema, Television & Blockbusters', 'cat_slug': 'cinema-film-tv-radio', 'icon': '🎬', 'desc': 'Cult cinema classics, famous directors, Academy Awards, and TV quotes.'},
    4: {'number': 4, 'name': 'World Geography & Visual Flags', 'cat_slug': 'match-flags', 'icon': '🗺️', 'desc': 'Continental capitals, world flags, ancient ruins, and extreme landforms.'},
    5: {'number': 5, 'name': 'The Big Wipeout Speed Sprint', 'cat_slug': 'gaming-esports', 'icon': '⚡', 'desc': 'Double Points Wipeout Round! Faster buzzer answers award massive bonus points.'},
}


def is_pub_host():
    """True for the accounts allowed to run a live pub quiz."""
    return (
        session.get('user_role') in ('super_admin', 'admin', 'quizmaster')
        or bool(session.get('admin_logged_in'))
    )


def needs_account_to_challenge(what='challenge'):
    """Guests may play. Only account holders may start something involving somebody else.

    A guest challenge is a dead end for everybody: the guest loses it the
    moment their session goes, the friend accepts an invite from
    "Challenger_7f3a1c", and the duel sits in the list for ever because nobody
    is coming back to finish it. Playing alone or against the bot stays open,
    because nobody else is waiting on it.

    Returns a redirect to sign-up when the person has no account, or None when
    they are fine to carry on.
    """
    if session.get('user_id'):
        return None
    flash(
        "👋 Almost there! Grab a free account and you can {what} — it takes "
        "about ten seconds, we only need a name and a PIN. Then your scores stick around, "
        "your mates can find you, and whoever you invite knows who they are playing. "
        "😊".format(what=what),
        "info")
    nxt = request.full_path if request.query_string else request.path
    return redirect(url_for('arena.player_register', next=nxt))


def needs_account_to_play(what='play this game'):
    """Both The Quiz Climber and Daily Lucky Wheel require an authenticated player account."""
    if session.get('user_id'):
        return None
    flash(
        "👋 Welcome! Grab a free account to {what} — your coins, expedition altitude, shields, and daily streaks will be saved to your profile forever! 😊".format(what=what),
        "info")
    nxt = request.full_path if request.query_string else request.path
    return redirect(url_for('arena.player_register', next=nxt))


def resolve_pub_team(state, player, table_num, team_name, is_virtual, require_pin=None):
    """Find the squad row that belongs to this browser session.

    In a physical venue a table number is deliberately shared, so the table
    number stays the identity. In a virtual league every player checks in from
    their own device, so the squad is keyed to the player instead — otherwise
    two players who both type Squad #1 silently end up on one scorecard.
    """
    teams = state.get('teams', [])
    owner_key = getattr(player, 'session_key', None)
    name_l = (team_name or '').strip().lower()
    # A physical table number is shared on purpose, so the number alone cannot be
    # proof of anything: without this, typing ?table=1 made a stranger that table.
    # Holding the venue PIN, or having checked the table in yourself, is the proof.
    holds_pin = bool(require_pin and session.get(f'pub_pin_{require_pin}'))

    def owned():
        if not owner_key:
            return None
        for t in teams:
            if t.get('owner') and t.get('owner') == owner_key:
                return t
            if owner_key in (t.get('member_keys') or []):
                return t
        return None

    if is_virtual:
        # A virtual squad belongs to the device that checked it in; table numbers are not shared
        mine = owned()
        if mine:
            return mine
        # Only unclaimed rows (manual host entries, legacy squads) may be adopted by name
        for t in teams:
            if name_l and not t.get('owner') and t.get('name', '').strip().lower() == name_l:
                return t
        return None

    mine = owned()
    if mine:
        return mine

    if require_pin and not holds_pin:
        # No PIN and not a table this browser checked in: start a fresh one instead
        # of adopting somebody else's scorecard.
        return None

    for t in teams:
        matches_table = table_num and str(t.get('table', '')).strip() == str(table_num)
        matches_name = name_l and t.get('name', '').strip().lower() == name_l
        if matches_table or matches_name:
            return t

    mine = owned()
    if mine:
        return mine

    return None


PUB_CODE_ALPHABET = 'ACDEFGHJKLMNPQRTUVWXY34679'


def new_pub_join_code(teams):
    """Short code a virtual squad shares so mates on other phones join the same scorecard."""
    taken = {(t.get('join_code') or '').upper() for t in teams}
    for _ in range(50):
        code = ''.join(random.choice(PUB_CODE_ALPHABET) for _ in range(4))
        if code not in taken:
            return code
    return ''.join(random.choice(PUB_CODE_ALPHABET) for _ in range(6))


def join_pub_squad_by_code(state, player, code):
    """Attach this player to an existing squad from its join code."""
    code = (code or '').strip().upper()
    if not code:
        return None
    for t in state.get('teams', []):
        if (t.get('join_code') or '').upper() == code:
            keys = t.setdefault('member_keys', [])
            if player.session_key not in keys and t.get('owner') != player.session_key:
                keys.append(player.session_key)
                t['members'] = max(int(t.get('members', 1)), len(keys) + 1)
            return t
    return None


def free_pub_squad_slot(teams, table_num, team_name):
    """Pick a squad number and squad name that no other virtual squad is already using."""
    taken_tables = {str(t.get('table', '')).strip() for t in teams}
    taken_names = {t.get('name', '').strip().lower() for t in teams}

    table_num = str(table_num or '1').strip() or '1'
    if table_num in taken_tables:
        n = 1
        while str(n) in taken_tables:
            n += 1
        table_num = str(n)

    team_name = (team_name or 'Squad').strip()
    if team_name.lower() in taken_names:
        suffix = 2
        while f"{team_name} ({suffix})".lower() in taken_names:
            suffix += 1
        team_name = f"{team_name} ({suffix})"
    return table_num, team_name


PUB_QUESTIONS_PER_ROUND = 5

# How long a quiz night can sit untouched before it counts as over. A pub quiz
# runs two or three hours, so six is generous even for a long night with a slow
# raffle in the middle. Override per league with config['night_timeout_hours'].
PUB_NIGHT_TIMEOUT_HOURS = 6
PUB_MIN_QUESTION_SECS = 15
PUB_MAX_QUESTION_SECS = 30


def pub_question_secs(cfg):
    """Seconds per question the host has configured, held inside the supported range."""
    try:
        secs = int(cfg.get('question_time_limit', 15))
    except (TypeError, ValueError):
        secs = 15
    return max(PUB_MIN_QUESTION_SECS, min(PUB_MAX_QUESTION_SECS, secs))


def score_pub_answers(state, round_num, raw_answers, cfg, total_rounds):
    """Score a squad's answers against the questions pinned for this round.

    The phone used to work out its own round total and post it, which meant the
    score was whatever the browser said it was. The answers are scored here now,
    against the pinned question set, so a tampered payload cannot invent points.
    Returns None when there is nothing scoreable, which the callers refuse.
    """
    if not raw_answers:
        return None
    try:
        submitted = json.loads(raw_answers) if isinstance(raw_answers, str) else raw_answers
    except Exception:
        return None
    if not isinstance(submitted, list):
        return None

    pinned = (state.get('round_questions') or {}).get(str(round_num)) or []
    if not pinned:
        return None

    time_limit = pub_question_secs(cfg)
    is_final_round = round_num >= total_rounds
    total = 0
    counted = set()
    for item in submitted:
        if not isinstance(item, dict):
            continue
        try:
            qid = int(item.get('id'))
        except (TypeError, ValueError):
            continue
        if qid not in pinned or qid in counted:
            continue
        counted.add(qid)
        q = QuizQuestion.query.get(qid)
        if not q or not item.get('choice') or item.get('choice') != q.correct_option:
            continue
        try:
            remaining = int(item.get('remaining') or 0)
        except (TypeError, ValueError):
            remaining = 0
        remaining = max(0, min(time_limit, remaining))
        pts = 100 + remaining * 2
        if is_final_round:
            pts = round(pts * 1.5)
        total += pts
    return total


def recompute_pub_score(team):
    """Total a squad from its banked round scores.

    Deriving the total rather than adding to it keeps the books straight when the
    same round gets banked twice — two phones polling at the instant a round
    deadline passes both try to close it.
    """
    total = 0
    for key, value in team.items():
        if key.startswith('round_') and value is not None:
            try:
                total += int(value)
            except (TypeError, ValueError):
                continue
    team['score'] = total
    return total


def rerank_pub_teams(teams):
    """Sort the standings by total score and stamp each squad's rank."""
    teams.sort(key=lambda x: x.get('score', 0), reverse=True)
    for idx, t in enumerate(teams, 1):
        t['rank'] = idx


def close_pub_round(state, round_num):
    """Lock a round: bank a partial score for every approved squad still unfinished."""
    teams = state.get('teams', [])
    for t in teams:
        if t.get('status') != 'pending' and t.get(f'round_{round_num}') is None:
            partial = int(t.get(f'partial_round_{round_num}', t.get(f'partial_score_{round_num}', 0)))
            t[f'round_{round_num}'] = partial
            recompute_pub_score(t)
    rerank_pub_teams(teams)
    state['teams'] = teams
    state['round_status'] = 'closed'


def record_pub_results(league, state):
    """Copy a finalised tournament into the permanent results table.

    The league state only holds the night in progress and a reset wipes it, so
    without this a finished quiz leaves no trace and there is nothing to build a
    league table from. Guarded by a flag, because the host can press Finalize
    twice and the unattended clock can reach the same place on its own.
    """
    if state.get('results_recorded'):
        return 0
    teams = [t for t in state.get('teams', []) if t.get('status') != 'pending']
    if not teams:
        return 0

    played_at = datetime.utcnow()
    season = pub_season_label(played_at)
    ranked = sorted(teams, key=lambda t: int(t.get('score', 0)), reverse=True)
    written = 0
    for idx, t in enumerate(ranked, 1):
        rounds = {k: v for k, v in t.items() if k.startswith('round_') and v is not None}
        name = (t.get('name') or 'Unnamed squad').strip()
        db.session.add(PubLeagueResult(
            league_id=league.id,
            season=season,
            played_at=played_at,
            team_name=name,
            team_key=slugify(name),
            table_num=str(t.get('table', '')),
            position=idx,
            total_score=int(t.get('score', 0)),
            rounds_played=len(rounds),
            round_scores_json=json.dumps(rounds),
            members=int(t.get('members', 1) or 1)
        ))
        written += 1

    state['results_recorded'] = True
    state['results_recorded_at'] = played_at.isoformat()
    return written


def apply_pub_auto_progression(league, state):
    """Run the clock for a live pub quiz without the host having to click.

    Players already watch a per-question countdown, so a round has a natural
    deadline; past it the round locks itself and the answers are revealed. A
    virtual league also rolls on to the next round when the break is over, since
    there is no quizmaster standing in the room to press the button.
    """
    cfg = state.get('config', {})
    curr_r = int(state.get('current_round', 1))
    status = state.get('round_status', 'waiting')
    total_rounds = int(cfg.get('total_rounds', 3 if league.is_virtual_league() else 5))
    now = datetime.utcnow()
    changed = False

    def expired(iso_ts):
        if not iso_ts:
            return False
        try:
            return datetime.fromisoformat(iso_ts) <= now
        except Exception:
            return False

    if status == 'active' and cfg.get('round_deadline_enabled', True) and expired(state.get('round_ends_at')):
        close_pub_round(state, curr_r)
        state.pop('round_ends_at', None)
        if cfg.get('auto_advance_enabled'):
            # Nobody is at the console, so the keys go up by themselves
            state['answers_revealed'] = True
            mins = int(cfg.get('interval_duration_mins', 8))
            state['round_status'] = 'break'
            state['break_ends_at'] = (now + timedelta(minutes=mins)).isoformat()
        changed = True
        status = state['round_status']

    if cfg.get('auto_advance_enabled') and status in ('closed', 'break') and expired(state.get('break_ends_at')):
        state.pop('break_ends_at', None)
        if curr_r < total_rounds:
            state['current_round'] = curr_r + 1
            state['round_status'] = 'active'
            state['answers_revealed'] = False
            state['round_ends_at'] = pub_round_deadline(cfg, now)
        else:
            state['round_status'] = 'finished'
            state['answers_revealed'] = True
            state['tournament_completed'] = True
            record_pub_results(league, state)
        changed = True

    if changed:
        pub_touch(state)
        league.set_state(state)
        db.session.commit()

    # A night nobody has touched for hours is over, whatever the console says.
    # Hosts close the till and go home without pressing Finalize, and until this
    # ran, last week's quiz stayed 'active' with its PIN and its tables live.
    if state.get('round_status') != 'finished':
        if pub_last_activity(state) is None:
            # Nothing to date it by: start the clock now rather than close a
            # night that may be about to start.
            pub_touch(state)
            league.set_state(state)
            db.session.commit()
            changed = True
        elif pub_night_is_over(league, state):
            close_pub_night(league, state)
            changed = True

    return changed


def pub_touch(state):
    """Mark the league as having just done something.

    This is what tells a stale night from a live one. A quiz night that nobody
    has touched for hours is over whether or not the host remembered to press
    Finalize, and in a real venue they usually do not.
    """
    state['last_activity_at'] = datetime.utcnow().isoformat()


def pub_last_activity(state):
    """When this league last did anything, as best we can tell.

    Leagues created before last_activity_at existed still carry round and break
    deadlines, a reset stamp or a results stamp, so an old night is still
    datable. One with none of them returns None and gets stamped instead, so the
    clock starts from now rather than closing a night nobody can date.
    """
    newest = None
    for key in ('last_activity_at', 'night_closed_at', 'results_recorded_at',
                'round_ends_at', 'break_ends_at', 'reset_ts'):
        raw = state.get(key)
        if not raw:
            continue
        try:
            ts = datetime.fromisoformat(str(raw))
        except Exception:
            continue
        if newest is None or ts > newest:
            newest = ts
    return newest


def pub_night_is_over(league, state):
    """Has this quiz night ended, by the host's hand or by the clock?"""
    if state.get('round_status') == 'finished' or state.get('tournament_completed'):
        return True
    cfg = state.get('config', {})
    try:
        hours = float(cfg.get('night_timeout_hours', PUB_NIGHT_TIMEOUT_HOURS))
    except (TypeError, ValueError):
        hours = PUB_NIGHT_TIMEOUT_HOURS
    if hours <= 0:
        return False
    last = pub_last_activity(state)
    if last is None:
        return False
    return (datetime.utcnow() - last) > timedelta(hours=hours)


def new_pub_pin(exclude_id=None):
    """A room PIN no other venue is using."""
    taken = set()
    for other in PubLeague.query.all():
        if exclude_id is not None and other.id == exclude_id:
            continue
        if other.pin_code:
            taken.add(str(other.pin_code).upper())
    for _ in range(80):
        pin = '%04d' % random.randint(1000, 9999)
        if pin not in taken:
            return pin
    return '%06d' % random.randint(100000, 999999)


def start_pub_night(state):
    """Put a league back to the start line, ready for the next quiz night.

    Everything that says 'this night is over' has to go, not just the round
    number — leaving tournament_completed behind is what made a reset look like
    it had worked while the lounge still showed the night as finished.
    """
    state['current_round'] = 1
    state['round_status'] = 'waiting'
    state['answers_revealed'] = False
    state['teams'] = []
    state['round_questions'] = {}
    state['tournament_completed'] = False
    for key in ('round_ends_at', 'break_ends_at', 'results_recorded',
                'results_recorded_at', 'night_closed_at', 'previous_pin'):
        state.pop(key, None)
    state['reset_ts'] = datetime.utcnow().isoformat()
    pub_touch(state)


def close_pub_night(league, state, rotate_pin=True):
    """Freeze a finished night, bank the results and retire the room PIN.

    The PIN is the venue's door key for one night. Leaving it up afterwards
    means last week's players — and anyone who reads the page — can still walk
    into the room, so a closed night always gets a new one.
    """
    state['round_status'] = 'finished'
    state['answers_revealed'] = True
    state['tournament_completed'] = True
    state.pop('round_ends_at', None)
    state.pop('break_ends_at', None)
    state.setdefault('night_closed_at', datetime.utcnow().isoformat())
    saved = record_pub_results(league, state)
    if rotate_pin:
        old = league.pin_code
        league.pin_code = new_pub_pin(exclude_id=league.id)
        state['previous_pin'] = old
    pub_touch(state)
    league.set_state(state)
    db.session.commit()
    return saved


def pub_round_deadline(cfg, now=None):
    """When the current round runs out: every question's clock plus a little slack."""
    now = now or datetime.utcnow()
    secs = pub_question_secs(cfg) * PUB_QUESTIONS_PER_ROUND + 20
    return (now + timedelta(seconds=secs)).isoformat()


@arena_bp.route('/leagues/<slug>/state')
def league_state(slug):
    """Real-time pub quiz state polling endpoint for Quizmaster console, TV projectors, and player buzzer phones."""
    league = PubLeague.query.filter_by(slug=slug, is_active=True).first_or_404()
    state = league.get_state()
    apply_pub_auto_progression(league, state)
    current_round = state.get('current_round', 1)
    cfg = state.get('config', {})
    teams = state.get('teams', [])
    approved_teams = [t for t in teams if t.get('status') != 'pending']
    pending_teams = [t for t in teams if t.get('status') == 'pending']
    completed_tables = [t for t in approved_teams if t.get(f'round_{current_round}') is not None]
    active_cfg = VIRTUAL_PUB_ROUNDS_CONFIG if league.is_virtual_league() else PUB_ROUNDS_CONFIG

    return jsonify({
        'success': True,
        'is_virtual': league.is_virtual_league(),
        'current_round': current_round,
        'round_status': state.get('round_status', 'waiting'),
        'answers_revealed': state.get('answers_revealed', False),
        'round_title': active_cfg.get(current_round, {}).get('name', 'Round ' + str(current_round)),
        'config': cfg,
        'break_ends_at': state.get('break_ends_at'),
        'round_ends_at': state.get('round_ends_at'),
        'approved_teams_count': len(approved_teams),
        'pending_teams_count': len(pending_teams),
        'completed_tables_count': len(completed_tables),
        'teams': teams,
        'approved_teams': approved_teams,
        'pending_teams': pending_teams
    })


@arena_bp.route('/leagues/<slug>/progress', methods=['POST'])
def league_progress(slug):
    """Receive live per-question progress & partial score from a table so Quizmaster sees live table progress."""
    league = PubLeague.query.filter_by(slug=slug, is_active=True).first_or_404()
    is_virtual = league.is_virtual_league()
    player = get_current_player(persist=False)
    state = league.get_state()
    teams = state.get('teams', [])
    tbl = str(request.form.get('table') or session.get('pub_table_num') or '').strip()
    tname = (request.form.get('team') or session.get('pub_team_name') or '').strip()
    curr_r = int(state.get('current_round', 1))
    q_idx = int(request.form.get('question_index') or 0)
    cfg = state.get('config', {})
    total_rounds = int(cfg.get('total_rounds', 3 if is_virtual else 5))
    scored = score_pub_answers(state, curr_r, request.form.get('answers'), cfg, total_rounds)
    if scored is None:
        return jsonify({'success': False, 'error': 'Answers required to score this round'}), 400
    partial_score = scored
    is_final_q = (q_idx >= PUB_QUESTIONS_PER_ROUND or request.form.get('is_final') == '1')

    target_team = resolve_pub_team(state, player, tbl, tname, is_virtual)

    # Live progress only counts while the host has the round open and the squad is through the bouncer
    if target_team and (target_team.get('status') == 'pending' or state.get('round_status') != 'active'):
        return jsonify({'success': False, 'error': 'Round is not open for this squad'}), 403

    if target_team:
        target_team[f'progress_q_{curr_r}'] = q_idx
        target_team[f'partial_round_{curr_r}'] = partial_score
        target_team[f'partial_score_{curr_r}'] = partial_score

        # If table just answered the 5th (final) question of the round, immediately lock in their round score!
        if is_final_q and target_team.get(f'round_{curr_r}') is None:
            target_team[f'round_{curr_r}'] = partial_score
            recompute_pub_score(target_team)
            rerank_pub_teams(teams)

            approved_teams = [t for t in teams if t.get('status') != 'pending']
            completed_tables = [t for t in approved_teams if t.get(f'round_{curr_r}') is not None]
            if len(approved_teams) > 0 and len(completed_tables) >= len(approved_teams) and state.get('round_status') == 'active':
                state['round_status'] = 'closed'

        state['teams'] = teams
        pub_touch(state)
        league.set_state(state)
        db.session.commit()

    return jsonify({'success': True})


@arena_bp.route('/leagues/<slug>/manager', methods=['GET', 'POST'])
def league_manager(slug):
    """Host / Quizmaster Manager Console — STRICTLY gated to Super Admins, Admins, and Quizmasters (NEVER Room PIN!)."""
    league = PubLeague.query.filter_by(slug=slug, is_active=True).first_or_404()
    is_mgr = is_pub_host()

    if not is_mgr:
        if session.get('user_id'):
            flash("Access Denied: The Quizmaster Console is strictly restricted to Quizmasters and Administrators. Room PINs are for player table check-in only.", "error")
            return redirect(url_for('arena.league_lounge', slug=slug))
        flash("Quizmaster / Administrator sign-in required to access the Host Console.", "error")
        return redirect(url_for('arena.player_login', next=request.path))

    state = league.get_state()
    apply_pub_auto_progression(league, state)
    config = state.get('config', {})
    teams = state.get('teams', [])
    pending_teams = [t for t in teams if t.get('status') == 'pending']
    approved_teams = [t for t in teams if t.get('status') != 'pending']
    curr_r = state.get('current_round', 1)
    total_rounds = int(config.get('total_rounds', 5 if not league.is_virtual_league() else 3))
    completed_tables = [t for t in approved_teams if t.get(f'round_{curr_r}') is not None]
    all_completed = len(approved_teams) > 0 and len(completed_tables) >= len(approved_teams)
    # STRICT SAFETY GATE: Can ONLY advance when at least 1 table is approved AND (all tables submitted OR round was locked/closed)
    can_advance = len(approved_teams) > 0 and (
        all_completed or state.get('round_status') in ('closed', 'break', 'finished')
    )
    is_final_round = curr_r >= total_rounds
    active_cfg = VIRTUAL_PUB_ROUNDS_CONFIG if league.is_virtual_league() else PUB_ROUNDS_CONFIG
    active_round_info = active_cfg.get(curr_r, {})
    next_round_info = active_cfg.get(curr_r + 1, {}) if curr_r < total_rounds else {}

    return render_template(
        'themes/quizhub/arena_league_manager.html',
        league=league,
        state=state,
        config=config,
        pending_teams=pending_teams,
        approved_teams=approved_teams,
        completed_tables=completed_tables,
        all_completed=all_completed,
        can_advance=can_advance,
        is_final_round=is_final_round,
        total_rounds=total_rounds,
        active_round_info=active_round_info,
        next_round_info=next_round_info
    )


@arena_bp.route('/leagues/<slug>/admin/control', methods=['POST'])
@arena_bp.route('/leagues/<slug>/manager/action', methods=['POST'])
def league_manager_action(slug):
    """Execute host commands: STRICTLY gated to Super Admins, Admins, and Quizmasters (NEVER Room PIN!)."""
    league = PubLeague.query.filter_by(slug=slug, is_active=True).first_or_404()
    is_authorized = is_pub_host()
    if not is_authorized:
        if 'text/html' in (request.headers.get('Accept') or ''):
            flash("Unauthorized: Only Quizmasters and Administrators may control live pub quizzes.", "error")
            return redirect(url_for('arena.league_lounge', slug=slug))
        return jsonify({'success': False, 'error': 'Unauthorized: Quizmaster or Admin account required'}), 403

    action = request.form.get('action')
    state = league.get_state()
    # Any host command means somebody is running the night, so the stale-night
    # clock starts again from here. Actions that change nothing never commit it.
    pub_touch(state)
    teams = state.get('teams', [])
    cfg = state.get('config', {})

    accept_hdr = request.headers.get('Accept') or ''
    is_browser_nav = 'text/html' in accept_hdr
    is_ajax = not is_browser_nav and (
        request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        or request.is_json
        or 'application/json' in accept_hdr
    )

    def respond(msg, extra=None):
        if is_ajax:
            payload = {'success': True, 'message': msg, 'state': league.get_state()}
            if extra:
                payload.update(extra)
            return jsonify(payload)
        if msg:
            flash(msg, "success")
        return redirect(url_for('arena.league_manager', slug=slug))

    def respond_error(err_msg):
        if is_ajax:
            return jsonify({'success': False, 'error': err_msg, 'state': league.get_state()}), 400
        flash(err_msg, "error")
        return redirect(url_for('arena.league_manager', slug=slug))

    if action == 'manager_logout':
        flash("Returned to Pub Lounge.", "info")
        return redirect(url_for('arena.league_lounge', slug=slug))

    elif action == 'approve_team':
        tbl = str(request.form.get('table') or '').strip()
        tname = (request.form.get('team_name') or '').strip()
        for t in teams:
            if (tbl and str(t.get('table')) == tbl) or (tname and t.get('name') == tname):
                t['status'] = 'approved'
        state['teams'] = teams
        league.set_state(state)
        db.session.commit()
        return respond(f"Table {tbl} approved! Room PIN {league.pin_code} unlocked for squad.")

    elif action == 'approve_all':
        for t in teams:
            t['status'] = 'approved'
        state['teams'] = teams
        league.set_state(state)
        db.session.commit()
        return respond("All pending tables approved!")

    elif action == 'reject_team':
        tbl = str(request.form.get('table') or '').strip()
        tname = (request.form.get('team_name') or '').strip()
        teams = [t for t in teams if not ((tbl and str(t.get('table')) == tbl) or (tname and t.get('name') == tname))]
        state['teams'] = teams
        league.set_state(state)
        db.session.commit()
        return respond(f"Table {tbl} removed.")

    elif action == 'add_manual_team':
        tbl = str(request.form.get('table') or '').strip()
        tname = (request.form.get('team_name') or '').strip()
        if tbl and tname:
            teams.append({
                'name': tname,
                'table': tbl,
                'members': 4,
                'score': 0,
                'rank': len(teams) + 1,
                'status': 'approved'
            })
            state['teams'] = teams
            league.set_state(state)
            db.session.commit()
            return respond(f"Table {tbl} ({tname}) added as verified!")
        return respond_error("Table number and team name required.")

    elif action == 'start_round':
        approved_teams = [t for t in teams if t.get('status') != 'pending']
        if not approved_teams:
            return respond_error("Step 1 Required: Approve at least 1 table in the Bouncer Queue (or add a manual table) before starting the round!")
        curr_r = int(state.get('current_round', 1))
        r = int(request.form.get('round') or curr_r)
        if r > curr_r:
            completed_tables = [t for t in approved_teams if t.get(f'round_{curr_r}') is not None]
            can_adv = len(completed_tables) >= len(approved_teams) or state.get('round_status') in ('closed', 'break')
            if not can_adv:
                return respond_error(f"Wait for all tables to finish Round {curr_r} (or click 'Lock / Time's Up') before starting Round {r}!")
        state['current_round'] = r
        state['round_status'] = 'active'
        state['answers_revealed'] = False
        state['round_ends_at'] = pub_round_deadline(cfg)
        state.pop('break_ends_at', None)
        league.set_state(state)
        db.session.commit()
        return respond(f"Round {r} launched! Questions broadcast to all {len(approved_teams)} approved table phones.")

    elif action == 'close_round':
        curr_r = state.get('current_round', 1)
        if state.get('round_status') != 'active':
            return respond_error(f"Round {curr_r} is not currently active.")
        # Record partial scores for any approved table that hasn't finished all questions yet
        close_pub_round(state, curr_r)
        state.pop('round_ends_at', None)
        league.set_state(state)
        db.session.commit()
        max_r = int(cfg.get('total_rounds', 5 if not league.is_virtual_league() else 3))
        next_msg = f"Click '▶ Start Round {curr_r + 1}' when ready!" if curr_r < max_r else "Click '🏆 Finalize & Crown Winner' when ready!"
        return respond(f"Round {curr_r} locked & partial scores saved! {next_msg}")

    elif action == 'reveal_answers':
        curr_r = state.get('current_round', 1)
        approved_teams = [t for t in teams if t.get('status') != 'pending']
        completed_tables = [t for t in approved_teams if t.get(f'round_{curr_r}') is not None]
        if not approved_teams or (len(completed_tables) < len(approved_teams) and state.get('round_status') not in ('closed', 'break', 'finished')):
            return respond_error("Wait for all tables to submit answers or click 'Lock / Time's Up' before revealing answers!")
        # A second click hides them again, so the host can put the keys up and take them down
        revealing = not state.get('answers_revealed')
        state['answers_revealed'] = revealing
        if revealing:
            state['round_status'] = 'closed' if state.get('round_status') == 'active' else state.get('round_status', 'closed')
            state.pop('round_ends_at', None)
        league.set_state(state)
        db.session.commit()
        if revealing:
            return respond("Official answers revealed on big screen and player screens!")
        return respond("Answer keys hidden again on all screens.")

    elif action == 'start_break':
        curr_r = state.get('current_round', 1)
        approved_teams = [t for t in teams if t.get('status') != 'pending']
        completed_tables = [t for t in approved_teams if t.get(f'round_{curr_r}') is not None]
        if not approved_teams or (len(completed_tables) < len(approved_teams) and state.get('round_status') not in ('closed', 'break', 'finished')):
            return respond_error("Wait for all tables to submit answers or click 'Lock / Time's Up' before starting the bar break!")
        state['round_status'] = 'break'
        state.pop('round_ends_at', None)
        duration_mins = int(cfg.get('interval_duration_mins', 8))
        break_ends = (datetime.utcnow() + timedelta(minutes=duration_mins)).isoformat()
        state['break_ends_at'] = break_ends
        league.set_state(state)
        db.session.commit()
        return respond(f"Bar break started ({duration_mins} mins)! Bar promo specials activated.")

    elif action in ('finish_tournament', 'advance_round'):
        curr = state.get('current_round', 1)
        approved_teams = [t for t in teams if t.get('status') != 'pending']
        completed_tables = [t for t in approved_teams if t.get(f'round_{curr}') is not None]
        can_adv = len(approved_teams) > 0 and (
            len(completed_tables) >= len(approved_teams) or state.get('round_status') in ('closed', 'break')
        )
        if not can_adv:
            return respond_error(f"Safety Gate: Wait for all {len(approved_teams)} tables to finish Round {curr} (or click 'Lock / Time's Up') first!")

        max_r = int(cfg.get('total_rounds', 5 if not league.is_virtual_league() else 3))
        if action == 'advance_round' and curr < max_r:
            state['current_round'] = curr + 1
            state['round_status'] = 'active'
            state['answers_revealed'] = False
            state['round_ends_at'] = pub_round_deadline(cfg)
            state.pop('break_ends_at', None)
            league.set_state(state)
            db.session.commit()
            return respond(f"Round {state['current_round']} launched! Questions broadcast to all phones.")
        else:
            saved = close_pub_night(league, state)
            tail = f" {saved} results saved to the league table." if saved else ""
            return respond(f"🏆 Tournament finalized! Champions crowned and final standings displayed on all "
                           f"screens. The room is now closed and the new PIN for next time is "
                           f"{league.pin_code}.{tail}")

    elif action == 'save_pin':
        new_pin = (request.form.get('pin_code') or '').strip().upper()
        if not (4 <= len(new_pin) <= 6) or not new_pin.isalnum():
            return respond_error("Room PIN must be 4 to 6 letters or digits.")
        clash = PubLeague.query.filter(PubLeague.pin_code == new_pin, PubLeague.id != league.id).first()
        if clash:
            return respond_error(f"Room PIN {new_pin} is already in use by {clash.name}. Pick another.")
        league.pin_code = new_pin
        # Approved tables hold the old PIN in their session; re-issue it on their next page load
        db.session.commit()
        return respond(f"Room PIN changed to {new_pin}. Announce it at the venue or show the big screen.")

    elif action == 'save_config':
        cfg['total_rounds'] = int(request.form.get('total_rounds', cfg.get('total_rounds', 5)))
        cfg['max_tables'] = int(request.form.get('max_tables', cfg.get('max_tables', 20)))
        cfg['question_time_limit'] = pub_question_secs(
            {'question_time_limit': request.form.get('question_time_limit', cfg.get('question_time_limit', 15))}
        )
        cfg['interval_duration_mins'] = int(request.form.get('interval_duration_mins', cfg.get('interval_duration_mins', 8)))
        cfg['bar_promo_enabled'] = bool(request.form.get('bar_promo_enabled'))
        cfg['round_deadline_enabled'] = bool(request.form.get('round_deadline_enabled'))
        cfg['auto_advance_enabled'] = bool(request.form.get('auto_advance_enabled'))
        if request.form.get('promo_title'): cfg['promo_title'] = request.form.get('promo_title').strip()
        if request.form.get('promo_desc'): cfg['promo_desc'] = request.form.get('promo_desc').strip()
        if request.form.get('promo_code'): cfg['promo_code'] = request.form.get('promo_code').strip()
        if request.form.get('first_prize'): cfg['first_prize'] = request.form.get('first_prize').strip()
        if request.form.get('second_prize'): cfg['second_prize'] = request.form.get('second_prize').strip()
        state['config'] = cfg
        league.set_state(state)
        db.session.commit()
        return respond("Tournament parameters & bar promos saved!")

    elif action in ('reset', 'reset_quiz', 'new_night'):
        # The finished night's results are already in the league table — closing
        # it banks them — so starting the next one loses nothing.
        was_finished = state.get('round_status') == 'finished' or state.get('tournament_completed')
        start_pub_night(state)
        league.set_state(state)
        db.session.commit()
        if action == 'new_night' or was_finished:
            return respond(f"New quiz night open at {league.name}! Last night's results are in the league "
                           f"table, the board is clear and the Room PIN for tonight is {league.pin_code}.")
        return respond("Tournament reset to Round 1! All tables cleared and player screens auto-notified.")

    elif action == 'clear_tables':
        state['teams'] = []
        # Clearing every table ends the live round too, or nobody could ever check in again
        state['round_status'] = 'waiting'
        # ...and takes the night off 'finished', or the room stays shut to the
        # tables the host has just cleared the way for.
        state['tournament_completed'] = False
        state.pop('night_closed_at', None)
        pub_touch(state)
        state['answers_revealed'] = False
        state.pop('round_ends_at', None)
        state.pop('break_ends_at', None)
        state.pop('results_recorded', None)
        state.pop('results_recorded_at', None)
        state['reset_ts'] = datetime.utcnow().isoformat()
        league.set_state(state)
        db.session.commit()
        return respond("All registered tables cleared!")

    league.set_state(state)
    db.session.commit()
    return respond("Action completed.")


@arena_bp.route('/leagues/<slug>/room', methods=['GET', 'POST'])
def league_room(slug):
    """Live Pub Quiz Interactive Session with table bouncer gating, 3-6 rounds, and bar promos."""
    player = get_current_player()
    league = PubLeague.query.filter_by(slug=slug, is_active=True).first_or_404()
    is_virtual = league.is_virtual_league()
    state = league.get_state()
    apply_pub_auto_progression(league, state)
    cfg = state.get('config', {})

    # The room is the live game. Once the night is over there is nothing to play,
    # and letting people back in is how a week-old quiz ends up handing out its
    # PIN and its tables. Send them to the lounge, where the final table is.
    if pub_night_is_over(league, state):
        session.pop(f'pub_pin_{slug}', None)
        if request.method == 'POST':
            return jsonify({'success': False, 'error': 'This quiz night has finished.'}), 403
        flash(f"{league.name} has finished for the night. The final scores are below, "
              f"and the Quizmaster will give out a new Room PIN for the next one.", "info")
        return redirect(url_for('arena.league_lounge', slug=slug))

    total_rounds = int(cfg.get('total_rounds', 3 if is_virtual else 5))
    current_round = int(state.get('current_round', 1))
    if current_round < 1 or current_round > total_rounds:
        current_round = 1

    table_num = (request.args.get('table') or request.form.get('table') or session.get('pub_table_num') or '1').strip()
    team_name = (request.args.get('team') or request.form.get('team') or session.get('pub_team_name') or f"Table {table_num} • {player.display_name}").strip()

    # Handle POST round score submission FIRST so it never hits GET redirects or race conditions!
    if request.method == 'POST':
        teams = state.get('teams', [])
        round_score = score_pub_answers(state, current_round, request.form.get('answers'), cfg, total_rounds)
        if round_score is None:
            return jsonify({'success': False, 'error': 'Answers required to score this round'}), 400
        team_entry = resolve_pub_team(state, player, table_num, team_name, is_virtual, require_pin=slug)

        # Only an approved squad may bank a score, and only while the host has the round open.
        # A score that arrives late (host already locked the round) is already banked by close_round.
        if not team_entry or team_entry.get('status') == 'pending':
            return jsonify({'success': False, 'error': 'Your squad has not been approved by the Quizmaster yet.'}), 403
        if state.get('round_status') != 'active' and team_entry.get(f'round_{current_round}') is None:
            return jsonify({'success': False, 'error': f'Round {current_round} is not open for submissions.'}), 403

        table_num = str(team_entry.get('table', table_num))
        team_name = team_entry.get('name', team_name)
        if team_entry.get(f'round_{current_round}') is None:
            team_entry[f'round_{current_round}'] = round_score
            team_entry[f'progress_q_{current_round}'] = PUB_QUESTIONS_PER_ROUND
            recompute_pub_score(team_entry)
        else:
            # Already banked (a squad mate on another phone got there first): report what counted
            round_score = int(team_entry[f'round_{current_round}'])

        rerank_pub_teams(teams)

        # Check if ALL approved tables have now completed this round!
        approved_teams = [t for t in teams if t.get('status') != 'pending']
        completed_tables = [t for t in approved_teams if t.get(f'round_{current_round}') is not None]
        all_tables_finished = len(approved_teams) > 0 and len(completed_tables) >= len(approved_teams)
        if all_tables_finished and state.get('round_status') == 'active':
            state['round_status'] = 'closed'

        state['teams'] = teams
        pub_touch(state)
        league.set_state(state)
        db.session.commit()
        player.add_xp(100 + round_score)

        next_round_num = current_round + 1 if current_round < total_rounds else None
        active_config = VIRTUAL_PUB_ROUNDS_CONFIG if is_virtual else PUB_ROUNDS_CONFIG
        next_round_title = active_config.get(current_round + 1, {}).get('name', 'Tournament Complete') if current_round < total_rounds else 'Tournament Complete'

        return jsonify({
            'success': True,
            'completed_round': current_round,
            'round_score': round_score,
            'total_score': team_entry.get('score', round_score),
            'rank': team_entry.get('rank', 1),
            'total_rounds': total_rounds,
            'all_tables_finished': all_tables_finished,
            'next_round': next_round_num,
            'next_round_title': next_round_title,
            'next_pub_date': get_next_weekly_pub_date()
        })

    # Optional PIN check if user typed a PIN on the lounge form
    pin_attempt = (request.args.get('pin') or '').strip()
    if pin_attempt and league.pin_code and pin_attempt != league.pin_code:
        flash(f"The Venue PIN '{pin_attempt}' did not match. Ask the Quizmaster at the venue for the PIN, or leave PIN blank to request Bouncer Approval.", "error")
        return redirect(url_for('arena.league_lounge', slug=slug))
    if pin_attempt and pin_attempt == league.pin_code:
        session[f'pub_pin_{slug}'] = pin_attempt

    active_cfg = VIRTUAL_PUB_ROUNDS_CONFIG if is_virtual else PUB_ROUNDS_CONFIG
    round_info = active_cfg.get(current_round, active_cfg.get(1, {'number': 1, 'name': f'Round {current_round}', 'cat_slug': 'world-history', 'icon': '🧠'}))

    # Check table capacity & Digital Bouncer approval (for BOTH physical and virtual pub quizzes)
    teams = state.get('teams', [])
    max_tables = int(cfg.get('max_tables', 20))
    team_entry = resolve_pub_team(state, player, table_num, team_name, is_virtual, require_pin=slug)

    # A squad mate on another phone joins the same scorecard with the squad's join code
    squad_code = (request.args.get('squad_code') or request.form.get('squad_code') or '').strip()
    if not team_entry and squad_code:
        team_entry = join_pub_squad_by_code(state, player, squad_code)
        if team_entry:
            league.set_state(state)
            db.session.commit()
        else:
            flash(f'Squad join code "{squad_code.upper()}" was not recognised for this league.', 'error')
            return redirect(url_for('arena.league_lounge', slug=slug))

    if not team_entry:
        # Strictly prevent new teams from joining a pub quiz tournament that has already started.
        # With no squads registered at all there is no tournament in progress to protect.
        quiz_already_started = bool(teams) and (
            state.get('current_round', 1) > 1 or state.get('round_status') in ('active', 'break', 'closed', 'finished')
        )
        if quiz_already_started:
            curr_r = state.get('current_round', 1)
            flash(f"Table registration is closed: {league.name} has already started Round {curr_r}. New tables cannot join mid-tournament. Please check in with the Quizmaster or join before the next match.", "error")
            return redirect(url_for('arena.league_lounge', slug=slug))

        approved_count = len([t for t in teams if t.get('status') != 'pending'])
        if approved_count >= max_tables:
            flash(f"This pub venue has reached its maximum table capacity of {max_tables} tables. Please check with the Quizmaster.", "error")
            return redirect(url_for('arena.league_lounge', slug=slug))
        if is_virtual:
            table_num, team_name = free_pub_squad_slot(teams, table_num, team_name)
        team_entry = {
            'name': team_name,
            'table': str(table_num),
            'members': 1 if is_virtual else 4,
            'score': 0,
            'rank': len(teams) + 1,
            'status': 'pending',  # Held in bouncer queue until Quizmaster approves
            'owner': player.session_key
        }
        if is_virtual:
            team_entry['join_code'] = new_pub_join_code(teams)
        teams.append(team_entry)
        state['teams'] = teams
        league.set_state(state)
        db.session.commit()
        is_approved = False
    else:
        # Always play under the squad number & name the host console actually shows
        table_num = str(team_entry.get('table', table_num))
        team_name = team_entry.get('name', team_name)
        is_approved = (team_entry.get('status') != 'pending')
        if is_approved:
            session[f'pub_pin_{slug}'] = league.pin_code

    session['pub_table_num'] = str(table_num)
    session['pub_team_name'] = team_name

    # Rounds this table was not here for. They stay unscored rather than being
    # skipped or back-filled, so the board stays honest — but the table is told,
    # instead of quietly wondering why it is bottom.
    missed_rounds = []
    if team_entry and current_round > 1:
        missed_rounds = [str(r) for r in range(1, current_round)
                         if team_entry.get(f'round_{r}') is None]

    # Check if this table has already submitted answers for the active round
    has_submitted_round = False
    submitted_round_score = 0
    if team_entry:
        r_score = team_entry.get(f'round_{current_round}')
        if r_score is not None:
            has_submitted_round = True
            submitted_round_score = int(r_score)

    # PINNED ROUND QUESTIONS: Guarantee all tables and TV screen receive identical questions
    round_questions_map = state.get('round_questions', {})
    r_key = str(current_round)
    pinned_ids = round_questions_map.get(r_key)
    questions = []
    if pinned_ids and isinstance(pinned_ids, list):
        for qid in pinned_ids:
            q = QuizQuestion.query.get(qid)
            if q:
                questions.append(q)

    if len(questions) < 5:
        all_pinned = []
        for q_list in round_questions_map.values():
            if isinstance(q_list, list):
                all_pinned.extend(q_list)
        seen_qids = session.get('pub_seen_qids', [])
        exclude_ids = list(set(seen_qids + all_pinned))
        cat_slug = round_info['cat_slug']
        questions = get_random_questions(category_slug=cat_slug, count=5, exclude_ids=exclude_ids)
        round_questions_map[r_key] = [q.id for q in questions]
        state['round_questions'] = round_questions_map
        league.set_state(state)
        db.session.commit()
        session['pub_seen_qids'] = list(set(exclude_ids + [q.id for q in questions]))

    # Always include answers in payload so client can reveal answers at end of round / quiz
    questions_json = [q.to_dict(include_answer=True) for q in questions]

    return render_template(
        'themes/quizhub/arena_league_room.html',
        player=player,
        league=league,
        team_name=team_name,
        table_num=table_num,
        current_round=current_round,
        total_rounds=total_rounds,
        round_info=round_info,
        questions=questions,
        questions_json=questions_json,
        is_virtual=is_virtual,
        is_approved=is_approved,
        join_code=team_entry.get('join_code') if team_entry else None,
        has_submitted_round=has_submitted_round,
        submitted_round_score=submitted_round_score,
        missed_rounds=missed_rounds,
        config=cfg,
        next_pub_date=get_next_weekly_pub_date(),
        state=state
    )


@arena_bp.route('/leagues/<slug>/tv')
def league_tv(slug):
    """Big-screen pub quiz display for TV projectors with live quizmaster host controls."""
    league = PubLeague.query.filter_by(slug=slug, is_active=True).first_or_404()
    # Host only: this screen prints the venue room PIN in full height for the room to read
    if not is_pub_host():
        flash("The Big Screen projector view is for the Quizmaster's venue screen only.", "error")
        return redirect(url_for('arena.league_lounge', slug=slug))
    is_virtual = league.is_virtual_league()
    state = league.get_state()
    apply_pub_auto_progression(league, state)
    current_round = state.get('current_round', 1)
    active_cfg = VIRTUAL_PUB_ROUNDS_CONFIG if is_virtual else PUB_ROUNDS_CONFIG
    round_info = active_cfg.get(current_round, active_cfg[1])

    # Big Screen TV MUST display the identical questions that tables are answering / reviewing
    round_questions_map = state.get('round_questions', {})
    pinned_ids = round_questions_map.get(str(current_round), [])
    questions = []
    if pinned_ids and isinstance(pinned_ids, list):
        for qid in pinned_ids:
            q = QuizQuestion.query.get(qid)
            if q:
                questions.append(q)

    if not questions:
        cat_slug = round_info['cat_slug']
        questions = QuizQuestion.query.filter_by(category_slug=cat_slug).limit(5).all()
        if len(questions) < 5:
            extra_q = QuizQuestion.query.filter(QuizQuestion.category_slug != cat_slug).limit(5 - len(questions)).all()
            questions = list(questions) + list(extra_q)

    teams = [t for t in league.get_teams() if t.get('status') != 'pending']
    cfg = state.get('config', {})
    total_rounds = int(cfg.get('total_rounds', 3 if is_virtual else 5))
    round_ticker = [
        (r_num, (active_cfg.get(r_num, {}).get('name') or f'Round {r_num}').split(': ', 1)[-1])
        for r_num in range(1, min(total_rounds, len(active_cfg)) + 1)
    ]
    return render_template(
        'themes/quizhub/arena_league_tv.html',
        league=league,
        teams=teams,
        state=state,
        config=cfg,
        current_round=current_round,
        total_rounds=total_rounds,
        round_info=round_info,
        round_ticker=round_ticker,
        questions=questions,
        is_virtual=is_virtual
    )


# =========================================================================
# Group Challenge: several players, one question at a time, no host
#
# The pub league proved the timing model - a deadline per round, applied by
# whoever happens to poll - so the same idea runs a question at a time here.
# Nobody hosts it: the lobby starts itself once enough people are in, and
# each question closes on its own clock.
# =========================================================================

GROUP_CODE_ALPHABET = 'ACDEFGHJKLMNPQRTUVWXY34679'

# Bots exist only to fill a lobby so a game can start. They are rows in
# group_players and nothing else, so they cannot reach a leaderboard.
GROUP_BOT_NAMES = [
    'Quiz Gremlin', 'Trivia Tortoise', 'Captain Cortex', 'The Quizzard',
    'Nimble Noggin', 'Factoid Fox', 'Buzzer Badger', 'Professor Pub',
    'Cranium Carol', 'Swotty Sid', 'Mastermind Mo', 'Quick Draw Quinn',
]
GROUP_BOT_ACCURACY = 0.6


def new_group_code():
    for _ in range(40):
        code = ''.join(random.choice(GROUP_CODE_ALPHABET) for _ in range(5))
        if not GroupGame.query.filter_by(code=code).first():
            return code
    return ''.join(random.choice(GROUP_CODE_ALPHABET) for _ in range(8))


def group_seat(game, player):
    """This player's seat in the game, if they have one."""
    if not player:
        return None
    return game.players.filter_by(player_key=player.session_key, is_bot=False).first()


def add_group_bot(game):
    """Drop a throwaway bot into a free seat."""
    taken = {p.display_name for p in game.players}
    pool = [n for n in GROUP_BOT_NAMES if n not in taken]
    if not pool or game.is_full():
        return None
    bot = GroupPlayer(
        game_id=game.id,
        player_key=None,
        display_name=random.choice(pool),
        avatar_key=random.choice([a['key'] for a in AVATAR_PRESETS if a['key'] != 'nova']),
        is_bot=True
    )
    db.session.add(bot)
    return bot


def group_questions(game):
    ids = game.get_question_ids()
    found = []
    for qid in ids:
        q = QuizQuestion.query.get(qid)
        if q:
            found.append(q)
    return found


def score_group_answer(question, choice, seconds_left, limit):
    """Same shape as the pub quiz: right answer plus whatever clock is left."""
    if not question or not choice or choice != question.correct_option:
        return 0
    seconds_left = max(0, min(int(limit), int(seconds_left or 0)))
    return 100 + seconds_left * 2


def settle_group_question(game):
    """Close the current question: score every seat, including the bots."""
    questions = group_questions(game)
    idx = game.current_index
    if idx >= len(questions):
        return
    question = questions[idx]
    limit = game.seconds_per_question or 15

    for seat in game.players:
        answers = seat.get_answers()
        key = str(idx)
        if key in answers:
            continue  # a human who answered in time is already recorded
        if seat.is_bot:
            correct = random.random() < GROUP_BOT_ACCURACY
            # Bots never look superhuman: they use up a believable slice of the clock
            left = random.randint(1, max(1, int(limit * 0.6)))
            choice = question.correct_option if correct else next(
                (o for o in ('A', 'B', 'C', 'D') if o != question.correct_option), 'A'
            )
            points = score_group_answer(question, choice, left, limit)
        else:
            choice, left, points = None, 0, 0  # ran out of clock
        answers[key] = {'choice': choice, 'left': left, 'points': points}
        seat.set_answers(answers)
        seat.score = int(seat.score or 0) + points


def advance_group_game(game):
    """Move the game along if a deadline has passed. Safe to call from any request."""
    now = datetime.utcnow()
    changed = False

    if game.status == 'lobby':
        count = game.players.count()
        if count >= (game.min_players or 3) and not game.starts_at:
            # Enough people: put a countdown on the board rather than waiting for a full house
            game.starts_at = now + timedelta(seconds=12)
            changed = True
        if game.starts_at and (now >= game.starts_at or game.is_full()):
            game.status = 'active'
            game.current_index = 0
            game.question_ends_at = now + timedelta(seconds=game.seconds_per_question or 15)
            changed = True

    if game.status == 'active' and game.question_ends_at and now >= game.question_ends_at:
        settle_group_question(game)
        game.status = 'reveal'
        game.reveal_ends_at = now + timedelta(seconds=game.reveal_seconds or 4)
        changed = True

    if game.status == 'reveal' and game.reveal_ends_at and now >= game.reveal_ends_at:
        if game.current_index + 1 >= len(game.get_question_ids()):
            game.status = 'finished'
            game.question_ends_at = None
            game.reveal_ends_at = None
        else:
            game.current_index += 1
            game.status = 'active'
            game.question_ends_at = now + timedelta(seconds=game.seconds_per_question or 15)
            game.reveal_ends_at = None
        changed = True

    if changed:
        db.session.commit()
    return changed


def group_standings(game):
    seats = sorted(game.players, key=lambda s: (-(s.score or 0), s.display_name.lower()))
    out = []
    for pos, seat in enumerate(seats, 1):
        out.append({
            'position': pos,
            'name': seat.display_name,
            'avatar': seat.avatar_key,
            'is_bot': seat.is_bot,
            'score': seat.score or 0,
            'last': (seat.get_answers().get(str(game.current_index)) or {}).get('points', 0)
        })
    return out


@arena_bp.route('/group/new', methods=['GET', 'POST'])
def group_new():
    """Open a lobby. Whoever opens it picks the size and the subject."""
    gate = needs_account_to_challenge('open a group game')
    if gate:
        return gate
    player = get_current_player()
    categories = db.session.query(QuizQuestion.category_slug, QuizQuestion.category_name).distinct().all()

    if request.method == 'POST':
        try:
            min_players = max(2, min(6, int(request.form.get('min_players') or 3)))
            max_players = max(min_players, min(6, int(request.form.get('max_players') or 6)))
            total_questions = max(3, min(15, int(request.form.get('total_questions') or 8)))
            seconds = max(10, min(30, int(request.form.get('seconds_per_question') or 15)))
        except (TypeError, ValueError):
            flash('Those game settings did not look right.', 'error')
            return redirect(url_for('arena.group_new'))

        # More than one subject can be ticked now, so the questions are drawn
        # a few at a time from each in turn rather than all from one. Nothing
        # ticked means the whole bank, which is the sensible default for a
        # lobby of friends who have not agreed on a subject.
        wanted = [s.strip() for s in request.form.getlist('category_slug') if s.strip()]
        # Deduplicated by slug: the categories query is DISTINCT over the slug
        # AND the name, so a slug stored under two spellings comes back twice
        # and would otherwise be counted as two subjects.
        chosen, seen_slugs = [], set()
        for c in categories:
            if c[0] in wanted and c[0] not in seen_slugs:
                seen_slugs.add(c[0])
                chosen.append(c)

        questions, used = [], []
        if chosen:
            # Round robin, so a thin category cannot crowd out the rest and a
            # fat one cannot take over.
            i = 0
            while len(questions) < total_questions and i < total_questions * 2:
                cat = chosen[i % len(chosen)]
                picked = get_random_questions(category_slug=cat[0], count=1, exclude_ids=used)
                for q in picked:
                    if q.id not in used:
                        questions.append(q)
                        used.append(q.id)
                i += 1
        # Top up from the whole bank when the chosen subjects run dry, and use
        # it outright when nothing was ticked.
        if len(questions) < total_questions:
            questions += get_random_questions(count=total_questions - len(questions),
                                              exclude_ids=used)
        random.shuffle(questions)
        questions = questions[:total_questions]

        if not questions:
            flash('There are not enough questions to start a game right now.', 'error')
            return redirect(url_for('arena.dashboard'))

        if not chosen:
            cat_slug, cat_name = 'mixed', 'Mixed Bag'
        elif len(chosen) == 1:
            cat_slug, cat_name = chosen[0][0], chosen[0][1]
        else:
            # One name and a count. These titles run long -- "Silicon Pioneers
            # & Coding Legends" is one of them -- so listing two blows out
            # every badge the name appears in.
            cat_slug = 'mixed'
            cat_name = '%s +%d more' % (chosen[0][1], len(chosen) - 1)

        game = GroupGame(
            code=new_group_code(),
            status='lobby',
            category_slug=cat_slug,
            category_name=cat_name,
            min_players=min_players,
            max_players=max_players,
            total_questions=len(questions),
            seconds_per_question=seconds,
            host_key=player.session_key
        )
        game.set_question_ids([q.id for q in questions])
        db.session.add(game)
        db.session.flush()

        db.session.add(GroupPlayer(
            game_id=game.id, player_key=player.session_key,
            display_name=player.display_name, avatar_key=player.avatar_key, is_bot=False
        ))
        db.session.commit()
        return redirect(url_for('arena.group_lobby', code=game.code))

    open_games = GroupGame.query.filter_by(status='lobby').order_by(GroupGame.created_at.desc()).limit(10).all()
    return render_template('themes/quizhub/arena_group_new.html',
                           player=player, categories=sorted(categories, key=lambda c: c[1]),
                           open_games=open_games,
                           # So the list can say which of these are yours, and
                           # offer to close them rather than to join them.
                           my_key=player.session_key)


@arena_bp.route('/group/<code>')
def group_lobby(code):
    """The lobby and the game itself; one page, driven by the live state."""
    player = get_current_player()
    game = GroupGame.query.filter_by(code=code.upper()).first_or_404()
    advance_group_game(game)

    seat = group_seat(game, player)
    if not seat and game.status == 'lobby' and not game.is_full():
        seat = GroupPlayer(game_id=game.id, player_key=player.session_key,
                           display_name=player.display_name, avatar_key=player.avatar_key, is_bot=False)
        db.session.add(seat)
        db.session.commit()
        advance_group_game(game)
    elif not seat:
        flash('That game is already under way, or full. Start your own!', 'error')
        return redirect(url_for('arena.group_new'))

    questions = group_questions(game)
    return render_template('themes/quizhub/arena_group_play.html',
                           player=player, game=game, seat=seat,
                           questions_json=[q.to_dict(include_answer=False) for q in questions],
                           total_questions=len(questions))


@arena_bp.route('/match/<match_code>/withdraw', methods=['POST'])
def match_withdraw(match_code):
    """Take back a duel invite nobody has accepted.

    Only the player who sent it, and only while the other seat is empty. Once
    somebody is in it they may have played a round, and a duel in progress is
    not one person's to delete.
    """
    player = get_current_player(persist=False)
    match = ArenaMatch.query.filter_by(match_code=match_code).first_or_404()
    me = player.session_key if player else None

    if not me or me != match.player1_session:
        flash('Only whoever sent that invite can take it back.', 'error')
        return redirect(url_for('arena.dashboard'))
    if match.player2_session:
        flash('Someone has already accepted that duel, so it has to play out.', 'error')
        return redirect(url_for('arena.match_lobby', match_code=match.match_code))

    ArenaRound.query.filter_by(match_id=match.id).delete()
    db.session.delete(match)
    db.session.commit()
    flash('Invite withdrawn.', 'success')
    return redirect(url_for('arena.dashboard'))


@arena_bp.route('/group/<code>/cancel', methods=['POST'])
def group_cancel(code):
    """Close a lobby you opened and nobody has started playing.

    Only the host, and only while it is still a lobby: once the questions are
    live, other people are mid-game and it is not one person's to end.
    """
    player = get_current_player(persist=False)
    game = GroupGame.query.filter_by(code=code.upper()).first_or_404()
    me = player.session_key if player else None

    if not me or me != game.host_key:
        flash('Only whoever opened that lobby can close it.', 'error')
        return redirect(url_for('arena.group_new'))
    if game.status != 'lobby':
        flash('That game has already started, so it has to play out.', 'error')
        return redirect(url_for('arena.group_lobby', code=game.code))

    GroupPlayer.query.filter_by(game_id=game.id).delete()
    db.session.delete(game)
    db.session.commit()
    flash('Lobby closed.', 'success')
    return redirect(url_for('arena.group_new'))


@arena_bp.route('/group/<code>/state')
def group_state(code):
    """Everything a phone needs to draw the current moment."""
    player = get_current_player(persist=False)
    game = GroupGame.query.filter_by(code=code.upper()).first_or_404()
    advance_group_game(game)

    seat = group_seat(game, player)
    now = datetime.utcnow()
    questions = group_questions(game)
    idx = game.current_index
    question = questions[idx] if idx < len(questions) else None

    def seconds_until(when):
        return max(0, round((when - now).total_seconds(), 1)) if when else None

    payload = {
        'success': True,
        'status': game.status,
        'code': game.code,
        'category': game.category_name,
        'question_number': idx + 1,
        'total_questions': len(questions),
        'players': [{
            'name': p.display_name, 'avatar': p.avatar_key, 'is_bot': p.is_bot,
            'score': p.score or 0, 'answered': str(idx) in p.get_answers()
        } for p in sorted(game.players, key=lambda x: x.joined_at or now)],
        'player_count': game.players.count(),
        'min_players': game.min_players,
        'max_players': game.max_players,
        'starts_in': seconds_until(game.starts_at),
        'question_ends_in': seconds_until(game.question_ends_at),
        'reveal_ends_in': seconds_until(game.reveal_ends_at),
        'you_answered': bool(seat and str(idx) in seat.get_answers()),
        'your_score': seat.score if seat else 0,
    }

    if game.status == 'active' and question:
        payload['question'] = {
            'id': question.id, 'prompt': question.prompt,
            'options': question.get_options(),
            'media_url': question.media_url, 'question_type': question.question_type
        }
    if game.status in ('reveal', 'finished') and question:
        payload['reveal'] = {
            'correct_option': question.correct_option,
            'explanation': question.explanation,
            'prompt': question.prompt,
            'your_answer': (seat.get_answers().get(str(idx)) or {}) if seat else {}
        }
    if game.status in ('reveal', 'finished'):
        payload['standings'] = group_standings(game)

    return jsonify(payload)


@arena_bp.route('/group/<code>/answer', methods=['POST'])
def group_answer(code):
    """Lock in an answer. The clock is the server's, not the phone's."""
    player = get_current_player(persist=False)
    game = GroupGame.query.filter_by(code=code.upper()).first_or_404()
    advance_group_game(game)

    seat = group_seat(game, player)
    if not seat:
        return jsonify({'success': False, 'error': 'You are not in this game'}), 403
    if game.status != 'active':
        return jsonify({'success': False, 'error': 'No question is open'}), 400

    idx = game.current_index
    answers = seat.get_answers()
    if str(idx) in answers:
        return jsonify({'success': False, 'error': 'Already answered'}), 400

    questions = group_questions(game)
    if idx >= len(questions):
        return jsonify({'success': False, 'error': 'No question is open'}), 400
    question = questions[idx]

    choice = (request.form.get('choice') or '').strip().upper()
    if choice not in ('A', 'B', 'C', 'D'):
        return jsonify({'success': False, 'error': 'Pick one of the four options'}), 400

    # The remaining clock comes from the server's own deadline, so a phone cannot claim more
    left = 0
    if game.question_ends_at:
        left = max(0, int((game.question_ends_at - datetime.utcnow()).total_seconds()))
    points = score_group_answer(question, choice, left, game.seconds_per_question or 15)

    answers[str(idx)] = {'choice': choice, 'left': left, 'points': points}
    seat.set_answers(answers)
    seat.score = int(seat.score or 0) + points

    # Everyone is in: no reason to make them watch the clock run down
    if all(str(idx) in p.get_answers() for p in game.players if not p.is_bot):
        settle_group_question(game)
        game.status = 'reveal'
        game.reveal_ends_at = datetime.utcnow() + timedelta(seconds=game.reveal_seconds or 4)

    db.session.commit()
    return jsonify({'success': True, 'locked': choice})


@arena_bp.route('/group/<code>/add-bot', methods=['POST'])
def group_add_bot(code):
    """Fill a seat so a quiet lobby can still get going."""
    player = get_current_player(persist=False)
    game = GroupGame.query.filter_by(code=code.upper()).first_or_404()
    if game.status != 'lobby':
        return jsonify({'success': False, 'error': 'The game has already started'}), 400
    if game.host_key and game.host_key != player.session_key:
        return jsonify({'success': False, 'error': 'Only whoever opened the lobby can add a bot'}), 403
    bot = add_group_bot(game)
    if not bot:
        return jsonify({'success': False, 'error': 'The lobby is full'}), 400
    db.session.commit()
    advance_group_game(game)
    return jsonify({'success': True, 'name': bot.display_name})


@arena_bp.route('/api/daily')
def api_daily_questions():
    """Return database-backed daily brain sprint questions rotated deterministically by calendar date."""
    now = datetime.utcnow()
    date_formatted = now.strftime('%A, %d %B %Y')
    start_date = datetime(2026, 1, 1)
    day_diff = max(1, (now - start_date).days + 1)
    challenge_num = f"#{day_diff}"

    total_q = QuizQuestion.query.count()
    if total_q > 0:
        offset = (day_diff * 5) % total_q
        questions = QuizQuestion.query.order_by(QuizQuestion.id.asc()).offset(offset).limit(5).all()
        if len(questions) < 5:
            extra = QuizQuestion.query.order_by(QuizQuestion.id.asc()).limit(5 - len(questions)).all()
            questions = list(questions) + list(extra)
    else:
        questions = []

    return jsonify({
        'success': True,
        'badge': f"DAILY BRAIN CHALLENGE • {now.strftime('%A').upper()}",
        'date_formatted': date_formatted,
        'challenge_num': challenge_num,
        'questions': [q.to_dict(include_answer=True) for q in questions]
    })


# -------------------------------------------------------------------------
# Community Quiz & Trivia Pack Studio
# -------------------------------------------------------------------------
PROFANITY_FLAGS = {'nude', 'viagra', 'casino', 'porn', 'scam', 'hack', 'warez', 'fuck', 'shit', 'bitch', 'asshole'}


def passes_safety_filter(text: str) -> bool:
    if not text:
        return True
    lower = text.lower()
    for bad in PROFANITY_FLAGS:
        if bad in lower:
            return False
    return True


@arena_bp.route('/create', methods=['GET', 'POST'])
def create_question():
    """Community Quiz and Trivia Pack Studio - strictly restricted to Super Admins, Admins, Quizmasters, and Creators."""
    user_id = session.get('user_id')
    user_role = session.get('user_role')
    is_creator = user_role in ('super_admin', 'admin', 'quizmaster', 'creator')

    if not user_id:
        flash("Quiz Creator Studio is reserved for Admins and Verified Quiz Creators. Please sign in.", "info")
        return redirect(url_for('arena.player_login', next=url_for('arena.create_question')))
    if not is_creator:
        flash("Quiz Creator Studio is restricted to Admins and Verified Quiz Creators.", "error")
        return redirect(url_for('arena.dashboard'))

    player = get_current_player()
    
    if request.method == 'POST':
        prompt = (request.form.get('prompt') or '').strip()
        category_slug = (request.form.get('category_slug') or 'general').strip()
        category_name = (request.form.get('category_name') or 'General Knowledge').strip()
        question_type = request.form.get('question_type', 'classic')
        media_url = (request.form.get('media_url') or '').strip()
        difficulty = request.form.get('difficulty', 'medium')
        correct_option = request.form.get('correct_option', 'A').strip().upper()
        explanation = (request.form.get('explanation') or '').strip()
        pack_slug = (request.form.get('pack_slug') or 'community').strip()
        author_name = (request.form.get('author_name') or player.display_name).strip()

        options = {
            'A': (request.form.get('opt_a') or '').strip(),
            'B': (request.form.get('opt_b') or '').strip(),
            'C': (request.form.get('opt_c') or '').strip(),
            'D': (request.form.get('opt_d') or '').strip()
        }

        if not prompt or not options['A'] or not options['B']:
            flash("Question prompt and at least options A and B are required.", "error")
            return redirect(url_for('arena.create_question'))

        # Safety filter
        combined_text = f"{prompt} {options['A']} {options['B']} {options['C']} {options['D']} {explanation}"
        is_safe = passes_safety_filter(combined_text)
        initial_status = 'approved' if is_safe else 'pending'

        q = QuizQuestion(
            prompt=prompt,
            question_type=question_type,
            media_url=media_url,
            options_json=json.dumps(options),
            correct_option=correct_option,
            explanation=explanation,
            category_slug=category_slug,
            category_name=category_name,
            difficulty=difficulty,
            points=100,
            time_limit=15,
            pack_slug=pack_slug,
            is_community=True,
            status=initial_status,
            author_name=author_name
        )
        db.session.add(q)

        # Ensure pack exists if custom pack specified
        pack = QuizPack.query.filter_by(slug=pack_slug).first()
        if not pack and pack_slug != 'core':
            pack = QuizPack(
                title=f"{category_name} Community Pack",
                slug=pack_slug,
                description=f"Curated trivia submitted by {author_name} and players.",
                icon='🧩',
                category_slug=category_slug,
                is_community=True,
                author_name=author_name,
                question_count=1
            )
            db.session.add(pack)
        elif pack:
            pack.question_count = (pack.question_count or 0) + 1

        # Reward player for contributing
        player.add_xp(150)
        player.coins = (player.coins or 0) + 50
        db.session.commit()

        if is_safe:
            flash(f"🎉 Question published to Quizmondo Arena! You earned +150 XP and +50 Coins!", "success")
        else:
            flash(f"🛡️ Question submitted! It is in the moderation queue for quick review. You earned +150 XP!", "info")

        return redirect(url_for('arena.dashboard'))

    categories = db.session.query(QuizQuestion.category_slug, QuizQuestion.category_name).distinct().all()
    packs = QuizPack.query.all()
    return render_template(
        'themes/quizhub/arena_create.html',
        player=player,
        categories=categories,
        packs=packs
    )


@arena_bp.route('/challenge-fresh/<target_session>', methods=['GET', 'POST'])
def challenge_fresh(target_session):
    """Start a direct Round 1 duel against a registered friend / past opponent (auto-notifies them in-app, no WhatsApp needed!)."""
    gate = needs_account_to_challenge('challenge another player')
    if gate:
        return gate
    player = get_current_player()
    target_player = PlayerProfile.query.filter_by(session_key=target_session).first()

    # If there is already an active duel between these two players, jump straight to it!
    if target_player and target_player.session_key != player.session_key:
        existing_active = ArenaMatch.query.filter(
            ((ArenaMatch.player1_session == player.session_key) & (ArenaMatch.player2_session == target_player.session_key)) |
            ((ArenaMatch.player1_session == target_player.session_key) & (ArenaMatch.player2_session == player.session_key)),
            ArenaMatch.status.in_(['waiting', 'in_progress'])
        ).order_by(ArenaMatch.updated_at.desc()).first()
        if existing_active:
            flash(f"⚔️ Resuming your active duel with {target_player.display_name}!", "info")
            return redirect(url_for('arena.match_lobby', match_code=existing_active.match_code))

    match_code = f"qm_{secrets.token_hex(4)}"
    questions = get_random_questions(count=3)
    q_ids = [q.id for q in questions]
    cat_slug = questions[0].category_slug if questions else 'general'
    cat_name = questions[0].category_name if questions else 'General Knowledge'

    match = ArenaMatch(
        match_code=match_code,
        player1_session=player.session_key,
        player1_name=player.display_name,
        player1_avatar=player.avatar_key,
        player2_session=target_player.session_key if target_player else None,
        player2_name=target_player.display_name if target_player else 'Challenger',
        player2_avatar=target_player.avatar_key if target_player else 'nova',
        status='in_progress' if target_player else 'waiting',
        current_round=1,
        current_turn=1,
        winner=0,
        p1_total_score=0,
        p2_total_score=0
    )
    db.session.add(match)
    db.session.flush()

    round_1 = ArenaRound(
        match_id=match.id,
        round_number=1,
        category_slug=cat_slug,
        category_name=cat_name,
        chosen_by=1,
        question_ids_json=json.dumps(q_ids),
        p1_score=0,
        p1_answers_json=json.dumps([]),
        p2_score=0,
        p2_answers_json=json.dumps([]),
        status='pending'
    )
    db.session.add(round_1)
    db.session.commit()

    if target_player:
        flash(f"⚔️ Direct Duel started with {target_player.display_name}! Play Round 1 now — {target_player.display_name} will be notified automatically!", "success")
    else:
        flash("New Round 1 duel created! Send the link on WhatsApp to challenge your friend.", "success")
    return redirect(url_for('arena.match_lobby', match_code=match_code))


@arena_bp.route('/packs')
def packs_directory():
    """Browse all Core and Community Trivia Packs."""
    player = get_current_player(persist=False)
    all_packs = QuizPack.query.order_by(QuizPack.is_community.asc(), QuizPack.created_at.desc()).all()
    return render_template(
        'themes/quizhub/arena_packs.html',
        player=player,
        packs=all_packs
    )

# ==============================================================================
# THE DAILY LUCKY COIN WHEEL ("THE VAULT SPINNER")
# ==============================================================================

WHEEL_SLICES = [
    {'index': 0, 'label': '50 Coins', 'type': 'coins', 'amount': 50, 'weight': 30, 'icon': '🪙', 'color': '#ec4899'},
    {'index': 1, 'label': 'Climber Shield', 'type': 'shield', 'amount': 1, 'weight': 15, 'icon': '🛡️', 'color': '#06b6d4'},
    {'index': 2, 'label': '100 Coins', 'type': 'coins', 'amount': 100, 'weight': 25, 'icon': '🪙', 'color': '#8b5cf6'},
    {'index': 3, 'label': '150 XP Boost', 'type': 'xp', 'amount': 150, 'weight': 15, 'icon': '⚡', 'color': '#f59e0b'},
    {'index': 4, 'label': '250 Coins', 'type': 'coins', 'amount': 250, 'weight': 8, 'icon': '💰', 'color': '#10b981'},
    {'index': 5, 'label': 'Safety Shield', 'type': 'shield', 'amount': 1, 'weight': 10, 'icon': '🛡️', 'color': '#3b82f6'},
    {'index': 6, 'label': 'JACKPOT 1,000 Coins', 'type': 'jackpot', 'amount': 1000, 'weight': 3, 'icon': '🌟', 'color': '#eab308'},
    {'index': 7, 'label': '75 Coins', 'type': 'coins', 'amount': 75, 'weight': 20, 'icon': '🪙', 'color': '#f43f5e'}
]


@arena_bp.route('/wheel')
def wheel():
    """Daily Vault Spinner screen for free daily coins and climber shields."""
    gate = needs_account_to_play('spin the Daily Vault Wheel')
    if gate:
        return gate
    player = get_current_player(persist=True)
    now = datetime.utcnow()
    can_spin = True
    seconds_left = 0

    if player.last_wheel_spin_at:
        elapsed = (now - player.last_wheel_spin_at).total_seconds()
        if elapsed < 86400:
            can_spin = False
            seconds_left = max(0, int(86400 - elapsed))

    return render_template(
        'themes/quizhub/arena_wheel.html',
        player=player,
        can_spin=can_spin,
        seconds_left=seconds_left,
        slices=WHEEL_SLICES
    )


@arena_bp.route('/wheel/spin', methods=['POST'])
def wheel_spin():
    """Spin the Daily Lucky Wheel with fair weighted odds and 24h cooldown."""
    if not session.get('user_id'):
        return jsonify({
            'success': False,
            'error': 'You must be logged in to spin the wheel.',
            'login_required': True,
            'redirect': url_for('arena.player_register', next=url_for('arena.wheel'))
        }), 401
    player = get_current_player(persist=True)
    now = datetime.utcnow()

    if player.last_wheel_spin_at:
        elapsed = (now - player.last_wheel_spin_at).total_seconds()
        if elapsed < 86400:
            seconds_left = int(86400 - elapsed)
            return jsonify({
                'success': False,
                'error': 'Daily spin cooldown active',
                'seconds_left': seconds_left
            }), 429

    weights = [s['weight'] for s in WHEEL_SLICES]
    prize = random.choices(WHEEL_SLICES, weights=weights, k=1)[0]

    # Award the prize
    if prize['type'] in ('coins', 'jackpot'):
        player.coins = (player.coins or 0) + prize['amount']
    elif prize['type'] == 'shield':
        player.climber_shields = (player.climber_shields or 0) + prize['amount']
    elif prize['type'] == 'xp':
        player.add_xp(prize['amount'])

    player.last_wheel_spin_at = now
    db.session.commit()

    return jsonify({
        'success': True,
        'slice': prize,
        'index': prize['index'],
        'coins': player.coins,
        'shields': player.climber_shields,
        'xp': player.xp,
        'level': player.level
    })


# ==============================================================================
# THE QUIZ CLIMBER ("THE WALL" — 30-DAY EXPEDITION STORY)
# ==============================================================================

EXPEDITION_STAGES = [
    {
        'stage': 1,
        'name': 'Valley Basecamp',
        'safe_haven': 'Pine Valley Basecamp',
        'altitude_range': '1,000m – 2,500m',
        'base_alt': 1000,
        'max_alt': 2500,
        'days': 'Days 1–5',
        'diff': 'easy',
        'coins_per_step': 50,
        'clue': 'Trek through pine forests and rhododendron valleys. Acclimatize and prepare supplies.',
        'icon': '🌲'
    },
    {
        'stage': 2,
        'name': 'Khumbu Icefall',
        'safe_haven': 'Camp 1 Plateau',
        'altitude_range': '2,500m – 4,000m',
        'base_alt': 2500,
        'max_alt': 4000,
        'days': 'Days 6–10',
        'diff': 'medium',
        'coins_per_step': 75,
        'clue': 'Cross bottomless crevasses and dodging unstable seracs on tied aluminum ladders.',
        'icon': '🪜'
    },
    {
        'stage': 3,
        'name': 'Western Cwm',
        'safe_haven': 'Camp 2 Advanced Base',
        'altitude_range': '4,000m – 5,500m',
        'base_alt': 4000,
        'max_alt': 5500,
        'days': 'Days 11–15',
        'diff': 'medium',
        'coins_per_step': 100,
        'clue': 'Navigate the Valley of Silence under the blazing reflection of Nuptse and Everest.',
        'icon': '☀️'
    },
    {
        'stage': 4,
        'name': 'Lhotse Ice Face',
        'safe_haven': 'Camp 3 Ice Perch',
        'altitude_range': '5,500m – 7,000m',
        'base_alt': 5500,
        'max_alt': 7000,
        'days': 'Days 16–20',
        'diff': 'hard',
        'coins_per_step': 150,
        'clue': 'Ascend the 1,125m wall of sheer blue ice and cross the prehistoric Yellow Band.',
        'icon': '🧗'
    },
    {
        'stage': 5,
        'name': 'South Col Death Zone',
        'safe_haven': 'Camp 4 High Camp',
        'altitude_range': '7,000m – 8,000m',
        'base_alt': 7000,
        'max_alt': 8000,
        'days': 'Days 21–25',
        'diff': 'hard',
        'coins_per_step': 200,
        'clue': 'Sub-zero hurricane winds in the Death Zone. Oxygen levels drop to one-third.',
        'icon': '☠️'
    },
    {
        'stage': 6,
        'name': 'Hillary Step & Summit',
        'safe_haven': 'Mount Everest Summit (8,848m)',
        'altitude_range': '8,000m – 8,848m',
        'base_alt': 8000,
        'max_alt': 8848,
        'days': 'Days 26–30',
        'diff': 'hard',
        'coins_per_step': 300,
        'clue': 'Traverse the knife-edge ridge, conquer the Hillary Step, and touch the sky at 8,848m!',
        'icon': '👑'
    }
]


CAMP_MISSIONS = {
    5: {
        'title': 'Pitch Windproof Storm Tents',
        'icon': '⛺',
        'camp_name': 'Valley Basecamp (Camp 1)',
        'objective': 'Anchor high-tension guy ropes and cross-braced poles before the Himalayan gale strikes.',
        'game_type': 'pairs',
        'instruction': 'Match all 4 pairs of alpine shelter gear before the storm hits!',
        'reward_desc': 'Basecamp secure! +1 Climber Shield & Health Restored.',
        'bonus_shield': 1,
        'bonus_coins': 50
    },
    10: {
        'title': 'Secure Khumbu Icefall Ladders',
        'icon': '🪜',
        'camp_name': 'Camp 1 Plateau',
        'objective': 'Fasten safety lines and link aluminum bridge ladders across bottomless crevasses.',
        'game_type': 'sequence',
        'instruction': 'Link the 4 ladder anchoring safety steps in the correct numerical order!',
        'reward_desc': 'Icefall ladder route secured! Camp Safe Haven locked.',
        'bonus_shield': 0,
        'bonus_coins': 75
    },
    15: {
        'title': 'Melt Glacial Snow & Cook Rations',
        'icon': '🍲',
        'camp_name': 'Camp 2 Advanced Base',
        'objective': 'Fire the sub-zero MSR stove, melt fresh glacier snow, and restore 4,000 calories.',
        'game_type': 'scramble',
        'instruction': 'Tap the 3 essential ration supplies to complete the expedition meal!',
        'reward_desc': 'Vital calories & hydration restored! Stamina refreshed.',
        'bonus_shield': 0,
        'bonus_coins': 100
    },
    20: {
        'title': 'Lhotse Face Medical Reflex Check',
        'icon': '❤️‍🩹',
        'camp_name': 'Camp 3 Ice Perch',
        'objective': 'Check blood oxygen pulse, test motor reflexes, and warm frozen extremities.',
        'game_type': 'reflex',
        'instruction': 'Memorize and tap the 4-cell green pulse sequence to pass the medical check!',
        'reward_desc': 'Cognitive health & vital stamina cleared for the Death Zone! +1 Shield.',
        'bonus_shield': 1,
        'bonus_coins': 150
    },
    25: {
        'title': 'Inspect South Col Oxygen Regulators',
        'icon': '🤿',
        'camp_name': 'Camp 4 High Camp (7,900m)',
        'objective': 'Calibrate high-pressure oxygen valves and life-support masks at 7,900m.',
        'game_type': 'precision',
        'instruction': 'Tap LOCK VALVE when the oxygen pressure needle enters the target green zone!',
        'reward_desc': 'High-pressure oxygen system online! Ready for the Hillary Step.',
        'bonus_shield': 1,
        'bonus_coins': 200
    },
    30: {
        'title': 'The Hillary Step & Plant Summit Flag',
        'icon': '👑',
        'camp_name': 'Mount Everest Summit (8,848m)',
        'objective': 'Scale the 12-meter vertical rock step and plant the Quizmondo flag on the summit!',
        'game_type': 'summit_sprint',
        'instruction': 'Final summit sprint! Stand atop the roof of the world at 8,848m!',
        'reward_desc': 'Mount Everest Conquered! Master mountaineer status unlocked!',
        'bonus_shield': 0,
        'bonus_coins': 1500
    }
}


def _calc_day_meta(day_num):
    """Compute stage, altitude, and rewards for any day (1 to 30) of the expedition."""
    day = max(1, min(30, int(day_num)))
    stage_idx = (day - 1) // 5
    stage_info = EXPEDITION_STAGES[stage_idx]
    step_in_stage = (day - 1) % 5 + 1

    if day == 30:
        alt = 8848
    else:
        span = stage_info['max_alt'] - stage_info['base_alt']
        alt = stage_info['base_alt'] + int((step_in_stage / 5.0) * span)

    is_camp_day = (day in CAMP_MISSIONS)
    mission = CAMP_MISSIONS.get(day)

    return {
        'day': day,
        'stage_number': stage_info['stage'],
        'stage_name': stage_info['name'],
        'safe_haven': stage_info['safe_haven'],
        'altitude': alt,
        'coins': stage_info['coins_per_step'],
        'diff': stage_info['diff'],
        'clue': stage_info['clue'],
        'icon': stage_info['icon'],
        'is_stage_gate': (step_in_stage == 5),
        'is_camp_day': is_camp_day,
        'camp_mission': mission,
        # A camp is somewhere you ARRIVE, at the end of its five days -- not
        # somewhere you already are. Every day of a stage used to announce the
        # stage's camp, so finishing day 1 told you that you were "safely at
        # Pine Valley Basecamp", which is where the expedition starts from.
        # camp_secured is the camp you have actually reached, and only on the
        # day you reach it; next_camp is the one you are still climbing to.
        'camp_secured': (stage_info['safe_haven'] if is_camp_day else None),
        'next_camp': stage_info['safe_haven'],
        'step_in_stage': step_in_stage,
    }


def _day_arrival(day_meta):
    """How to describe where a finished day leaves you.

    Reaching a camp happens on the last day of its stage. On the other four
    you have gained height and the camp is still above you, so saying you are
    "safely at" it is both wrong and deflating -- the first day of the whole
    expedition used to announce that you had arrived at the basecamp you set
    off from.
    """
    alt = '{:,}m'.format(day_meta['altitude'])
    if day_meta.get('camp_secured'):
        return {
            'where': day_meta['camp_secured'],
            'headline': 'Secured %s' % day_meta['camp_secured'],
            'detail': 'Camp secured at %s.' % alt,
        }
    return {
        'where': alt,
        'headline': 'Climbed to %s' % alt,
        'detail': '%s is still above you -- %s to go.' % (
            day_meta['next_camp'], '{:,}m'.format(
                max(0, _stage_top(day_meta) - day_meta['altitude']))),
    }


def _stage_top(day_meta):
    """The altitude of the camp this stage ends at."""
    for st in EXPEDITION_STAGES:
        if st['stage'] == day_meta['stage_number']:
            return st['max_alt']
    return day_meta['altitude']


def get_or_create_climber_season():
    """Retrieve or create the active month's expedition season."""
    month_key = datetime.utcnow().strftime('%Y-%m')
    season = ClimberSeason.query.filter_by(month_key=month_key, is_active=True).first()
    if not season:
        sponsor_post = Post.query.filter_by(status='publish').first()
        article_slug = sponsor_post.slug if sponsor_post else ''

        season = ClimberSeason(
            month_key=month_key,
            title='Everest 30-Day Expedition',
            mountain_name='Mount Everest',
            elevation_m=8848,
            sponsor_name='Alpine Dynamics & Mountain Gear',
            sponsor_url='/posts/' + article_slug if article_slug else '/posts',
            sponsor_article_slug=article_slug,
            starts_at=datetime.utcnow(),
            is_active=True
        )
        db.session.add(season)
        db.session.commit()
    return season


def _roll_climber_day(progress):
    """Move the expedition on to the next day once the 24-hour lock expires.

    Finishing a day set is_day_completed, banked the coins and stamped
    last_climbed_date, and the answer endpoint even worked out next_day_num to
    tell the browser about -- but nothing ever wrote current_day back. So the
    climb stayed on day 1 for good: while the lock held you were told to come
    back tomorrow, and when it lifted the day was still flagged complete, so
    no question was picked and the same day sat there finished. That is the
    "keeps restarting at day 1, no progress saved" everyone was seeing.

    One day per visit, not one per day elapsed: missing a week should not skip
    a week of the mountain.
    """
    if not progress.is_day_completed:
        return False
    today = datetime.utcnow().date()
    if progress.last_climbed_date and progress.last_climbed_date >= today:
        return False  # still locked for today
    if (progress.current_day or 1) >= 30:
        return False  # summited; the expedition stands finished

    progress.current_day = (progress.current_day or 1) + 1
    progress.current_step = progress.current_day
    meta = _calc_day_meta(progress.current_day)
    progress.current_stage = meta['stage_number']
    progress.day_questions_total = 1 if meta.get('is_camp_day') else 5
    progress.day_question_index = 1
    progress.is_day_completed = False
    progress.status = 'climbing'
    return True


def get_or_create_climber_progress(player_id, season_id):
    """Retrieve or initialize player climb progress for active season."""
    progress = ClimberProgress.query.filter_by(
        player_profile_id=player_id,
        season_id=season_id
    ).first()

    if not progress:
        day_meta = _calc_day_meta(1)
        total_q = 1 if day_meta.get('is_camp_day') else 5
        progress = ClimberProgress(
            player_profile_id=player_id,
            season_id=season_id,
            current_stage=1,
            current_day=1,
            current_step=1,
            day_question_index=1,
            day_questions_total=total_q,
            is_day_completed=False,
            secured_camp_stage=1,
            altitude_m=1000,
            banked_coins=0,
            unbanked_coins=0,
            highest_altitude=1000,
            status='climbing'
        )
        db.session.add(progress)
        db.session.commit()
    else:
        # Roll the day on first, so the repairs below work on the day the
        # climber is actually starting rather than the one they finished.
        changed = _roll_climber_day(progress)
        day_meta = _calc_day_meta(progress.current_day or 1)
        expected_total = 1 if day_meta.get('is_camp_day') else 5
        if progress.day_questions_total != expected_total:
            progress.day_questions_total = expected_total
            changed = True
        if not progress.day_question_index or progress.day_question_index <= 0:
            progress.day_question_index = 1
            changed = True
        if progress.is_day_completed is None:
            progress.is_day_completed = False
            changed = True
        if not progress.current_day or progress.current_day < 1:
            progress.current_day = 1
            changed = True
        if changed:
            db.session.commit()
    return progress


def _get_unseen_climber_fact(player_id, stage_number):
    """Retrieve an unseen historical or mountaineering fact for this player from DB."""
    seen_ids = [row[0] for row in db.session.query(UserClimberFactSeen.fact_id).filter_by(player_profile_id=player_id).all()]
    query = ClimberFact.query.filter_by(stage_number=stage_number)
    if seen_ids:
        query = query.filter(~ClimberFact.id.in_(seen_ids))
    fact = query.order_by(func.random()).first()

    if not fact:
        query_all = ClimberFact.query
        if seen_ids:
            query_all = query_all.filter(~ClimberFact.id.in_(seen_ids))
        fact = query_all.order_by(func.random()).first()

    if not fact:
        fact = ClimberFact.query.order_by(func.random()).first()

    if fact:
        already = UserClimberFactSeen.query.filter_by(player_profile_id=player_id, fact_id=fact.id).first()
        if not already:
            db.session.add(UserClimberFactSeen(player_profile_id=player_id, fact_id=fact.id))
            db.session.commit()

    return fact


def _pick_climber_question(diff='easy', exclude_id=None):
    """Select a playable question for the current altitude tier."""
    query = QuizQuestion.query.filter(QuizQuestion.status == 'approved')
    if diff:
        query = query.filter_by(difficulty=diff)
    if exclude_id:
        query = query.filter(QuizQuestion.id != exclude_id)
    count = query.count()
    if count == 0:
        return QuizQuestion.query.filter(QuizQuestion.status == 'approved').first()
    return query.offset(random.randint(0, count - 1)).first()


@arena_bp.route('/climber/reset', methods=['POST'])
def climber_reset():
    """Start the expedition again from Day 1.

    POST only, deliberately. It used to answer GET as well, so merely
    fetching the URL threw away a player's progress -- a prefetch, a
    restored tab or a link someone shared was enough, with nothing to
    confirm and no way back. A real player lost a part-finished expedition
    to exactly that.
    """
    player = get_current_player(persist=True)
    season = get_or_create_climber_season()
    progress = get_or_create_climber_progress(player.id, season.id)

    progress.current_day = 1
    progress.current_step = 1
    progress.current_stage = 1
    progress.day_question_index = 1
    progress.day_questions_total = 5
    progress.is_day_completed = False
    progress.altitude_m = 1000
    progress.highest_altitude = 1000
    progress.unbanked_coins = 0
    progress.last_climbed_date = None
    progress.status = 'climbing'
    db.session.commit()
    flash("Climber challenge reset to Day 1! Ready for your 60-second speed sprint.", "success")
    return redirect(url_for('arena.climber'))


@arena_bp.route('/climber')
def climber():
    """The Quiz Climber: 30-Day Everest Expedition Screen."""
    gate = needs_account_to_play('tackle The Quiz Climber expedition')
    if gate:
        return gate
    player = get_current_player(persist=True)
    season = get_or_create_climber_season()
    progress = get_or_create_climber_progress(player.id, season.id)

    day_meta = _calc_day_meta(progress.current_day)

    # Check 24-hour calendar lock
    today_date = datetime.utcnow().date()
    is_locked_for_today = bool(progress.is_day_completed and progress.last_climbed_date and progress.last_climbed_date >= today_date)

    # Calculate seconds until midnight UTC
    now_utc = datetime.utcnow()
    midnight_utc = (now_utc + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_until_midnight = int((midnight_utc - now_utc).total_seconds())

    question = None
    if not progress.is_day_completed and not day_meta.get('is_camp_day'):
        question = _pick_climber_question(diff=day_meta['diff'])

    fact = _get_unseen_climber_fact(player.id, day_meta['stage_number'])

    return render_template(
        'themes/quizhub/arena_climber.html',
        player=player,
        season=season,
        progress=progress,
        day_meta=day_meta,
        expedition_stages=EXPEDITION_STAGES,
        question=question,
        mountain_fact=fact,
        is_locked_for_today=is_locked_for_today,
        seconds_until_midnight=seconds_until_midnight
    )


@arena_bp.route('/climber/answer', methods=['POST'])
def climber_answer():
    """Validate answer on the rock wall: climb higher, use shield, or fall to Camp Safe Haven."""
    if not session.get('user_id'):
        return jsonify({
            'success': False,
            'error': 'You must be logged in to climb.',
            'login_required': True,
            'redirect': url_for('arena.player_register', next=url_for('arena.climber'))
        }), 401
    player = get_current_player(persist=True)
    if not player:
        return jsonify({'success': False, 'error': 'Player profile not found. Please refresh.'}), 401
    season = get_or_create_climber_season()
    progress = get_or_create_climber_progress(player.id, season.id)

    if progress.is_day_completed:
        return jsonify({
            'success': False,
            'error': 'Today\'s expedition is already complete! The next mountain stage opens tomorrow at midnight.',
            'day_completed': True,
            'current_day': progress.current_day
        }), 400

    data = request.get_json() or {}
    question_id = data.get('question_id')
    selected = data.get('selected')
    seconds_left = max(0, min(60, int(data.get('seconds_left') or 0)))

    question = db.session.get(QuizQuestion, question_id)
    if not question:
        return jsonify({'success': False, 'error': 'Question not found'}), 404

    is_correct = (str(selected).strip().upper() == str(question.correct_option).strip().upper())
    day_meta = _calc_day_meta(progress.current_day)
    total_q = progress.day_questions_total or 5
    curr_idx = progress.day_question_index or 1

    if is_correct:
        coins_per_q = day_meta['coins'] // total_q
        if curr_idx >= total_q:
            coins_awarded_this_q = day_meta['coins'] - (coins_per_q * (total_q - 1))
        else:
            coins_awarded_this_q = coins_per_q

        progress.unbanked_coins += coins_awarded_this_q

        if curr_idx < total_q:
            # Advance to next question in this day
            progress.day_question_index = curr_idx + 1
            progress.is_day_completed = False
            progress.status = 'climbing'
            db.session.commit()

            next_q = _pick_climber_question(diff=day_meta['diff'], exclude_id=question.id)
            next_q_data = None
            if next_q:
                next_q_data = {
                    'id': next_q.id,
                    'prompt': next_q.prompt,
                    'media_url': next_q.media_url or '',
                    'options': next_q.get_options(),
                    'difficulty': next_q.difficulty
                }

            return jsonify({
                'success': True,
                'correct': True,
                'day_completed': False,
                'summit': False,
                'current_day': progress.current_day,
                'day_question_index': progress.day_question_index,
                'day_questions_total': progress.day_questions_total,
                'coins_gained': coins_awarded_this_q,
                'unbanked_coins': progress.unbanked_coins,
                'current_altitude': progress.altitude_m,
                'day_meta': day_meta,
                'next_question': next_q_data,
                'explanation': question.explanation or 'Checkpoint cleared! Advance to the next question for today.'
            })
        else:
            # ALL 5 QUESTIONS COMPLETED!
            speed_bonus = seconds_left
            if speed_bonus > 0:
                progress.unbanked_coins += speed_bonus

            # AUTOMATICALLY SECURE ALL EARNED COINS INTO PERMANENT WALLET!
            coins_won_today = progress.unbanked_coins
            if coins_won_today > 0:
                player.coins = (player.coins or 0) + coins_won_today
                progress.banked_coins = (progress.banked_coins or 0) + coins_won_today
                progress.unbanked_coins = 0

            progress.is_day_completed = True
            progress.altitude_m = day_meta['altitude']
            progress.highest_altitude = max(progress.highest_altitude, progress.altitude_m)
            progress.last_climbed_date = datetime.utcnow().date()

            if progress.current_day >= 30:
                progress.altitude_m = 8848
                progress.status = 'summit'
                progress.total_summits += 1
                progress.highest_altitude = 8848

                summit_bonus = 1500
                total_awarded = coins_won_today + summit_bonus
                player.coins = (player.coins or 0) + summit_bonus
                progress.banked_coins = (progress.banked_coins or 0) + summit_bonus
                db.session.commit()

                return jsonify({
                    'success': True,
                    'correct': True,
                    'day_completed': True,
                    'summit': True,
                    'current_day': 30,
                    'day_question_index': total_q,
                    'day_questions_total': total_q,
                    'new_altitude': 8848,
                    'coins_gained': coins_awarded_this_q,
                    'speed_bonus': speed_bonus,
                    'coins_won_today': total_awarded,
                    'coins_awarded': total_awarded,
                    'wallet_coins': player.coins,
                    'safe_haven': 'Everest Summit (8,848m)',
                    'explanation': 'Safely reached the Summit of Mount Everest at 8,848m! All coins secured to your wallet!'
                })

            if day_meta['is_stage_gate']:
                progress.secured_camp_stage = min(6, day_meta['stage_number'] + 1)

            progress.status = 'day_completed'
            db.session.commit()

            next_day_num = progress.current_day + 1
            next_day_meta = _calc_day_meta(next_day_num)

            return jsonify({
                'success': True,
                'correct': True,
                'day_completed': True,
                'summit': False,
                'current_day': progress.current_day,
                'next_day': next_day_num,
                'day_question_index': total_q,
                'day_questions_total': total_q,
                'coins_gained': coins_awarded_this_q,
                'speed_bonus': speed_bonus,
                'coins_won_today': coins_won_today,
                'unbanked_coins': 0,
                'wallet_coins': player.coins,
                'new_altitude': progress.altitude_m,
                'secured_camp_stage': progress.secured_camp_stage,
                'day_meta': day_meta,
                'next_day_meta': next_day_meta,
                'safe_haven': _day_arrival(day_meta)['where'],
                'arrival': _day_arrival(day_meta),
                'explanation': f"{_day_arrival(day_meta)['headline']}. +{coins_won_today} 🪙 secured to your wallet."
            })

    else:
        # INCORRECT ANSWER: advance to next question of 5 without adding coins
        lost_coins = 0
        shield_saved = False
        if (player.climber_shields or 0) > 0:
            player.climber_shields -= 1
            shield_saved = True
            db.session.commit()
        else:
            lost_coins = progress.unbanked_coins
            progress.unbanked_coins = 0

        if curr_idx < total_q:
            # Advance to next question of 5
            progress.day_question_index = curr_idx + 1
            progress.is_day_completed = False
            progress.status = 'climbing'
            db.session.commit()

            next_q = _pick_climber_question(diff=day_meta['diff'], exclude_id=question.id)
            next_q_data = None
            if next_q:
                next_q_data = {
                    'id': next_q.id,
                    'prompt': next_q.prompt,
                    'media_url': next_q.media_url or '',
                    'options': next_q.get_options(),
                    'difficulty': next_q.difficulty
                }

            return jsonify({
                'success': True,
                'correct': False,
                'day_completed': False,
                'shield_saved': shield_saved,
                'shields_left': player.climber_shields or 0,
                'lost_coins': lost_coins,
                'current_day': progress.current_day,
                'day_question_index': progress.day_question_index,
                'day_questions_total': total_q,
                'unbanked_coins': progress.unbanked_coins,
                'current_altitude': progress.altitude_m,
                'correct_answer': question.correct_option,
                'explanation': ('🛡️ Climber Shield absorbed the slip! ' if shield_saved else f'⚠️ Slip! Lost +{lost_coins} unbanked coins. ') + (question.explanation or f'Correct answer was ({question.correct_option}). Keep moving, clock is ticking!'),
                'next_question': next_q_data,
                'day_meta': day_meta
            })
        else:
            # ALL 5 QUESTIONS COMPLETED (even if 5th was incorrect)
            coins_won_today = progress.unbanked_coins
            if coins_won_today > 0:
                player.coins = (player.coins or 0) + coins_won_today
                progress.banked_coins = (progress.banked_coins or 0) + coins_won_today
                progress.unbanked_coins = 0

            progress.is_day_completed = True
            progress.altitude_m = day_meta['altitude']
            progress.highest_altitude = max(progress.highest_altitude, progress.altitude_m)
            progress.last_climbed_date = datetime.utcnow().date()
            progress.status = 'day_completed'
            db.session.commit()

            next_day_num = progress.current_day + 1
            next_day_meta = _calc_day_meta(next_day_num)

            return jsonify({
                'success': True,
                'correct': False,
                'day_completed': True,
                'summit': False,
                'shield_saved': shield_saved,
                'shields_left': player.climber_shields or 0,
                'lost_coins': lost_coins,
                'current_day': progress.current_day,
                'next_day': next_day_num,
                'day_question_index': total_q,
                'day_questions_total': total_q,
                'coins_won_today': coins_won_today,
                'unbanked_coins': 0,
                'wallet_coins': player.coins,
                'new_altitude': progress.altitude_m,
                'secured_camp_stage': progress.secured_camp_stage,
                'day_meta': day_meta,
                'next_day_meta': next_day_meta,
                'safe_haven': _day_arrival(day_meta)['where'],
                'arrival': _day_arrival(day_meta),
                'correct_answer': question.correct_option,
                'explanation': ('🛡️ Shield absorbed the slip! ' if shield_saved else '⚠️ Slip on the last hold! ') + f"{_day_arrival(day_meta)['headline']}."
            })


@arena_bp.route('/climber/camp_complete', methods=['POST'])
def climber_camp_complete():
    """Complete a Camp Safe Haven survival task (tent pitch, ladder link, rations, reflex check, oxygen)."""
    player = get_current_player(persist=True)
    if not player:
        return jsonify({'success': False, 'error': 'Player profile not found.'}), 401
    season = get_or_create_climber_season()
    progress = get_or_create_climber_progress(player.id, season.id)

    day_meta = _calc_day_meta(progress.current_day)
    if not day_meta.get('is_camp_day'):
        return jsonify({'success': False, 'error': 'Today is a climbing sprint day, not a camp day'}), 400

    if progress.is_day_completed:
        return jsonify({'success': False, 'error': 'Camp mission already completed for today!'}), 400

    mission = day_meta.get('camp_mission') or {}
    coins_gained = day_meta['coins'] + mission.get('bonus_coins', 0)
    progress.unbanked_coins += coins_gained

    bonus_shield = mission.get('bonus_shield', 0)
    if bonus_shield > 0:
        player.climber_shields = (player.climber_shields or 0) + bonus_shield

    # Auto-secure all coins on camp mission completion
    coins_won_today = progress.unbanked_coins
    if coins_won_today > 0:
        player.coins = (player.coins or 0) + coins_won_today
        progress.banked_coins = (progress.banked_coins or 0) + coins_won_today
        progress.unbanked_coins = 0

    progress.is_day_completed = True
    progress.altitude_m = day_meta['altitude']
    progress.highest_altitude = max(progress.highest_altitude, progress.altitude_m)
    progress.secured_camp_stage = min(6, day_meta['stage_number'] + 1)
    progress.last_climbed_date = datetime.utcnow().date()
    progress.status = 'day_completed'
    db.session.commit()

    next_day_num = progress.current_day + 1
    next_day_meta = _calc_day_meta(next_day_num) if next_day_num <= 30 else None

    return jsonify({
        'success': True,
        'mission_completed': True,
        'mission_title': mission.get('title'),
        'reward_desc': mission.get('reward_desc'),
        'coins_gained': coins_gained,
        'coins_won_today': coins_won_today,
        'unbanked_coins': 0,
        'wallet_coins': player.coins,
        'bonus_shield': bonus_shield,
        'shields_total': player.climber_shields or 0,
        'altitude': progress.altitude_m,
        'secured_camp_stage': progress.secured_camp_stage,
        'current_day': progress.current_day,
        'next_day': next_day_num,
        'day_meta': day_meta,
        'next_day_meta': next_day_meta,
        'safe_haven': _day_arrival(day_meta)['where'],
        'arrival': _day_arrival(day_meta),
        'explanation': f"{_day_arrival(day_meta)['headline']}. +{coins_won_today} 🪙 safely banked in your wallet."
    })


@arena_bp.route('/climber/timeout', methods=['POST'])
def climber_timeout():
    """Handle 60-second blizzard time-out on rock wall: completes today's sprint."""
    player = get_current_player(persist=True)
    if not player:
        return jsonify({'success': False, 'error': 'Player profile not found.'}), 401
    season = get_or_create_climber_season()
    progress = get_or_create_climber_progress(player.id, season.id)

    day_meta = _calc_day_meta(progress.current_day)

    shield_saved = False
    lost_coins = 0
    if (player.climber_shields or 0) > 0:
        player.climber_shields -= 1
        shield_saved = True
        db.session.commit()
    else:
        lost_coins = progress.unbanked_coins
        progress.unbanked_coins = 0

    coins_won_today = progress.unbanked_coins
    if coins_won_today > 0:
        player.coins = (player.coins or 0) + coins_won_today
        progress.banked_coins = (progress.banked_coins or 0) + coins_won_today
        progress.unbanked_coins = 0

    progress.is_day_completed = True
    progress.last_climbed_date = datetime.utcnow().date()
    progress.status = 'day_completed'
    db.session.commit()

    next_day_num = progress.current_day + 1
    next_day_meta = _calc_day_meta(next_day_num)

    return jsonify({
        'success': True,
        'day_completed': True,
        'shield_saved': shield_saved,
        'shields_left': player.climber_shields or 0,
        'lost_coins': lost_coins,
        'current_day': progress.current_day,
        'next_day': next_day_num,
        'day_question_index': 5,
        'day_questions_total': 5,
        'coins_won_today': coins_won_today,
        'unbanked_coins': 0,
        'wallet_coins': player.coins,
        'new_altitude': progress.altitude_m,
        'secured_camp_stage': progress.secured_camp_stage,
        'day_meta': day_meta,
        'next_day_meta': next_day_meta,
        'safe_haven': _day_arrival(day_meta)['where'],
        'arrival': _day_arrival(day_meta),
        'explanation': ('🛡️ Climber Shield absorbed the frostbite! ' if shield_saved else '⚠️ Blizzard struck as the 60-second clock expired! ') + f"{_day_arrival(day_meta)['headline']}. Rest until tomorrow."
    })


@arena_bp.route('/climber/advance_day', methods=['POST'])
def climber_advance_day():
    """Advance the expedition to the next day after completing today's questions."""
    player = get_current_player(persist=True)
    if not player:
        return jsonify({'success': False, 'error': 'Player profile not found.'}), 401
    season = get_or_create_climber_season()
    progress = get_or_create_climber_progress(player.id, season.id)

    today_date = datetime.utcnow().date()
    data = request.get_json(silent=True) or {}
    is_admin = session.get('user_role') in ('admin', 'super_admin') or (player and player.user and player.user.role in ('admin', 'super_admin')) or current_app.config.get('TESTING')
    force_advance = request.args.get('force') == '1' or data.get('force') is True

    # 24-hour calendar day lock
    if progress.is_day_completed and progress.last_climbed_date and progress.last_climbed_date >= today_date:
        if not (is_admin and force_advance):
            return jsonify({
                'success': False,
                'error': 'Today\'s expedition is complete! The next mountain stage opens tomorrow at midnight.',
                'locked': True
            }), 400

    if not progress.is_day_completed and progress.current_day < 30:
        return jsonify({
            'success': False,
            'error': 'You must complete all questions or the camp survival mission for today before pushing forward!'
        }), 400

    if progress.current_day >= 30:
        return jsonify({
            'success': False,
            'error': 'Summit already achieved!'
        }), 400

    progress.current_day += 1
    progress.current_step = progress.current_day
    progress.day_question_index = 1
    
    day_meta = _calc_day_meta(progress.current_day)
    progress.day_questions_total = 1 if day_meta.get('is_camp_day') else 5
    progress.is_day_completed = False

    progress.altitude_m = day_meta['altitude']
    progress.current_stage = day_meta['stage_number']
    progress.highest_altitude = max(progress.highest_altitude, progress.altitude_m)
    progress.status = 'climbing'
    db.session.commit()

    next_q = None
    if not day_meta.get('is_camp_day'):
        next_q = _pick_climber_question(diff=day_meta['diff'])

    next_fact = _get_unseen_climber_fact(player.id, day_meta['stage_number'])

    next_q_data = None
    if next_q:
        next_q_data = {
            'id': next_q.id,
            'prompt': next_q.prompt,
            'media_url': next_q.media_url or '',
            'options': next_q.get_options(),
            'difficulty': next_q.difficulty
        }

    return jsonify({
        'success': True,
        'new_day': progress.current_day,
        'day_question_index': 1,
        'day_questions_total': progress.day_questions_total,
        'new_altitude': progress.altitude_m,
        'unbanked_coins': progress.unbanked_coins,
        'day_meta': day_meta,
        'next_question': next_q_data,
        'next_fact': {
            'title': next_fact.title if next_fact else '',
            'text': next_fact.fact_text if next_fact else '',
            'icon': next_fact.icon if next_fact else '⛰️'
        } if next_fact else None
    })


@arena_bp.route('/climber/bank', methods=['POST'])
def climber_bank():
    """Push-your-luck Safe Haven: Bank unbanked coins permanently into player wallet."""
    if not session.get('user_id'):
        return jsonify({
            'success': False,
            'error': 'You must be logged in to bank coins.',
            'login_required': True,
            'redirect': url_for('arena.player_register', next=url_for('arena.climber'))
        }), 401
    player = get_current_player(persist=True)
    if not player:
        return jsonify({'success': False, 'error': 'Player profile not found.'}), 401
    season = get_or_create_climber_season()
    progress = get_or_create_climber_progress(player.id, season.id)

    if progress.unbanked_coins <= 0:
        return jsonify({'success': False, 'error': 'No unbanked coins to secure'}), 400

    amount = progress.unbanked_coins
    player.coins = (player.coins or 0) + amount
    progress.banked_coins += amount
    progress.unbanked_coins = 0
    db.session.commit()

    return jsonify({
        'success': True,
        'banked_amount': amount,
        'wallet_coins': player.coins,
        'unbanked_coins': 0,
        'altitude': progress.altitude_m,
        'day': progress.current_day
    })


@arena_bp.route('/climber/restart', methods=['POST'])
def climber_restart():
    """Start fresh from current Camp Safe Haven."""
    if not session.get('user_id'):
        return jsonify({
            'success': False,
            'error': 'You must be logged in to restart climb.',
            'login_required': True,
            'redirect': url_for('arena.player_register', next=url_for('arena.climber'))
        }), 401
    player = get_current_player(persist=True)
    if not player:
        return jsonify({'success': False, 'error': 'Player profile not found.'}), 401
    season = get_or_create_climber_season()
    progress = get_or_create_climber_progress(player.id, season.id)

    camp_day = (progress.secured_camp_stage - 1) * 5 + 1
    progress.current_day = camp_day
    progress.current_step = camp_day
    progress.day_question_index = 1
    camp_meta = _calc_day_meta(camp_day)
    progress.day_questions_total = 1 if camp_meta.get('is_camp_day') else 5
    progress.is_day_completed = False
    progress.unbanked_coins = 0
    progress.altitude_m = camp_meta['altitude']
    progress.status = 'climbing'
    db.session.commit()

    next_q = None
    if not camp_meta.get('is_camp_day'):
        next_q = _pick_climber_question(diff=camp_meta['diff'])

    next_q_data = None
    if next_q:
        next_q_data = {
            'id': next_q.id,
            'prompt': next_q.prompt,
            'media_url': next_q.media_url or '',
            'options': next_q.get_options(),
            'difficulty': next_q.difficulty
        }

    return jsonify({
        'success': True,
        'day': camp_day,
        'altitude': progress.altitude_m,
        'day_meta': camp_meta,
        'next_question': next_q_data
    })
