import unittest
import os
import json
from api import app, db
from api.models import User, Tournament, TournamentPlayers, Matches
from config import Config

class TestConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = 'sqlite://'

class TestBackendApi(unittest.TestCase):

  def setUp(self):
    self.app = app(TestConfig)
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    #self.client = self.app.test_client

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()
 

  # def testApiOne(self):
  #   response = self.client().get('/bracket-api/api')
  #   data = json.loads(response.get_data(as_text=True))
  #   self.assertEqual(data['msg'], "hello from api")

  def testApiCreate(self):
    print("TESTING CREATE USER:")
    headers = {'content-type': 'application/json'}
    data = {      
      'email':"test23423@test.com",
      'username': "testUserOne",
      'password': "testpassword"
      }
    resp = self.client().post('/bracket-api/users/create', data=json.dumps(data), headers=headers)
    print(resp.data)
    with self.app.app_context():
      user = User.query.filter_by(username='testUserOne').first()
      print(user.token)
    self.assertEqual(resp.status_code, 201)

  # def listUser(self):
  #   with self.app.app_context():
  #     print("listing user")
  #     user = User.query.filter_by(username='testUserOne').first()
  #     if(user):
  #       print("user token is")
  #       print(user.token)
      
  # def test_createTourn(self):
  #   print("===============================")
  #   print("Testing Create Tournament")
  #   print("===============================")
  #   headers = {'content-type': 'application/json'}
  #   # bracket = {
  #   #   'playerOne': "Bob",
  #   #   'playerTwo': "Jane",
  #   #   'playerOne': "Jim",
  #   #   'playerTwo': "Janice",
  #   #   'playerOne': 'Test'
  #   # }
  #   bracket = ('playerOne','Bob')
  #   data = {
  #     'bracket': bracket,
  #     'tournamentName': 'Tournament One',
  #     'round': 1
  #   }

  #   resp = self.client().post('/bracket-api/test', data=json.dumps(data), headers=headers)
  #   print(resp.data)
  #   self.assertEqual(resp.status_code, 200)

  # def tearDown(self):
  #   with self.app.app_context():
  #     if User.query.filter_by(username='testUserOne').first():
  #       print("deleting test user")
  #       user = User.query.filter_by(username='testUserOne').first()
  #       db.session.delete(user)
  #       db.session.commit()

class TestTournament(unittest.TestCase):
  pass
if __name__ == "__main__":
  unittest.main()