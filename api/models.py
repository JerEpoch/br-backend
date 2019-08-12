from api import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

#import jwt
from flask import current_app
# 1 = regular user, 2 = streamer(elevated stuff), 3 = admin(full access)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    elPage = db.Column(db.String(256))
    twitch = db.Column(db.String(128))
    twitter = db.Column(db.String(256))
    about = db.Column(db.String)
    token = db.Column(db.String(32), index=True, unique=True)
    userAccess = db.Column(db.String(32), index=True, default='user')
    tournaments = db.relationship('Tournament', backref="tournaments", lazy='dynamic')
    news_posts = db.relationship('MemberNewsPost', backref="author", lazy='dynamic')

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
    
    def edit_user_profile(self, data):
        for field in ['email', 'elPage', 'twitch', 'twitter', 'about']:
            if field in data:
                setattr(self, field, data[field])
            if 'newPassword' in data:
                self.set_password(data['newPassword'])

    @staticmethod
    def check_user_token(token):
        user = User.query.filter_by(token=token).first
        if user is None:
            return None
        
        return user

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
        return dict(id=self.id, email=self.email, username=self.username, userAccess=self.userAccess, elPage=self.elPage, twitter=self.twitter, twitch=self.twitch, aboutMe=self.about)


class Tournament(db.Model):
    __tablename__ = 'tournaments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tournament_title = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_completed = db.Column(db.Boolean, default=False)
    players = db.relationship('TournamentPlayers', backref='players', lazy='dynamic')
    matches = db.relationship('Matches', backref='match_round', lazy='dynamic')

    def __repr__(self):
        return '<Tournament {}>'.format(self.tournament_title)

    # sets the tournament completation status. Should pretty much be true as false is default
    def set_isCompleted(self, isCompleted):
        self.is_completed = isCompleted

    def to_dict(self):
        return dict(id=self.id, userID=self.user_id, tournament_title=self.tournament_title, players=[player.to_dict() for player in self.players], 
        match=[match.to_dict() for match in self.matches],tournamentCompleted=self.is_completed)


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
    title = db.Column(db.String(100), nullable=False)
    player_one = db.Column(db.String(100), nullable=False)
    player_two = db.Column(db.String(100), nullable=True)
    round_completed = db.Column(db.Boolean, default=False)
    tournament_id  = db.Column(db.Integer, db.ForeignKey('tournaments.id'))
    #bracket_position = db.Column(db.Integer)

    # sets the match up for next round
    def set_nextMatch(self, playerOne, playerTwo, round):
        self.round = round
        self.player_one = playerOne
        self.player_two = playerTwo

    


    def to_dict(self):
        return dict(id=self.id, tournamentId=self.tournament_id, playerOne=self.player_one, playerTwo=self.player_two, round=self.round, isCompleted=self.round_completed, roundTitle=self.title)


class MemberNewsPost(db.Model):
    __tablename__ = 'membernewspost'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.Column(db.String, nullable=False)
    news_title = db.Column(db.String, nullable=False)
    news_post = db.Column(db.String, nullable=False)
    is_announcement = db.Column(db.Boolean, nullable=False, default=False)
    publish_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Post {}>'.format(self.news_post)

    def from_dict(self, data):
        for field in ['news_title', 'news_post', 'is_announcement']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        return dict(id=self.id, user=self.user, newsTitle=self.news_title, newsPost=self.news_post, publishDate=self.publish_date, isAnnouncement=self.is_announcement)