from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
#import dash

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager()
login.init_app(app)
login.login_view = 'login'
# login.login_message = u'custom message'  --> defualt is 'Please log in to access this page'

#########################dash
#using dash for one of the pages
#app_dash = dash.Dash(__name__, server=app, url_base_pathname='/pathname')
########################


from app import routes, models
