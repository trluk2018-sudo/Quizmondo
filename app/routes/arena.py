import json
import random
import secrets
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash, current_app
from ..models import db, User, PlayerProfile, ArenaMatch, ArenaRound, QuizQuestion, QuizPack, PubLeague, SiteSetting

arena_bp = Blueprint('arena', __name__, url_prefix='/arena')

from .public import inject_global_data

@arena_bp.context_processor
def inject_arena_global_data():
    return inject_global_data()

AVATAR_PRESETS = [
    {'key': 'quizzy', 'name': 'Quizzy', 'badge': 'Hyper Star', 'bg': 'from-purple-600 to-indigo-600', 'border': 'border-purple-400'},
    {'key': 'nova', 'name': 'Nova', 'badge': 'Cyber Explorer', 'bg': 'from-cyan-500 to-blue-600', 'border': 'border-cyan-400'},
    {'key': 'pixel', 'name': 'Pixel', 'badge': '8-Bit Bot', 'bg': 'from-emerald-500 to-teal-700', 'border': 'border-emerald-400'},
    {'key': 'sage', 'name': 'Sage', 'badge': 'Owl Scholar', 'bg': 'from-amber-500 to-orange-600', 'border': 'border-amber-400'},
]


def get_current_player():
    """Retrieve or initialize the active player profile using session cookie."""
    player_key = session.get('qm_player_key')
    profile = None
    if player_key:
        profile = PlayerProfile.query.filter_by(session_key=player_key).first()

    if not profile:
        new_key = secrets.token_urlsafe(16)
        session['qm_player_key'] = new_key
        rand_avatar = random.choice(AVATAR_PRESETS)['key']
        rand_name = f"Challenger_{random.randint(100, 999)}"
        profile = PlayerProfile(
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
        db.session.add(profile)
        db.session.commit()

    return profile


@arena_bp.route('/')
def dashboard():
    """Arena Hub: Active duels, leaderboards preview, daily sprint, and quick play."""
    player = get_current_player()
    
    # Active matches where player is participant
    active_matches = ArenaMatch.query.filter(
        (ArenaMatch.player1_session == player.session_key) | (ArenaMatch.player2_session == player.session_key),
        ArenaMatch.status.in_(['waiting', 'in_progress'])
    ).order_by(ArenaMatch.updated_at.desc()).all()

    # Finished matches
    history_matches = ArenaMatch.query.filter(
        (ArenaMatch.player1_session == player.session_key) | (ArenaMatch.player2_session == player.session_key),
        ArenaMatch.status.in_(['completed', 'forfeited'])
    ).order_by(ArenaMatch.updated_at.desc()).limit(8).all()

    # Top leaderboards
    top_players = PlayerProfile.query.order_by(PlayerProfile.xp.desc()).limit(5).all()

    # Available Packs
    packs = QuizPack.query.order_by(QuizPack.created_at.desc()).limit(6).all()

    return render_template(
        'themes/quizhub/arena_dashboard.html',
        player=player,
        active_matches=active_matches,
        history_matches=history_matches,
        top_players=top_players,
        packs=packs,
        avatars=AVATAR_PRESETS
    )


@arena_bp.route('/new', methods=['POST'])
def create_match():
    """Create a new head-to-head match or challenge."""
    player = get_current_player()
    opponent_mode = request.form.get('opponent_mode', 'friend')  # 'friend', 'bot'
    category_slug = request.form.get('category_slug')

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

    # Pick 3 questions for Round 1
    questions = QuizQuestion.query.filter_by(category_slug=cat_slug).limit(3).all()
    if not questions:
        questions = QuizQuestion.query.limit(3).all()
    q_ids = [q.id for q in questions]

    match = ArenaMatch(
        match_code=match_code,
        player1_session=player.session_key,
        player1_name=player.display_name,
        player1_avatar=player.avatar_key,
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

    return redirect(url_for('arena.match_lobby', match_code=match_code))


@arena_bp.route('/match/<match_code>')
def match_lobby(match_code):
    """Lobby and scoreboard overview for a match."""
    player = get_current_player()
    match = ArenaMatch.query.filter_by(match_code=match_code).first_or_404()

    # If opening player is not Player 1 and Player 2 slot is open, claim Player 2!
    if match.player1_session != player.session_key and (not match.player2_session or match.player2_session.startswith('bot')):
        match.player2_session = player.session_key
        match.player2_name = player.display_name
        match.player2_avatar = player.avatar_key
        match.status = 'in_progress'
        db.session.commit()

    is_player1 = (match.player1_session == player.session_key)
    is_player2 = (match.player2_session == player.session_key)
    is_participant = is_player1 or is_player2

    # Check if current round requires player action
    active_round = match.rounds.filter_by(round_number=match.current_round).first()
    my_turn = False
    if match.status in ('waiting', 'in_progress'):
        if is_player1 and match.current_turn == 1:
            my_turn = True
        elif is_player2 and match.current_turn == 2:
            my_turn = True

    # WhatsApp share message
    base_url = current_app.config.get('APP_PUBLIC_URL', request.host_url.rstrip('/'))
    invite_url = f"{base_url}/arena/match/{match.match_code}"
    whatsapp_text = (
        f"🎮 Duel Challenge on Quizmondo! I challenge you to a trivia showdown. "
        f"Tap here to play your round: {invite_url}"
    )

    all_rounds = match.rounds.all()

    return render_template(
        'themes/quizhub/arena_match.html',
        match=match,
        player=player,
        is_player1=is_player1,
        is_player2=is_player2,
        is_participant=is_participant,
        active_round=active_round,
        my_turn=my_turn,
        all_rounds=all_rounds,
        invite_url=invite_url,
        whatsapp_text=whatsapp_text
    )


@arena_bp.route('/match/<match_code>/play')
def play_round(match_code):
    """Live interactive round play screen with timer and mascot reaction."""
    player = get_current_player()
    match = ArenaMatch.query.filter_by(match_code=match_code).first_or_404()

    is_player1 = (match.player1_session == player.session_key)
    is_player2 = (match.player2_session == player.session_key)
    if not (is_player1 or is_player2):
        flash("You are viewing as a spectator. Challenge a friend to start your own match!", "info")
        return redirect(url_for('arena.match_lobby', match_code=match_code))

    active_round = match.rounds.filter_by(round_number=match.current_round).first()
    if not active_round:
        flash("Round is not yet ready or match has ended.", "warning")
        return redirect(url_for('arena.match_lobby', match_code=match_code))

    # Fetch questions for this round
    q_ids = active_round.get_question_ids()
    questions = QuizQuestion.query.filter(QuizQuestion.id.in_(q_ids)).all()
    # Preserve ordering
    q_dict = {q.id: q for q in questions}
    ordered_questions = [q_dict[qid] for qid in q_ids if qid in q_dict]

    # Mask correct answers on client side initially
    client_questions = []
    for q in ordered_questions:
        client_questions.append({
            'id': q.id,
            'prompt': q.prompt,
            'question_type': q.question_type,
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
    """Receive player round responses, compute score, and transition turn."""
    player = get_current_player()
    match = ArenaMatch.query.filter_by(match_code=match_code).first_or_404()

    is_player1 = (match.player1_session == player.session_key)
    is_player2 = (match.player2_session == player.session_key)
    if not (is_player1 or is_player2):
        return jsonify({'error': 'Unauthorized participant'}), 403

    payload = request.get_json() or {}
    answers = payload.get('answers', [])  # list of { question_id, choice, time_left }

    active_round = match.rounds.filter_by(round_number=match.current_round).first()
    if not active_round:
        return jsonify({'error': 'Active round not found'}), 404

    q_ids = active_round.get_question_ids()
    questions = QuizQuestion.query.filter(QuizQuestion.id.in_(q_ids)).all()
    q_map = {q.id: q for q in questions}

    round_score = 0
    detailed_results = []

    for ans in answers:
        qid = ans.get('question_id')
        choice = (ans.get('choice') or '').strip().upper()
        time_left = max(0, int(ans.get('time_left', 0)))

        q = q_map.get(qid)
        if not q:
            continue

        is_correct = (choice == q.correct_option)
        points_awarded = 0
        if is_correct:
            # Base 100 points + speed bonus (e.g. 10 points per leftover second)
            speed_bonus = time_left * 5
            points_awarded = q.points + speed_bonus
            round_score += points_awarded

        detailed_results.append({
            'question_id': q.id,
            'prompt': q.prompt,
            'selected': choice,
            'correct_option': q.correct_option,
            'is_correct': is_correct,
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

    # Determine turn flip or round progression
    # If opponent is AI bot, simulate bot round!
    if match.player2_session == 'bot_quizmondo_ai' and is_player1:
        # Bot answers with 65% probability
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
        active_round.p2_score = bot_score
        active_round.p2_answers_json = json.dumps(bot_detailed)
        match.p2_total_score = (match.p2_total_score or 0) + bot_score
        active_round.status = 'completed'

    # Check if both have completed this round
    has_p1_done = bool(active_round.p1_answers_json and active_round.p1_answers_json != '[]')
    has_p2_done = bool(active_round.p2_answers_json and active_round.p2_answers_json != '[]')

    if has_p1_done and has_p2_done:
        active_round.status = 'completed'
        if match.current_round >= 6:
            # Match is finished!
            match.status = 'completed'
            if match.p1_total_score > match.p2_total_score:
                match.winner = 1
                player.matches_won = (player.matches_won or 0) + 1
            elif match.p2_total_score > match.p1_total_score:
                match.winner = 2
            else:
                match.winner = 0  # Tie
            player.matches_played = (player.matches_played or 0) + 1
        else:
            # Advance to next round!
            match.current_round += 1
            # Alternate chooser: Round 2 chosen by player 2, Round 3 by player 1, etc.
            next_turn = 2 if match.current_turn == 1 else 1
            match.current_turn = next_turn

            # Pick next round category and questions
            all_cats = db.session.query(QuizQuestion.category_slug, QuizQuestion.category_name).distinct().all()
            chosen_cat = random.choice(all_cats) if all_cats else ('general', 'General')
            next_q = QuizQuestion.query.filter_by(category_slug=chosen_cat[0]).limit(3).all()
            if not next_q:
                next_q = QuizQuestion.query.limit(3).all()

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
        # Flip turn to player 2
        match.current_turn = 2 if is_player1 else 1
        match.status = 'in_progress'

    db.session.commit()

    return jsonify({
        'success': True,
        'round_score': round_score,
        'detailed_results': detailed_results,
        'player_level': player.level,
        'player_xp': player.xp,
        'p1_total_score': match.p1_total_score,
        'p2_total_score': match.p2_total_score,
        'match_status': match.status,
        'next_round': match.current_round
    })


@arena_bp.route('/profile/update', methods=['POST'])
def update_profile():
    """Update active player avatar and display name."""
    player = get_current_player()
    new_name = (request.form.get('display_name') or '').strip()
    new_avatar = (request.form.get('avatar_key') or '').strip()

    if new_name:
        player.display_name = new_name[:40]
    if new_avatar in [a['key'] for a in AVATAR_PRESETS]:
        player.avatar_key = new_avatar

    db.session.commit()
    flash("Avatar & Profile updated successfully!", "success")
    return redirect(url_for('arena.dashboard'))


@arena_bp.route('/leaderboard')
def leaderboard():
    """Full global leaderboard ranking table."""
    player = get_current_player()
    top_players = PlayerProfile.query.order_by(PlayerProfile.xp.desc()).limit(50).all()
    return render_template(
        'themes/quizhub/arena_leaderboard.html',
        player=player,
        top_players=top_players
    )


@arena_bp.route('/leagues')
def leagues():
    """Virtual & Pub Quiz Leagues directory."""
    player = get_current_player()
    all_leagues = PubLeague.query.filter_by(is_active=True).order_by(PubLeague.created_at.desc()).all()
    return render_template(
        'themes/quizhub/arena_leagues.html',
        player=player,
        leagues=all_leagues
    )


@arena_bp.route('/api/daily')
def api_daily_questions():
    """Return database-backed daily brain sprint questions."""
    questions = QuizQuestion.query.order_by(QuizQuestion.id.asc()).limit(5).all()
    return jsonify({
        'success': True,
        'badge': 'DAILY BRAIN CHALLENGE • LIVE SPRINT',
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
    """Community Quiz and Trivia Pack Studio."""
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


@arena_bp.route('/packs')
def packs_directory():
    """Browse all Core and Community Trivia Packs."""
    player = get_current_player()
    all_packs = QuizPack.query.order_by(QuizPack.is_community.asc(), QuizPack.created_at.desc()).all()
    return render_template(
        'themes/quizhub/arena_packs.html',
        player=player,
        packs=all_packs
    )
