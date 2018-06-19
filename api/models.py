from api import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

import jwt
from flask import current_app
# 1 = regular user, 2 = streamer(elevated stuff), 3 = admin(full access)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    userAccess = db.Column(db.String(32), index=True, default='user')
    tournaments = db.relationship('Tournament', backref="tournaments", lazy='dynamic')

    def __repr__(self):
        return '<User {}> <userAccess {}>'.format(self.username, self.userAccess)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def set_user_role(self, role):
        self.userAccess = role

    def set_user_token(self, token):
        self.token = token

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
            if new_user and 'password' in data:
                self.set_password(data['password'])

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None
        
        return user

    def to_dict(self):
        return dict(id=self.id, email=self.email, username=self.username, userAccess=self.userAccess)


class Tournament(db.Model):
    __tablename__ = 'tournaments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tournament_title = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_completed = db.Column(db.Boolean, default=False)
    players = db.relationship('TournamentPlayers', backref='players', lazy='dynamic')
    matches = db.relationship('Matches', backref='matches', lazy='dynamic')

    def __repr__(self):
        return '<Tournament {}>'.format(self.tournament_title)

    # sets the tournament completation status. Should pretty much be true as false is default
    def set_isCompleted(self, isCompleted):
        self.is_completed = isCompleted

    def to_dict(self):
        return dict(id=self.id, tournament_title=self.tournament_title, players=[player.to_dict() for player in self.players], match=[match.to_dict() for match in self.matches])


class TournamentPlayers(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100), nullable=False)
    is_elimanated = db.Column(db.Boolean, default=False)
    is_winner = db.Column(db.Boolean, default=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'))

    def to_dict(self):
        return dict(id=self.id, playerName= self.player_name, eliminated=self.is_elimanated, isWinner=self.is_winner)


class Matches(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.Integer, nullable=False)
    player_one = db.Column(db.String(100), nullable=False)
    player_two = db.Column(db.String(100), nullable=False)
    tournament_id  = db.Column(db.Integer, db.ForeignKey('tournaments.id'))
    #bracket_position = db.Column(db.Integer)

    # sets the match up for next round
    def set_nextMatch(self, playerOne, playerTwo, round):
        self.round = round
        self.player_one = playerOne
        self.player_two = playerTwo

    


    def to_dict(self):
        return dict(id=self.id, tournamentId=self.tournament_id, playerOne=self.player_one, playerTwo=self.player_two, round=self.round)
     