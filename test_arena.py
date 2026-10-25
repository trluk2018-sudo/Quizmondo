import unittest
import json
from app import create_app
from app.models import db, PlayerProfile, ArenaMatch, ArenaRound, QuizQuestion

class ArenaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SECRET_KEY': 'test-secret'
        })
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def test_arena_dashboard_auto_player(self):
        res = self.client.get('/arena/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Arena Headquarters', res.data)
        self.assertIn(b'Quizmondo.com', res.data)

    def test_create_friend_match_and_whatsapp_invite(self):
        # 1. Create match
        res = self.client.post('/arena/new', data={'opponent_mode': 'friend'}, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'MATCH ID:', res.data)
        self.assertIn(b'whatsappText', res.data)
        self.assertIn(b'Play Round 1 Now', res.data)

    def test_create_bot_match_and_play_round(self):
        # 1. Create bot match
        res = self.client.post('/arena/new', data={'opponent_mode': 'bot'}, follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        match_lobby_url = res.headers['Location']
        match_code = match_lobby_url.split('/')[-1]

        # 2. Check play round screen
        res_play = self.client.get(f'/arena/match/{match_code}/play')
        self.assertEqual(res_play.status_code, 200)
        self.assertIn(b'ROUND 1/6', res_play.data)

        # 3. Submit answers to round
        with self.app.app_context():
            m = ArenaMatch.query.filter_by(match_code=match_code).first()
            r = m.rounds.filter_by(round_number=1).first()
            q_ids = r.get_question_ids()
            payload = {
                'answers': [
                    {'question_id': q_ids[0], 'choice': 'B', 'time_left': 10},
                    {'question_id': q_ids[1], 'choice': 'C', 'time_left': 12},
                    {'question_id': q_ids[2], 'choice': 'A', 'time_left': 8}
                ]
            }

        res_sub = self.client.post(f'/arena/match/{match_code}/submit', json=payload)
        self.assertEqual(res_sub.status_code, 200)
        data = json.loads(res_sub.data)
        self.assertTrue(data['success'])
        self.assertIn('round_score', data)
        self.assertIn('player_xp', data)

    def test_leaderboard(self):
        res = self.client.get('/arena/leaderboard')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'GLOBAL LEADERBOARD', res.data)

    def test_leagues(self):
        res = self.client.get('/arena/leagues')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'PUB LEAGUES', res.data)

    def test_community_question_creation_and_packs(self):
        # 1. View create form
        res = self.client.get('/arena/create')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Author Quizmondo Trivia', res.data)

        # 2. Submit clean question
        post_data = {
            'prompt': 'What is the speed of light in vacuum?',
            'question_type': 'classic',
            'category_slug': 'science-cosmos',
            'category_name': 'Science & Cosmos',
            'opt_a': '299,792 km/s',
            'opt_b': '150,000 km/s',
            'opt_c': '384,400 km/s',
            'opt_d': '1,080 km/s',
            'correct_option': 'A',
            'explanation': 'Light moves at roughly 300,000 km/s in vacuum.',
            'difficulty': 'medium',
            'pack_slug': 'physics-master'
        }
        res_post = self.client.post('/arena/create', data=post_data, follow_redirects=True)
        self.assertEqual(res_post.status_code, 200)
        self.assertIn(b'Question published to Quizmondo Arena', res_post.data)

        # Verify question in DB
        with self.app.app_context():
            q = QuizQuestion.query.filter_by(prompt='What is the speed of light in vacuum?').first()
            self.assertIsNotNone(q)
            self.assertEqual(q.status, 'approved')
            self.assertTrue(q.is_community)

        # 3. View packs directory
        res_packs = self.client.get('/arena/packs')
        self.assertEqual(res_packs.status_code, 200)
        self.assertIn(b'Trivia Packs', res_packs.data)

    def test_profanity_filter_triggers_pending_moderation(self):
        # Submit question containing flagged keyword
        post_data = {
            'prompt': 'Is this a free casino scam test question?',
            'question_type': 'classic',
            'category_slug': 'general',
            'category_name': 'General Knowledge',
            'opt_a': 'Yes',
            'opt_b': 'No',
            'correct_option': 'A'
        }
        res_post = self.client.post('/arena/create', data=post_data, follow_redirects=True)
        self.assertEqual(res_post.status_code, 200)
        self.assertIn(b'in the moderation queue', res_post.data)

        with self.app.app_context():
            q = QuizQuestion.query.filter_by(prompt='Is this a free casino scam test question?').first()
            self.assertIsNotNone(q)
            self.assertEqual(q.status, 'pending')

    def test_pub_league_pin_join_lounge_and_tv(self):
        # 1. Join via PIN code
        res_join = self.client.post('/arena/leagues/join', data={'pin_code': '7742'}, follow_redirects=True)
        self.assertEqual(res_join.status_code, 200)
        self.assertIn(b'Dog &amp; Partridge', res_join.data)
        self.assertIn(b'TABLE ROOM PIN', res_join.data)

        # 2. Big Screen TV Mode
        res_tv = self.client.get('/arena/leagues/dog-and-partridge/tv')
        self.assertEqual(res_tv.status_code, 200)
        self.assertIn(b'LIVE VENUE TOURNAMENT', res_tv.data)
        self.assertIn(b'1ST PLACE', res_tv.data)

        # 3. Enter interactive room
        res_room = self.client.get('/arena/leagues/dog-and-partridge/room?team=The+Quizly+Bears')
        self.assertEqual(res_room.status_code, 200)
        self.assertIn(b'PUB ROUND 1', res_room.data)

        # 4. Submit round score
        res_sub = self.client.post('/arena/leagues/dog-and-partridge/room', data={'score': '450'}, follow_redirects=True)
        self.assertEqual(res_sub.status_code, 200)
        self.assertIn(b'Round submitted for Team', res_sub.data)

if __name__ == '__main__':
    unittest.main()
