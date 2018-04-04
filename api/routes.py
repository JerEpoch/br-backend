from api import app
from flask import json
from flask_cors import cross_origin

@app.route('/')
def index():
    return 'Hello World'


@app.route('/api')
def api():
    return json.dumps({"msg": "hello from api"})

@app.route('/api/two')
def api_two():
    return json.dumps({"msg": "This is api two"})