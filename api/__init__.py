from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# login = LoginManager(app)
# jwt = JWTManager(app)
#CORS(app)

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
jwt = JWTManager()
cors = CORS()

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)

  db.init_app(app)
  migrate.init_app(app, db)
  login.init_app(app)
  cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
  jwt.init_app(app)

  from api.auth import bp as auth_bp
  app.register_blueprint(auth_bp)

  from api.main import bp as main_bp
  app.register_blueprint(main_bp)

  from api.testing import bp as testing_bp
  app.register_blueprint(testing_bp)

  return app

#from api import routes, users, models, tournament
from api import models