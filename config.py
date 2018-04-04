import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dhisisakey390slk39lkj94kjz'