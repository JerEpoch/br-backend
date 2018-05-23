from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
login = LoginManager(app)
jwt = JWTManager(app)
#CORS(app)

from api import routes, users, models