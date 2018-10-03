from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    registration_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stats = db.Column(db.PickleType) # df of the form input
    course = db.Column(db.String(32), index=True)
    timestamp = db.Column(db.Date, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer, index=True)
    tourney = db.Column(db.Boolean, index=True)
    eighteen = db.Column(db.Boolean, index=True) # eighteen holes or not
    nine = db.Column(db.Boolean, index=True)
    statistics = db.Column(db.PickleType) # df of values for stats
    notes = db.Column(db.String(140))
    classifier = db.Column(db.String(10), index=True, default='Alright')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(15), index=True)
    course = db.Column(db.String(32), index=True)
    layout = db.Column(db.PickleType)

# this is used for the current_user functionality
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
