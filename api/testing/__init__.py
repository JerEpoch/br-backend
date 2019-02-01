from flask import Blueprint

bp = Blueprint('testing', __name__)

from api.testing import routes