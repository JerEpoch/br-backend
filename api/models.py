from api import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
# 1 = regular user, 2 = stream(elevated stuff), 3 = admin(full access)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    userAccess = db.Column(db.String(64), index=True, default='user')

    def __repr__(self):
        return '<User {}> <userAccess {}>'.format(self.username, self.userAccess)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def set_user_role(self, role):
        self.userAccess = role

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
            if new_user and 'password' in data:
                self.set_password(data['password'])

    @classmethod
    def authenticate(cls, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')

        if not username or not password:
            return None

        user = cls.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return None
        
        return user

    def to_dict(self):
        return dict(id=self.id, email=self.email, username=self.username, userAccess=self.userAccess)
    