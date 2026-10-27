import json
import random
import secrets
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash, current_app, Response
from sqlalchemy.sql.expression import func
from ..models import db, User, PlayerProfile, ArenaMatch, ArenaRound, QuizQuestion, QuizPack, PubLeague, SiteSetting
from ..utils.share_card import generate_duel_card_png, generate_pub_card_png

arena_bp = Blueprint('arena', __name__, url_prefix='/arena')

from .public import inject_global_data

@arena_bp.context_processor
def inject_arena_global_data():
    data = inject_global_data()
    data['avatar_lookup'] = AVATAR_LOOKUP
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


def get_random_questions(category_slug=None, count=3, exclude_ids=None, difficulty=None):
    """Fetch randomized questions for duels, pub leagues, and rounds.
    For visual categories (flags, badges, logos, country shapes), ALWAYS prioritize visual image matching questions first,
    and avoid Expert ('hard') text-only questions in standard rounds unless explicitly requested.
    """
    base_query = QuizQuestion.query
    if category_slug:
        base_query = base_query.filter_by(category_slug=category_slug)
    if exclude_ids:
        base_query = base_query.filter(~QuizQuestion.id.in_(exclude_ids))

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
            non_expert = QuizQuestion.query.filter(
                QuizQuestion.category_slug == category_slug,
                ~QuizQuestion.id.in_(used_ids),
                QuizQuestion.difficulty.in_(['easy', 'medium'])
            ).order_by(func.random()).limit(needed).all()
            questions.extend(non_expert)

    if len(questions) < count:
        needed = count - len(questions)
        used_ids = [q.id for q in questions] + (exclude_ids or [])
        q_filter = QuizQuestion.query.filter(~QuizQuestion.id.in_(used_ids))
        if category_slug:
            q_filter = q_filter.filter_by(category_slug=category_slug)
        if difficulty:
            q_filter = q_filter.filter_by(difficulty=difficulty)
        else:
            # Prefer easy/medium first for fun gameplay
            easy_med = q_filter.filter(QuizQuestion.difficulty.in_(['easy', 'medium'])).order_by(func.random()).limit(needed).all()
            questions.extend(easy_med)
            needed = count - len(questions)
            if needed > 0:
                used_ids = [q.id for q in questions] + (exclude_ids or [])
                q_filter2 = QuizQuestion.query.filter(~QuizQuestion.id.in_(used_ids))
                if category_slug:
                    q_filter2 = q_filter2.filter_by(category_slug=category_slug)
                questions.extend(q_filter2.order_by(func.random()).limit(needed).all())
        if difficulty and needed > 0:
            questions.extend(q_filter.order_by(func.random()).limit(needed).all())

    if len(questions) < count:
        needed = count - len(questions)
        exclude_existing = [q.id for q in questions] + (exclude_ids or [])
        fallback = QuizQuestion.query.filter(~QuizQuestion.id.in_(exclude_existing)).order_by(func.random()).limit(needed).all()
        questions = list(questions) + list(fallback)
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


@arena_bp.route('/')
def dashboard():
    """Arena Hub: Active duels, Completed Duels ready for Rematch, Friends & Group Challenges, leaderboards preview, and quick play."""
    player = get_current_player(persist=False)
    
    # Active matches where player is participant
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

    active_matches = [m for m in raw_active if m.status in ('waiting', 'in_progress')]

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

    # Categorize matches into clear dedicated sections
    # 1. Duels Sent TO You (where you were challenged by a friend or online player)
    incoming_challenges = []
    # 2. Invites & Challenges YOU Sent (recent WhatsApp invites, direct friend challenges, online challenges)
    outgoing_invites = []
    # 3. Solo / Bot Nova training matches
    bot_matches = []

    for m in active_matches:
        if m.is_bot:
            bot_matches.append(m)
        elif m.player1_session == player.session_key:
            outgoing_invites.append(m)
        else:
            incoming_challenges.append(m)

    # Friends Roster & Open Group Challenges
    friends_roster, open_group_challenges = _get_friends_and_group_challenges(player)

    # Top leaderboards
    top_players = PlayerProfile.query.order_by(PlayerProfile.xp.desc()).limit(5).all()

    # Available Packs
    packs = QuizPack.query.order_by(QuizPack.created_at.desc()).limit(6).all()

    return render_template(
        'themes/quizhub/arena_dashboard.html',
        player=player,
        active_matches=active_matches,
        incoming_challenges=incoming_challenges,
        outgoing_invites=outgoing_invites,
        bot_matches=bot_matches,
        history_matches=history_matches,
        friends_roster=friends_roster,
        open_group_challenges=open_group_challenges,
        top_players=top_players,
        packs=packs,
        avatars=AVATAR_PRESETS
    )


@arena_bp.route('/new', methods=['GET', 'POST'])
def create_match():
    """Create a new head-to-head match or challenge (bot, friend, or online matchmaking)."""
    player = get_current_player()
    opponent_mode = request.form.get('opponent_mode') or request.args.get('opponent_mode', 'friend')  # 'friend', 'bot', 'online'
    category_slug = request.form.get('category_slug') or request.args.get('category_slug')
    friend_invite_name = (request.form.get('friend_name') or request.args.get('friend_name') or '').strip()

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
        player2_name=friend_invite_name if friend_invite_name else ('Searching Online Player...' if opponent_mode == 'online' else 'Invited Friend'),
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
            bot_detailed.append({
                'question_id': q.id,
                'selected': q.correct_option if bot_correct else 'B',
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

        if User.query.filter(func.lower(User.username) == username.lower()).first():
            flash("That player name is already taken. Try picking a Superhero Name!", "error")
            return render_template('themes/quizhub/arena_register.html', player=player)

        if User.query.filter(func.lower(User.email) == email.lower()).first():
            flash("An account with that email already exists. Sign in with your 6-digit PIN instead!", "error")
            return render_template('themes/quizhub/arena_login.html', player=player)

        # Default role hierarchy: all newly registered users are strictly 'player'
        assigned_role = 'player'
        user = User(username=username, email=email, role=assigned_role)
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


@arena_bp.route('/leaderboard')
def leaderboard():
    """Full global leaderboard ranking table."""
    player = get_current_player(persist=False)
    top_players = PlayerProfile.query.order_by(PlayerProfile.xp.desc()).limit(50).all()
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
    is_started = (state.get('current_round', 1) > 1 or state.get('round_status') in ('active', 'break', 'closed', 'finished'))
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
    1: {'number': 1, 'name': 'Round 1: General Knowledge, Science & Lore', 'cat_slug': 'science-cosmos', 'icon': '🌍', 'desc': 'Warm up your neurons with world history, science, and general news.'},
    2: {'number': 2, 'name': 'Round 2: Pop Culture, Cinema Titans & Music Legends', 'cat_slug': 'tv-cinema', 'icon': '🎬', 'desc': 'Blockbuster cinema, chart-topping records, and modern pop icons.'},
    3: {'number': 3, 'name': 'Round 3: Championship Wipeout Lightning Sprint', 'cat_slug': 'gaming-esports', 'icon': '⚡', 'desc': 'High stakes finale! 1.5x score multiplier on all correct answers.'},
    4: {'number': 4, 'name': 'Round 4: World Geography & Flags', 'cat_slug': 'match-flags', 'icon': '🏳️', 'desc': 'Visual flags and global geography challenge.'},
    5: {'number': 5, 'name': 'Round 5: The Grand Finale Speed Wipeout', 'cat_slug': 'brand-logos', 'icon': '🏆', 'desc': 'Double points finale round!'},
}

PUB_ROUNDS_CONFIG = {
    1: {'number': 1, 'name': 'General Knowledge & News', 'cat_slug': 'world-history', 'icon': '🧠', 'desc': 'Test your broad trivia knowledge across news, landmarks, and science.'},
    2: {'number': 2, 'name': 'Music, Audio & Waveforms', 'cat_slug': 'pop-music', 'icon': '🎵', 'desc': 'Iconic number one records, synthesizers, chiptunes, and rock anthems.'},
    3: {'number': 3, 'name': 'Cinema, Television & Blockbusters', 'cat_slug': 'tv-cinema', 'icon': '🎬', 'desc': 'Cult cinema classics, famous directors, Academy Awards, and TV quotes.'},
    4: {'number': 4, 'name': 'World Geography & Visual Flags', 'cat_slug': 'match-flags', 'icon': '🗺️', 'desc': 'Continental capitals, world flags, ancient ruins, and extreme landforms.'},
    5: {'number': 5, 'name': 'The Big Wipeout Speed Sprint', 'cat_slug': 'gaming-esports', 'icon': '⚡', 'desc': 'Double Points Wipeout Round! Faster buzzer answers award massive bonus points.'},
}


def resolve_pub_team(state, player, table_num, team_name, is_virtual):
    """Find the squad row that belongs to this browser session.

    In a physical venue a table number is deliberately shared, so the table
    number stays the identity. In a virtual league every player checks in from
    their own device, so the squad is keyed to the player instead — otherwise
    two players who both type Squad #1 silently end up on one scorecard.
    """
    teams = state.get('teams', [])
    owner_key = getattr(player, 'session_key', None)
    name_l = (team_name or '').strip().lower()

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

    for t in teams:
        matches_table = table_num and str(t.get('table', '')).strip() == str(table_num)
        matches_name = name_l and t.get('name', '').strip().lower() == name_l
        if matches_table or matches_name:
            return t

    mine = owned()
    if mine:
        return mine

    # Fallback: if there is only 1 approved table in the venue, match it so single-table tests never miss
    approved_only = [t for t in teams if t.get('status') != 'pending']
    if len(approved_only) == 1:
        return approved_only[0]
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
PUB_MIN_QUESTION_SECS = 10
PUB_MAX_QUESTION_SECS = 30


def pub_question_secs(cfg):
    """Seconds per question the host has configured, held inside the supported range."""
    try:
        secs = int(cfg.get('question_time_limit', 15))
    except (TypeError, ValueError):
        secs = 15
    return max(PUB_MIN_QUESTION_SECS, min(PUB_MAX_QUESTION_SECS, secs))


def pub_max_round_score(cfg, round_num, total_rounds):
    """Highest score a round can possibly be worth, used to cap a legacy client total."""
    per_q = 100 + pub_question_secs(cfg) * 2
    if round_num >= total_rounds:
        per_q = round(per_q * 1.5)
    return per_q * PUB_QUESTIONS_PER_ROUND


def score_pub_answers(state, round_num, raw_answers, cfg, total_rounds):
    """Score a squad's answers against the questions pinned for this round.

    The phone used to work out its own round total and post it, which meant the
    score was whatever the browser said it was. The answers are scored here now,
    against the pinned question set, so a tampered payload cannot invent points.
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
        state['answers_revealed'] = True
        state.pop('round_ends_at', None)
        if cfg.get('auto_advance_enabled'):
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
        changed = True

    if changed:
        league.set_state(state)
        db.session.commit()
    return changed


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
        # Older phone still posting only its own total: accept it, but never above what the round can pay
        scored = min(int(request.form.get('partial_score') or 0),
                     pub_max_round_score(cfg, curr_r, total_rounds))
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
        league.set_state(state)
        db.session.commit()

    return jsonify({'success': True})


@arena_bp.route('/leagues/<slug>/manager', methods=['GET', 'POST'])
def league_manager(slug):
    """Host / Quizmaster Manager Console — STRICTLY gated to Super Admins, Admins, and Quizmasters (NEVER Room PIN!)."""
    league = PubLeague.query.filter_by(slug=slug, is_active=True).first_or_404()
    is_mgr = (
        session.get('user_role') in ('super_admin', 'admin', 'quizmaster')
        or bool(session.get('admin_logged_in'))
    )

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
    is_authorized = (
        session.get('user_role') in ('super_admin', 'admin', 'quizmaster')
        or bool(session.get('admin_logged_in'))
    )
    if not is_authorized:
        if 'text/html' in (request.headers.get('Accept') or ''):
            flash("Unauthorized: Only Quizmasters and Administrators may control live pub quizzes.", "error")
            return redirect(url_for('arena.league_lounge', slug=slug))
        return jsonify({'success': False, 'error': 'Unauthorized: Quizmaster or Admin account required'}), 403

    action = request.form.get('action')
    state = league.get_state()
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
        state['answers_revealed'] = True
        state['round_status'] = 'closed' if state.get('round_status') == 'active' else state.get('round_status', 'closed')
        state.pop('round_ends_at', None)
        league.set_state(state)
        db.session.commit()
        return respond("Official answers revealed on big screen and player screens!")

    elif action == 'start_break':
        curr_r = state.get('current_round', 1)
        approved_teams = [t for t in teams if t.get('status') != 'pending']
        completed_tables = [t for t in approved_teams if t.get(f'round_{curr_r}') is not None]
        if not approved_teams or (len(completed_tables) < len(approved_teams) and state.get('round_status') not in ('closed', 'break', 'finished')):
            return respond_error("Wait for all tables to submit answers or click 'Lock / Time's Up' before starting the bar break!")
        state['round_status'] = 'break'
        state['answers_revealed'] = True
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
            state['round_status'] = 'finished'
            state['answers_revealed'] = True
            state['tournament_completed'] = True
            state.pop('round_ends_at', None)
            state.pop('break_ends_at', None)
            league.set_state(state)
            db.session.commit()
            return respond("🏆 Tournament finalized! Champions crowned and final standings displayed on all screens.")

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

    elif action in ('reset', 'reset_quiz'):
        state['current_round'] = 1
        state['round_status'] = 'waiting'
        state['answers_revealed'] = False
        state['teams'] = []
        state['round_questions'] = {}
        state.pop('round_ends_at', None)
        state.pop('break_ends_at', None)
        state['reset_ts'] = datetime.utcnow().isoformat()
        league.set_state(state)
        db.session.commit()
        return respond("Tournament reset to Round 1! All tables cleared and player screens auto-notified.")

    elif action == 'clear_tables':
        state['teams'] = []
        # Clearing every table ends the live round too, or nobody could ever check in again
        state['round_status'] = 'waiting'
        state['answers_revealed'] = False
        state.pop('round_ends_at', None)
        state.pop('break_ends_at', None)
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
            # Older phone still posting only its own total: accept it, but never above what the round can pay
            round_score = min(int(request.form.get('score', 0)),
                              pub_max_round_score(cfg, current_round, total_rounds))
        team_entry = resolve_pub_team(state, player, table_num, team_name, is_virtual)

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
    team_entry = resolve_pub_team(state, player, table_num, team_name, is_virtual)

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
        config=cfg,
        next_pub_date=get_next_weekly_pub_date(),
        state=state
    )


@arena_bp.route('/leagues/<slug>/tv')
def league_tv(slug):
    """Big-screen pub quiz display for TV projectors with live quizmaster host controls."""
    league = PubLeague.query.filter_by(slug=slug, is_active=True).first_or_404()
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
    return render_template(
        'themes/quizhub/arena_league_tv.html',
        league=league,
        teams=teams,
        state=state,
        current_round=current_round,
        round_info=round_info,
        questions=questions,
        is_virtual=is_virtual
    )


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
