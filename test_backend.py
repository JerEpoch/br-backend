import unittest
import os
import json
from api import app, db
from api.models import User

class TestBackendApi(unittest.TestCase):

  def setUp(self):
    self.app = app
    self.client = self.app.test_client
    

  def testApiOne(self):
    response = self.client().get('/bracket-api/api')
    data = json.loads(response.get_data(as_text=True))
    self.assertEqual(data['msg'], "hello from api")

  def testApiCreate(self):
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

  def listUser(self):
    with self.app.app_context():
      print("listing user")
      user = User.query.filter_by(username='testUserOne').first()
      if(user):
        print("user token is")
        print(user.token)
      
  def create_tourn(self):
    pass

  def tearDown(self):
    with self.app.app_context():
      if User.query.filter_by(username='testUserOne').first():
        print("deleting test user")
        user = User.query.filter_by(username='testUserOne').first()
        db.session.delete(user)
        db.session.commit()


if __name__ == "__main__":
  unittest.main()