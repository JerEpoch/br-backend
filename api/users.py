import base64
import os
from flask import jsonify, request, json, current_app, g
from api import db, app
from api.models import User
from datetime import datetime, timedelta
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import jwt

# def create_token(username):
#     token = jwt.encode({
#         'sub': username,
#         'iat':datetime.utcnow(),
#         'exp': datetime.utcnow() + timedelta(minutes=30)},
#         current_app.config['SECRET_KEY'])
#     g.current_user.set_user_token(token)
#     #db.session.add(token)
#     db.session.commit()
#     return { 'token': token.decode('UTF-8') }

def create_user_token(username):
    expires = timedelta(days=7)
    user_tkn = {
        'access_token': create_access_token(identity=username, expires_delta=expires),
    }
    # g.current_user.set_user_token(user_tkn['access_token'])
    # db.session.commit()
    return user_tkn

def check_user_email(data):
    if 'email' not in data:
        return True
    else:
        if User.query.filter_by(email=data['email']).first():
            return False

@app.route('/bracket-api/users/create', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"errorMsg": "Something went wrong with adding user."}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"errorMsg": "Username is taken."}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"errorMsg": "That email is already taken."}), 400
    user = User()
    g.current_user = user
    try:
        user.from_dict(data, new_user=True)
        db.session.add(user)
        db.session.commit()
        # print(user.id)
        #create_token(data['username'])
        u_token = create_user_token(data['username'])
        #response = jsonify({"successMsg": "User was created"}, token)
        response = jsonify(user.to_dict(), u_token)
        response.status_code = 201
        return response
    except:
        return jsonify({'errorMsg': 'Something went wrong.'}), 500

@app.route('/bracket-api/users/login', methods=['POST'])
def login_user():
    data = request.get_json() or {}
    user = User.authenticate(**data)
    g.current_user = user

    if not user:
        return jsonify({'errorMsg': 'Invalid credentials', 'authenticated': False}), 401

    
    token = jsonify(create_user_token(g.current_user.username))
    return token

@app.route('/bracket-api/testjwt', methods=['POST', 'GET'])
@jwt_required
def test_jwt():
    return jsonify({'msg': 'cool, jwt protected work!!'})

# @app.route('/bracket-api/users/access', methods=['POST'])
# @jwt_required
# def get_userAccess():
#     current_user = get_jwt_identity()

@app.route('/bracket-api/users/edit/user', methods=['POST', 'GET'])
@jwt_required
def edit_user():
    current_user = get_jwt_identity()
    if current_user:

        data = request.get_json() or {}
        user = User.query.filter_by(username=current_user).first()
        if request.method == 'GET':
            return jsonify(user.to_dict()), 200
        
        if request.method == 'POST':
            if user.check_password(data['password']):
                if not check_user_email(data):
                    return jsonify({"errorMsg": "Please use a different email address."}), 400 
                try:
                    user.edit_user_profile(data)
                    db.session.add(user)
                    db.session.commit()
                    return jsonify({'data': user.to_dict()})
                except:
                    return jsonify({'errorMsg': 'Something went wrong.'}), 500
            else:
                return jsonify({'errorMsg': 'Email and password do not match.'})
    else:
        return jsonify({'errorMsg': 'Unauthorized user.'})


@app.route('/bracket-api/users/user', methods=['POST', 'GET'])
@jwt_required
def get_user():
    # auth_header = request.headers.get('Authorization', '').split()
    # token = auth_header[0]
    # data = jwt.decode(token, current_app.config['SECRET_KEY'])
    # user = User.query.filter_by(username=data['sub']).first()
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    user_access = user.userAccess
    userId = user.id
    ret_data = {'logged_in_as':current_user, 'userId': userId, 'user_access': user_access}
    return jsonify(ret_data), 200
    #return jsonify({'stuff': 'this is a user'})

    # invalid_msg = {'errorMsg': 'Please Login', 'authenticated': False}


    # if len(auth_header) !=2:
    #     return jsonify(invalid_msg), 401

    # try:
    #     token = auth_header[1]
    #     data = jwt.decode(token, current_app.config['SECRET_KEY'])
    #     user = User.query.filter_by(username=data['sub']).first()
    #     if not user:
    #         raise RuntimeError('User was not found')
    #     return jsonify({'username': user.username})
    # except jwt.ExpiredSignature:
    #     # return jsonify(invalid_msg), 401
    #     return jsonify({'msg': 'expired'})
    # except(jwt.InvalidTokenError, Exception) as e:
    #     return jsonify(invalid_msg), 401

