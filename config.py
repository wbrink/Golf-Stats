import os
basedir = os.path.abspath(os.path.dirname(__file__))
# absolute path of the directory where config.py resides
# os.path.dirname(__file__) returns that but with forward slashes instead of back slashes
# abspath() fixes this so its backslashes [good for linux]

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
