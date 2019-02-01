#from api import app
from flask import json, jsonify
from flask_cors import cross_origin
from api.models import User
from api.testing import bp
  

@bp.route('/')
def index():
    return 'Hello World'


@bp.route('/bracket-api/api')
def api():
    return json.dumps({"msg": "hello from api"})

@bp.route('/bracket-api/api/two')
def api_two():
    user = User.query.filter_by(username='blah01').first()
    token = user.token
    if(token):
        return jsonify({'msg': token.decode('UTF-8')})
    return jsonify({'user': user.email})
    
    
    # users = User.query.all()

    # user_list = []
    # for user in users:
    #     user_data = {}
    #     user_data['username'] = user.username
    #     user_data['user_access'] = user.userAccess
    #     # user_data['token'] = user.token
    #     user_list.append(user_data)
    # return jsonify({'users': user_list})
    
    # return json.dumps({"msg": "This is api two"})

