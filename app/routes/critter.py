"""Mondo Critters: full-screen landscape daily trivia companion blueprint."""
import random
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from sqlalchemy.sql.expression import func

from ..models import db, QuizQuestion
from ..models_critter import CritterCompanion
from .arena import get_current_player
from .public import inject_global_data

critter_bp = Blueprint('critter', __name__, url_prefix='/arena/critter')


@critter_bp.context_processor
def inject_critter_globals():
    return inject_global_data()


VALID_SPECIES = ('fox', 'cat', 'pup', 'dragon', 'owl', 'bunny', 'dino', 'axolotl', 'sloth', 'spirit')
VALID_HAIR = ('none', 'tuft', 'spiky', 'curly', 'mohawk', 'fringe', 'horns', 'antenna')
VALID_HATS = ('none', 'crown', 'beanie', 'tophat', 'wizard', 'cap', 'cowboy', 'halo')
VALID_SCARVES = ('none', 'striped', 'bowtie', 'cape', 'bandana', 'chain')

SHOP_ITEMS = {
    'tonic':  {'cost': 50,  'label': 'Health Tonic (+25 All & Cure)'},
    'feast':  {'cost': 30,  'label': 'Gourmet Feast (+40 Hunger)'},
    'gym':    {'cost': 30,  'label': 'Mega Gym (+40 Fitness)'},
    'party':  {'cost': 30,  'label': 'Arcade Party (+40 Happiness)'},
    'revive': {'cost': 150, 'label': 'Phoenix Elixir (Full Revive)'},
}


def _get_or_create_critter(player):
    critter = CritterCompanion.query.filter_by(player_profile_id=player.id).first()
    if not critter:
        critter = CritterCompanion(
            player_profile_id=player.id,
            name='Nova',
            hunger=80,
            fitness=80,
            happiness=80,
            care_tokens=2,
            days_alive=1,
            last_decay_date=datetime.utcnow().date(),
        )
        db.session.add(critter)
        db.session.commit()
    else:
        if critter.apply_daily_decay():
            db.session.commit()
    return critter


def _pick_5_unique_category_questions():
    """Draw 5 approved questions, each guaranteed from a unique category."""
    cats = [
        r[0] for r in db.session.query(QuizQuestion.category_slug)
        .filter(QuizQuestion.status == 'approved', QuizQuestion.category_slug.isnot(None))
        .distinct().all()
        if r[0]
    ]
    random.shuffle(cats)
    chosen_ids = []
    for cslug in cats:
        q = QuizQuestion.query.filter_by(status='approved', category_slug=cslug).order_by(func.random()).first()
        if q:
            chosen_ids.append(q.id)
        if len(chosen_ids) >= 5:
            break
    if len(chosen_ids) < 5:
        extra = QuizQuestion.query.filter(
            QuizQuestion.status == 'approved',
            ~QuizQuestion.id.in_(chosen_ids) if chosen_ids else True
        ).order_by(func.random()).limit(5 - len(chosen_ids)).all()
        chosen_ids.extend([q.id for q in extra])
    return chosen_ids


def _ensure_today_quiz(critter):
    today = datetime.utcnow().date()
    if critter.last_quiz_date != today:
        q_ids = _pick_5_unique_category_questions()
        critter.last_quiz_date = today
        critter.today_q_index = 0
        critter.today_correct = 0
        critter.today_wrong = 0
        critter.sick_penalty_applied = False
        critter.set_today_q_ids(q_ids)
        db.session.commit()
    elif not critter.get_today_q_ids():
        critter.set_today_q_ids(_pick_5_unique_category_questions())
        db.session.commit()


@critter_bp.route('', methods=['GET'])
@critter_bp.route('/', methods=['GET'])
def critter_home():
    if not session.get('user_id'):
        return redirect(url_for('arena.player_register', next=url_for('critter.critter_home')))
    player = get_current_player(persist=True)
    if not player:
        return redirect(url_for('arena.player_register', next=url_for('critter.critter_home')))
    critter = _get_or_create_critter(player)

    now_utc = datetime.utcnow()
    midnight = (now_utc + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_until_midnight = max(0, int((midnight - now_utc).total_seconds()))

    return render_template(
        'themes/quizhub/arena_critter.html',
        player=player,
        critter=critter.to_dict(),
        seconds_until_midnight=seconds_until_midnight,
        shop_items=SHOP_ITEMS,
    )


@critter_bp.route('/customize', methods=['POST'])
def critter_customize():
    if not session.get('user_id'):
        return jsonify({'success': False, 'error': 'Please sign in first.'}), 401
    player = get_current_player(persist=True)
    critter = _get_or_create_critter(player)
    data = request.get_json(silent=True) or {}

    name = (data.get('name') or critter.name or 'Nova').strip()[:24]
    if name:
        critter.name = name

    app_data = {}
    if data.get('species') in VALID_SPECIES:
        app_data['species'] = data['species']
    if data.get('hair') in VALID_HAIR:
        app_data['hair'] = data['hair']
    if data.get('hat') in VALID_HATS:
        app_data['hat'] = data['hat']
    if data.get('scarf') in VALID_SCARVES:
        app_data['scarf'] = data['scarf']
    if isinstance(data.get('color'), str) and data['color'].startswith('#') and len(data['color']) in (4, 7):
        app_data['color'] = data['color']
    if isinstance(data.get('accent'), str) and data['accent'].startswith('#') and len(data['accent']) in (4, 7):
        app_data['accent'] = data['accent']
    if isinstance(data.get('preset_id'), int) and 1 <= data['preset_id'] <= 100:
        app_data['preset_id'] = data['preset_id']

    critter.set_appearance(app_data)
    db.session.commit()
    return jsonify({'success': True, 'critter': critter.to_dict()})


@critter_bp.route('/daily-quiz', methods=['GET'])
def critter_daily_quiz():
    if not session.get('user_id'):
        return jsonify({'success': False, 'error': 'Please sign in first.'}), 401
    player = get_current_player(persist=True)
    critter = _get_or_create_critter(player)
    if critter.status == 'fainted':
        return jsonify({'success': False, 'error': 'Your critter has fainted! Revive or hatch a new one first.'}), 400

    _ensure_today_quiz(critter)
    q_ids = critter.get_today_q_ids()
    idx = critter.today_q_index or 0
    if idx >= len(q_ids) or idx >= 5:
        return jsonify({'success': True, 'done': True, 'critter': critter.to_dict()})

    q = db.session.get(QuizQuestion, q_ids[idx])
    if not q:
        q = QuizQuestion.query.filter_by(status='approved').order_by(func.random()).first()
    return jsonify({
        'success': True,
        'done': False,
        'index': idx,
        'total': 5,
        'question': {
            'id': q.id,
            'prompt': q.prompt,
            'options': q.get_options(),
            'category_name': q.category_name or q.category_slug or 'General',
            'difficulty': q.difficulty or 'medium',
        },
        'critter': critter.to_dict(),
    })


@critter_bp.route('/answer', methods=['POST'])
def critter_answer():
    if not session.get('user_id'):
        return jsonify({'success': False, 'error': 'Please sign in first.'}), 401
    player = get_current_player(persist=True)
    critter = _get_or_create_critter(player)
    _ensure_today_quiz(critter)

    idx = critter.today_q_index or 0
    if idx >= 5:
        return jsonify({'success': False, 'error': "You've already finished today's 5 questions!"}), 400

    data = request.get_json(silent=True) or {}
    q_id = data.get('question_id')
    selected = (data.get('selected') or '').strip().upper()
    q = db.session.get(QuizQuestion, q_id) if q_id else None
    if not q:
        return jsonify({'success': False, 'error': 'Question not found.'}), 404

    is_correct = (selected == (q.correct_option or '').strip().upper())
    critter.today_q_index = idx + 1
    coins_won = 0
    sick_triggered = False

    if is_correct:
        critter.today_correct = (critter.today_correct or 0) + 1
        critter.total_correct = (critter.total_correct or 0) + 1
        critter.care_tokens = (critter.care_tokens or 0) + 1
        coins_won = 15
        player.coins = (player.coins or 0) + coins_won
        player.xp = (player.xp or 0) + 15
    else:
        critter.today_wrong = (critter.today_wrong or 0) + 1
        # Core rule: more than 2 wrong in a day triggers danger / sickness!
        if critter.today_wrong >= 3 and not critter.sick_penalty_applied:
            critter.sick_penalty_applied = True
            sick_triggered = True
            critter.hunger = max(0, (critter.hunger or 0) - 25)
            critter.fitness = max(0, (critter.fitness or 0) - 25)
            critter.happiness = max(0, (critter.happiness or 0) - 25)

    critter.recalc_status()
    db.session.commit()

    return jsonify({
        'success': True,
        'correct': is_correct,
        'correct_option': q.correct_option,
        'explanation': q.explanation or '',
        'coins_won': coins_won,
        'wallet_coins': player.coins or 0,
        'sick_triggered': sick_triggered,
        'done': critter.today_q_index >= 5,
        'critter': critter.to_dict(),
    })


@critter_bp.route('/care', methods=['POST'])
def critter_care():
    if not session.get('user_id'):
        return jsonify({'success': False, 'error': 'Please sign in first.'}), 401
    player = get_current_player(persist=True)
    critter = _get_or_create_critter(player)
    if critter.status == 'fainted':
        return jsonify({'success': False, 'error': 'Your critter has fainted — revive it in the Coin Shop or hatch a new one.'}), 400
    if (critter.care_tokens or 0) <= 0:
        return jsonify({'success': False, 'error': 'No Care Tokens left! Answer daily questions or visit the Coin Shop.'}), 400

    action = ((request.get_json(silent=True) or {}).get('action') or '').strip().lower()
    if action == 'feed':
        critter.hunger = min(100, (critter.hunger or 0) + 25)
        msg = f'{critter.name} munched a cosmic snack! (+25 Hunger)'
    elif action == 'exercise':
        critter.fitness = min(100, (critter.fitness or 0) + 25)
        msg = f'{critter.name} crushed a workout sprint! (+25 Fitness)'
    elif action == 'play':
        critter.happiness = min(100, (critter.happiness or 0) + 25)
        msg = f'{critter.name} had a blast playing! (+25 Happiness)'
    else:
        return jsonify({'success': False, 'error': 'Invalid care action.'}), 400

    critter.care_tokens -= 1
    if min(critter.hunger, critter.fitness, critter.happiness) > 45:
        critter.sick_penalty_applied = False
    critter.recalc_status()
    db.session.commit()
    return jsonify({'success': True, 'message': msg, 'critter': critter.to_dict()})


@critter_bp.route('/shop', methods=['POST'])
def critter_shop():
    if not session.get('user_id'):
        return jsonify({'success': False, 'error': 'Please sign in first.'}), 401
    player = get_current_player(persist=True)
    critter = _get_or_create_critter(player)
    item_key = ((request.get_json(silent=True) or {}).get('item') or '').strip().lower()
    item = SHOP_ITEMS.get(item_key)
    if not item:
        return jsonify({'success': False, 'error': 'Unknown shop item.'}), 400
    cost = item['cost']
    if (player.coins or 0) < cost:
        return jsonify({'success': False, 'error': f'Not enough coins! Need {cost} 🪙 (you have {player.coins or 0} 🪙).'}), 400

    if item_key == 'revive':
        critter.hunger = 70
        critter.fitness = 70
        critter.happiness = 70
        critter.sick_penalty_applied = False
        msg = f'✨ Phoenix Elixir worked! {critter.name} is back and glowing!'
    else:
        if critter.status == 'fainted':
            return jsonify({'success': False, 'error': 'Use Phoenix Elixir to revive a fainted critter first!'}), 400
        if item_key == 'tonic':
            critter.hunger = min(100, (critter.hunger or 0) + 25)
            critter.fitness = min(100, (critter.fitness or 0) + 25)
            critter.happiness = min(100, (critter.happiness or 0) + 25)
            critter.sick_penalty_applied = False
            msg = f'🧪 Health Tonic boosted all stats +25 and cured sickness!'
        elif item_key == 'feast':
            critter.hunger = min(100, (critter.hunger or 0) + 40)
            msg = f'🍖 Gourmet Feast! +40 Hunger!'
        elif item_key == 'gym':
            critter.fitness = min(100, (critter.fitness or 0) + 40)
            msg = f'🏋️ Mega Gym session! +40 Fitness!'
        elif item_key == 'party':
            critter.happiness = min(100, (critter.happiness or 0) + 40)
            msg = f'🎪 Arcade Party! +40 Happiness!'

    player.coins = (player.coins or 0) - cost
    critter.recalc_status()
    db.session.commit()
    return jsonify({'success': True, 'message': msg, 'wallet_coins': player.coins, 'critter': critter.to_dict()})


@critter_bp.route('/hatch', methods=['POST'])
def critter_hatch():
    if not session.get('user_id'):
        return jsonify({'success': False, 'error': 'Please sign in first.'}), 401
    player = get_current_player(persist=True)
    critter = _get_or_create_critter(player)
    critter.hunger = 80
    critter.fitness = 80
    critter.happiness = 80
    critter.care_tokens = 2
    critter.days_alive = 1
    critter.sick_penalty_applied = False
    critter.status = 'healthy'
    critter.last_decay_date = datetime.utcnow().date()
    db.session.commit()
    return jsonify({'success': True, 'message': '🥚 A fresh Mondo Critter hatched!', 'critter': critter.to_dict()})
