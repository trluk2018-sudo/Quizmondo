"""Initial question seed and pack catalog for Quizmondo Arena."""
import json
from ..models import db, QuizQuestion, QuizPack, PubLeague

SEED_PACKS = [
    {
        'title': 'Science & Cosmos Odyssey',
        'slug': 'science-cosmos',
        'description': 'Astrophysics, planetary science, chemistry, and cosmological mysteries.',
        'icon': '🚀',
        'category_slug': 'science-cosmos',
        'questions': [
            {
                'prompt': 'Which planet in our solar system has the highest number of confirmed moons?',
                'options': {'A': 'Jupiter', 'B': 'Saturn', 'C': 'Uranus', 'D': 'Neptune'},
                'correct': 'B',
                'explanation': 'Saturn has 146 confirmed moons officially recognized by the IAU, surpassing Jupiter\'s 95.',
                'difficulty': 'medium'
            },
            {
                'prompt': 'What is the chemical symbol for the precious metal Gold?',
                'options': {'A': 'Ag', 'B': 'Fe', 'C': 'Au', 'D': 'Gd'},
                'correct': 'C',
                'explanation': 'Au comes from the Latin word "Aurum", meaning shining dawn.',
                'difficulty': 'easy'
            },
            {
                'prompt': 'Approximately how long does light from the Sun take to reach planet Earth?',
                'options': {'A': '8 minutes and 20 seconds', 'B': '30 seconds', 'C': '4 minutes and 10 seconds', 'D': '12 minutes and 45 seconds'},
                'correct': 'A',
                'explanation': 'At a distance of roughly 150 million km, sunlight takes approximately 8 minutes and 20 seconds (500 seconds) to reach Earth.',
                'difficulty': 'medium'
            },
            {
                'prompt': 'Which particle is known as the mediator of the electromagnetic force?',
                'options': {'A': 'Gluon', 'B': 'Photon', 'C': 'W Boson', 'D': 'Graviton'},
                'correct': 'B',
                'explanation': 'Photons are the gauge bosons responsible for mediating electromagnetic interactions.',
                'difficulty': 'hard'
            }
        ]
    },
    {
        'title': 'Retro Gaming & Microcomputing',
        'slug': 'gaming-esports',
        'description': '8-bit arcades, 16-bit consoles, legendary speedruns, and microcomputer lore.',
        'icon': '🕹️',
        'category_slug': 'gaming-esports',
        'questions': [
            {
                'prompt': 'In which year did the Nintendo Entertainment System (NES) launch in North America?',
                'options': {'A': '1983', 'B': '1985', 'C': '1988', 'D': '1990'},
                'correct': 'B',
                'explanation': 'The NES test-launched in New York in October 1985 before its nationwide North American rollout in 1986.',
                'difficulty': 'medium'
            },
            {
                'prompt': 'What sound synthesizer chip powered the iconic Commodore 64 home computer?',
                'options': {'A': 'Yamaha YM2612', 'B': 'MOS Technology 6581 SID', 'C': 'General Instrument AY-3-8910', 'D': 'Texas Instruments SN76489'},
                'correct': 'B',
                'explanation': 'The MOS 6581/8580 SID (Sound Interface Device) gave the C64 its revolutionary 3-channel audio synthesis.',
                'difficulty': 'hard'
            },
            {
                'prompt': 'What was Mario originally called in the 1981 arcade game Donkey Kong?',
                'options': {'A': 'Jumpman', 'B': 'Plumber Pete', 'C': 'Buster', 'D': 'Luigi'},
                'correct': 'A',
                'explanation': 'Shigeru Miyamoto originally named the carpenter character "Jumpman" before he was christened Mario.',
                'difficulty': 'easy'
            },
            {
                'prompt': 'Which classic 1993 first-person shooter was created by id Software pioneers John Carmack and John Romero?',
                'options': {'A': 'Wolfenstein 3D', 'B': 'DOOM', 'C': 'Quake', 'D': 'Hexen'},
                'correct': 'B',
                'explanation': 'DOOM was released as shareware in December 1993, defining network multiplayer and 3D PC gaming.',
                'difficulty': 'easy'
            }
        ]
    },
    {
        'title': 'World Geography & Lost Civilizations',
        'slug': 'world-history',
        'description': 'Ancient world wonders, global capital cities, cartography, and archaeological puzzles.',
        'icon': '🌍',
        'category_slug': 'world-history',
        'questions': [
            {
                'prompt': 'Which ancient wonder of the world was located in the city of Alexandria, Egypt?',
                'options': {'A': 'The Hanging Gardens', 'B': 'The Colossus', 'C': 'The Pharos Lighthouse', 'D': 'The Mausoleum at Halicarnassus'},
                'correct': 'C',
                'explanation': 'The Lighthouse of Alexandria (Pharos), built by the Ptolemaic Kingdom around 280 BC, was one of the Seven Wonders.',
                'difficulty': 'medium'
            },
            {
                'prompt': 'What is the capital city of Australia?',
                'options': {'A': 'Sydney', 'B': 'Melbourne', 'C': 'Canberra', 'D': 'Brisbane'},
                'correct': 'C',
                'explanation': 'Canberra was chosen as the compromise capital of Australia in 1908 to resolve the rivalry between Sydney and Melbourne.',
                'difficulty': 'easy'
            },
            {
                'prompt': 'Which river is officially recognized as the longest in the world by the majority of geographers?',
                'options': {'A': 'Amazon River', 'B': 'Nile River', 'C': 'Yangtze River', 'D': 'Mississippi-Missouri'},
                'correct': 'B',
                'explanation': 'The Nile stretches approximately 6,650 km through northeastern Africa, historically ranking as the longest.',
                'difficulty': 'medium'
            },
            {
                'prompt': 'In which modern-day country would you find the ruins of the ancient city of Persepolis?',
                'options': {'A': 'Iraq', 'B': 'Iran', 'C': 'Turkey', 'D': 'Jordan'},
                'correct': 'B',
                'explanation': 'Persepolis was the ceremonial capital of the Achaemenid Empire, located near modern-day Shiraz, Iran.',
                'difficulty': 'hard'
            }
        ]
    },
    {
        'title': 'Pop Culture & Cinema Titans',
        'slug': 'tv-cinema',
        'description': 'Legendary cinema directors, cult television classics, and blockbuster movie quotes.',
        'icon': '🎬',
        'category_slug': 'tv-cinema',
        'questions': [
            {
                'prompt': 'Who directed the 1994 sci-fi action masterpiece "Pulp Fiction"?',
                'options': {'A': 'Martin Scorsese', 'B': 'Quentin Tarantino', 'C': 'David Fincher', 'D': 'Steven Spielberg'},
                'correct': 'B',
                'explanation': 'Quentin Tarantino wrote and directed Pulp Fiction, winning the Palme d\'Or at Cannes in 1994.',
                'difficulty': 'easy'
            },
            {
                'prompt': 'In The Matrix (1999), what color pill does Neo take to wake up in the real world?',
                'options': {'A': 'Blue', 'B': 'Red', 'C': 'Green', 'D': 'Yellow'},
                'correct': 'B',
                'explanation': 'Morpheus explains: "You take the blue pill—the story ends... You take the red pill—you stay in Wonderland, and I show you how deep the rabbit hole goes."',
                'difficulty': 'easy'
            },
            {
                'prompt': 'Which British actor portrayed the mysterious Tenth Doctor in the long-running BBC sci-fi series Doctor Who?',
                'options': {'A': 'Christopher Eccleston', 'B': 'Matt Smith', 'C': 'David Tennant', 'D': 'Peter Capaldi'},
                'correct': 'C',
                'explanation': 'David Tennant starred as the beloved Tenth Doctor from 2005 to 2010.',
                'difficulty': 'medium'
            }
        ]
    },
    {
        'title': 'Music & Rhythm Legends',
        'slug': 'pop-music',
        'description': 'From vinyl grooves to synthwave riffs: iconic bands, number one hits, and guitar solos.',
        'icon': '🎵',
        'category_slug': 'pop-music',
        'questions': [
            {
                'prompt': 'Which legendary band recorded the best-selling 1973 studio album "The Dark Side of the Moon"?',
                'options': {'A': 'Led Zeppelin', 'B': 'Pink Floyd', 'C': 'The Who', 'D': 'Queen'},
                'correct': 'B',
                'explanation': 'Pink Floyd\'s The Dark Side of the Moon spent over 950 weeks on the Billboard 200 chart.',
                'difficulty': 'easy'
            },
            {
                'prompt': 'Who released the 1982 album "Thriller", which remains the highest-selling album of all time?',
                'options': {'A': 'Prince', 'B': 'Michael Jackson', 'C': 'Stevie Wonder', 'D': 'Lionel Richie'},
                'correct': 'B',
                'explanation': 'Michael Jackson\'s Thriller has sold an estimated 70+ million copies worldwide.',
                'difficulty': 'easy'
            },
            {
                'prompt': 'What synthesizer brand made the legendary Minimoog analog synth launched in 1970?',
                'options': {'A': 'Roland', 'B': 'Moog', 'C': 'Korg', 'D': 'Yamaha'},
                'correct': 'B',
                'explanation': 'Robert Moog designed the Minimoog Model D, transforming popular electronic music.',
                'difficulty': 'medium'
            }
        ]
    },
    {
        'title': 'Sports & Championship Arenas',
        'slug': 'sports-arena',
        'description': 'World Cup finals, Olympic records, Wimbledon rallies, and motorsport podiums.',
        'icon': '🏆',
        'category_slug': 'sports-arena',
        'questions': [
            {
                'prompt': 'Which nation won the inaugural FIFA Men\'s World Cup tournament held in 1930?',
                'options': {'A': 'Argentina', 'B': 'Brazil', 'C': 'Uruguay', 'D': 'Italy'},
                'correct': 'C',
                'explanation': 'Host nation Uruguay defeated Argentina 4-2 in the final in Montevideo.',
                'difficulty': 'medium'
            },
            {
                'prompt': 'How many meters is an official Olympic standard swimming pool in length?',
                'options': {'A': '25 meters', 'B': '50 meters', 'C': '75 meters', 'D': '100 meters'},
                'correct': 'B',
                'explanation': 'Olympic standard long-course pools are exactly 50 meters in length.',
                'difficulty': 'easy'
            },
            {
                'prompt': 'Who holds the official world record for the men\'s 100-meter sprint at 9.58 seconds?',
                'options': {'A': 'Carl Lewis', 'B': 'Tyson Gay', 'C': 'Usain Bolt', 'D': 'Asafa Powell'},
                'correct': 'C',
                'explanation': 'Usain Bolt of Jamaica clocked 9.58 seconds at the 2009 World Athletics Championships in Berlin.',
                'difficulty': 'easy'
            }
        ]
    }
]


def seed_quizmondo_arena_defaults():
    """Ensure starter question packs and categories are seeded."""
    for pack_data in SEED_PACKS:
        pack = QuizPack.query.filter_by(slug=pack_data['slug']).first()
        if not pack:
            pack = QuizPack(
                title=pack_data['title'],
                slug=pack_data['slug'],
                description=pack_data['description'],
                icon=pack_data['icon'],
                category_slug=pack_data['category_slug'],
                is_community=False,
                author_name='Quizmondo Master',
                question_count=len(pack_data['questions'])
            )
            db.session.add(pack)
            db.session.flush()

        for q_item in pack_data['questions']:
            existing_q = QuizQuestion.query.filter_by(prompt=q_item['prompt']).first()
            if not existing_q:
                q = QuizQuestion(
                    prompt=q_item['prompt'],
                    question_type='classic',
                    options_json=json.dumps(q_item['options']),
                    correct_option=q_item['correct'],
                    explanation=q_item['explanation'],
                    category_slug=pack_data['category_slug'],
                    category_name=pack_data['title'],
                    difficulty=q_item.get('difficulty', 'medium'),
                    pack_slug=pack_data['slug'],
                    points=100,
                    time_limit=15
                )
                db.session.add(q)

    # Seed default Pub League demo
    if not PubLeague.query.first():
        league = PubLeague(
            name='The Dog & Partridge Quiz League',
            slug='dog-and-partridge',
            pin_code='7742',
            venue_name='The Dog & Partridge Sports & Social Lounge',
            description='Weekly Thursday showdown with live big screen leaderboards and bar vouchers.',
            schedule_day='Every Thursday at 20:00'
        )
        db.session.add(league)

    db.session.commit()
