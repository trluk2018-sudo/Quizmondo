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

if __name__ == '__main__':
    unittest.main()
