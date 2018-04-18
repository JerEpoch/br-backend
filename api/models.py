from api import db
# 1 = regular user, 2 = stream(elevated stuff), 3 = admin(full access)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    userAccess = db.Column(db.Integer, index=True, default=1)

    def __repr__(self):
        return '<User {}> <userAccess {}>'.format(self.username, self.userAccess)