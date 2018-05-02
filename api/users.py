import base64
import os
from flask import jsonify, request, json, current_app
from api import db, app
from api.models import User
from datetime import datetime, timedelta
from flask_httpauth import HTTPBasicAuth
import jwt

def create_token(email):
    token = jwt.encode({
        'sub': email,
        'iat':datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        current_app.config['SECRET_KEY'])
    return { 'token': token.decode('UTF-8') }

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
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    token = create_token(data['email'])
    response = jsonify({"successMsg": "User was created"}, token)
    response.status_code = 201
    return response
    
@app.route('/bracket-api/users/login', methods=['POST'])
def login_user():
    data = request.get_json() or {}
    user = User.authenticate(**data)

    if not user:
        return jsonify({'errorMsg': 'Invalid credentials', 'authenticated': False}), 401

    token = jsonify(create_token(data['email']))
    return token

