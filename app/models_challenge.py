"""Games Challenge: five mini games, two players, one week.

Its own module, like models_games and models_mail, so models.py stays
untouched.

The scoring is deliberately NOT a sum of normalised scores. Mini game scores
are wildly different animals -- a good Picture Slide is a few thousand, a good
Digit Span is a couple of hundred -- and the registry's xp_rate exists to turn
each into XP, not to make them comparable to each other. Its own comment says
it only aims to land a good run "somewhere around 60-180 XP", so two players
could be three times apart on XP while being equally good at the games.

So each game is its own head to head: whoever scored higher on that game wins
that game, and the challenge goes to whoever won more of the five. That is
immune to how the rates are tuned, it is easier to say out loud -- you won
three games to two -- and it keeps a challenge alive until the last game.
Normalised XP is kept only to break a 2-2 or similar tie.
"""
import json
import secrets
import string
from datetime import datetime, timedelta

from .models import db

# Long enough that a link cannot be guessed, short enough to read out.
CODE_ALPHABET = string.ascii_uppercase + string.digits
CODE_LENGTH = 6
GAMES_PER_CHALLENGE = 5
# A week. Long enough to fit around a life, short enough to stay interesting.
CHALLENGE_DAYS = 7


def new_challenge_code():
    for _ in range(40):
        code = ''.join(secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH))
        if not GameChallenge.query.filter_by(code=code).first():
            return code
    return ''.join(secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH + 2))


class GameChallenge(db.Model):
    """Five games, picked once when the challenge is opened."""
    __tablename__ = 'game_challenges'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(12), unique=True, index=True, nullable=False)
    status = db.Column(db.String(20), default='waiting')   # waiting | active | complete

    creator_key = db.Column(db.String(64), index=True, nullable=False)
    creator_name = db.Column(db.String(80), default='Player')
    creator_avatar = db.Column(db.String(40), default='quizzy')

    opponent_key = db.Column(db.String(64), index=True)
    opponent_name = db.Column(db.String(80))
    opponent_avatar = db.Column(db.String(40), default='quizzy')

    game_keys_json = db.Column(db.Text, default='[]')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime,
                           default=lambda: datetime.utcnow() + timedelta(days=CHALLENGE_DAYS))

    def games(self):
        try:
            return list(json.loads(self.game_keys_json or '[]'))
        except (TypeError, ValueError):
            return []

    def set_games(self, keys):
        self.game_keys_json = json.dumps(list(keys))

    @property
    def expired(self):
        return bool(self.expires_at and datetime.utcnow() >= self.expires_at)

    def days_left(self):
        """Rounded up, so a challenge opened a minute ago says seven, not six.

        .days truncates, and "6 days left" on something you have just started
        reads like it has already eaten a day.
        """
        if not self.expires_at:
            return 0
        left = self.expires_at - datetime.utcnow()
        if left.total_seconds() <= 0:
            return 0
        return max(1, -(-left.total_seconds() // 86400).__int__())

    def is_player(self, key):
        return key and key in (self.creator_key, self.opponent_key)

    def scores_for(self, key):
        """{game_key: score} for one player."""
        rows = GameChallengeScore.query.filter_by(challenge_id=self.id, player_key=key).all()
        return {r.game_key: (r.score or 0) for r in rows}

    def standings(self):
        """Who won each game, and therefore the challenge.

        A game nobody has played yet is nobody's. A game only one player has
        played is theirs -- if the other never gets round to it, not playing
        is losing.
        """
        mine = self.scores_for(self.creator_key)
        theirs = self.scores_for(self.opponent_key) if self.opponent_key else {}
        rows, c_wins, o_wins = [], 0, 0
        for key in self.games():
            a, b = mine.get(key), theirs.get(key)
            winner = None
            if a is not None and b is not None:
                winner = 'creator' if a > b else ('opponent' if b > a else 'tie')
            elif a is not None and self.expired:
                winner = 'creator'
            elif b is not None and self.expired:
                winner = 'opponent'
            if winner == 'creator':
                c_wins += 1
            elif winner == 'opponent':
                o_wins += 1
            rows.append({'game_key': key, 'creator_score': a, 'opponent_score': b,
                         'winner': winner, 'played_by_both': a is not None and b is not None})
        return {'rows': rows, 'creator_wins': c_wins, 'opponent_wins': o_wins}

    def leader(self, xp_rates=None):
        """'creator', 'opponent' or None, counting games won then XP."""
        table = self.standings()
        if table['creator_wins'] != table['opponent_wins']:
            return 'creator' if table['creator_wins'] > table['opponent_wins'] else 'opponent'
        if not xp_rates:
            return None
        mine = self.scores_for(self.creator_key)
        theirs = self.scores_for(self.opponent_key) if self.opponent_key else {}
        cx = sum((mine.get(k) or 0) * xp_rates.get(k, 0.1) for k in self.games())
        ox = sum((theirs.get(k) or 0) * xp_rates.get(k, 0.1) for k in self.games())
        if abs(cx - ox) < 0.5:
            return None
        return 'creator' if cx > ox else 'opponent'


class GameChallengeScore(db.Model):
    """One player's score on one game of one challenge.

    Separate from MiniGameScore, which keeps a single lifetime best per game
    and so cannot hold a result that belongs to a particular contest.
    """
    __tablename__ = 'game_challenge_scores'
    __table_args__ = (
        db.UniqueConstraint('challenge_id', 'player_key', 'game_key',
                            name='uq_challenge_player_game'),
    )

    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, index=True, nullable=False)
    player_key = db.Column(db.String(64), index=True, nullable=False)
    game_key = db.Column(db.String(40), nullable=False)
    score = db.Column(db.Integer, default=0)
    played_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def record(challenge, player_key, game_key, score):
        """First score counts. One go each, or it becomes a grinding contest."""
        existing = GameChallengeScore.query.filter_by(
            challenge_id=challenge.id, player_key=player_key, game_key=game_key).first()
        if existing:
            return False
        db.session.add(GameChallengeScore(
            challenge_id=challenge.id, player_key=player_key,
            game_key=game_key, score=max(0, int(score or 0))))
        db.session.commit()
        return True
