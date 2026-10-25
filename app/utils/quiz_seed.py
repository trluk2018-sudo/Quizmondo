"""Initial question seed, packs catalog, pub leagues, and homepage module synchronizer for Quizmondo Arena."""
import json
from datetime import datetime, timedelta
from ..models import db, QuizQuestion, QuizPack, PubLeague, PageModule, MenuItem, Post, Category, SiteSetting
from .modules import get_default_config, MODULE_DEFINITIONS

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
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'What is the chemical symbol for the precious metal Gold?',
                'options': {'A': 'Ag', 'B': 'Fe', 'C': 'Au', 'D': 'Gd'},
                'correct': 'C',
                'explanation': 'Au comes from the Latin word "Aurum", meaning shining dawn.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'Approximately how long does light from the Sun take to reach planet Earth?',
                'options': {'A': '8 minutes and 20 seconds', 'B': '30 seconds', 'C': '4 minutes and 10 seconds', 'D': '12 minutes and 45 seconds'},
                'correct': 'A',
                'explanation': 'At a distance of roughly 150 million km, sunlight takes approximately 8 minutes and 20 seconds (500 seconds) to reach Earth.',
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'Which particle is known as the mediator of the electromagnetic force in quantum physics?',
                'options': {'A': 'Gluon', 'B': 'Photon', 'C': 'W Boson', 'D': 'Graviton'},
                'correct': 'B',
                'explanation': 'Photons are the gauge bosons responsible for mediating electromagnetic interactions.',
                'difficulty': 'hard',
                'type': 'classic'
            },
            {
                'prompt': 'What is known as the "powerhouse of the cell" responsible for generating ATP energy?',
                'options': {'A': 'Ribosome', 'B': 'Mitochondria', 'C': 'Endoplasmic Reticulum', 'D': 'Golgi Apparatus'},
                'correct': 'B',
                'explanation': 'Mitochondria generate most of the chemical energy (ATP) needed by cellular biochemical reactions.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'In what year did the Hubble Space Telescope deploy into low Earth orbit aboard Space Shuttle Discovery?',
                'options': {'A': '1985', 'B': '1990', 'C': '1995', 'D': '2001'},
                'correct': 'B',
                'explanation': 'Hubble launched on April 24, 1990, revolutionizing observational astrophysics.',
                'difficulty': 'medium',
                'type': 'classic'
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
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'What sound synthesizer chip powered the iconic Commodore 64 home computer?',
                'options': {'A': 'Yamaha YM2612', 'B': 'MOS Technology 6581 SID', 'C': 'General Instrument AY-3-8910', 'D': 'Texas Instruments SN76489'},
                'correct': 'B',
                'explanation': 'The MOS 6581/8580 SID (Sound Interface Device) gave the C64 its revolutionary 3-channel audio synthesis.',
                'difficulty': 'hard',
                'type': 'classic'
            },
            {
                'prompt': 'What was Mario originally called in the 1981 arcade game Donkey Kong?',
                'options': {'A': 'Jumpman', 'B': 'Plumber Pete', 'C': 'Buster', 'D': 'Luigi'},
                'correct': 'A',
                'explanation': 'Shigeru Miyamoto originally named the carpenter character "Jumpman" before he was christened Mario.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'Which classic 1993 first-person shooter was created by id Software pioneers John Carmack and John Romero?',
                'options': {'A': 'Wolfenstein 3D', 'B': 'DOOM', 'C': 'Quake', 'D': 'Hexen'},
                'correct': 'B',
                'explanation': 'DOOM was released as shareware in December 1993, defining network multiplayer and 3D PC gaming.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'In Minecraft, what rare green ore is primarily used as currency to trade with villagers?',
                'options': {'A': 'Diamond', 'B': 'Emerald', 'C': 'Jade', 'D': 'Lapis Lazuli'},
                'correct': 'B',
                'explanation': 'Emeralds serve as the native currency in Minecraft village economies.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'Listen to the opening theme of this legendary video game. Which 1989 Game Boy classic is this?',
                'options': {'A': 'Super Mario Land', 'B': 'Tetris (Type A)', 'C': 'Pokemon Red', 'D': 'The Legend of Zelda'},
                'correct': 'B',
                'explanation': 'The iconic Type A theme is based on the 19th-century Russian folk song "Korobeiniki".',
                'difficulty': 'medium',
                'type': 'youtube_clip',
                'media_url': 'https://www.youtube.com/watch?v=NmCCQxVBfyM'
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
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'What is the capital city of Australia?',
                'options': {'A': 'Sydney', 'B': 'Melbourne', 'C': 'Canberra', 'D': 'Brisbane'},
                'correct': 'C',
                'explanation': 'Canberra was chosen as the compromise capital of Australia in 1908 to resolve the rivalry between Sydney and Melbourne.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'Which river is officially recognized as the longest in the world by the majority of geographers?',
                'options': {'A': 'Amazon River', 'B': 'Nile River', 'C': 'Yangtze River', 'D': 'Mississippi-Missouri'},
                'correct': 'B',
                'explanation': 'The Nile stretches approximately 6,650 km through northeastern Africa, historically ranking as the longest.',
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'In which modern-day country would you find the ruins of the ancient ceremonial capital of Persepolis?',
                'options': {'A': 'Iraq', 'B': 'Iran', 'C': 'Turkey', 'D': 'Jordan'},
                'correct': 'B',
                'explanation': 'Persepolis was the ceremonial capital of the Achaemenid Empire, located near modern-day Shiraz, Iran.',
                'difficulty': 'hard',
                'type': 'classic'
            },
            {
                'prompt': 'In what year was the historic Magna Carta signed by King John at Runnymede near Windsor?',
                'options': {'A': '1066', 'B': '1215', 'C': '1415', 'D': '1688'},
                'correct': 'B',
                'explanation': 'The Great Charter established for the first time that everyone, even the king, was subject to the law.',
                'difficulty': 'medium',
                'type': 'classic'
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
                'prompt': 'Who directed the 1994 cinema masterpiece "Pulp Fiction"?',
                'options': {'A': 'Martin Scorsese', 'B': 'Quentin Tarantino', 'C': 'David Fincher', 'D': 'Steven Spielberg'},
                'correct': 'B',
                'explanation': 'Quentin Tarantino wrote and directed Pulp Fiction, winning the Palme d\'Or at Cannes in 1994.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'In The Matrix (1999), what color pill does Neo take to wake up in the real world?',
                'options': {'A': 'Blue', 'B': 'Red', 'C': 'Green', 'D': 'Yellow'},
                'correct': 'B',
                'explanation': 'Morpheus explains: "You take the red pill—you stay in Wonderland, and I show you how deep the rabbit hole goes."',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'Which British actor portrayed the Tenth Doctor in the long-running BBC sci-fi series Doctor Who?',
                'options': {'A': 'Christopher Eccleston', 'B': 'Matt Smith', 'C': 'David Tennant', 'D': 'Peter Capaldi'},
                'correct': 'C',
                'explanation': 'David Tennant starred as the Tenth Doctor from 2005 to 2010.',
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'What film won the Academy Award for Best Picture at the 1998 Oscars, winning 11 Academy Awards in total?',
                'options': {'A': 'L.A. Confidential', 'B': 'Titanic', 'C': 'Saving Private Ryan', 'D': 'Good Will Hunting'},
                'correct': 'B',
                'explanation': 'James Cameron\'s Titanic tied Ben-Hur with 11 Oscar wins in 1998.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'In the Lord of the Rings films, which actor portrayed the wizard Gandalf the Grey?',
                'options': {'A': 'Patrick Stewart', 'B': 'Ian McKellen', 'C': 'Christopher Lee', 'D': 'Michael Gambon'},
                'correct': 'B',
                'explanation': 'Sir Ian McKellen received an Academy Award nomination for portraying Gandalf in The Fellowship of the Ring.',
                'difficulty': 'easy',
                'type': 'classic'
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
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'Who released the 1982 album "Thriller", which remains the highest-selling album of all time?',
                'options': {'A': 'Prince', 'B': 'Michael Jackson', 'C': 'Stevie Wonder', 'D': 'Lionel Richie'},
                'correct': 'B',
                'explanation': 'Michael Jackson\'s Thriller has sold an estimated 70+ million copies worldwide.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'What synthesizer brand made the legendary Minimoog analog synth launched in 1970?',
                'options': {'A': 'Roland', 'B': 'Moog', 'C': 'Korg', 'D': 'Yamaha'},
                'correct': 'B',
                'explanation': 'Robert Moog designed the Minimoog Model D, transforming popular electronic music.',
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'Which Swedish pop quartet won the Eurovision Song Contest in 1974 with the song "Waterloo"?',
                'options': {'A': 'Roxette', 'B': 'ABBA', 'C': 'Ace of Base', 'D': 'The Cardigans'},
                'correct': 'B',
                'explanation': 'ABBA\'s historic victory in Brighton launched their global music superstardom.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'What famous 1975 Queen anthem features the operatic line "Scaramouche, Scaramouche, will you do the Fandango?"',
                'options': {'A': 'Somebody to Love', 'B': 'Bohemian Rhapsody', 'C': 'Killer Queen', 'D': 'Radio Ga Ga'},
                'correct': 'B',
                'explanation': 'Written by Freddie Mercury, Bohemian Rhapsody remained at number one on the UK Singles Chart for nine weeks.',
                'difficulty': 'easy',
                'type': 'classic'
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
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'How many meters is an official Olympic standard swimming pool in length?',
                'options': {'A': '25 meters', 'B': '50 meters', 'C': '75 meters', 'D': '100 meters'},
                'correct': 'B',
                'explanation': 'Olympic standard long-course pools are exactly 50 meters in length.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'Who holds the official world record for the men\'s 100-meter sprint at 9.58 seconds?',
                'options': {'A': 'Carl Lewis', 'B': 'Tyson Gay', 'C': 'Usain Bolt', 'D': 'Asafa Powell'},
                'correct': 'C',
                'explanation': 'Usain Bolt of Jamaica clocked 9.58 seconds at the 2009 World Athletics Championships in Berlin.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'Which iconic jersey number did Michael Jordan wear for the majority of his legendary Chicago Bulls career?',
                'options': {'A': '21', 'B': '23', 'C': '24', 'D': '33'},
                'correct': 'B',
                'explanation': 'Michael Jordan famously wore number 23, winning 6 NBA championships with the Bulls.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'On what surface is the prestigious Wimbledon tennis championship traditionally contested?',
                'options': {'A': 'Clay', 'B': 'Hard Court', 'C': 'Grass', 'D': 'Carpet'},
                'correct': 'C',
                'explanation': 'Wimbledon is the only Grand Slam tennis tournament still played on traditional grass courts.',
                'difficulty': 'easy',
                'type': 'classic'
            }
        ]
    }
]

SEED_LEAGUES = [
    {
        'name': 'The Dog & Partridge Quiz League',
        'slug': 'dog-and-partridge',
        'pin_code': '7742',
        'venue_name': 'The Dog & Partridge Sports & Social Lounge',
        'description': 'Weekly Thursday showdown with live big screen leaderboards and bar vouchers.',
        'schedule_day': 'Every Thursday at 20:00 GMT',
        'teams': [
            {'name': 'The Quizly Bears', 'score': 540, 'members': 4, 'rank': 1},
            {'name': 'Tequila Mockingbird', 'score': 490, 'members': 3, 'rank': 2},
            {'name': 'Trivia Newton John', 'score': 450, 'members': 5, 'rank': 3},
            {'name': 'Quiz Pro Quo', 'score': 380, 'members': 2, 'rank': 4}
        ]
    },
    {
        'name': 'The Red Lion Virtual Pub Showdown',
        'slug': 'red-lion',
        'pin_code': '8821',
        'venue_name': 'The Red Lion Tavern & Craft Ale Bar',
        'description': 'High-octane pub quiz tournament with 5 rounds of audio, cinema, and history trivia.',
        'schedule_day': 'Every Tuesday at 19:30 GMT',
        'teams': [
            {'name': 'Smarty Pints', 'score': 620, 'members': 4, 'rank': 1},
            {'name': 'Beer Today, Gone Tomorrow', 'score': 580, 'members': 4, 'rank': 2},
            {'name': 'Fact Hunters', 'score': 510, 'members': 3, 'rank': 3},
            {'name': 'The Fellowship of the Quiz', 'score': 460, 'members': 5, 'rank': 4}
        ]
    },
    {
        'name': "The King's Arms Sunday Brain Buster",
        'slug': 'kings-arms',
        'pin_code': '4096',
        'venue_name': "The King's Arms Traditional Coaching Inn",
        'description': 'End your weekend with the ultimate pub quiz championship. Prizes for 1st, 2nd, and Best Team Name!',
        'schedule_day': 'Every Sunday at 18:00 GMT',
        'teams': [
            {'name': 'Agatha Quiztie', 'score': 590, 'members': 4, 'rank': 1},
            {'name': 'Universally Challenged', 'score': 540, 'members': 4, 'rank': 2},
            {'name': 'Panic at the Distro', 'score': 480, 'members': 3, 'rank': 3}
        ]
    }
]

SEED_POSTS = [
    {
        'title': 'Which Planet Has the Most Moons? Saturn Overtakes Jupiter in Latest Astronomy Count',
        'slug': 'which-planet-has-the-most-moons-saturn-jupiter',
        'excerpt': 'In the great celestial moon race, astronomers have officially verified 146 satellites orbiting Saturn, settling one of astronomy\'s most fiercely contested trivia debates.',
        'content': '''<p>For decades, planetary trivia enthusiasts grew up memorizing that Jupiter was the undisputed satellite champion of our solar system. However, recent telescopic surveys utilizing Canada-France-Hawaii Telescope interferometry have dramatically rewritten astrophysics textbooks.</p>
<h3>The Shift to Saturn's Ringed Empire</h3>
<p>In May 2023, the International Astronomical Union (IAU) certified 62 new irregular moons orbiting Saturn, bringing its total to 146 confirmed satellites. Jupiter currently stands at 95 verified moons, leaving Saturn with a decisive cosmic lead.</p>
<p>Most of Saturn's newly discovered satellites belong to the Norse, Gallic, and Inuit orbital groups—fragments of larger proto-moons pulverized by catastrophic collisions billions of years ago.</p>
<h3>How to Use This in Your Next Quiz Duels</h3>
<p>When this question appears in the <strong>Science & Cosmos</strong> arena track on Quizmondo, remember: <em>Saturn is currently the Moon Titan of the solar system!</em></p>''',
        'category_name': 'Astronomy & Physics'
    },
    {
        'title': 'The Evolution of Speedruns: Breaking Impossible Video Game Records',
        'slug': 'evolution-of-speedruns-breaking-impossible-video-game-records',
        'excerpt': 'From early DOOM demo recordings to sub-5-minute Super Mario Bros runs, explore how human reflex optimization transformed gaming trivia forever.',
        'content': '''<p>Speedrunning represents the absolute pinnacle of human dexterity, memory compression, and reverse engineering. What began with sharing 1.44MB floppy disk demo files of DOOM in 1993 has evolved into an international esports spectacle.</p>
<h3>Sub-5: The Holy Grail of Super Mario Bros</h3>
<p>For years, mathematicians argued whether completing World 1-1 through 8-4 on original NES hardware in under 4 minutes and 55 seconds was humanly attainable. In September 2021, runner Niftski achieved a staggering 4:54.948 by mastering sub-pixel framerule manipulation.</p>
<h3>Test Your Retro Knowledge</h3>
<p>Jump into Quizmondo's <strong>Retro Gaming & Microcomputing</strong> pack to test your knowledge of glitch hunting, TAS runs, and iconic developer easter eggs!</p>''',
        'category_name': 'Gaming & Esports'
    },
    {
        'title': 'Ancient Enigmas: 7 Historical Trivia Facts That Sound Completely Fake',
        'slug': 'ancient-enigmas-7-historical-trivia-facts-that-sound-fake',
        'excerpt': 'From woolly mammoths surviving while pyramids were constructed to Oxford University predating the Aztec Empire, explore history\'s greatest timeline twists.',
        'content': '''<p>Human perception of history is often compartmentalized by textbooks into neat, separated eras. But when historical timelines are viewed side-by-side, staggering chronological intersections emerge.</p>
<ol class="space-y-4">
  <li><strong>Mammoths & The Great Pyramids:</strong> Isolated populations of woolly mammoths survived on Wrangel Island in Siberia until roughly 1650 BC—meaning Pharaoh Khufu was building the Great Pyramid of Giza while mammoths still walked the Earth.</li>
  <li><strong>Oxford Predates the Aztecs:</strong> Teaching existed at Oxford University as early as 1096 AD. The Aztec civilization was not founded until the construction of Tenochtitlan around 1325 AD.</li>
  <li><strong>Cleopatra\'s Timeline:</strong> Cleopatra lived closer in time to the 1969 Apollo 11 Moon landing than to the construction of the Great Pyramid.</li>
</ol>''',
        'category_name': 'World History & Lore'
    },
    {
        'title': 'The 10 Commandments of Running a Legend-Tier Pub Quiz Night',
        'slug': 'the-10-commandments-of-running-a-legend-tier-pub-quiz-night',
        'excerpt': 'The essential playbook for quizmasters: pacing, balance, audio rounds, and projector scoreboard management.',
        'content': '''<p>Whether you are hosting for 20 locals at your neighborhood pub or running a 200-person corporate tournament, these rules guarantee a legendary trivia night.</p>
<ul>
  <li><strong>Commandment 1:</strong> Keep rounds punchy—never more than 8 to 10 questions per round.</li>
  <li><strong>Commandment 2:</strong> Incorporate audio waveforms and visual clues. Text-only quizzes cause table fatigue.</li>
  <li><strong>Commandment 3:</strong> Use synchronized digital leaderboards like Quizmondo\'s Big-Screen TV mode to eliminate paper scoring delays.</li>
</ul>''',
        'category_name': 'Pub Quiz Culture'
    },
    {
        'title': 'Chiptunes & Waveforms: How 8-Bit Audio Tricks Your Brain into Remembering Trivia',
        'slug': 'chiptunes-waveforms-how-8-bit-audio-boosts-trivia-recall',
        'excerpt': 'Neuroscience explains why procedural audio cues, pulse waves, and heartbeat countdowns enhance trivia memory retention.',
        'content': '''<p>Ever wondered why you remember the melody to Tetris or Mario three decades later? Studies in auditory cognitive neuroscience show that square-wave and triangle-wave synthesizers stimulate deep memory pathways in the brain\'s temporal lobe.</p>
<p>Quizmondo utilizes real-time browser Web Audio API synthesis—generating procedural ticks, heartbeat countdowns, and ascending chimes without downloading heavy audio files.</p>''',
        'category_name': 'Audio & Science'
    },
    {
        'title': 'BBC House of Games & Quiz Planet: Why Asynchronous Turn-Based Duels Are the Future',
        'slug': 'bbc-house-of-games-quiz-planet-why-turn-based-duels-rule',
        'excerpt': 'Why modern players prefer taking their turn during coffee breaks over waiting in rigid synchronous lobbies.',
        'content': '''<p>The success of television shows like BBC\'s Richard Osman\'s House of Games and viral mobile apps like Quiz Planet highlights a powerful truth: players love clever, multi-format trivia games, but they have busy lives.</p>
<p>Asynchronous turn-based play allows you to play Round 1 in the morning, send a WhatsApp nudge to your best friend, and let them play their turn whenever they have a free moment. Fair, thrilling, and infinitely replayable.</p>''',
        'category_name': 'Game Design & TV Lore'
    }
]


def seed_quizmondo_full_environment():
    """Seed and synchronize modules, packs, pub leagues, navigation, and articles."""
    # 1. Synchronize SiteSettings
    SiteSetting.set('site_title', 'Quizmondo.com')
    SiteSetting.set('site_tagline', 'The Cosmic Arcade Trivia Arena & Multiplayer Brain Showdowns')
    SiteSetting.set('site_logo', '/static/img/quizmondo_logo.svg')
    SiteSetting.set('footer_logo', '/static/img/quizmondo_logo.svg')
    SiteSetting.set('active_theme', 'quizhub')
    SiteSetting.set('footer_copyright', '© 2026 Quizmondo.com. All rights reserved.')
    SiteSetting.set('footer_about_text', 'Quizmondo is the premier gamified brain arena featuring turn-based WhatsApp duels, weekly pub quiz leagues, community quiz decks, and prize vault rewards.')

    # 2. Synchronize Question Packs & Questions
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
        else:
            pack.question_count = len(pack_data['questions'])

        for q_item in pack_data['questions']:
            existing_q = QuizQuestion.query.filter_by(prompt=q_item['prompt']).first()
            if not existing_q:
                q = QuizQuestion(
                    prompt=q_item['prompt'],
                    question_type=q_item.get('type', 'classic'),
                    media_url=q_item.get('media_url', ''),
                    options_json=json.dumps(q_item['options']),
                    correct_option=q_item['correct'],
                    explanation=q_item['explanation'],
                    category_slug=pack_data['category_slug'],
                    category_name=pack_data['title'],
                    difficulty=q_item.get('difficulty', 'medium'),
                    pack_slug=pack_data['slug'],
                    points=100,
                    time_limit=15,
                    status='approved',
                    is_community=False
                )
                db.session.add(q)
            else:
                existing_q.question_type = q_item.get('type', existing_q.question_type or 'classic')
                existing_q.media_url = q_item.get('media_url', existing_q.media_url or '')
                existing_q.status = 'approved'

    # 3. Synchronize Pub Leagues
    for lg_data in SEED_LEAGUES:
        league = PubLeague.query.filter_by(slug=lg_data['slug']).first()
        if not league:
            league = PubLeague(
                name=lg_data['name'],
                slug=lg_data['slug'],
                pin_code=lg_data['pin_code'],
                venue_name=lg_data['venue_name'],
                description=lg_data['description'],
                schedule_day=lg_data['schedule_day'],
                is_active=True
            )
            league.set_teams(lg_data['teams'])
            db.session.add(league)
        else:
            if not league.get_teams():
                league.set_teams(lg_data['teams'])

    # 4. Synchronize Categories & Posts
    for p_item in SEED_POSTS:
        cat_name = p_item['category_name']
        cat = Category.query.filter_by(name=cat_name).first()
        if not cat:
            cat = Category(name=cat_name, slug=cat_name.lower().replace('&', 'and').replace(' ', '-'))
            db.session.add(cat)
            db.session.flush()

        post = Post.query.filter_by(slug=p_item['slug']).first()
        if not post:
            post = Post(
                title=p_item['title'],
                slug=p_item['slug'],
                excerpt=p_item['excerpt'],
                content=p_item['content'],
                category_id=cat.id,
                status='publish',
                created_at=datetime.utcnow() - timedelta(days=SEED_POSTS.index(p_item))
            )
            db.session.add(post)
        else:
            post.title = p_item['title']
            post.excerpt = p_item['excerpt']
            post.content = p_item['content']
            post.status = 'publish'

    # 5. Synchronize Homepage PageModules for 'quizhub' theme
    PageModule.query.filter_by(is_home=True).delete()
    
    home_order = [
        'hero',
        'daily_quiz',
        'features_strip',
        'about',
        'services',
        'case_studies',
        'posts',
        'testimonials',
        'trust_strip',
        'contact_form'
    ]

    for idx, m_type in enumerate(home_order, 1):
        defn = MODULE_DEFINITIONS.get(m_type, {})
        pm = PageModule(
            is_home=True,
            theme='quizhub',
            module_type=m_type,
            title=defn.get('name', m_type.replace('_', ' ').title()),
            placement='above',
            sort_order=idx,
            is_enabled=True
        )
        pm.set_config(get_default_config(m_type))
        db.session.add(pm)

    # 6. Synchronize Header & Footer Navigation
    MenuItem.query.filter(MenuItem.location.in_(['header', 'footer'])).delete()

    nav_links = [
        ('Arena Home', '/', False),
        ('Play Duels', '/arena/', False),
        ('Trivia Decks', '/arena/packs', False),
        ('Pub Leagues', '/arena/leagues', False),
        ('Leaderboard', '/arena/leaderboard', False),
        ('Quiz Studio', '/arena/create', False),
        ('Articles', '/posts', False)
    ]

    for idx, (title, url, open_new) in enumerate(nav_links, 1):
        h_item = MenuItem(location='header', title=title, url=url, sort_order=idx, open_new_tab=open_new)
        f_item = MenuItem(location='footer', title=title, url=url, sort_order=idx, open_new_tab=open_new)
        db.session.add(h_item)
        db.session.add(f_item)

    db.session.commit()
    print("QUIZMONDO_SEED_SYNCHRONIZED_SUCCESSFULLY")
