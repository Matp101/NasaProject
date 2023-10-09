'''
models.py
Creates the database models in SQLAlchemy
'''
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.dialects.sqlite import JSON

class User(db.Model, UserMixin): # Every successful registered user is saved as a User in the User table
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    age = db.Column(db.Integer)
    experience = db.Column(db.Integer)  # 1-Beginner, 2-Intermediate, 3-Advanced
    affiliation = db.Column(db.String(128))
    interest = db.Column(JSON)

class Projects(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.String(64000))
    experience_level = db.Column(db.Integer)  # 1-Beginner, 2-Intermediate, 3-Advanced
    skills = db.Column(JSON)
    date_posted = db.Column(db.DateTime(timezone=True), default=func.now())
    # Foreign key reference to User model's primary key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Define the relationship with User model
    user = db.relationship('User', backref=db.backref('projects', lazy=True))
