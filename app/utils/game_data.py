"""Content and puzzle generators for the single-player mini games.

Everything a mini game needs is prepared here and handed to the template as
JSON, so the browser never has to call back mid-game. Where we can reuse the
trivia question bank (crossword clues, flag/badge/logo images) we do, so the
games stay in the same world as the Arena instead of feeling bolted on.
"""
import json
import os
import random
import re
from functools import lru_cache

# ---------------------------------------------------------------------------
# Word search
# ---------------------------------------------------------------------------

WORD_SEARCH_THEMES = [
    {'title': 'Premier League Clubs', 'icon': '⚽', 'words': ['ARSENAL', 'CHELSEA', 'EVERTON', 'FULHAM', 'SPURS', 'VILLA', 'WOLVES', 'BRENTFORD']},
    {'title': 'British Cities', 'icon': '🏙️', 'words': ['LONDON', 'LEEDS', 'CARDIFF', 'BRISTOL', 'NORWICH', 'DUNDEE', 'YORK', 'BELFAST']},
    {'title': 'In The Kitchen', 'icon': '🍳', 'words': ['WHISK', 'KETTLE', 'SPATULA', 'LADLE', 'GRATER', 'SIEVE', 'TEAPOT', 'OVEN']},
    {'title': 'Planets & Space', 'icon': '🪐', 'words': ['SATURN', 'MERCURY', 'COMET', 'NEBULA', 'ORBIT', 'GALAXY', 'ECLIPSE', 'ROCKET']},
    {'title': 'Weather Watch', 'icon': '🌦️', 'words': ['DRIZZLE', 'THUNDER', 'FROST', 'BREEZE', 'MONSOON', 'HAIL', 'SUNNY', 'GALE']},
    {'title': 'Musical Terms', 'icon': '🎵', 'words': ['TEMPO', 'CHORUS', 'GUITAR', 'ENCORE', 'OCTAVE', 'BALLAD', 'RHYTHM', 'VIOLIN']},
    {'title': 'Animal Kingdom', 'icon': '🦊', 'words': ['BADGER', 'OTTER', 'PUFFIN', 'LEOPARD', 'GIBBON', 'WALRUS', 'FERRET', 'HERON']},
    {'title': 'Pub Quiz Night', 'icon': '🍺', 'words': ['ROUNDS', 'BUZZER', 'POINTS', 'TIEBREAK', 'TEAMS', 'ANSWER', 'HALFTIME', 'WINNER']},
    {'title': 'On The Move', 'icon': '🚂', 'words': ['TRAIN', 'FERRY', 'TRAM', 'COACH', 'CYCLE', 'SCOOTER', 'TAXI', 'AIRPORT']},
    {'title': 'Body Parts', 'icon': '🫀', 'words': ['KIDNEY', 'SPLEEN', 'FEMUR', 'TENDON', 'CORNEA', 'BICEP', 'SKULL', 'ANKLE']},
    {'title': 'Film & Telly', 'icon': '🎬', 'words': ['SEQUEL', 'ACTOR', 'SCRIPT', 'CAMERA', 'STUDIO', 'TRAILER', 'BOXSET', 'EPISODE']},
    {'title': 'Garden Jobs', 'icon': '🌱', 'words': ['PRUNING', 'COMPOST', 'SEEDS', 'TROWEL', 'MOWER', 'HEDGE', 'WEEDING', 'PATIO']},
]

# ---------------------------------------------------------------------------
# Anagrams  (word, category hint)
# ---------------------------------------------------------------------------

ANAGRAM_BANK = [
    ('PENGUIN', 'Animal'), ('TRUMPET', 'Instrument'), ('CABBAGE', 'Vegetable'),
    ('DOLPHIN', 'Animal'), ('COMPASS', 'Navigation'), ('BLANKET', 'Household'),
    ('MONSOON', 'Weather'), ('PYRAMID', 'Landmark'), ('CRUMPET', 'Food'),
    ('JUPITER', 'Planet'), ('TRIBUTE', 'Praise'), ('SANDALS', 'Footwear'),
    ('HARBOUR', 'Coastal'), ('MUSTARD', 'Condiment'), ('LANTERN', 'Light'),
    ('PANCAKE', 'Food'), ('DIAMOND', 'Gemstone'), ('TORNADO', 'Weather'),
    ('CATTLE', 'Farm'), ('WALNUT', 'Nut'), ('VIOLIN', 'Instrument'),
    ('ORANGE', 'Fruit'), ('CASTLE', 'Building'), ('WINTER', 'Season'),
    ('DRAGON', 'Mythical'), ('SILVER', 'Metal'), ('PUFFIN', 'Bird'),
    ('TEAPOT', 'Kitchen'), ('MARKET', 'Shopping'), ('GARDEN', 'Outdoors'),
    ('BISCUIT', 'Snack'), ('TRAFFIC', 'Roads'), ('LIBRARY', 'Building'),
    ('WHISTLE', 'Sound'), ('CLIMATE', 'Weather'), ('AIRPORT', 'Travel'),
    ('OSTRICH', 'Bird'), ('SPINACH', 'Vegetable'), ('GLACIER', 'Landscape'),
    ('TRACTOR', 'Vehicle'), ('BALCONY', 'Building'), ('CUSTARD', 'Pudding'),
    ('HAMSTER', 'Pet'), ('JOURNEY', 'Travel'), ('KETTLE', 'Kitchen'),
    ('MEADOW', 'Landscape'), ('NUTMEG', 'Spice'), ('OYSTER', 'Seafood'),
    ('PARROT', 'Bird'), ('QUARRY', 'Industry'), ('RABBIT', 'Animal'),
    ('SALMON', 'Fish'), ('TUNNEL', 'Transport'), ('UMPIRE', 'Sport'),
    ('VELVET', 'Fabric'), ('WALRUS', 'Animal'), ('YOGHURT', 'Dairy'),
    ('ZEBRA', 'Animal'), ('CLOUD', 'Sky'), ('FLUTE', 'Instrument'),
    ('GRAPE', 'Fruit'), ('HONEY', 'Food'), ('IGLOO', 'Shelter'),
    ('JELLY', 'Pudding'), ('KOALA', 'Animal'), ('LEMON', 'Fruit'),
    ('MANGO', 'Fruit'), ('NURSE', 'Job'), ('OTTER', 'Animal'),
    ('PIANO', 'Instrument'), ('RADAR', 'Technology'), ('SHEEP', 'Farm'),
    ('TIGER', 'Animal'), ('VODKA', 'Drink'), ('WAGON', 'Vehicle'),
    ('CHIMNEY', 'Building'), ('DOLLAR', 'Currency'), ('EMERALD', 'Gemstone'),
    ('FESTIVAL', 'Event'), ('GRAVITY', 'Science'), ('HOSPITAL', 'Building'),
    ('ICEBERG', 'Ocean'), ('JACKPOT', 'Winning'), ('KINGDOM', 'Realm'),
    ('LEOPARD', 'Animal'), ('MAGNET', 'Science'), ('NETBALL', 'Sport'),
    ('OCTOPUS', 'Sea Life'), ('PENALTY', 'Football'), ('RAINBOW', 'Sky'),
    ('SAUSAGE', 'Food'), ('THEATRE', 'Night Out'), ('VOLCANO', 'Geography'),
    ('WHISKEY', 'Drink'), ('BANDAGE', 'First Aid'), ('CARAVAN', 'Holiday'),
    ('DENTIST', 'Job'), ('ENVELOPE', 'Post'), ('FLAMINGO', 'Bird'),
    ('GOALKEEPER', 'Football'), ('HEDGEHOG', 'Animal'), ('LIGHTNING', 'Weather'),
]

# ---------------------------------------------------------------------------
# Missing vowels (Only Connect style)
# ---------------------------------------------------------------------------

MISSING_VOWELS = [
    {'category': 'Premier League Grounds', 'items': ['OLD TRAFFORD', 'ANFIELD', 'THE EMIRATES', 'GOODISON PARK']},
    {'category': 'British Sitcoms', 'items': ['ONLY FOOLS AND HORSES', 'FAWLTY TOWERS', 'BLACKADDER', 'THE OFFICE']},
    {'category': 'Biscuit Tin', 'items': ['CUSTARD CREAM', 'JAMMIE DODGER', 'BOURBON', 'DIGESTIVE']},
    {'category': 'Seaside Towns', 'items': ['BLACKPOOL', 'BRIGHTON', 'SCARBOROUGH', 'WHITBY']},
    {'category': 'Bond Films', 'items': ['GOLDFINGER', 'SKYFALL', 'THUNDERBALL', 'MOONRAKER']},
    {'category': 'Breakfast Items', 'items': ['SCRAMBLED EGGS', 'BAKED BEANS', 'BLACK PUDDING', 'HASH BROWN']},
    {'category': 'Board Games', 'items': ['MONOPOLY', 'SCRABBLE', 'CLUEDO', 'BACKGAMMON']},
    {'category': 'Weather Words', 'items': ['DRIZZLE', 'HEATWAVE', 'THUNDERSTORM', 'HAILSTONE']},
    {'category': 'Pop Legends', 'items': ['ELTON JOHN', 'KATE BUSH', 'DAVID BOWIE', 'AMY WINEHOUSE']},
    {'category': 'London Landmarks', 'items': ['TOWER BRIDGE', 'BIG BEN', 'THE SHARD', 'HYDE PARK']},
    {'category': 'Takeaway Night', 'items': ['FISH AND CHIPS', 'CHICKEN TIKKA', 'SWEET AND SOUR', 'DONER KEBAB']},
    {'category': 'Olympic Sports', 'items': ['SYNCHRONISED DIVING', 'POLE VAULT', 'DRESSAGE', 'TAEKWONDO']},
]

# ---------------------------------------------------------------------------
# Emoji riddles
# ---------------------------------------------------------------------------

EMOJI_RIDDLES = [
    {'emoji': '🦁👑', 'answer': 'THE LION KING', 'category': 'Film'},
    {'emoji': '🧊🎂', 'answer': 'ICE CREAM', 'category': 'Food', 'note': 'Two words, frozen pudding'},
    {'emoji': '⚡🧙', 'answer': 'HARRY POTTER', 'category': 'Film'},
    {'emoji': '🚢🧊💔', 'answer': 'TITANIC', 'category': 'Film'},
    {'emoji': '🕷️🧑', 'answer': 'SPIDERMAN', 'category': 'Film'},
    {'emoji': '🐝🎬', 'answer': 'BEE MOVIE', 'category': 'Film'},
    {'emoji': '🌧️👨', 'answer': 'RAIN MAN', 'category': 'Film'},
    {'emoji': '🦈🦷', 'answer': 'JAWS', 'category': 'Film'},
    {'emoji': '👑🗣️', 'answer': 'THE KINGS SPEECH', 'category': 'Film'},
    {'emoji': '🥔👨', 'answer': 'MASHED POTATO', 'category': 'Food'},
    {'emoji': '🐟🍟', 'answer': 'FISH AND CHIPS', 'category': 'Food'},
    {'emoji': '🍳🍞', 'answer': 'EGG ON TOAST', 'category': 'Food'},
    {'emoji': '🐄🥛', 'answer': 'MILKSHAKE', 'category': 'Food'},
    {'emoji': '🧂🌊', 'answer': 'SALT WATER', 'category': 'Nature'},
    {'emoji': '🔥🏠', 'answer': 'FIRE STATION', 'category': 'Places'},
    {'emoji': '🚂🚉', 'answer': 'TRAIN STATION', 'category': 'Places'},
    {'emoji': '🌞🌻', 'answer': 'SUNFLOWER', 'category': 'Nature'},
    {'emoji': '🌈🏹', 'answer': 'RAINBOW', 'category': 'Nature'},
    {'emoji': '🦶⚽', 'answer': 'FOOTBALL', 'category': 'Sport'},
    {'emoji': '🏀🥅', 'answer': 'BASKETBALL', 'category': 'Sport'},
    {'emoji': '🐎🏁', 'answer': 'HORSE RACING', 'category': 'Sport'},
    {'emoji': '🎾🏆', 'answer': 'WIMBLEDON', 'category': 'Sport'},
    {'emoji': '🧊🏒', 'answer': 'ICE HOCKEY', 'category': 'Sport'},
    {'emoji': '👑🇬🇧', 'answer': 'BUCKINGHAM PALACE', 'category': 'Landmark'},
    {'emoji': '🕰️🔔', 'answer': 'BIG BEN', 'category': 'Landmark'},
    {'emoji': '🗼🥐', 'answer': 'EIFFEL TOWER', 'category': 'Landmark'},
    {'emoji': '🧱🐉', 'answer': 'GREAT WALL OF CHINA', 'category': 'Landmark'},
    {'emoji': '🎸🪲', 'answer': 'THE BEATLES', 'category': 'Music'},
    {'emoji': '👑🎤', 'answer': 'QUEEN', 'category': 'Music'},
    {'emoji': '🌹🔫', 'answer': 'GUNS N ROSES', 'category': 'Music'},
    {'emoji': '🧊🧊🧊', 'answer': 'COLD AS ICE', 'category': 'Saying'},
    {'emoji': '🐱🌧️🐶', 'answer': 'RAINING CATS AND DOGS', 'category': 'Saying'},
    {'emoji': '🍰🚶', 'answer': 'A PIECE OF CAKE', 'category': 'Saying'},
    {'emoji': '👀🐍', 'answer': 'SNAKE EYES', 'category': 'Saying'},
    {'emoji': '🛏️🐛', 'answer': 'BED BUG', 'category': 'Saying'},
    {'emoji': '🌙🚶', 'answer': 'MOONWALK', 'category': 'Music'},
    {'emoji': '🧛🦇', 'answer': 'DRACULA', 'category': 'Books'},
    {'emoji': '🐳⚓', 'answer': 'MOBY DICK', 'category': 'Books'},
    {'emoji': '🤖🚗', 'answer': 'TRANSFORMERS', 'category': 'Film'},
    {'emoji': '❄️👸', 'answer': 'FROZEN', 'category': 'Film'},
]

# ---------------------------------------------------------------------------
# Hangman phrase bank
# ---------------------------------------------------------------------------

HANGMAN_BANK = [
    ('PENALTY SHOOTOUT', 'Football'), ('OFFSIDE TRAP', 'Football'),
    ('EXTRA TIME', 'Football'), ('HAT TRICK', 'Football'),
    ('FISH AND CHIPS', 'British Food'), ('SUNDAY ROAST', 'British Food'),
    ('CREAM TEA', 'British Food'), ('TOAD IN THE HOLE', 'British Food'),
    ('BANGERS AND MASH', 'British Food'), ('STICKY TOFFEE PUDDING', 'British Food'),
    ('NORTHERN LIGHTS', 'Nature'), ('SOLAR ECLIPSE', 'Nature'),
    ('CORAL REEF', 'Nature'), ('RAIN FOREST', 'Nature'),
    ('TOWER BRIDGE', 'Landmark'), ('STONEHENGE', 'Landmark'),
    ('LOCH NESS', 'Landmark'), ('GIANTS CAUSEWAY', 'Landmark'),
    ('DOCTOR WHO', 'Telly'), ('STRICTLY COME DANCING', 'Telly'),
    ('ONLY FOOLS AND HORSES', 'Telly'), ('THE GREAT ESCAPE', 'Film'),
    ('GROUNDHOG DAY', 'Film'), ('JURASSIC PARK', 'Film'),
    ('DOUBLE DECKER BUS', 'Transport'), ('ZEBRA CROSSING', 'Transport'),
    ('ROUNDABOUT', 'Transport'), ('UNDERGROUND', 'Transport'),
    ('PERIODIC TABLE', 'Science'), ('BLACK HOLE', 'Science'),
    ('SPEED OF LIGHT', 'Science'), ('DOUBLE HELIX', 'Science'),
    ('GOALKEEPER GLOVES', 'Sport'), ('WOODEN SPOON', 'Sport'),
    ('PHOTO FINISH', 'Sport'), ('HOLE IN ONE', 'Sport'),
    ('WEATHER FORECAST', 'Everyday'), ('CUP OF TEA', 'Everyday'),
    ('WASHING LINE', 'Everyday'), ('CORNER SHOP', 'Everyday'),
    ('BANK HOLIDAY', 'Everyday'), ('QUEUE JUMPER', 'Everyday'),
    ('PUB QUIZ MACHINE', 'Quiz Night'), ('TIE BREAKER', 'Quiz Night'),
    ('PICTURE ROUND', 'Quiz Night'), ('FULL MARKS', 'Quiz Night'),
]

# ---------------------------------------------------------------------------
# Boggle dice (classic 16-dice distribution, Qu treated as Q)
# ---------------------------------------------------------------------------

BOGGLE_DICE = [
    'AAEEGN', 'ABBJOO', 'ACHOPS', 'AFFKPS', 'AOOTTW', 'CIMOTU', 'DEILRX',
    'DELRVY', 'DISTTY', 'EEGHNW', 'EEINSU', 'EHRTVW', 'EIOSST', 'ELRTTY',
    'HIMNQU', 'HLNNRZ',
]

# Letter frequency bag used for the word wheel / letter grids
LETTER_BAG = ('AAAAAAAAABBCCDDDDEEEEEEEEEEEEFFGGGHHIIIIIIIIIJKLLLLMMNNNNNN'
              'OOOOOOOOPPQRRRRRRSSSSTTTTTTUUUUVVWWXYYZ')

# Nine-letter words for the word wheel; centre letter is index 0 after shuffle
WHEEL_WORDS = [
    'BREAKFAST', 'CHOCOLATE', 'DANGEROUS', 'ELEPHANTS', 'FANTASTIC',
    'GOALPOSTS', 'HEDGEHOGS', 'IMPORTANT', 'JELLYFISH', 'KNOWLEDGE',
    'LIGHTNING', 'MOUNTAINS', 'NEWSPAPER', 'ORCHESTRA', 'PINEAPPLE',
    'RASPBERRY', 'SCARECROW', 'TELEPHONE', 'UMBRELLAS', 'VEGETABLE',
    'WATERFALL', 'YESTERDAY', 'ADVENTURE', 'BUTTERFLY', 'CELEBRATE',
    'DETECTIVE', 'EDUCATION', 'FIREPLACE', 'GOLDFINCH', 'HAMBURGER',
]

# ---------------------------------------------------------------------------
# Sorting buckets ("Sort It")
# ---------------------------------------------------------------------------

SORT_SETS = [
    {'title': 'Fruit or Vegetable?', 'buckets': ['Fruit', 'Vegetable'],
     'items': [('Tomato', 'Fruit'), ('Rhubarb', 'Vegetable'), ('Avocado', 'Fruit'),
               ('Courgette', 'Fruit'), ('Parsnip', 'Vegetable'), ('Mango', 'Fruit'),
               ('Leek', 'Vegetable'), ('Olive', 'Fruit'), ('Celery', 'Vegetable'),
               ('Pomegranate', 'Fruit'), ('Swede', 'Vegetable'), ('Cucumber', 'Fruit')]},
    {'title': 'Which Continent?', 'buckets': ['Europe', 'Asia', 'Africa'],
     'items': [('Portugal', 'Europe'), ('Vietnam', 'Asia'), ('Namibia', 'Africa'),
               ('Latvia', 'Europe'), ('Nepal', 'Asia'), ('Ghana', 'Africa'),
               ('Croatia', 'Europe'), ('Laos', 'Asia'), ('Zambia', 'Africa'),
               ('Slovenia', 'Europe'), ('Bhutan', 'Asia'), ('Senegal', 'Africa')]},
    {'title': 'Mammal, Bird or Fish?', 'buckets': ['Mammal', 'Bird', 'Fish'],
     'items': [('Dolphin', 'Mammal'), ('Puffin', 'Bird'), ('Haddock', 'Fish'),
               ('Bat', 'Mammal'), ('Heron', 'Bird'), ('Pike', 'Fish'),
               ('Otter', 'Mammal'), ('Kestrel', 'Bird'), ('Mackerel', 'Fish'),
               ('Hedgehog', 'Mammal'), ('Wren', 'Bird'), ('Halibut', 'Fish')]},
    {'title': 'Which Decade Was The Hit?', 'buckets': ['1960s', '1980s', '2000s'],
     'items': [('Hey Jude', '1960s'), ('Thriller', '1980s'), ('Hey Ya', '2000s'),
               ('Satisfaction', '1960s'), ('Sweet Dreams', '1980s'), ('Crazy In Love', '2000s'),
               ('Good Vibrations', '1960s'), ('Billie Jean', '1980s'), ('Mr Brightside', '2000s'),
               ('Respect', '1960s'), ('Like A Prayer', '1980s'), ('Rehab', '2000s')]},
    {'title': 'Metal, Gas or Liquid?', 'buckets': ['Metal', 'Gas', 'Liquid'],
     'items': [('Titanium', 'Metal'), ('Helium', 'Gas'), ('Mercury', 'Liquid'),
               ('Zinc', 'Metal'), ('Argon', 'Gas'), ('Bromine', 'Liquid'),
               ('Nickel', 'Metal'), ('Neon', 'Gas'), ('Petrol', 'Liquid'),
               ('Cobalt', 'Metal'), ('Radon', 'Gas'), ('Glycerol', 'Liquid')]},
    {'title': 'Sport: Ball, Bat or Neither?', 'buckets': ['Ball Only', 'Bat & Ball', 'Neither'],
     'items': [('Netball', 'Ball Only'), ('Cricket', 'Bat & Ball'), ('Judo', 'Neither'),
               ('Basketball', 'Ball Only'), ('Baseball', 'Bat & Ball'), ('Fencing', 'Neither'),
               ('Rugby', 'Ball Only'), ('Rounders', 'Bat & Ball'), ('Archery', 'Neither'),
               ('Volleyball', 'Ball Only'), ('Softball', 'Bat & Ball'), ('Rowing', 'Neither')]},
]

# ---------------------------------------------------------------------------
# Lexicon
# ---------------------------------------------------------------------------

_LEXICON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'data', 'qm-lexicon.json'
)


@lru_cache(maxsize=1)
def lexicon() -> tuple:
    """The whole word list, sorted. Cached for the life of the process."""
    try:
        with open(_LEXICON_PATH, encoding='utf-8') as fh:
            return tuple(json.load(fh))
    except Exception:
        return tuple()


@lru_cache(maxsize=12)
def words_of_length(n: int) -> tuple:
    return tuple(w for w in lexicon() if len(w) == n)


# ---------------------------------------------------------------------------
# The full dictionary
# ---------------------------------------------------------------------------
# Held in the process as one read-only frozenset, so every word game and every
# player checks against the same copy. 315,000 words is far too much to send to
# a phone, so the browser keeps the small list above for instant answers and
# asks the server about anything it does not recognise.

_DICTIONARY_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'words-en.txt.gz'
)


@lru_cache(maxsize=1)
def dictionary() -> frozenset:
    """Every word the games will accept. Empty if the file is missing."""
    import gzip
    try:
        with gzip.open(_DICTIONARY_PATH, 'rt', encoding='utf-8') as fh:
            return frozenset(line.strip() for line in fh if line.strip())
    except Exception:
        return frozenset()


def is_word(candidate: str) -> bool:
    word = re.sub(r'[^A-Za-z]', '', candidate or '').lower()
    if not word:
        return False
    words = dictionary()
    if words:
        return word in words
    # No dictionary file: fall back to the harvested list rather than
    # rejecting everything a player types.
    return word in set(lexicon())


@lru_cache(maxsize=12)
def dictionary_words_of_length(n: int) -> tuple:
    """Every dictionary word of one length, for the games that can inline them."""
    words = dictionary()
    if not words:
        return words_of_length(n)
    return tuple(sorted(w for w in words if len(w) == n))


# ---------------------------------------------------------------------------
# Word ladder
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _ladder_graph() -> dict:
    """Adjacency map over four-letter words differing by exactly one letter.

    Built from the harvested common-word list rather than the full dictionary,
    so the rungs of a generated ladder are words people have actually heard of.
    Players may still climb using anything in the full dictionary.
    """
    words = [w for w in words_of_length(4)]
    buckets = {}
    for w in words:
        for i in range(4):
            buckets.setdefault(w[:i] + '_' + w[i + 1:], []).append(w)
    graph = {w: set() for w in words}
    for group in buckets.values():
        for a in group:
            for b in group:
                if a != b:
                    graph[a].add(b)
    return {w: tuple(sorted(n)) for w, n in graph.items()}


def word_ladder(rng=None, steps=4):
    """Find a start/end pair exactly `steps` moves apart, plus one valid route."""
    rng = rng or random
    graph = _ladder_graph()
    if not graph:
        return None
    candidates = [w for w, n in graph.items() if len(n) >= 3]
    if not candidates:
        return None

    for _ in range(60):
        start = rng.choice(candidates)
        # Breadth-first search outwards, remembering how we got to each word
        frontier = [start]
        came_from = {start: None}
        depth = {start: 0}
        reached = []
        while frontier:
            nxt = []
            for word in frontier:
                if depth[word] >= steps:
                    continue
                for neighbour in graph.get(word, ()):
                    if neighbour in came_from:
                        continue
                    came_from[neighbour] = word
                    depth[neighbour] = depth[word] + 1
                    if depth[neighbour] == steps:
                        reached.append(neighbour)
                    nxt.append(neighbour)
            frontier = nxt
        if not reached:
            continue
        end = rng.choice(reached)
        route = [end]
        while came_from[route[-1]] is not None:
            route.append(came_from[route[-1]])
        route.reverse()
        return {'start': start.upper(), 'end': end.upper(),
                'steps': steps, 'solution': [w.upper() for w in route]}
    return None


# ---------------------------------------------------------------------------
# Trivia clues & crossword
# ---------------------------------------------------------------------------

def trivia_clues(min_len=3, max_len=9, limit=400, rng=None, difficulties=None,
                 exclude_categories=None, max_clue_chars=0):
    """Single-word trivia answers paired with their question, for word puzzles.

    Pass an rng to make the selection repeatable: the rows come back in id
    order and are shuffled with that generator instead of being randomised by
    the database. The daily puzzle needs this, because every web worker has to
    build the identical grid from the same date.
    """
    from ..models import QuizQuestion, db
    from sqlalchemy.sql.expression import func

    query = QuizQuestion.query.filter(
        QuizQuestion.question_type == 'classic',
        db.or_(QuizQuestion.status == 'approved', QuizQuestion.status.is_(None)),
    )
    if difficulties:
        query = query.filter(QuizQuestion.difficulty.in_(list(difficulties)))
    if exclude_categories:
        query = query.filter(~QuizQuestion.category_slug.in_(list(exclude_categories)))

    if rng is not None:
        rows = query.order_by(QuizQuestion.id.asc()).all()
        rng.shuffle(rows)
        rows = rows[:limit * 6]
    else:
        rows = query.order_by(func.random()).limit(limit * 6).all()

    out = []
    seen = set()
    for q in rows:
        answer = (q.get_options().get(q.correct_option) or '').strip()
        if not re.fullmatch(r'[A-Za-z]{%d,%d}' % (min_len, max_len), answer):
            continue
        key = answer.upper()
        if key in seen:
            continue
        seen.add(key)
        clue = re.sub(r'\s+', ' ', (q.prompt or '')).strip()
        # Some prompts run to two hundred characters. That is fine in a duel,
        # where one question fills the screen, but a crossword shows every
        # clue at once and a wall of prose is unreadable on a phone.
        if max_clue_chars and len(clue) > max_clue_chars:
            continue
        out.append({'answer': key, 'clue': clue, 'category': q.category_name or 'Trivia'})
        if len(out) >= limit:
            break
    return out


_COMMON_WORDS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'crossword_words.json'
)


@lru_cache(maxsize=1)
def _common_words():
    """Everyday words with plain clues, loaded once.

    The trivia bank only yields about 550 usable single-word answers, and the
    bulk of them are nutrition, anatomy and linguistics questions, so a grid
    built from it alone reads like a medical exam. It is also desperately
    short of three- and four-letter words — fifteen of the former in the whole
    bank — which are exactly what interlocks a grid.
    """
    try:
        with open(_COMMON_WORDS_PATH, encoding='utf-8') as fh:
            raw = json.load(fh).get('words') or []
    except (OSError, ValueError):
        return []
    out = []
    for item in raw:
        answer = (item.get('a') or '').strip().upper()
        clue = (item.get('c') or '').strip()
        if not answer or not clue:
            continue
        out.append({'answer': answer, 'clue': clue,
                    'category': 'Everyday', 'band': item.get('b') or 'easy'})
    return out


def common_clues(min_len=3, max_len=9, bands=None):
    """The everyday words that fit a grid of this size."""
    wanted = set(bands) if bands else None
    return [dict(c) for c in _common_words()
            if min_len <= len(c['answer']) <= max_len
            and (wanted is None or c['band'] in wanted)]


def _place_fits(grid, size, word, row, col, horizontal):
    """How many letters this placement would share with words already down.

    Returns False when the placement is illegal, otherwise the number of
    crossings (0 for a word that touches nothing).
    """
    length = len(word)
    if horizontal:
        if col < 0 or col + length > size or not (0 <= row < size):
            return False
    else:
        if row < 0 or row + length > size or not (0 <= col < size):
            return False

    crossings = 0
    for i, ch in enumerate(word):
        r = row + (0 if horizontal else i)
        c = col + (i if horizontal else 0)
        cell = grid[r][c]
        if cell is not None:
            if cell != ch:
                return False
            crossings += 1
        else:
            # A new letter must not brush up against a parallel word
            if horizontal:
                if r > 0 and grid[r - 1][c] is not None:
                    return False
                if r < size - 1 and grid[r + 1][c] is not None:
                    return False
            else:
                if c > 0 and grid[r][c - 1] is not None:
                    return False
                if c < size - 1 and grid[r][c + 1] is not None:
                    return False

    # The cells immediately before and after the word must be empty
    if horizontal:
        if col > 0 and grid[row][col - 1] is not None:
            return False
        if col + length < size and grid[row][col + length] is not None:
            return False
    else:
        if row > 0 and grid[row - 1][col] is not None:
            return False
        if row + length < size and grid[row + length][col] is not None:
            return False
    return crossings


def _compile_attempt(pool, size, target_words, rng):
    """One go at building a grid. Returns (placed, quality) or (None, -1).

    Where the old compiler took each word in turn and hooked it onto the first
    thing that would take it, this looks at every remaining word at every step
    and places whichever one interlocks best. That difference is the whole
    point: hooking words onto the first long one in order produces a comb -
    one spine with teeth hanging off it, every word crossing exactly once and
    no word helping you with any other. Choosing the best available placement
    each time lets short words bridge two long ones, which is what makes
    guessing one answer worth something for the next.
    """
    grid = [[None] * size for _ in range(size)]
    placed = []

    def write(word, row, col, horizontal):
        for i, ch in enumerate(word):
            r = row + (0 if horizontal else i)
            c = col + (i if horizontal else 0)
            grid[r][c] = ch

    remaining = list(pool)
    if not remaining:
        return None, -1

    # Seed with a long word across the middle; everything else grows off it.
    long_enough = [c for c in remaining if len(c['answer']) >= min(6, size)]
    seed = rng.choice(long_enough) if long_enough else remaining[0]
    remaining.remove(seed)
    seed_row = size // 2
    seed_col = max(0, (size - len(seed['answer'])) // 2)
    write(seed['answer'], seed_row, seed_col, True)
    placed.append({'entry': seed, 'row': seed_row, 'col': seed_col,
                   'horizontal': True, 'crossings': 0})

    centre = (size - 1) / 2.0

    while len(placed) < target_words and remaining:
        best = None
        for cand in remaining:
            word = cand['answer']
            for p in placed:
                p_word = p['entry']['answer']
                for pi, p_ch in enumerate(p_word):
                    pr = p['row'] + (0 if p['horizontal'] else pi)
                    pc = p['col'] + (pi if p['horizontal'] else 0)
                    for wi, w_ch in enumerate(word):
                        if w_ch != p_ch:
                            continue
                        horizontal = not p['horizontal']
                        row = pr if horizontal else pr - wi
                        col = pc - wi if horizontal else pc
                        crossings = _place_fits(grid, size, word, row, col, horizontal)
                        if not crossings:
                            continue
                        # Crossings dominate everything else, then length, then
                        # staying near the middle so the grid does not sprawl.
                        mid_r = row + (0 if horizontal else len(word) / 2.0)
                        mid_c = col + (len(word) / 2.0 if horizontal else 0)
                        drift = abs(mid_r - centre) + abs(mid_c - centre)
                        score = crossings * 1000 + len(word) * 8 - drift
                        if best is None or score > best[0]:
                            best = (score, cand, row, col, horizontal, crossings)
        if best is None:
            break
        _, cand, row, col, horizontal, crossings = best
        write(cand['answer'], row, col, horizontal)
        placed.append({'entry': cand, 'row': row, 'col': col,
                       'horizontal': horizontal, 'crossings': crossings})
        remaining.remove(cand)

    if len(placed) < 4:
        return None, -1

    # How well knitted together it came out. Words that cross more than once
    # are what a solver actually feels, so they count for most.
    total = sum(p['crossings'] for p in placed)
    multi = sum(1 for p in placed if p['crossings'] >= 2)
    quality = total * 3 + multi * 10 + len(placed)
    return placed, quality


# Trivia categories whose single-word answers are almost all specialist terms.
# Nutrition, anatomy and linguistics between them supply a third of the whole
# clue pool, which is why grids kept coming out readable only by a doctor.
SPECIALIST_CATEGORIES = ('nutrition-diet', 'human-body', 'languages-linguistics')


def crossword_puzzle(rng=None, size=9, target_words=7, difficulties=None,
                     deterministic=False, attempts=14, easy_mix=0.35,
                     everyday=0.6, avoid_specialist=True):
    """Compile a small interlocking crossword from trivia and everyday clues.

    Builds the grid several times over and keeps the best knitted one. A
    single greedy pass is at the mercy of which word it happened to start
    with, and a bad start cannot be recovered from once words are down.

    easy_mix salts the pool with easier questions whatever band was asked for,
    so a hard grid still has a way in rather than being uniformly obscure.

    everyday is the share of the pool drawn from the plain-English clue bank
    instead of the trivia questions. That bank is what makes a grid solvable
    by someone who is not a specialist, and it is also where nearly all the
    short words come from, so turning it down costs interlocking as well as
    approachability.
    """
    rng = rng or random
    # Nothing longer than the grid itself, or the seed word runs off the edge.
    longest = min(9, size)
    seeded = rng if deterministic else None
    skip = SPECIALIST_CATEGORIES if avoid_specialist else None

    def fetch(bands):
        return [c for c in trivia_clues(min_len=3, max_len=longest, limit=900,
                                        rng=seeded, difficulties=bands,
                                        exclude_categories=skip,
                                        max_clue_chars=110)
                if 3 <= len(c["answer"]) <= longest]

    pool = fetch(difficulties)
    if difficulties and easy_mix > 0 and 'easy' not in difficulties:
        easy = fetch(['easy'])
        want = int(len(pool) * easy_mix)
        if easy and want:
            rng.shuffle(easy)
            known = {c['answer'] for c in pool}
            pool += [c for c in easy if c['answer'] not in known][:want]

    if everyday > 0:
        # A share of the grid, not a top-up: the trivia pool is big enough to
        # crowd these out entirely if they are merely appended.
        bands = ['easy'] if (difficulties == ['easy']) else None
        plain = common_clues(3, longest, bands=bands)
        if plain:
            rng.shuffle(plain)
            known = {c['answer'] for c in pool}
            plain = [c for c in plain if c['answer'] not in known]
            if everyday >= 1:
                pool = plain
            else:
                # Trim the trivia side so the everyday words really are that
                # share of what the compiler gets to choose from — and do it
                # length by length. Blending on the whole pool is not enough:
                # the compiler reaches for long words first, and the trivia
                # answers are much the longer of the two sets, so every long
                # slot in the grid went to a trivia clue however the overall
                # ratio was set.
                by_len = {}
                for clue in plain:
                    by_len.setdefault(len(clue['answer']), 0)
                    by_len[len(clue['answer'])] += 1
                buckets = {}
                rng.shuffle(pool)
                for clue in pool:
                    buckets.setdefault(len(clue['answer']), []).append(clue)
                trimmed = []
                for length, clues in buckets.items():
                    # No everyday words this long means the trivia bank is the
                    # only source for the slot, so keep them all.
                    available = by_len.get(length, 0)
                    if not available:
                        trimmed += clues
                        continue
                    keep = int(available * (1 - everyday) / everyday) or 1
                    trimmed += clues[:keep]
                pool = trimmed + plain

    if len(pool) < 4:
        return None

    best_placed, best_quality = None, -1
    for attempt in range(max(1, attempts)):
        shuffled = list(pool)
        rng.shuffle(shuffled)
        # Longer words first within the shuffle: they give later words more
        # letters to hook onto, without fixing the order the way sorting did.
        shuffled.sort(key=lambda c: -len(c['answer']) if attempt % 2 == 0 else 0)
        placed, quality = _compile_attempt(shuffled, size, target_words, rng)
        if placed and quality > best_quality:
            best_placed, best_quality = placed, quality

    if not best_placed:
        return None
    placed = best_placed

    # Crop to the used area so the grid is tight on a phone screen
    rows_used = [p['row'] for p in placed] + [
        p['row'] + (0 if p['horizontal'] else len(p['entry']['answer']) - 1) for p in placed]
    cols_used = [p['col'] for p in placed] + [
        p['col'] + (len(p['entry']['answer']) - 1 if p['horizontal'] else 0) for p in placed]
    r0, r1 = min(rows_used), max(rows_used)
    c0, c1 = min(cols_used), max(cols_used)

    entries = []
    for p in placed:
        entries.append({
            'answer': p['entry']['answer'],
            'clue': p['entry']['clue'],
            'row': p['row'] - r0,
            'col': p['col'] - c0,
            'dir': 'across' if p['horizontal'] else 'down',
        })
    # Number entries the way a crossword does: reading order of their first cell
    entries.sort(key=lambda e: (e['row'], e['col'], e['dir']))
    numbers = {}
    n = 0
    for e in entries:
        cell = (e['row'], e['col'])
        if cell not in numbers:
            n += 1
            numbers[cell] = n
        e['number'] = numbers[cell]
    entries.sort(key=lambda e: (e['number'], e['dir']))

    return {'rows': r1 - r0 + 1, 'cols': c1 - c0 + 1, 'entries': entries}


# ---------------------------------------------------------------------------
# The daily crossword
# ---------------------------------------------------------------------------
# One puzzle a day, the same for everybody, which gets harder as the week goes
# on and starts again on Monday. A difficulty that only ever climbs would be
# unsolvable within a few months, so this follows the newspaper convention:
# Monday is a warm-up, Saturday is the brute, Sunday is a big friendly one.

# 'everyday' is the share of the clue pool taken from the plain-English bank
# rather than the trivia questions. It is the week's real difficulty dial:
# Monday is almost all everyday words, Saturday leans on the trivia bank.
DAILY_LADDER = {
    0: {'name': 'Monday',    'size': 7,  'words': 6,  'tier': 'Warm-up',   'difficulties': ['easy'],
        'everyday': 0.95, 'seconds': 300, 'blurb': 'A gentle start to the week.'},
    1: {'name': 'Tuesday',   'size': 8,  'words': 7,  'tier': 'Steady',    'difficulties': ['easy', 'medium'],
        'everyday': 0.8, 'seconds': 330, 'blurb': 'A little more to chew on.'},
    2: {'name': 'Wednesday', 'size': 9,  'words': 8,  'tier': 'Midweek',   'difficulties': ['easy', 'medium'],
        'everyday': 0.7, 'seconds': 360, 'blurb': 'Halfway, and it knows it.'},
    3: {'name': 'Thursday',  'size': 9,  'words': 9,  'tier': 'Tricky',    'difficulties': ['medium'],
        'everyday': 0.55, 'seconds': 390, 'blurb': 'The clues stop being generous.'},
    4: {'name': 'Friday',    'size': 10, 'words': 10,  'tier': 'Testing',   'difficulties': ['medium', 'hard'],
        'everyday': 0.45, 'seconds': 420, 'blurb': 'Earn your weekend.'},
    5: {'name': 'Saturday',  'size': 11, 'words': 11, 'tier': 'The Brute', 'difficulties': ['medium', 'hard'],
        'everyday': 0.35, 'seconds': 480, 'blurb': 'The hardest grid of the week.'},
    6: {'name': 'Sunday',    'size': 10, 'words': 10,  'tier': 'The Big One', 'difficulties': ['easy', 'medium', 'hard'],
        'everyday': 0.6, 'seconds': 480, 'blurb': 'A large one to do over a long breakfast.'},
}


def daily_spec(day):
    """The shape of the puzzle for a given date."""
    spec = dict(DAILY_LADDER[day.weekday()])
    spec['date'] = day
    spec['key'] = 'crossword-%s' % day.isoformat()
    return spec


@lru_cache(maxsize=8)
def _daily_crossword_cached(iso_date: str, size: int, words: int, difficulties: tuple,
                            everyday: float = 0.6):
    # Seeded from the date, so every web worker builds the identical grid and
    # the puzzle only has to be compiled once a day rather than once a request.
    seed = int(iso_date.replace('-', ''))
    rng = random.Random(seed)
    puzzle = crossword_puzzle(rng, size=size, target_words=words,
                              difficulties=list(difficulties), deterministic=True,
                              everyday=everyday)
    if not puzzle:
        # A thin difficulty band can starve the compiler; fall back to the
        # whole question bank rather than showing nobody a puzzle.
        rng = random.Random(seed)
        puzzle = crossword_puzzle(rng, size=size, target_words=words,
                                  deterministic=True, everyday=everyday)
    return puzzle


def daily_crossword(day):
    spec = daily_spec(day)
    puzzle = _daily_crossword_cached(
        day.isoformat(), spec['size'], spec['words'], tuple(spec['difficulties']),
        spec.get('everyday', 0.6)
    )
    return spec, puzzle


# ---------------------------------------------------------------------------
# Images from the question bank (flags, badges, logos, country shapes)
# ---------------------------------------------------------------------------

IMAGE_SETS = {
    'match-flags': {'label': 'World Flags', 'icon': '🏴'},
    'football-badges': {'label': 'Club Badges', 'icon': '⚽'},
    'brand-logos': {'label': 'Brand Logos', 'icon': '🏷️'},
    'country-shapes': {'label': 'Country Shapes', 'icon': '🗺️'},
}


def image_pairs(category_slug=None, limit=60):
    """Distinct (image, label) pairs harvested from the visual question packs."""
    from ..models import QuizQuestion, db

    query = QuizQuestion.query.filter(
        QuizQuestion.question_type == 'image',
        QuizQuestion.media_url != '',
        QuizQuestion.media_url.isnot(None),
        db.or_(QuizQuestion.status == 'approved', QuizQuestion.status.is_(None)),
    )
    if category_slug:
        query = query.filter(QuizQuestion.category_slug == category_slug)

    seen = {}
    for q in query.all():
        url = q.media_url
        if url in seen:
            continue
        label = (q.get_options().get(q.correct_option) or '').strip()
        if not label:
            continue
        seen[url] = {'url': url, 'label': label, 'set': q.category_slug}
        if len(seen) >= limit:
            break
    return list(seen.values())


# ---------------------------------------------------------------------------
# Small helpers shared by several games
# ---------------------------------------------------------------------------

def shuffled(items, rng=None):
    out = list(items)
    (rng or random).shuffle(out)
    return out


def roll_boggle(rng=None):
    rng = rng or random
    dice = shuffled(BOGGLE_DICE, rng)
    return [rng.choice(die) for die in dice]


def wheel_puzzle(rng=None):
    """Nine letters with one compulsory centre letter, plus every word in them."""
    rng = rng or random
    word = rng.choice(WHEEL_WORDS)
    letters = list(word)
    rng.shuffle(letters)
    centre = letters[0]
    import collections
    available = collections.Counter(letters)

    solutions = []
    for candidate in (dictionary() or set(lexicon())):
        if len(candidate) < 3 or centre.lower() not in candidate:
            continue
        need = collections.Counter(candidate.upper())
        if all(available.get(ch, 0) >= cnt for ch, cnt in need.items()):
            solutions.append(candidate.upper())
    # The nine-letter word is the whole point of the round, so it counts even
    # when the harvested lexicon happens not to carry it.
    solutions.append(word)
    return {
        'centre': centre,
        'outer': letters[1:],
        'solutions': sorted(set(solutions), key=lambda w: (-len(w), w)),
    }
