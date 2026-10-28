"""Module registry, default configurations, and layout seeding for Quizmondo Arena."""

import copy

MODULE_DEFINITIONS = {
    'hero': {
        'type': 'hero',
        'name': 'Hero Arcade Banner',
        'icon': 'hero',
        'badge': 'Hero Header',
        'description': 'Full-width arcade header with headline, subtext, dual game buttons, and verified player metrics.',
        'default_placement': 'above',
        'default_config': {
            'badge': 'ARCADE TRIVIA & MULTIPLAYER DUELS',
            'headline': 'The Cosmic Brain Arena: Challenge Friends & Climb the Leaderboards',
            'subtext': 'Battle head-to-head in turn-based trivia duels, join weekly live pub quiz leagues, and author community quiz decks. 100% free with instant WhatsApp invitations!',
            'primary_btn_text': 'Play Daily Challenge ⚡',
            'primary_btn_url': '/arena/',
            'secondary_btn_text': 'Browse Trivia Decks',
            'secondary_btn_url': '/arena/packs',
            'metric_val_1': '50,000+', 'metric_lbl_1': 'Questions Answered',
            'metric_val_2': '6 Tracks', 'metric_lbl_2': 'Master Categories',
            'metric_val_3': '12 Max', 'metric_lbl_3': 'Daily Concurrent Duels',
            'metric_val_4': '100% Free', 'metric_lbl_4': 'Zero App Store Needed',
            'cert_text': 'Fair-play certified scoring with combo streaks and speed multipliers',
            'bg_style': 'gradient-navy',
            'yt_enabled': '0',
            'yt_video_url': '',
            'yt_start': '',
            'yt_end': '',
            'yt_overlay_color': '#090317',
            'yt_overlay_opacity': '85',
        }
    },
    'daily_quiz': {
        'type': 'daily_quiz',
        'name': 'Daily Brain Challenge Widget',
        'icon': 'quiz',
        'badge': 'Interactive Arena',
        'description': 'Live interactive daily question sprint with Web Audio sound effects, mascot reactions, and WhatsApp score sharing.',
        'default_placement': 'above',
        'default_config': {
            'badge': 'DAILY SPRINT',
            'headline': 'Live Daily Brain Challenge',
            'subtext': 'Test your speed and precision against today\'s curated cosmic trivia question!',
        }
    },
    'features_strip': {
        'type': 'features_strip',
        'name': 'Core Features Highlight Strip',
        'icon': 'strip',
        'badge': '3-Column Highlights',
        'description': '3-column highlights showcasing duels, community creator studio, and pub quiz leagues.',
        'default_placement': 'above',
        'default_config': {
            'item1_title': 'Turn-Based Head-to-Head Duels',
            'item1_text': '6-round turn-based matches inspired by Quiz Planet. Invite friends via WhatsApp or battle AI Bot Nova instantly.',
            'item1_icon': 'shield',
            'item2_title': 'Community Trivia Studio',
            'item2_text': 'Author custom question decks like Sporcle and JetPunk. Every approved deck rewards you with +150 XP and coins.',
            'item2_icon': 'cloud',
            'item3_title': 'Pub Quiz Leagues & Big Screen TV',
            'item3_text': 'Enter venue room PINs or project live tournament leaderboards onto venue TVs for the ultimate pub quiz night.',
            'item3_icon': 'cpu',
            'bg_style': 'navy',
        }
    },
    'about': {
        'type': 'about',
        'name': 'About & Game Engine Lore',
        'icon': 'about',
        'badge': 'Engine Lore',
        'description': 'The Quizmondo origin narrative, unique game design, fair-play rules, and interactive formats.',
        'default_placement': 'above',
        'default_config': {
            'badge': 'GAME ENGINE & PHILOSOPHY',
            'headline': 'Where Knowledge Meets Arcade Gaming & TV Game Show Thrills',
            'subtext': 'Inspired by timeless classics like Quiz Planet, television brain championships, and authentic pub quiz culture, Quizmondo re-imagines trivia for the mobile web era with zero app store gatekeepers.',
            'year_established': '2026',
            'check_1': 'Zero-bandwidth procedural Web Audio synthesizer with arcade heartbeat timers',
            'check_2': 'Multi-format rounds: Classic 4-choice, YouTube music/video clips, and visual puzzles',
            'check_3': 'Dynamic speed multipliers: Faster answers award up to +50 bonus XP per round',
            'stat1_val': '250+ XP', 'stat1_lbl': 'Avg Match Experience Gain',
            'stat2_val': '100% Free', 'stat2_lbl': 'Client-Side WhatsApp Deep Linking',
        }
    },
    'services': {
        'type': 'services',
        'name': 'Trivia Disciplines & Categories Grid',
        'icon': 'services',
        'badge': '6-Card Grid',
        'description': 'Showcase the 6 primary arena disciplines and custom question tracks.',
        'default_placement': 'above',
        'default_config': {
            'badge': 'ARENA DISCIPLINES',
            'headline': 'Explore the 6 Master Trivia Categories',
            'subtext': 'Choose your specialty in head-to-head matches or conquer all 6 categories to prove your trivia supremacy.',
            'srv1_title': '🌌 Science & Cosmos',
            'srv1_text': 'Planetary astronomy, astrophysics, quantum particles, biological oddities, and space missions.',
            'srv2_title': '🎮 Gaming & Esports',
            'srv2_text': 'Retro 8-bit classics, console wars, modern competitive esports, speedrun records, and lore.',
            'srv3_title': '🏛️ World History & Enigmas',
            'srv3_text': 'Ancient civilizations, lost empires, pivotal revolutions, wartime strategies, and unsolved mysteries.',
            'srv4_title': '🎵 Music & Sound Waveforms',
            'srv4_text': 'Name that track, iconic guitar riffs, synthpop anthems, chiptunes, and chart-topping legends.',
            'srv5_title': '🎬 Cinema & TV Pop Culture',
            'srv5_text': 'Blockbuster sagas, cult television classics, Academy Award trivia, anime, and directors.',
            'srv6_title': '⚽ Sports & Olympic Lore',
            'srv6_text': 'World cups, premier league history, Olympic gold moments, basketball titans, and records.',
        }
    },
    'case_studies': {
        'type': 'case_studies',
        'name': 'Prize Vault, Merch & Rewards',
        'icon': 'cases',
        'badge': 'Rewards Vault',
        'description': 'Showcase prizes, Quizmondo merch (t-shirts, mugs), and partner discounts.',
        'default_placement': 'below',
        'default_config': {
            'badge': 'PRIZE VAULT & MERCH',
            'headline': 'Win Exclusive Merch, T-Shirts & Partner Discounts',
            'subtext': 'Top the weekly leaderboard, maintain your streak, or win pub tournaments to unlock real-world swag!',
            'cs1_tag': 'Arcade Apparel',
            'cs1_title': 'Official Quizmondo Champion T-Shirts',
            'cs1_result': 'Awarded to Monthly Arena Grandmasters and tournament winners.',
            'cs2_tag': 'Ceramic Swag',
            'cs2_title': 'The Grandmaster Cosmic Coffee Mug',
            'cs2_result': 'Double-walled ceramic mug for late-night trivia strategists.',
            'cs3_tag': 'Partner Perks',
            'cs3_title': 'Local Pub Quiz Drinks Vouchers',
            'cs3_result': 'Partner discounts at participating virtual and physical trivia venues.',
        }
    },
    'posts': {
        'type': 'posts',
        'name': 'Latest Trivia Dispatches & Articles',
        'icon': 'news',
        'badge': 'Dynamic Feed',
        'description': 'Dynamic feed of recent trivia articles, game guides, and tournament announcements.',
        'default_placement': 'below',
        'default_config': {
            'badge': 'TRIVIA DISPATCHES',
            'headline': 'Latest Articles, Quiz Guides & Strategy',
            'subtext': 'Deep dives into science lore, pop culture history, and expert tips from master quizmasters.',
            'count': '3',
        }
    },
    'testimonials': {
        'type': 'testimonials',
        'name': 'Player & Pub Captain Reviews',
        'icon': 'reviews',
        'badge': 'Player Endorsements',
        'description': 'Real reviews from casual players, pub quiz captains, and trivia enthusiasts.',
        'default_placement': 'below',
        'default_config': {
            'badge': 'PLAYER VOICES',
            'headline': 'Loved by Casual Thinkers & Pub Quiz Champions',
            'subtext': 'See how players across the UK and worldwide are using Quizmondo to test their minds every day.',
            't1_quote': 'The turn-based duels on WhatsApp are brilliant. We challenge each other during lunch break, and nobody has to install a bloated app!',
            't1_author': 'Liam K.',
            't1_role': 'Pub Quiz Team Captain, London',
            't2_quote': 'The YouTube video rounds and procedural audio make this feel like playing a real TV game show. Truly unmatched.',
            't2_author': 'Elena R.',
            't2_role': 'Trivia Enthusiast & Speedrunner',
        }
    },
    'trust_strip': {
        'type': 'trust_strip',
        'name': 'Game Show & Fair Play Strip',
        'icon': 'trust',
        'badge': 'Standards',
        'description': 'Fair play standards, zero spam guarantee, and verified community badges.',
        'default_placement': 'below',
        'default_config': {
            'headline': 'Quizmondo Fair-Play & Integrity Standards',
            'badge1': '100% Free Core Gameplay',
            'badge2': 'Zero Heavy App Downloads',
            'badge3': 'Human & AI Moderated Questions',
            'badge4': 'Encrypted Player Sessions',
        }
    },
    'contact_form': {
        'type': 'contact_form',
        'name': 'Host a Tournament / Inquiry Desk',
        'icon': 'form',
        'badge': 'Tournament Desk',
        'description': 'Contact form for venue partnerships, corporate trivia nights, and custom quiz pack sponsorships.',
        'default_placement': 'below',
        'default_config': {
            'badge': 'HOST A TOURNAMENT',
            'headline': 'Bring Quizmondo to Your Pub, School, or Corporate Event',
            'subtext': 'Want a private tournament room with custom questions, sponsor branding, or big-screen TV projector integration? Let\'s build your event!',
            'noc_title': 'Are You a Pub Landlord or Quizmaster?',
            'noc_text': 'Generate recurring weekly league PINs with automated team leaderboards and zero paperwork.',
            'button_text': 'Inquire About Venue Hosting →',
        }
    },
    'game_arcade': {
        'type': 'game_arcade',
        'name': 'Game Arcade Picks',
        'icon': 'games',
        'badge': 'Game Shelf',
        'description': 'A hand-picked shelf of up to 6 games, puzzles or quizzes, each with its own artwork, tag and link, over animated arcade backdrop art.',
        'default_placement': 'above',
        'default_config': {
            'badge': 'TODAY IN THE ARCADE',
            'headline': 'Pick Your Game',
            'subtext': 'Daily puzzles, word games and quiz rounds. No downloads, no sign-up needed \u2014 just pick one and play.',
            'columns': '3',
            'art_style': 'arcade-grid',
            'art_placement': 'background',
            'art_opacity': '55',
            'art_accent': '#22d3ee',
            'art_second': '#a855f7',
            'c1_on': '1', 'c1_emoji': '\U0001f5d3\ufe0f', 'c1_tag': 'Daily',
            'c1_title': 'Daily Crossword Challenge',
            'c1_text': 'A fresh grid every morning that builds through the week, from Monday gentle to Sunday fiendish.',
            'c1_url': '/games/crossword', 'c1_cta': 'Solve today', 'c1_accent': 'amber',
            'c2_on': '1', 'c2_emoji': '\u26a1', 'c2_tag': 'Sprint',
            'c2_title': 'Daily Brain Sprint',
            'c2_text': 'One quick-fire question set against the clock. Speed bonuses, streaks and a place on the board.',
            'c2_url': '/games/daily', 'c2_cta': 'Start sprint', 'c2_accent': 'cyan',
            'c3_on': '1', 'c3_emoji': '\U0001f50d', 'c3_tag': 'Word Game',
            'c3_title': 'Word Search',
            'c3_text': 'Themed grids with hidden words to hunt down. Easy to start, hard to put down.',
            'c3_url': '/games/word-search', 'c3_cta': 'Find the words', 'c3_accent': 'emerald',
            'c4_on': '1', 'c4_emoji': '\u2694\ufe0f', 'c4_tag': 'Multiplayer',
            'c4_title': 'Head-to-Head Duel',
            'c4_text': 'Six rounds, turn by turn, against a friend over WhatsApp or against Bot Nova right now.',
            'c4_url': '/arena/', 'c4_cta': 'Challenge someone', 'c4_accent': 'rose',
            'c5_on': '1', 'c5_emoji': '\U0001f9e9', 'c5_tag': 'Puzzle',
            'c5_title': 'Anagrams',
            'c5_text': 'Untangle the letters before the timer runs out, with a hint if you get properly stuck.',
            'c5_url': '/games/anagrams', 'c5_cta': 'Unscramble', 'c5_accent': 'purple',
            'c6_on': '1', 'c6_emoji': '\U0001f3c6', 'c6_tag': 'All Games',
            'c6_title': 'The Full Games Hub',
            'c6_text': 'Twenty-odd mini games in one place, with your best scores and the daily leaderboard.',
            'c6_url': '/games/', 'c6_cta': 'Browse them all', 'c6_accent': 'pink',
            'button_text': 'See every game',
            'button_url': '/games/',
            'button_note': 'Free to play, nothing to install.',
        }
    },
    'rich_text': {
        'type': 'rich_text',
        'name': 'Custom Content & Callout Block',
        'icon': 'text',
        'badge': 'Flexible Content',
        'description': 'Add custom headings, optional styled excerpt, rich text/HTML body, or custom highlighted announcements.',
        'default_placement': 'below',
        'default_config': {
            'badge': 'SPECIAL ANNOUNCEMENT',
            'headline': 'Weekly Cosmic Championship Series',
            'excerpt': 'Compete every Sunday at 8 PM GMT for exclusive badges and prize vault loot.',
            'body': '<p>Register your squad or enter as a solo gladiator. 3 rounds of 10 high-speed questions covering all 6 arena tracks!</p>',
            'bg_style': 'slate-50',
            'button_text': 'Join Tournament Lobby',
            'button_url': '/arena/leagues',
        }
    }
}


def get_default_config(module_type: str) -> dict:
    defn = MODULE_DEFINITIONS.get(module_type)
    if defn and 'default_config' in defn:
        return copy.deepcopy(defn['default_config'])
    return {}


def get_module_definition(module_type: str) -> dict:
    return MODULE_DEFINITIONS.get(module_type, {
        'type': module_type,
        'name': module_type.replace('_', ' ').title(),
        'icon': 'cube',
        'badge': 'Custom Module',
        'description': '',
        'default_placement': 'above',
        'default_config': {}
    })
