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
    return inject_global_data()

AVATAR_PRESETS = [
    {'key': 'quizzy', 'name': 'Quizzy', 'badge': 'Hyper Star', 'bg': 'from-purple-600 to-indigo-600', 'border': 'border-purple-400'},
    {'key': 'nova', 'name': 'Nova', 'badge': 'Cyber Explorer', 'bg': 'from-cyan-500 to-blue-600', 'border': 'border-cyan-400'},
    {'key': 'pixel', 'name': 'Pixel', 'badge': '8-Bit Bot', 'bg': 'from-emerald-500 to-teal-700', 'border': 'border-emerald-400'},
    {'key': 'sage', 'name': 'Sage', 'badge': 'Owl Scholar', 'bg': 'from-amber-500 to-orange-600', 'border': 'border-amber-400'},
]


def get_random_questions(category_slug=None, count=3, exclude_ids=None):
    """Fetch randomized questions for duels, pub leagues, and rounds."""
    query = QuizQuestion.query
    if category_slug:
        query = query.filter_by(category_slug=category_slug)
    if exclude_ids:
        query = query.filter(~QuizQuestion.id.in_(exclude_ids))

    questions = query.order_by(func.random()).limit(count).all()
    if len(questions) < count:
        needed = count - len(questions)
        exclude_existing = [q.id for q in questions] + (exclude_ids or [])
        fallback = QuizQuestion.query.filter(~QuizQuestion.id.in_(exclude_existing)).order_by(func.random()).limit(needed).all()
        questions = list(questions) + list(fallback)
    return questions


def get_current_player():
    """Retrieve or initialize the active player profile using session cookie or user_id."""
    user_id = session.get('user_id')
    profile = None
    if user_id:
        profile = PlayerProfile.query.filter_by(user_id=user_id).first()
        if profile:
            session['qm_player_key'] = profile.session_key
            return profile

    player_key = session.get('qm_player_key')
    if player_key:
        profile = PlayerProfile.query.filter_by(session_key=player_key).first()

    if not profile:
        new_key = secrets.token_urlsafe(16)
        session['qm_player_key'] = new_key
        rand_avatar = random.choice(AVATAR_PRESETS)['key']
        rand_name = f"Challenger_{random.randint(100, 999)}"
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
        db.session.add(profile)
        db.session.commit()
    elif user_id and not profile.user_id:
        profile.user_id = user_id
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


@arena_bp.route('/new', methods=['GET', 'POST'])
def create_match():
    """Create a new head-to-head match or challenge."""
    player = get_current_player()
    opponent_mode = request.form.get('opponent_mode') or request.args.get('opponent_mode', 'friend')  # 'friend', 'bot'
    category_slug = request.form.get('category_slug') or request.args.get('category_slug')

    # Challenging a real person requires creating a free account
    if opponent_mode != 'bot' and not session.get('user_id'):
        flash("Create a free player account to challenge friends on WhatsApp, track lifetime head-to-head records, and compete on leaderboards!", "info")
        return redirect(url_for('arena.player_register', next=url_for('arena.dashboard')))

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

    # If opening player is not Player 1 and Player 2 slot is open (not bot), AND match is still on Round 1:
    if match.player1_session != player.session_key and (not match.player2_session or match.player2_session in ('pending_invite', '')) and match.current_round == 1:
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
    if is_participant and match.status in ('waiting', 'in_progress'):
        if is_player1 and match.current_turn == 1:
            my_turn = True
        elif is_player2 and match.current_turn == 2:
            my_turn = True

    # Identify opponent for specific nudge vs new friend challenge
    opponent_name = match.player2_name if is_player1 else match.player1_name
    opponent_assigned = bool(match.player2_session and match.player2_session not in ('pending_invite', ''))

    # WhatsApp share & nudge messages point DIRECTLY into the playable round
    base_url = current_app.config.get('APP_PUBLIC_URL', request.host_url.rstrip('/'))
    play_url = f"{base_url}/arena/match/{match.match_code}/play"
    invite_url = play_url
    active_cat = active_round.category_name if active_round else "General Trivia"
    target_nudgee = opponent_name if (opponent_assigned and opponent_name) else 'Challenger'
    whatsapp_text = (
        f"┏━━━━━━━━━━━━━━━━━━━━━┓\n"
        f"⚡ *QUIZMONDO ARENA DUEL* ⚡\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━┛\n"
        f"🎯 *{player.display_name}* has challenged you to a live trivia duel!\n"
        f"🔥 *Round {match.current_round}:* {active_cat}\n"
        f"🏆 *Target Score:* {match.p1_total_score} PTS\n\n"
        f"👇 *TAP LINK BELOW TO CLASH NOW:* 👇\n"
        f"{play_url}"
    )
    whatsapp_nudge_text = (
        f"┏━━━━━━━━━━━━━━━━━━━━━┓\n"
        f"🔔 *ROUND {match.current_round} ARENA NUDGE* 🔔\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━┛\n"
        f"⚔️ Hey *{target_nudgee}*! *{player.display_name}* just finished Round {match.current_round}!\n"
        f"📊 *Scoreboard:* {player.display_name} ({match.p1_total_score} pts) vs {opponent_name} ({match.p2_total_score} pts)\n"
        f"⚡ It's *YOUR TURN* to buzz in and take the lead!\n\n"
        f"👇 *TAP LINK BELOW TO PLAY ROUND {match.current_round}:* 👇\n"
        f"{play_url}"
    )

    all_rounds = match.rounds.all()

    return render_template(
        'themes/quizhub/arena_match.html',
        match=match,
        player=player,
        is_player1=is_player1,
        is_player2=is_player2,
        is_participant=is_participant,
        opponent_name=opponent_name,
        opponent_assigned=opponent_assigned,
        active_round=active_round,
        my_turn=my_turn,
        all_rounds=all_rounds,
        invite_url=invite_url,
        whatsapp_text=whatsapp_text,
        whatsapp_nudge_text=whatsapp_nudge_text,
        has_account=bool(session.get('user_id'))
    )


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
    player = get_current_player()
    match = ArenaMatch.query.filter_by(match_code=match_code).first_or_404()

    is_player1 = (match.player1_session == player.session_key)
    is_player2 = (match.player2_session == player.session_key)
    if not (is_player1 or is_player2):
        # Only allow auto-claim if match is in Round 1 and Player 2 slot is unassigned!
        if match.current_round == 1 and (not match.player2_session or match.player2_session in ('pending_invite', '')):
            match.player2_session = player.session_key
            match.player2_name = player.display_name
            match.player2_avatar = player.avatar_key
            match.status = 'in_progress'
            db.session.commit()
            is_player2 = True
        else:
            flash(f"This duel is already locked between {match.player1_name} and {match.player2_name or 'another challenger'} (Round {match.current_round}). You cannot join mid-game.", "info")
            return redirect(url_for('arena.match_lobby', match_code=match_code))

    # Gating requirement: Beyond Round 1 in friend duels, players MUST be logged in
    if not match.is_bot and match.current_round > 1 and not session.get('user_id'):
        flash(f"Round 1 completed! Create a free account or log in to unlock Round {match.current_round} and save your XP, streaks, and duel progress.", "info")
        return redirect(url_for('arena.player_register', next=url_for('arena.play_round', match_code=match_code)))

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

    # Gated beyond Round 1 in human duels: Account required
    if not match.is_bot and match.current_round > 1 and not session.get('user_id'):
        return jsonify({
            'error': 'login_required',
            'message': 'Create a free account or log in to submit answers beyond Round 1.',
            'redirect': url_for('arena.player_register', next=url_for('arena.play_round', match_code=match_code))
        }), 401

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
            if match.is_bot:
                next_turn = 1
                match.current_turn = 1
            else:
                next_turn = 2 if match.current_turn == 1 else 1
                match.current_turn = next_turn

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
        'bot_score': active_round.p2_score if match.is_bot else 0,
        'detailed_results': detailed_results,
        'player_level': player.level,
        'player_xp': player.xp,
        'p1_total_score': match.p1_total_score,
        'p2_total_score': match.p2_total_score,
        'match_status': match.status,
        'is_bot': match.is_bot,
        'opponent_name': match.player2_name,
        'current_round': active_round.round_number,
        'next_round': match.current_round if match.status != 'completed' else None,
        'next_category_name': chosen_cat[1] if (match.status != 'completed' and 'chosen_cat' in locals()) else '',
        'winner': match.winner,
        'has_account': bool(session.get('user_id'))
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
    new_name = (request.form.get('display_name') or '').strip()
    new_avatar = (request.form.get('avatar_key') or '').strip()

    if new_name:
        player.display_name = new_name[:40]
    if new_avatar in [a['key'] for a in AVATAR_PRESETS]:
        player.avatar_key = new_avatar

    db.session.commit()
    flash("Avatar & Profile updated successfully!", "success")
    return redirect(url_for('arena.dashboard'))


@arena_bp.route('/register', methods=['GET', 'POST'])
def player_register():
    """Create a permanent player account to save streaks, XP, coins, and duels."""
    player = get_current_player()
    if session.get('user_id'):
        flash(f"You are already signed in as {session.get('username')}.", "info")
        return redirect(url_for('arena.dashboard'))

    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        confirm_password = request.form.get('confirm_password') or ''

        if not username or len(username) < 3:
            flash("Username must be at least 3 characters long.", "error")
            return render_template('themes/quizhub/arena_register.html', player=player)

        if not email or '@' not in email:
            flash("Please enter a valid email address.", "error")
            return render_template('themes/quizhub/arena_register.html', player=player)

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return render_template('themes/quizhub/arena_register.html', player=player)

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template('themes/quizhub/arena_register.html', player=player)

        if User.query.filter_by(username=username).first():
            flash("That username is already taken. Please choose another.", "error")
            return render_template('themes/quizhub/arena_register.html', player=player)

        if User.query.filter_by(email=email).first():
            flash("An account with that email already exists. Try logging in instead.", "error")
            return render_template('themes/quizhub/arena_register.html', player=player)

        user = User(username=username, email=email, role='player')
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        player.user_id = user.id
        player.display_name = username
        # Update past match player names to permanently replace guest tag with real username
        ArenaMatch.query.filter_by(player1_session=player.session_key).update({'player1_name': username})
        ArenaMatch.query.filter_by(player2_session=player.session_key).update({'player2_name': username})
        db.session.commit()

        session['user_id'] = user.id
        session['username'] = user.username
        session['user_role'] = user.role
        session['qm_player_key'] = player.session_key

        flash(f"Welcome to Quizmondo, {username}! Your stats, coins, and duels are now permanently saved.", "success")
        next_url = request.args.get('next')
        if next_url and next_url.startswith('/'):
            return redirect(next_url)
        return redirect(url_for('arena.dashboard'))

    return render_template('themes/quizhub/arena_register.html', player=player)


@arena_bp.route('/login', methods=['GET', 'POST'])
def player_login():
    """Sign in to access saved player profile, streaks, and tournament ranks."""
    if session.get('user_id'):
        return redirect(url_for('arena.dashboard'))

    if request.method == 'POST':
        login_id = (request.form.get('username') or '').strip()
        password = request.form.get('password') or ''

        user = User.query.filter((User.username == login_id) | (User.email == login_id.lower())).first()
        if user and user.check_password(password) and user.is_active:
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_role'] = user.role

            guest_key = session.get('qm_player_key')
            profile = PlayerProfile.query.filter_by(user_id=user.id).first()
            if profile:
                session['qm_player_key'] = profile.session_key
                profile.last_active_at = datetime.utcnow()
                if guest_key and guest_key != profile.session_key:
                    ArenaMatch.query.filter_by(player1_session=guest_key).update({
                        'player1_session': profile.session_key,
                        'player1_name': profile.display_name,
                        'player1_avatar': profile.avatar_key
                    })
                    ArenaMatch.query.filter_by(player2_session=guest_key).update({
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
            next_url = request.args.get('next')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect(url_for('arena.dashboard'))
        else:
            flash("Invalid username or password.", "error")

    player = get_current_player()
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
    player = get_current_player()
    league = PubLeague.query.filter_by(slug=slug, is_active=True).first_or_404()
    # Only display approved real teams on lounge scoreboard (no mock demo teams!)
    teams = [t for t in league.get_teams() if t.get('status') != 'pending']
    return render_template(
        'themes/quizhub/arena_league_lounge.html',
        player=player,
        league=league,
        teams=teams
    )


@arena_bp.route('/leagues/<slug>/card.png')
def league_card_image(slug):
    """Dynamic 1200x630 OpenGraph pub quiz venue invite card for WhatsApp / social previews."""
    league = PubLeague.query.filter_by(slug=slug, is_active=True).first_or_404()
    state = league.get_state()
    cfg = state.get('config', {})
    png_bytes = generate_pub_card_png(
        venue_name=league.venue_name or league.name,
        pin_code=league.pin_code,
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
    1: {'number': 1, 'name': 'Level 1: General Knowledge, Science & Lore', 'cat_slug': 'science-cosmos', 'icon': '🌍', 'desc': 'Warm up your neurons with world history, science, and general news.'},
    2: {'number': 2, 'name': 'Level 2: Pop Culture, Cinema Titans & Music Legends', 'cat_slug': 'tv-cinema', 'icon': '🎬', 'desc': 'Blockbuster cinema, chart-topping records, and modern pop icons.'},
    3: {'number': 3, 'name': 'Level 3: Championship Wipeout Lightning Sprint', 'cat_slug': 'gaming-esports', 'icon': '⚡', 'desc': 'High stakes finale! 1.5x score multiplier on all correct answers.'},
}

PUB_ROUNDS_CONFIG = {
    1: {'number': 1, 'name': 'General Knowledge & News', 'cat_slug': 'world-history', 'icon': '🧠', 'desc': 'Test your broad trivia knowledge across news, landmarks, and science.'},
    2: {'number': 2, 'name': 'Music, Audio & Waveforms', 'cat_slug': 'pop-music', 'icon': '🎵', 'desc': 'Iconic number one records, synthesizers, chiptunes, and rock anthems.'},
    3: {'number': 3, 'name': 'Cinema, Television & Blockbusters', 'cat_slug': 'tv-cinema', 'icon': '🎬', 'desc': 'Cult cinema classics, famous directors, Academy Awards, and TV quotes.'},
    4: {'number': 4, 'name': 'World Geography & Lost Civilizations', 'cat_slug': 'world-geography', 'icon': '🗺️', 'desc': 'Continental capitals, mountain summits, ancient ruins, and extreme landforms.'},
    5: {'number': 5, 'name': 'The Big Wipeout Speed Sprint', 'cat_slug': 'gaming-esports', 'icon': '⚡', 'desc': 'Double Points Wipeout Round! Faster buzzer answers award massive bonus points.'},
}


@arena_bp.route('/leagues/<slug>/state')
def league_state(slug):
    """Real-time pub quiz state polling endpoint for TV projectors and player buzzer phones."""
    league = PubLeague.query.filter_by(slug=slug, is_active=True).first_or_404()
    state = league.get_state()
    current_round = state.get('current_round', 1)
    cfg = state.get('config', {})
    teams = state.get('teams', [])
    approved_teams = [t for t in teams if t.get('status') != 'pending']
    pending_teams = [t for t in teams if t.get('status') == 'pending']
    active_cfg = VIRTUAL_PUB_ROUNDS_CONFIG if league.is_virtual_league() else PUB_ROUNDS_CONFIG

    return jsonify({
        'success': True,
        'is_virtual': league.is_virtual_league(),
        'current_round': current_round,
        'round_status': state.get('round_status', 'active' if league.is_virtual_league() else 'waiting'),
        'answers_revealed': state.get('answers_revealed', False),
        'round_title': active_cfg.get(current_round, {}).get('name', 'Round ' + str(current_round)),
        'config': cfg,
        'break_ends_at': state.get('break_ends_at'),
        'approved_teams_count': len(approved_teams),
        'pending_teams_count': len(pending_teams),
        'teams': approved_teams
    })


@arena_bp.route('/leagues/<slug>/manager', methods=['GET', 'POST'])
def league_manager(slug):
    """Host / Quizmaster Manager Console for table bouncer approvals, live game control, and bar promos."""
    league = PubLeague.query.filter_by(slug=slug, is_active=True).first_or_404()
    is_mgr = session.get(f'pub_mgr_{slug}') or session.get('user_role') == 'admin'

    if request.method == 'POST' and request.form.get('action') == 'manager_login':
        pin = (request.form.get('pin') or '').strip()
        if pin == league.pin_code or session.get('user_role') == 'admin':
            session[f'pub_mgr_{slug}'] = True
            is_mgr = True
            flash("Quizmaster Console Unlocked! Welcome to the live manager deck.", "success")
        else:
            flash("Invalid Manager Host PIN. Please check the venue PIN and try again.", "error")
            return render_template('themes/quizhub/arena_league_manager_login.html', league=league)

    if not is_mgr:
        return render_template('themes/quizhub/arena_league_manager_login.html', league=league)

    state = league.get_state()
    config = state.get('config', {})
    teams = state.get('teams', [])
    pending_teams = [t for t in teams if t.get('status') == 'pending']
    approved_teams = [t for t in teams if t.get('status') != 'pending']
    curr_r = state.get('current_round', 1)
    active_cfg = VIRTUAL_PUB_ROUNDS_CONFIG if league.is_virtual_league() else PUB_ROUNDS_CONFIG
    active_round_info = active_cfg.get(curr_r, {})

    return render_template(
        'themes/quizhub/arena_league_manager.html',
        league=league,
        state=state,
        config=config,
        pending_teams=pending_teams,
        approved_teams=approved_teams,
        active_round_info=active_round_info
    )


@arena_bp.route('/leagues/<slug>/admin/control', methods=['POST'])
@arena_bp.route('/leagues/<slug>/manager/action', methods=['POST'])
def league_manager_action(slug):
    """Execute host commands: approve/reject bouncer tables, control rounds, and configure promos."""
    league = PubLeague.query.filter_by(slug=slug, is_active=True).first_or_404()
    is_authorized = session.get(f'pub_mgr_{slug}') or session.get('user_role') == 'admin'
    pin = (request.form.get('pin') or '').strip()
    if not is_authorized and pin != league.pin_code:
        if 'text/html' in (request.headers.get('Accept') or ''):
            flash("Unauthorized Quizmaster access. Please log in with venue PIN.", "error")
            return redirect(url_for('arena.league_manager', slug=slug))
        return jsonify({'success': False, 'error': 'Unauthorized Quizmaster'}), 403

    action = request.form.get('action')
    state = league.get_state()
    teams = state.get('teams', [])
    cfg = state.get('config', {})

    accept_hdr = request.headers.get('Accept') or ''
    # Browser standard form navigations always accept text/html
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

    if action == 'manager_logout':
        session.pop(f'pub_mgr_{slug}', None)
        flash("Quizmaster signed out.", "info")
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
        return respond(f"Table {tbl} approved!")

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
        return respond(f"Table {tbl} rejected.")

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
        return respond("Table number and team name required.")

    elif action == 'start_round':
        r = int(request.form.get('round') or state.get('current_round', 1))
        state['current_round'] = r
        state['round_status'] = 'active'
        state['answers_revealed'] = False
        league.set_state(state)
        db.session.commit()
        return respond(f"Round {r} launched! Questions sent to all player phones.")

    elif action == 'close_round':
        state['round_status'] = 'closed'
        league.set_state(state)
        db.session.commit()
        return respond("Round locked! Answers submitted.")

    elif action == 'reveal_answers':
        state['answers_revealed'] = True
        league.set_state(state)
        db.session.commit()
        return respond("Official answers revealed on big screen and player screens!")

    elif action == 'start_break':
        state['round_status'] = 'break'
        state['answers_revealed'] = True
        duration_mins = int(cfg.get('interval_duration_mins', 8))
        break_ends = (datetime.utcnow() + timedelta(minutes=duration_mins)).isoformat()
        state['break_ends_at'] = break_ends
        league.set_state(state)
        db.session.commit()
        return respond(f"Bar break started ({duration_mins} mins)! Bar promo specials activated.")

    elif action == 'advance_round':
        curr = state.get('current_round', 1)
        max_r = int(cfg.get('total_rounds', 5 if not league.is_virtual_league() else 3))
        if curr < max_r:
            state['current_round'] = curr + 1
            state['round_status'] = 'waiting' if not league.is_virtual_league() else 'active'
            state['answers_revealed'] = False
        else:
            state['round_status'] = 'finished'
            state['answers_revealed'] = True
        league.set_state(state)
        db.session.commit()
        return respond(f"Advanced to Round {state['current_round']}!")

    elif action == 'save_config':
        cfg['total_rounds'] = int(request.form.get('total_rounds', cfg.get('total_rounds', 5)))
        cfg['max_tables'] = int(request.form.get('max_tables', cfg.get('max_tables', 20)))
        cfg['question_time_limit'] = int(request.form.get('question_time_limit', cfg.get('question_time_limit', 15)))
        cfg['interval_duration_mins'] = int(request.form.get('interval_duration_mins', cfg.get('interval_duration_mins', 8)))
        cfg['bar_promo_enabled'] = bool(request.form.get('bar_promo_enabled'))
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
        state['round_status'] = 'waiting' if not league.is_virtual_league() else 'active'
        state['answers_revealed'] = False
        state['teams'] = []
        state['round_questions'] = {}
        league.set_state(state)
        db.session.commit()
        return respond("Tournament reset! All tables cleared. Ready for fresh check-ins.")

    elif action == 'clear_tables':
        state['teams'] = []
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
    cfg = state.get('config', {})

    # Verify PIN if this is a physical in-venue pub quiz
    pin_attempt = (request.args.get('pin') or request.form.get('pin') or session.get(f'pub_pin_{slug}') or '').strip()
    if not is_virtual and league.pin_code and pin_attempt != league.pin_code:
        flash(f"Please enter the 4-digit Table Room PIN displayed on the venue screen to join {league.name}.", "error")
        return redirect(url_for('arena.league_lounge', slug=slug))
    if pin_attempt == league.pin_code:
        session[f'pub_pin_{slug}'] = pin_attempt

    # In virtual mode: 3 distinct levels; in venue mode: configured rounds (default 5)
    if is_virtual:
        total_rounds = 3
        current_round = int(request.args.get('round', 1))
        if current_round < 1 or current_round > total_rounds:
            current_round = 1
        round_info = VIRTUAL_PUB_ROUNDS_CONFIG.get(current_round, VIRTUAL_PUB_ROUNDS_CONFIG[1])
    else:
        total_rounds = int(cfg.get('total_rounds', 5))
        # IN-VENUE PUB QUIZ: The active round is GOVERNED STRICTLY BY THE QUIZMASTER!
        current_round = int(state.get('current_round', 1))
        if current_round < 1 or current_round > total_rounds:
            current_round = 1
        round_info = PUB_ROUNDS_CONFIG.get(current_round, PUB_ROUNDS_CONFIG.get(1, {'number': 1, 'name': f'Round {current_round}', 'cat_slug': 'world-history', 'icon': '🧠'}))

    table_num = request.args.get('table') or session.get('pub_table_num') or '1'
    session['pub_table_num'] = str(table_num)

    team_name = request.args.get('team') or session.get('pub_team_name') or f"Table {table_num} • {player.display_name}"
    session['pub_team_name'] = team_name

    # Check table capacity & in-venue bouncer approval
    teams = state.get('teams', [])
    max_tables = int(cfg.get('max_tables', 20))
    team_entry = next((t for t in teams if str(t.get('table')) == str(table_num) or t.get('name') == team_name), None)

    if not is_virtual:
        if not team_entry:
            approved_count = len([t for t in teams if t.get('status') != 'pending'])
            if approved_count >= max_tables:
                flash(f"This pub venue has reached its maximum table capacity of {max_tables} tables. Please check with the Quizmaster.", "error")
                return redirect(url_for('arena.league_lounge', slug=slug))
            team_entry = {
                'name': team_name,
                'table': str(table_num),
                'members': 4,
                'score': 0,
                'rank': len(teams) + 1,
                'status': 'pending'  # Held in bouncer queue until Quizmaster approves
            }
            teams.append(team_entry)
            state['teams'] = teams
            league.set_state(state)
            db.session.commit()
            is_approved = False
        else:
            is_approved = (team_entry.get('status') != 'pending')
    else:
        is_approved = True

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

    if request.method == 'POST':
        round_score = int(request.form.get('score', 0))
        # 1.5x Wipeout Multiplier on finale round
        if (is_virtual and current_round == 3) or (not is_virtual and current_round == total_rounds):
            round_score = int(round_score * 1.5)

        teams = league.get_teams()
        updated = False
        for t in teams:
            if str(t.get('table')) == str(table_num) or t.get('name') == team_name:
                t['score'] = (t.get('score', 0)) + round_score
                t[f'round_{current_round}'] = round_score
                team_entry = t
                updated = True
                break

        if not updated:
            team_entry = {
                'name': team_name,
                'score': round_score,
                'members': 4,
                'table': str(table_num),
                'rank': len(teams) + 1,
                'status': 'approved',
                f'round_{current_round}': round_score
            }
            teams.append(team_entry)

        teams.sort(key=lambda x: x.get('score', 0), reverse=True)
        for idx, t in enumerate(teams, 1):
            t['rank'] = idx
        league.set_teams(teams)
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
            'next_round': next_round_num,
            'next_round_title': next_round_title,
            'next_pub_date': get_next_weekly_pub_date()
        })

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
    current_round = state.get('current_round', 1)
    round_info = PUB_ROUNDS_CONFIG.get(current_round, PUB_ROUNDS_CONFIG[1])

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


@arena_bp.route('/challenge-fresh/<target_session>', methods=['GET', 'POST'])
def challenge_fresh(target_session):
    """Start a brand new Round 1 duel against a specific opponent."""
    player = get_current_player()
    target_player = PlayerProfile.query.filter_by(session_key=target_session).first()

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
        status='waiting',
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

    flash(f"New Round 1 duel created! Send the link to challenge your friend.", "success")
    return redirect(url_for('arena.match_lobby', match_code=match_code))


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
