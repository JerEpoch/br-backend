from api.models import User
from api import db

def main():
  if User.query.filter_by(username='jeradmin').first():
    print("User exists, exiting...")
  else:
    print("creating the admin...")
    user = User(username='jeradmin', email='jersoc@gmail.com', userAccess='admin')
    user.set_password('jeradmin')
    db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
  main()
