"""Initial question seed, packs catalog, pub leagues, and homepage module synchronizer for Quizmondo Arena."""
import os
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
            },
            {
                'prompt': 'At what Lagrange point in space does the James Webb Space Telescope orbit the Sun?',
                'options': {'A': 'L1', 'B': 'L2', 'C': 'L4', 'D': 'L5'},
                'correct': 'B',
                'explanation': 'JWST orbits the second Lagrange point (L2), approximately 1.5 million kilometers beyond Earth.',
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'Which scientific pioneers were credited with elucidating the double-helix structure of DNA in 1953?',
                'options': {'A': 'Watson & Crick', 'B': 'Bohr & Fermi', 'C': 'Pasteur & Koch', 'D': 'Curie & Becquerel'},
                'correct': 'A',
                'explanation': 'James Watson and Francis Crick, utilizing Rosalind Franklin\'s X-ray diffraction data, solved the structure.',
                'difficulty': 'easy',
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
                'prompt': 'Which 19th-century Russian folk song serves as the iconic "Type A" theme music in the 1989 Game Boy classic Tetris?',
                'options': {'A': 'Kalinka', 'B': 'Korobeiniki', 'C': 'Katyusha', 'D': 'Dark Eyes (Ochi Chyornye)'},
                'correct': 'B',
                'explanation': 'Composer Hirokazu Tanaka arranged the 19th-century Russian folk song "Korobeiniki" (The Peddlers) into the legendary Game Boy Tetris Type A theme.',
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'In The Legend of Zelda: Ocarina of Time (1998), what musical instrument is used to warp across Hyrule?',
                'options': {'A': 'Harp', 'B': 'Ocarina', 'C': 'Flute', 'D': 'Lute'},
                'correct': 'B',
                'explanation': 'Link plays the Ocarina of Time to manipulate time, open the Door of Time, and warp between temples.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'What iconic melee weapon is wielded by physicist Gordon Freeman in the Half-Life series?',
                'options': {'A': 'Wrench', 'B': 'Crowbar', 'C': 'Pipe', 'D': 'Machete'},
                'correct': 'B',
                'explanation': 'The red crowbar became the hallmark symbol of Valve\'s groundbreaking 1998 sci-fi shooter.',
                'difficulty': 'easy',
                'type': 'classic'
            }
        ]
    },
    {
        'title': 'World Geography & Lost Civilizations',
        'slug': 'world-history',
        'description': 'Ancient world wonders, global capital cities, cartography, and archaeological puzzles.',
        'icon': '🏛️',
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
            },
            {
                'prompt': 'Which American explorer brought the 15th-century Inca citadel of Machu Picchu to international attention in 1911?',
                'options': {'A': 'Howard Carter', 'B': 'Hiram Bingham', 'C': 'Percy Fawcett', 'D': 'Roald Amundsen'},
                'correct': 'B',
                'explanation': 'Hiram Bingham III climbed to the ridge above the Urubamba River with local guide Melchor Arteaga in 1911.',
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'What archaeological discovery in 1799 provided the vital key to deciphering ancient Egyptian hieroglyphics?',
                'options': {'A': 'The Rosetta Stone', 'B': 'The Dead Sea Scrolls', 'C': 'The Elgin Marbles', 'D': 'The Code of Hammurabi'},
                'correct': 'A',
                'explanation': 'Featuring decrees written in Hieroglyphic, Demotic, and Ancient Greek, it allowed Jean-François Champollion to unlock hieroglyphs.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'Which Roman Emperor officially moved the capital of the Roman Empire to Byzantium (later Constantinople) in 330 AD?',
                'options': {'A': 'Julius Caesar', 'B': 'Augustus', 'C': 'Constantine the Great', 'D': 'Nero'},
                'correct': 'C',
                'explanation': 'Constantine established the New Rome on the Bosphorus, launching over a millennium of Byzantine civilization.',
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
            },
            {
                'prompt': 'In the acclaimed TV drama "Breaking Bad", what alias does Walter White adopt in the criminal underworld?',
                'options': {'A': 'Oppenheimer', 'B': 'Heisenberg', 'C': 'Schrödinger', 'D': 'Fermi'},
                'correct': 'B',
                'explanation': 'Walter White chooses the name Heisenberg in homage to theoretical physicist Werner Heisenberg.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'Which Studio Ghibli masterpiece directed by Hayao Miyazaki won the Academy Award for Best Animated Feature in 2003?',
                'options': {'A': 'Princess Mononoke', 'B': 'My Neighbor Totoro', 'C': 'Spirited Away', 'D': 'Howl\'s Moving Castle'},
                'correct': 'C',
                'explanation': 'Spirited Away made history as the first non-English hand-drawn animated film to win the Oscar.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'In Christopher Nolan\'s 2010 film "Inception", what small spinning object serves as Cobb\'s personal totem?',
                'options': {'A': 'Loaded Die', 'B': 'Spinning Top', 'C': 'Chess Pawn', 'D': 'Brass Token'},
                'correct': 'B',
                'explanation': 'Dom Cobb tests reality by watching whether the spinning top will eventually tumble or spin perpetually.',
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
            },
            {
                'prompt': 'Which Parisian electronic duo produced the seminal dance albums "Homework" and "Discovery"?',
                'options': {'A': 'Justice', 'B': 'Air', 'C': 'Daft Punk', 'D': 'Cassius'},
                'correct': 'C',
                'explanation': 'Thomas Bangalter and Guy-Manuel de Homem-Christo performed as robot alter-egos in Daft Punk.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'What alter ego did David Bowie introduce on his 1972 concept album featuring the Spiders from Mars?',
                'options': {'A': 'The Thin White Duke', 'B': 'Ziggy Stardust', 'C': 'Major Tom', 'D': 'Aladdin Sane'},
                'correct': 'B',
                'explanation': 'Ziggy Stardust presented an androgynous alien rock superstar delivering hope to Earth.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'Which British rock band famously performed their final public concert on the rooftop of Apple Corps in London in 1969?',
                'options': {'A': 'The Rolling Stones', 'B': 'The Beatles', 'C': 'The Kinks', 'D': 'Cream'},
                'correct': 'B',
                'explanation': 'The Beatles performed an unannounced 42-minute set on the rooftop at 3 Savile Row on January 30, 1969.',
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
            },
            {
                'prompt': 'How many Grand Slam men\'s singles titles did Swiss tennis maestro Roger Federer win in his career?',
                'options': {'A': '18', 'B': '20', 'C': '22', 'D': '24'},
                'correct': 'B',
                'explanation': 'Federer was the first man in tennis history to reach 20 Grand Slam singles crowns.',
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'What color jersey is traditionally awarded to the overall general classification leader in the Tour de France?',
                'options': {'A': 'Green', 'B': 'Yellow (Maillot Jaune)', 'C': 'Polka Dot', 'D': 'White'},
                'correct': 'B',
                'explanation': 'The Yellow Jersey (Maillot Jaune) was created in 1919, matching the yellow paper of L\'Auto newspaper.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'In what year did England win their sole FIFA World Cup trophy, defeating West Germany at Wembley?',
                'options': {'A': '1958', 'B': '1966', 'C': '1970', 'D': '1974'},
                'correct': 'B',
                'explanation': 'Geoff Hurst scored a hat-trick as England triumphed 4-2 after extra time.',
                'difficulty': 'easy',
                'type': 'classic'
            }
        ]
    },
    {
        'title': 'World Geography & Continental Wonders',
        'slug': 'world-geography',
        'description': 'Capital cities, island archipelagos, extreme landforms, and international borders.',
        'icon': '🗺️',
        'category_slug': 'world-geography',
        'questions': [
            {
                'prompt': 'Which European capital city is built across 14 islands connected by over 50 bridges?',
                'options': {'A': 'Copenhagen', 'B': 'Stockholm', 'C': 'Amsterdam', 'D': 'Helsinki'},
                'correct': 'B',
                'explanation': 'Stockholm sits on the Stockholm archipelago where Lake Mälaren meets the Baltic Sea.',
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'What is the highest uninterrupted waterfall in the world, plunging 979 meters in Venezuela?',
                'options': {'A': 'Iguazu Falls', 'B': 'Victoria Falls', 'C': 'Angel Falls', 'D': 'Niagara Falls'},
                'correct': 'C',
                'explanation': 'Angel Falls (Kerepakupai Merú) drops from the Auyán-tepui mountain in Canaima National Park.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'Which South American country has two official capitals: Sucre (constitutional) and La Paz (seat of government)?',
                'options': {'A': 'Paraguay', 'B': 'Ecuador', 'C': 'Bolivia', 'D': 'Uruguay'},
                'correct': 'C',
                'explanation': 'Sucre is the historical constitutional capital, while La Paz hosts the executive and legislative branches.',
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'Which country in the world possesses the longest total coastline, measuring over 202,000 km?',
                'options': {'A': 'Russia', 'B': 'Australia', 'C': 'Canada', 'D': 'Norway'},
                'correct': 'C',
                'explanation': 'Canada\'s sprawling arctic and island geography gives it by far the longest coastline on Earth.',
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'What is the driest non-polar desert on Earth, located in South America west of the Andes?',
                'options': {'A': 'Kalahari Desert', 'B': 'Atacama Desert', 'C': 'Gobi Desert', 'D': 'Mojave Desert'},
                'correct': 'B',
                'explanation': 'Parts of Chile\'s Atacama Desert have had zero recorded rainfall for decades.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'On which continent and in which country would you find Mount Kilimanjaro?',
                'options': {'A': 'Kenya', 'B': 'Tanzania', 'C': 'Uganda', 'D': 'Ethiopia'},
                'correct': 'B',
                'explanation': 'Mount Kilimanjaro (5,895m) is a dormant volcano in northeastern Tanzania.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'Which historic transcontinental metropolis spans both the European and Asian continents across the Bosphorus Strait?',
                'options': {'A': 'Cairo', 'B': 'Athens', 'C': 'Istanbul', 'D': 'Tbilisi'},
                'correct': 'C',
                'explanation': 'Istanbul is the only major world city situated on two continents simultaneously.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'What Siberian lake is both the world\'s deepest and oldest freshwater lake by volume?',
                'options': {'A': 'Lake Superior', 'B': 'Lake Victoria', 'C': 'Lake Baikal', 'D': 'Caspian Sea'},
                'correct': 'C',
                'explanation': 'Lake Baikal reaches a maximum depth of 1,642 meters, holding 20% of the world\'s unfrozen surface freshwater.',
                'difficulty': 'medium',
                'type': 'classic'
            }
        ]
    },
    {
        'title': 'Culinary Arts & Epicurean Lore',
        'slug': 'culinary-arts',
        'description': 'Gastronomic traditions, classic cocktails, Michelin techniques, and global spices.',
        'icon': '🍕',
        'category_slug': 'culinary-arts',
        'questions': [
            {
                'prompt': 'What fresh aromatic herb is the primary base ingredient for traditional Genovese pesto?',
                'options': {'A': 'Coriander', 'B': 'Basil', 'C': 'Oregano', 'D': 'Tarragon'},
                'correct': 'B',
                'explanation': 'Pesto alla Genovese combines fresh basil, pine nuts, garlic, olive oil, and Parmigiano/Pecorino cheese.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'What precious culinary spice is harvested by hand from the dried stigmas of the Crocus sativus flower?',
                'options': {'A': 'Cardamom', 'B': 'Saffron', 'C': 'Vanilla', 'D': 'Star Anise'},
                'correct': 'B',
                'explanation': 'Saffron requires up to 75,000 blossoms to produce one single pound of dried spice.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'Which classic French mother sauce is made by whisking egg yolks with melted butter and lemon juice?',
                'options': {'A': 'Béchamel', 'B': 'Velouté', 'C': 'Hollandaise', 'D': 'Espagnole'},
                'correct': 'C',
                'explanation': 'Hollandaise is an emulsion sauce perfected in classic French culinary codified doctrine.',
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'In which country did the smoky agave spirit Mezcal originate?',
                'options': {'A': 'Peru', 'B': 'Mexico', 'C': 'Colombia', 'D': 'Cuba'},
                'correct': 'B',
                'explanation': 'Mezcal is produced in Mexico, particularly Oaxaca, from roasted piñas of agave plants.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'Which famous Italian cocktail consists of equal parts Gin, Campari, and Sweet Red Vermouth, garnished with orange peel?',
                'options': {'A': 'Aperol Spritz', 'B': 'Negroni', 'C': 'Bellini', 'D': 'Americano'},
                'correct': 'B',
                'explanation': 'Count Camillo Negroni asked bartender Forsco Scarselli in Florence to stiffen his Americano with gin in 1919.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'From which country does the famous blue-veined sheep milk cheese Roquefort originate?',
                'options': {'A': 'Italy', 'B': 'France', 'C': 'Switzerland', 'D': 'Spain'},
                'correct': 'B',
                'explanation': 'Roquefort is aged in the natural Combalou caves of Roquefort-sur-Soulzon in southern France.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'What measurement scale is universally used to quantify the piquancy and heat of chili peppers?',
                'options': {'A': 'Brix Scale', 'B': 'Scoville Scale', 'C': 'Mohs Scale', 'D': 'Baumé Scale'},
                'correct': 'B',
                'explanation': 'Wilbur Scoville devised the Scoville Organoleptic Test in 1912 to measure capsaicin concentration.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'Real authentic Japanese wasabi is traditionally grated using what specialized tool made from sharkskin?',
                'options': {'A': 'Oroshigane', 'B': 'Mandoline', 'C': 'Suribachi', 'D': 'Chasen'},
                'correct': 'A',
                'explanation': 'An oroshigane sharkskin grater breaks the wasabi rhizome cells to release allylisothiocyanate aromas.',
                'difficulty': 'hard',
                'type': 'classic'
            }
        ]
    },
    {
        'title': 'Silicon Pioneers & Coding Legends',
        'slug': 'tech-computing',
        'description': 'Computing history, programming breakthroughs, network protocols, and Silicon Valley lore.',
        'icon': '💻',
        'category_slug': 'tech-computing',
        'questions': [
            {
                'prompt': 'Who is celebrated as the world\'s first computer programmer for writing an algorithm for Babbage\'s Analytical Engine?',
                'options': {'A': 'Grace Hopper', 'B': 'Ada Lovelace', 'C': 'Margaret Hamilton', 'D': 'Katherine Johnson'},
                'correct': 'B',
                'explanation': 'Ada Lovelace translated Menabrea\'s memoir and added Note G, the first published computer algorithm.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'In what year did Finnish student Linus Torvalds announce the initial release of the Linux kernel?',
                'options': {'A': '1987', 'B': '1991', 'C': '1995', 'D': '1998'},
                'correct': 'B',
                'explanation': 'Linus Torvalds posted his famous "just a hobby, won\'t be big and professional" message on August 25, 1991.',
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'Which legendary computer scientist devised the foundational imitation game test for machine intelligence in 1950?',
                'options': {'A': 'John von Neumann', 'B': 'Claude Shannon', 'C': 'Alan Turing', 'D': 'Marvin Minsky'},
                'correct': 'C',
                'explanation': 'Alan Turing introduced the Turing Test in his landmark paper "Computing Machinery and Intelligence".',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'What does the acronym HTTP stand for in computer networking?',
                'options': {'A': 'HyperText Transfer Protocol', 'B': 'High Tactical Transfer Port', 'C': 'Hyper Terminal Tool Packet', 'D': 'Host Transmission Traffic Parser'},
                'correct': 'A',
                'explanation': 'HTTP is the foundational application layer protocol powering data exchange across the World Wide Web.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'In which programming language was the Unix operating system rewritten in 1972 by Dennis Ritchie at Bell Labs?',
                'options': {'A': 'Assembly', 'B': 'Fortran', 'C': 'C', 'D': 'Pascal'},
                'correct': 'C',
                'explanation': 'Dennis Ritchie created C to rewrite Unix, giving it unprecedented portability across diverse computer architectures.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'What material was the casing of Douglas Engelbart\'s original 1964 prototype computer mouse made from?',
                'options': {'A': 'Bakelite Plastic', 'B': 'Wood', 'C': 'Cast Aluminum', 'D': 'Steel'},
                'correct': 'B',
                'explanation': 'The first computer mouse, patented in 1970, was carved out of a block of wood with two perpendicular wheels.',
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'Guido van Rossum created the Python programming language in 1989. What was the name inspired by?',
                'options': {'A': 'The Burmese Python snake', 'B': 'Monty Python\'s Flying Circus', 'C': 'Greek Mythological Python', 'D': 'A code encryption cipher'},
                'correct': 'B',
                'explanation': 'Guido was reading published scripts from BBC comedy troupe Monty Python\'s Flying Circus during Christmas break.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'What was the name of the first graphical web browser created by Marc Andreessen and Eric Bina at NCSA in 1993?',
                'options': {'A': 'Netscape Navigator', 'B': 'NCSA Mosaic', 'C': 'WorldWideWeb', 'D': 'Internet Explorer'},
                'correct': 'B',
                'explanation': 'NCSA Mosaic was the breakout browser that brought inline pictures and sound to the general public.',
                'difficulty': 'medium',
                'type': 'classic'
            }
        ]
    },
    {
        'title': 'Rhyme Time & Wordplay Enigmas',
        'slug': 'words-rhymes',
        'description': 'Clever rhyming pairs, literary riddles, and linguistic wit.',
        'icon': '📚',
        'category_slug': 'words-rhymes',
        'questions': [
            {
                'prompt': 'RHYME TIME: An electric kitchen appliance that browns sliced bread, and a thrilling amusement park track with loops and drops?',
                'options': {'A': 'Toaster & Rollercoaster', 'B': 'Kettle & Metal', 'C': 'Blender & Pretender', 'D': 'Griddle & Riddle'},
                'correct': 'A',
                'explanation': 'Toaster and Rollercoaster form an exact phonetic rhyme pair!',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'RHYME TIME: A portable electronic gadget used for math arithmetic, and a large semi-aquatic reptile with sharp teeth?',
                'options': {'A': 'Abacus & Platypus', 'B': 'Calculator & Alligator', 'C': 'Compass & Walrus', 'D': 'Screen & Marine'},
                'correct': 'B',
                'explanation': 'Calculator and Alligator form an exact phonetic rhyme pair.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'RHYME TIME: A portable battery beam of light for dark rooms, and a covered architectural veranda at a front doorway?',
                'options': {'A': 'Lantern & Cistern', 'B': 'Torch & Porch', 'C': 'Lamp & Ramp', 'D': 'Flare & Stair'},
                'correct': 'B',
                'explanation': 'Torch and Porch are classic single-syllable rhyming words.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'RHYME TIME: A delicious chilled dairy dessert scooped into a waffle cone, and a loud, terrified vocal shriek?',
                'options': {'A': 'Parfait & Buffet', 'B': 'Gelato & Staccato', 'C': 'Ice Cream & Scream', 'D': 'Sundae & Monday'},
                'correct': 'C',
                'explanation': 'Ice Cream and Scream rhyme cleanly!',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'RHYME TIME: A curved yellow tropical fruit packed with potassium, and a patterned cloth handkerchief worn around the head or neck?',
                'options': {'A': 'Mango & Fandango', 'B': 'Banana & Bandana', 'C': 'Papaya & Wire', 'D': 'Melon & Felon'},
                'correct': 'B',
                'explanation': 'Banana and Bandana form a classic 3-syllable rhyming pair!',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'Which epic poem by Homer recounts the ten-year journey of Odysseus attempting to return home to Ithaca?',
                'options': {'A': 'The Iliad', 'B': 'The Aeneid', 'C': 'The Odyssey', 'D': 'Metamorphoses'},
                'correct': 'C',
                'explanation': 'The Odyssey chronicles Odysseus\' encounters with the Cyclops Polyphemus, Circe, and the Sirens.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'Who authored the 1818 landmark Gothic sci-fi novel "Frankenstein; or, The Modern Prometheus" at age 20?',
                'options': {'A': 'Jane Austen', 'B': 'Mary Shelley', 'C': 'Emily Brontë', 'D': 'Virginia Woolf'},
                'correct': 'B',
                'explanation': 'Mary Wollstonecraft Shelley conceived the novel during the "Year Without a Summer" in Switzerland in 1816.',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'In George Orwell\'s dystopian novel 1984, what totalitarian concept refers to holding two contradictory beliefs simultaneously?',
                'options': {'A': 'Newspeak', 'B': 'Thoughtcrime', 'C': 'Doublethink', 'D': 'Crimestop'},
                'correct': 'C',
                'explanation': 'Doublethink is the power of holding two contradictory beliefs in one\'s mind simultaneously, and accepting both of them.',
                'difficulty': 'medium',
                'type': 'classic'
            },
            {
                'prompt': 'In William Shakespeare\'s Hamlet, what famous soliloquy begins with the Prince of Denmark contemplating existence?',
                'options': {'A': 'All the world\'s a stage', 'B': 'To be, or not to be', 'C': 'Now is the winter of our discontent', 'D': 'Friends, Romans, countrymen'},
                'correct': 'B',
                'explanation': 'Act III, Scene 1 features Prince Hamlet\'s immortal speech: "To be, or not to be: that is the question".',
                'difficulty': 'easy',
                'type': 'classic'
            },
            {
                'prompt': 'In F. Scott Fitzgerald\'s "The Great Gatsby", what colored light at the end of Daisy\'s dock symbolizes Gatsby\'s yearning?',
                'options': {'A': 'Red light', 'B': 'Green light', 'C': 'Blue light', 'D': 'Gold light'},
                'correct': 'B',
                'explanation': 'The green light across Long Island Sound represents Gatsby\'s unattainable hopes and dreams.',
                'difficulty': 'easy',
                'type': 'classic'
            }
        ]
    }
]

SEED_LEAGUES = [
    {
        'name': 'The Cyber Tavern • Global Online Pub League',
        'slug': 'global-online-pub-league',
        'pin_code': '9999',
        'venue_name': 'Quizmondo Cyber Tavern (Online Virtual Pub)',
        'description': 'Compete from home! Join a virtual pub squad, rep your local town, and battle remote teams across the globe in online pub quiz showdowns.',
        'schedule_day': 'Live 24/7 • Hourly Tournaments',
        'teams': []
    },
    {
        'name': 'The Dog & Partridge Quiz League',
        'slug': 'dog-and-partridge',
        'pin_code': '7742',
        'venue_name': 'The Dog & Partridge Sports & Social Lounge',
        'description': 'Weekly Thursday showdown with live big screen leaderboards and bar vouchers.',
        'schedule_day': 'Every Thursday at 20:00 GMT',
        'teams': []
    },
    {
        'name': 'The Red Lion Virtual Pub Showdown',
        'slug': 'red-lion',
        'pin_code': '8821',
        'venue_name': 'The Red Lion Tavern & Craft Ale Bar',
        'description': 'High-octane pub quiz tournament with 5 rounds of audio, cinema, and history trivia.',
        'schedule_day': 'Every Tuesday at 19:30 GMT',
        'teams': []
    },
    {
        'name': "The King's Arms Sunday Brain Buster",
        'slug': 'kings-arms',
        'pin_code': '4096',
        'venue_name': "The King's Arms Traditional Coaching Inn",
        'description': 'End your weekend with the ultimate pub quiz championship. Prizes for 1st, 2nd, and Best Team Name!',
        'schedule_day': 'Every Sunday at 18:00 GMT',
        'teams': []
    }
]

# ---------------------------------------------------------------------------
# Pinned how-to guides. These sit at the top of Guides & Facts so a new player
# can find out how the place works before wading into the trivia articles.
# ---------------------------------------------------------------------------
GUIDE_CATEGORY = 'Getting Started'

GUIDE_POSTS = [
    {
        'title': 'How to Set Up Your Quizmondo Player Account',
        'slug': 'how-to-create-a-quizmondo-account',
        'pin_order': 1,
        'featured_image': '/static/img/guides/guide-register.svg',
        'excerpt': 'You can start playing without signing up at all. Here is what an account adds, and how to make one in about two minutes with just a name and a six-digit PIN.',
        'content': """<p>You do not need an account to play Quizmondo. Open the Arena and you are given a guest player straight away, with a name and an avatar, and you can answer questions immediately. An account matters when you want to keep what you earn.</p>
<h3>What an account gives you</h3>
<ul>
<li><strong>Your XP and rank survive.</strong> A guest lives in your browser. Clear your cookies, switch to your phone, and that progress is gone.</li>
<li><strong>Duels find you again.</strong> Friends challenging you by link need somewhere to send the result.</li>
<li><strong>One identity everywhere.</strong> The same account works on your laptop, your phone and a pub table.</li>
</ul>
<h3>Making one</h3>
<ol>
<li>Choose <strong>Quick Setup</strong> in the Arena header, or go to <code>/arena/register</code>.</li>
<li>Pick a <strong>player name</strong> of at least three characters. This is what opponents see, so make it something you would enjoy seeing on a leaderboard.</li>
<li>Add your <strong>email</strong>, which is only used to sign you back in.</li>
<li>Set a <strong>six-digit PIN</strong>. It works like a phone passcode and is quicker than a password on a mobile keyboard.</li>
</ol>
<p>If you were already playing as a guest, your XP comes with you rather than starting again.</p>
<h3>Signing back in</h3>
<p>Go to <code>/arena/login</code> and enter your player name or email with your PIN. Forgotten which name you used? The email works just as well.</p>
<p><a href="/arena/register"><strong>Set up an account now</strong></a> or carry on as a guest and do it later.</p>""",
    },
    {
        'title': 'How to Duel a Friend at Trivia',
        'slug': 'how-to-play-trivia-duels-against-friends',
        'pin_order': 2,
        'featured_image': '/static/img/guides/guide-duels.svg',
        'excerpt': 'Duels are turn-based, so nobody has to be online at the same time. Send a link, play your three questions, and your opponent answers whenever it suits them.',
        'content': """<p>A Quizmondo duel is not a race against someone staring at the same screen. It is turn-based, like playing chess by post: you take your turn, they take theirs, and the app keeps score. Neither of you has to be free at the same moment.</p>
<h3>Starting one</h3>
<ol>
<li>From the Arena, choose to start a duel. You get a match with its own code and link.</li>
<li>Share it. There is a <strong>WhatsApp invite</strong> button that writes the message for you, or you can copy the link anywhere.</li>
<li>Your friend taps the link. They can play as a guest, so there is nothing to install and no sign-up wall.</li>
</ol>
<h3>How a round works</h3>
<p>Each round is <strong>three questions</strong> from one category, and both players get the identical three, so the comparison is fair. Points come from being right and from being quick, so a confident fast answer beats a cautious slow one.</p>
<p>When you have both finished a round, you see a question-by-question breakdown of who got what. Then a fresh category is drawn and the next round begins, led off by whoever caught up last.</p>
<h3>If they take their time</h3>
<p>Nothing is lost while you wait. The match sits in your lobby and you can send a nudge, which writes another WhatsApp message pointing at the same link. If they never come back, you can <a href="/posts/how-to-play-trivia-against-the-bot">hand the match to the bot</a> and finish it anyway.</p>
<p><a href="/arena/"><strong>Open the Arena and start a duel</strong></a></p>""",
    },
    {
        'title': 'How to Play Against the Bot, Cyber Bot Nova',
        'slug': 'how-to-play-trivia-against-the-bot',
        'pin_order': 3,
        'featured_image': '/static/img/guides/guide-bot.svg',
        'excerpt': 'No opponent to hand, or one who has gone quiet? Nova will take the other side of any duel, answers instantly, and is a genuinely useful way to practise a category.',
        'content': """<p><strong>Cyber Bot Nova</strong> is the house opponent. Nova never needs an invitation, never leaves you waiting, and answers the moment it is their turn, which makes a bot duel the fastest way to get a game in.</p>
<h3>When to reach for the bot</h3>
<ul>
<li><strong>Nobody is about.</strong> Start a duel and take Nova instead of waiting on a friend.</li>
<li><strong>A match has stalled.</strong> If an opponent has not taken their turn, switch the match to the bot from the lobby and play it out.</li>
<li><strong>You want practice.</strong> Learning a category against Nova costs you nothing on the leaderboard that matters to your pride.</li>
</ul>
<h3>How hard is Nova?</h3>
<p>Nova gets roughly two questions in three right, with a varying speed bonus, so a solid round will beat them and a sloppy one will not. They are a fair benchmark rather than a pushover or an unbeatable machine.</p>
<h3>How it plays</h3>
<p>Exactly like a duel against a person: three questions a round, the same questions for both sides, the same scoring. The difference is that Nova's round is already done by the time you finish yours, so you go straight to the comparison and on to the next round at your own pace.</p>
<p><a href="/arena/"><strong>Start a duel and pick the bot</strong></a></p>""",
    },
    {
        'title': 'How to Join or Run a Live Pub Quiz',
        'slug': 'how-to-play-pub-quiz-games',
        'pin_order': 4,
        'featured_image': '/static/img/guides/guide-pub.svg',
        'excerpt': 'Pub quizzes are the live, hosted side of Quizmondo: a quizmaster runs the rounds, tables check in on their phones, and scores land on a big screen. Here is both sides of it.',
        'content': """<p>A pub quiz is not a duel. It is a live event with a quizmaster calling the rounds, several tables playing at once, and a shared scoreboard. Quizmondo runs them two ways: <strong>in-house</strong>, in an actual pub, and <strong>virtual</strong>, where everyone is at home.</p>
<h3>Joining as a player</h3>
<ol>
<li>Open <strong>Pub Leagues</strong> and pick the league you are playing.</li>
<li><strong>In a pub?</strong> Enter your table number and team name. The venue PIN is announced in the room or shown on the TV. Everyone on your table shares one scorecard, so one phone per table is plenty.</li>
<li><strong>Playing from home?</strong> Give your squad a name. You get your own scorecard and a <strong>squad join code</strong> you can share, so mates on other phones can play on the same card as you.</li>
<li>Wait for the quizmaster to wave you through. Your screen unlocks by itself the moment they approve you.</li>
</ol>
<h3>What a round feels like</h3>
<p>Five questions, a countdown on each one, and no feedback until the end. Your answers lock in as you go, so a lost signal or a closed tab does not cost you the round. When every table is in, the quizmaster reveals the answers and the standings move.</p>
<p>Between rounds there is usually an interval, and if the venue is running a bar offer it appears on your phone then.</p>
<h3>Running one as quizmaster</h3>
<p>Hosting needs a quizmaster or admin account. From the league's host console you approve tables as they check in, start each round, lock a round if a table wanders off, reveal the answers, call the interval and finally crown the winners. You can drive it from your phone while the big screen runs on a laptop plugged into the TV.</p>
<p>Two settings are worth knowing. <strong>Lock each round on the clock</strong> closes a round by itself once every question's timer has run out, so one table leaving early never holds up the room. <strong>Roll on to the next round by itself</strong> runs the whole quiz unattended, which is what you want for a virtual league and usually not what you want with a microphone in your hand.</p>
<p><a href="/arena/leagues"><strong>Find a pub quiz league</strong></a></p>""",
    },
    {
        'title': 'How Quizmondo Scoring, Streaks and Ranks Work',
        'slug': 'how-quizmondo-scoring-and-ranks-work',
        'pin_order': 5,
        'featured_image': '/static/img/guides/guide-arena.svg',
        'excerpt': 'Why a fast right answer is worth more than a slow one, what the final round multiplier does, and how XP turns into a rank. Worth two minutes before your next duel.',
        'content': """<p>Quizmondo rewards knowing the answer <em>and</em> knowing it quickly. Understanding the sums is worth a surprising number of points.</p>
<h3>Points on a question</h3>
<p>A correct answer is worth a base <strong>100 points</strong>, plus a <strong>speed bonus</strong> of two points for every second still on the clock. Answer a 15-second question in four seconds and the bonus is worth 22 points on top. A wrong answer and a timeout both score nothing, so a confident guess costs you no more than running the clock down.</p>
<h3>The final round counts for more</h3>
<p>The last round of a pub quiz carries a <strong>1.5x multiplier</strong> on everything you get right. A quiz is rarely over before it is over, and a table three rounds adrift can still take the night.</p>
<h3>Where the time limit comes from</h3>
<p>In a pub quiz the quizmaster sets it, anywhere from 15 to 30 seconds. Fifteen is a fast buzzer round; thirty gives a table room to argue. It is worth asking which you are playing before the first question.</p>
<h3>XP and ranks</h3>
<p>Playing earns <strong>XP</strong>, which accumulates across duels and pub quizzes and sets your position on the global leaderboard. Unlike a single match score, XP only ever goes up, so turning up regularly counts for as much as a single brilliant night.</p>
<p>One thing worth knowing: your scores are worked out on the server from the answers you send, not by your phone. Nothing you do in the browser can inflate them.</p>
<p><a href="/arena/leaderboard"><strong>See where you stand</strong></a></p>""",
    },
]

# Stock covers for the trivia articles, which shipped with no image at all and so
# every card in the feed fell back to the same esports photo.
ARTICLE_COVERS = [
    '/static/img/quizhub_trivia.jpg',
    '/static/img/quizhub_arcade.jpg',
    '/static/img/quizhub_hero.jpg',
    '/static/img/quizhub_esports.jpg',
]


SEED_POSTS = [
    {
        'title': 'Two Countries, One Flag: How Chad and Romania Ended Up Identical',
        'slug': 'chad-romania-identical-flags',
        'featured_image': '/static/img/guides/article-flags.svg',
        'excerpt': 'Blue, yellow and red vertical stripes, in that order, flown by two nations 2,500 miles apart. One of them complained to the United Nations about it. Neither has budged.',
        'content': """<p>Put the flags of Chad and Romania side by side and most people cannot tell them apart. Both are vertical tricolours of blue, yellow and red, in that order, in almost the same proportions. The only difference is a slightly deeper shade of blue on the Chadian flag, and even that is not reliable across manufacturers.</p>
<h3>How it happened</h3>
<p>Romania's colours go back to the 1860s, drawn from the arms of the historic principalities that united to form the country. Chad adopted its flag in 1959, on the eve of independence from France. The designers wanted the French blue, white and red but could not use white, because the neighbouring Mali had already taken the green, yellow and red of pan-Africanism and a white stripe would have clashed with another regional flag. Yellow went in instead, and the result was, by coincidence, Romania's flag.</p>
<p>For three decades nobody much minded, because Romania under Ceausescu flew a version with the communist coat of arms in the middle. When that emblem was removed after the 1989 revolution, the two flags became effectively identical.</p>
<h3>The complaint</h3>
<p>In 2004, as Romania prepared to join the European Union, Chad raised the matter at the United Nations and asked for a review. Romania's president at the time replied that the flag had been Romanian since 1848 and would stay as it was. No ruling followed, because no international body has the authority to award a colour scheme to anyone. Both flags still fly.</p>
<h3>They are not the only ones</h3>
<p>Monaco and Indonesia have the same two horizontal bands of red over white, differing only in proportion. Haiti and Liechtenstein discovered at the 1936 Berlin Olympics that their flags matched; Liechtenstein added a gold crown the following year. Flag design has a limited vocabulary and a very long history, and collisions are inevitable.</p>
<p>In the <strong>Match the Flags</strong> round, this pair catches almost everyone the first time.</p>""",
        'category_name': 'World Trivia'
    },
    {
        'title': 'Honey Never Spoils: The 3,000-Year-Old Jars That Are Still Edible',
        'slug': 'why-honey-never-spoils',
        'featured_image': '/static/img/guides/article-honey.svg',
        'excerpt': 'Archaeologists have opened sealed pots of honey from Egyptian tombs and found the contents perfectly good. The reason is a neat piece of chemistry that has nothing to do with preservatives.',
        'content': """<p>Honey is the only common food that does not go off. Sealed properly and kept dry, it will outlast the jar, the shelf and quite possibly the building. Pots recovered from Egyptian tombs, thousands of years old, have been found with their contents still recognisably honey.</p>
<h3>Why bacteria cannot get a foothold</h3>
<p>Three things work together. First, honey is extremely low in water. Bees fan nectar until most of the moisture has evaporated, leaving a syrup that is roughly 80 per cent sugar. Any bacterium that lands in it is dehydrated by osmosis before it can multiply.</p>
<p>Second, honey is acidic, with a pH around 3.9, which is hostile to most spoilage organisms. Third, bees add an enzyme called glucose oxidase, which produces small amounts of hydrogen peroxide as the honey matures. Between the dryness, the acid and the peroxide, there is simply nowhere for anything to grow.</p>
<h3>The catch</h3>
<p>All of that depends on the honey staying sealed. Honey is hygroscopic, meaning it pulls water out of the air, and honey that has absorbed enough moisture can ferment. This is not a modern inconvenience but an ancient discovery: mead, one of the oldest alcoholic drinks known, is fermented honey.</p>
<p>There is one genuine safety note. Raw honey can carry spores of <em>Clostridium botulinum</em>, which an adult gut handles without trouble but an infant's cannot. Honey is not recommended for children under one year old.</p>
<h3>What happens when it crystallises</h3>
<p>Honey turning cloudy and grainy in the cupboard has not gone bad. The glucose is simply coming out of solution. Stand the jar in warm water and it returns to liquid, unharmed.</p>""",
        'category_name': 'World Food & Culinary Traditions'
    },
    {
        'title': 'Why Pluto Was Demoted, and What It Takes to Count as a Planet',
        'slug': 'why-pluto-is-not-a-planet',
        'featured_image': '/static/img/guides/article-pluto.svg',
        'excerpt': 'Pluto did not change in 2006. The definition did. The real culprit was a slightly larger object called Eris, and a question astronomers could no longer dodge.',
        'content': """<p>Pluto was discovered in 1930 and taught as the ninth planet for three generations. In August 2006 it was reclassified as a dwarf planet, and a great many people took it personally. Pluto itself was unaffected. What changed was that astronomers finally had to write down what a planet is.</p>
<h3>The problem was Eris</h3>
<p>Through the 1990s and early 2000s, surveys of the outer Solar System began turning up more and more icy bodies beyond Neptune, in what is now called the Kuiper Belt. In 2005 a team found one, later named Eris, that was comparable to Pluto in size and more massive.</p>
<p>That left two options. Either Eris became the tenth planet, and so did the next dozen objects of similar size that were clearly coming, or the definition had to be tightened. The International Astronomical Union chose the second.</p>
<h3>The three tests</h3>
<ol>
<li>It must <strong>orbit the Sun</strong>. This rules out moons.</li>
<li>It must have <strong>enough mass to be roughly round</strong>, pulled into a sphere by its own gravity.</li>
<li>It must have <strong>cleared its orbital neighbourhood</strong> of other comparable bodies.</li>
</ol>
<p>Pluto passes the first two comfortably. It fails the third. Pluto shares its region with a great many Kuiper Belt objects, and it is not even gravitationally dominant among them; its orbit is shepherded by Neptune, which it crosses.</p>
<h3>So what is it now?</h3>
<p>Pluto is the best known of the dwarf planets, alongside Eris, Ceres, Haumea and Makemake. Ceres, incidentally, has been through this before: it was called a planet after its discovery in 1801, then reclassified as an asteroid when more of them turned up. Pluto is in good company.</p>
<p>The New Horizons probe flew past in 2015 and sent back images of ice mountains and a vast nitrogen glacier shaped like a heart. Whatever we call it, it turned out to be far more interesting than a label.</p>""",
        'category_name': 'Science & Cosmos'
    },
    {
        'title': 'Where the Pub Quiz Came From: A 1970s Idea to Fill Empty Mondays',
        'slug': 'history-of-the-pub-quiz',
        'featured_image': '/static/img/guides/article-pubquiz.svg',
        'excerpt': 'The British pub quiz is barely fifty years old. It was invented to get people into pubs on the quiet nights, and it worked so well that it became a national institution.',
        'content': """<p>The pub quiz feels like something that has always existed, in the way that darts and dominoes do. It has not. It is a product of the 1970s, and it was invented as a commercial fix for a specific problem: pubs were empty from Monday to Wednesday.</p>
<h3>The men who made it a business</h3>
<p>In 1976 Sharon Burns and Tom Porter set up a company called Burns and Porter to run quiz leagues in pubs. The idea was straightforward. Supply a landlord with questions, a format and a league table, and the regulars would come in on a dead night to defend their position. Within a few years they were running leagues in thousands of pubs.</p>
<p>It spread because the economics were irresistible. A quiz costs a pub almost nothing, needs no equipment beyond a microphone, and fills the slowest trading hours of the week with people buying drinks between rounds.</p>
<h3>Why the format stuck</h3>
<p>Several rounds of mixed questions, teams of four to six, answers written on paper and swapped with another table for marking, a halfway break, and a prize that is usually a bar tab. Almost every element exists for a practical reason. Teams mean nobody sits in silence. Swapping papers means the quizmaster is not marking for twenty minutes. The interval exists to sell another round.</p>
<p>The handwritten answer sheet is the part that has finally started to go. Phones made cheating trivially easy, which pushed quizzes towards either strict no-phone rules or, increasingly, running the whole thing <em>through</em> the phones instead, with answers locked in and timed.</p>
<h3>Still growing</h3>
<p>Britain is estimated to host over 20,000 pub quizzes a week, and the format has been exported wherever there are pubs. The online version, which lockdowns turned from a novelty into a habit, is the first genuine change to the model since Burns and Porter printed their first question sheet.</p>
<p>If you fancy running one yourself, <a href="/posts/how-to-play-pub-quiz-games">the guide to hosting is here</a>.</p>""",
        'category_name': 'Pub Quiz Culture'
    },
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
        'title': 'Why Asynchronous Turn-Based Quiz Duels Are the Future of Trivia',
        'slug': 'why-turn-based-quiz-duels-are-the-future',
        'excerpt': 'Why modern players prefer taking their turn during coffee breaks over waiting in rigid synchronous lobbies.',
        'content': '''<p>The success of television trivia tournaments and viral mobile quiz duels highlights a powerful truth: players love clever, multi-format trivia games, but they have busy lives.</p>
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

    # Remove legacy leaky questions
    QuizQuestion.query.filter(QuizQuestion.prompt.ilike('%flashlight torch%')).delete(synchronize_session=False)
    db.session.commit()

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
            pack.title = pack_data['title']
            pack.description = pack_data['description']
            pack.icon = pack_data['icon']
            pack.category_slug = pack_data['category_slug']
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
                existing_q.explanation = q_item['explanation']
                existing_q.options_json = json.dumps(q_item['options'])
                existing_q.correct_option = q_item['correct']
                existing_q.category_name = pack_data['title']

    # Clean up legacy Tetris YouTube clip question that displayed the answer in the video title
    legacy_yt = QuizQuestion.query.filter(
        (QuizQuestion.question_type == 'youtube_clip') |
        (QuizQuestion.prompt.like('%Listen to the opening theme of this legendary video game%'))
    ).all()
    for lq in legacy_yt:
        lq.prompt = 'Which 19th-century Russian folk song serves as the iconic "Type A" theme music in the 1989 Game Boy classic Tetris?'
        lq.question_type = 'classic'
        lq.media_url = ''
        lq.options_json = json.dumps({'A': 'Kalinka', 'B': 'Korobeiniki', 'C': 'Katyusha', 'D': 'Dark Eyes (Ochi Chyornye)'})
        lq.correct_option = 'B'
        lq.explanation = 'Composer Hirokazu Tanaka arranged the 19th-century Russian folk song "Korobeiniki" (The Peddlers) into the legendary Game Boy Tetris Type A theme.'
    db.session.commit()

    # 2b. Synchronize Extra Questions
    try:
        from .extra_questions import EXTRA_QUESTIONS
        for cat_slug, q_list in EXTRA_QUESTIONS.items():
            pack = QuizPack.query.filter_by(category_slug=cat_slug).first()
            for q_data in q_list:
                if not QuizQuestion.query.filter_by(prompt=q_data['prompt']).first():
                    q = QuizQuestion(
                        category_slug=cat_slug,
                        category_name=pack.title if pack else cat_slug.replace('-', ' ').title(),
                        prompt=q_data['prompt'],
                        question_type=q_data.get('type', 'classic'),
                        options_json=json.dumps(q_data['options']),
                        correct_option=q_data['correct'],
                        explanation=q_data['explanation'],
                        difficulty=q_data.get('difficulty', 'medium'),
                        time_limit=15,
                        points=100
                    )
                    db.session.add(q)
        db.session.commit()
    except Exception as e:
        print('Error seeding extra questions:', e)

    # 2c. Synchronize 15 Mega Categories (3,000+ Questions)
    try:
        mega_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'mega_questions_3000.json')
        if os.path.exists(mega_path):
            with open(mega_path, 'r', encoding='utf-8') as f:
                mega_data = json.load(f)

            for cat_slug, cat_info in mega_data.get('categories', {}).items():
                pack = QuizPack.query.filter_by(category_slug=cat_slug).first()
                if not pack:
                    pack = QuizPack(
                        title=cat_info['title'],
                        slug=cat_slug,
                        description=cat_info['description'],
                        icon=cat_info['icon'],
                        category_slug=cat_slug,
                        is_community=False,
                        author_name='Quizmondo Master',
                        question_count=cat_info['question_count']
                    )
                    db.session.add(pack)
                    db.session.flush()
                else:
                    pack.title = cat_info['title']
                    pack.description = cat_info['description']
                    pack.icon = cat_info['icon']
                    pack.question_count = cat_info['question_count']

                if cat_slug in ('match-flags', 'football-badges', 'brand-logos', 'country-shapes'):
                    vis_cnt = QuizQuestion.query.filter_by(category_slug=cat_slug, question_type='image').count()
                    if vis_cnt < 100:
                        QuizQuestion.query.filter_by(category_slug=cat_slug, is_community=False).delete(synchronize_session=False)
                        db.session.commit()

                existing_prompts = set(
                    r[0] for r in db.session.query(QuizQuestion.prompt).filter_by(category_slug=cat_slug).all()
                )

                new_q_objects = []
                media_updates = 0
                for q_item in cat_info.get('questions', []):
                    if q_item['prompt'] not in existing_prompts:
                        q = QuizQuestion(
                            category_slug=cat_slug,
                            category_name=cat_info['title'],
                            pack_slug=cat_slug,
                            prompt=q_item['prompt'],
                            question_type=q_item.get('type', 'classic'),
                            media_url=q_item.get('media_url', ''),
                            options_json=json.dumps(q_item['options']),
                            correct_option=q_item['correct'],
                            explanation=q_item['explanation'],
                            difficulty=q_item.get('difficulty', 'medium'),
                            points=100,
                            time_limit=15,
                            status='approved',
                            is_community=False
                        )
                        new_q_objects.append(q)
                        existing_prompts.add(q_item['prompt'])
                    elif q_item.get('media_url'):
                        existing_q = QuizQuestion.query.filter_by(category_slug=cat_slug, prompt=q_item['prompt']).first()
                        if existing_q and existing_q.media_url != q_item['media_url']:
                            existing_q.media_url = q_item['media_url']
                            existing_q.question_type = q_item.get('type', 'image')
                            media_updates += 1

                if new_q_objects:
                    db.session.bulk_save_objects(new_q_objects)
                if new_q_objects or media_updates:
                    db.session.commit()
            print("MEGA_CATEGORIES_SYNCHRONIZED_SUCCESSFULLY")
    except Exception as e:
        print('Error seeding mega categories:', e)

    # 3. Synchronize Pub Leagues (Always start clean with 0 demo tables)
    DEMO_TEAM_NAMES = {
        'The Quizly Bears', 'Tequila Mockingbird', 'Trivia Newton John', 'Quiz Pro Quo',
        'Smarty Pints', 'Beer Today, Gone Tomorrow', 'Fact Hunters', 'The Fellowship of the Quiz',
        'Agatha Quiztie', 'Universally Challenged', 'Panic at the Distro',
        'London Pint Pullers', 'Dublin Craic Squad', 'Sydney Harbour Brains', 'New York Trivia Cartel'
    }
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
            league.set_teams([])
            db.session.add(league)
        else:
            # Purge any legacy demo tables from existing leagues
            current_teams = league.get_teams()
            real_teams = [t for t in current_teams if t.get('name') not in DEMO_TEAM_NAMES]
            if len(real_teams) != len(current_teams):
                league.set_teams(real_teams)
    db.session.commit()

    # 4. Synchronize Categories & Posts
    for p_item in GUIDE_POSTS:
        guide_cat = Category.query.filter_by(name=GUIDE_CATEGORY).first()
        if not guide_cat:
            guide_cat = Category(name=GUIDE_CATEGORY, slug='getting-started')
            db.session.add(guide_cat)
            db.session.flush()

        # Match on slug, then on title, so renaming a guide in the admin does not make
        # the next deploy create a second copy of it alongside the renamed one
        guide = Post.query.filter_by(slug=p_item['slug']).first()
        if not guide:
            guide = Post.query.filter_by(title=p_item['title']).first()
        is_new_guide = guide is None
        if is_new_guide:
            guide = Post(slug=p_item['slug'], category_id=guide_cat.id,
                         created_at=datetime.utcnow() - timedelta(days=400))
            db.session.add(guide)
        # The wording is maintained here in code, so it keeps improving on each deploy
        guide.title = p_item['title']
        guide.excerpt = p_item['excerpt']
        guide.content = p_item['content']
        guide.status = 'publish'
        # Where it sits is the admin's call, so only set that when first created,
        # otherwise a reorder or an unpin would be undone by the next deploy
        if is_new_guide:
            guide.is_pinned = True
            guide.pin_order = p_item['pin_order']
        # Likewise the cover: replace the packaged artwork, never a hand-picked image
        if not guide.featured_image or guide.featured_image.startswith('/static/img/guides/'):
            guide.featured_image = p_item['featured_image']
    db.session.commit()

    # Give the trivia articles a cover each, rather than all sharing one fallback
    for idx, art in enumerate(Post.query.order_by(Post.id.asc()).all()):
        if not art.featured_image:
            art.featured_image = ARTICLE_COVERS[idx % len(ARTICLE_COVERS)]
    db.session.commit()

    # One-off cleanup: earlier seeding runs created second copies of some articles under
    # different slugs, so the same piece appeared twice in the feed. Keep the original -
    # the one whose slug still matches the seed - and drop the stray copy. Scoped to the
    # seeded titles, so two posts an admin deliberately named the same are never touched.
    for p_item in SEED_POSTS:
        same_title = Post.query.filter_by(title=p_item['title']).order_by(Post.id.asc()).all()
        if len(same_title) > 1:
            keep = next((x for x in same_title if x.slug == p_item['slug']), same_title[0])
            for stray in same_title:
                if stray.id != keep.id and not stray.is_pinned:
                    db.session.delete(stray)
    db.session.commit()

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
        # Give it the packaged cover, unless somebody has chosen their own
        if p_item.get('featured_image') and (
            not post.featured_image or post.featured_image.startswith('/static/img/')
        ):
            post.featured_image = p_item['featured_image']

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
        ('Guides, Facts & Trivia', '/posts', False)
    ]

    for idx, (title, url, open_new) in enumerate(nav_links, 1):
        h_item = MenuItem(location='header', title=title, url=url, sort_order=idx, open_new_tab=open_new)
        f_item = MenuItem(location='footer', title=title, url=url, sort_order=idx, open_new_tab=open_new)
        db.session.add(h_item)
        db.session.add(f_item)

    db.session.commit()
    print("QUIZMONDO_SEED_SYNCHRONIZED_SUCCESSFULLY")
