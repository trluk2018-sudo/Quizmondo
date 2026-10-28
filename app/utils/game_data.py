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

def trivia_clues(min_len=3, max_len=9, limit=400):
    """Single-word trivia answers paired with their question, for word puzzles."""
    from ..models import QuizQuestion, db
    from sqlalchemy.sql.expression import func

    rows = QuizQuestion.query.filter(
        QuizQuestion.question_type == 'classic',
        db.or_(QuizQuestion.status == 'approved', QuizQuestion.status.is_(None)),
    ).order_by(func.random()).limit(limit * 6).all()

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
        out.append({'answer': key, 'clue': clue, 'category': q.category_name or 'Trivia'})
        if len(out) >= limit:
            break
    return out


def crossword_puzzle(rng=None, size=9, target_words=7):
    """Compile a small interlocking crossword from real trivia clues.

    Classic greedy compiler: seed with one long word, then keep trying to hook
    the next word onto a letter already on the grid, rejecting any placement
    that would create accidental adjacent lettering.
    """
    rng = rng or random
    pool = [c for c in trivia_clues(min_len=4, max_len=9, limit=260) if len(c['answer']) >= 4]
    if len(pool) < 4:
        return None
    rng.shuffle(pool)
    pool.sort(key=lambda c: -len(c['answer']))

    grid = [[None] * size for _ in range(size)]
    placed = []

    def fits(word, row, col, horizontal):
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

    def write(word, row, col, horizontal):
        for i, ch in enumerate(word):
            r = row + (0 if horizontal else i)
            c = col + (i if horizontal else 0)
            grid[r][c] = ch

    # Seed: longest available word across the middle
    seed = pool.pop(0)
    seed_row = size // 2
    seed_col = max(0, (size - len(seed['answer'])) // 2)
    write(seed['answer'], seed_row, seed_col, True)
    placed.append({'entry': seed, 'row': seed_row, 'col': seed_col, 'horizontal': True})

    for cand in pool:
        if len(placed) >= target_words:
            break
        word = cand['answer']
        options = []
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
                    crossings = fits(word, row, col, horizontal)
                    if crossings:
                        options.append((crossings, row, col, horizontal))
        if not options:
            continue
        rng.shuffle(options)
        options.sort(key=lambda o: -o[0])
        _, row, col, horizontal = options[0]
        write(word, row, col, horizontal)
        placed.append({'entry': cand, 'row': row, 'col': col, 'horizontal': horizontal})

    if len(placed) < 4:
        return None

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
