# Import the db instance from the current package (__init__.py)
from . import db
# Import UserMixin to add default implementations for user authentication methods
from flask_login import UserMixin
# Import func from SQLAlchemy to use SQL functions
from sqlalchemy.sql import func

# Define the Note model representing the notes table in the database
class Note(db.Model):
    # Define the columns of the notes table
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    data = db.Column(db.String(10000))  # Column to store the note data, with a maximum length of 10,000 characters
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # Column to store the date and time of the note creation, with a default value of the current time
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key column to reference the user who created the note

# Define the User model representing the users table in the database
class User(db.Model, UserMixin):
    # Define the columns of the users table
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    email = db.Column(db.String(150), unique=True, nullable=False)  # Column to store the user's email, which must be unique and cannot be null
    password = db.Column(db.String(150), nullable=False)  # Column to store the user's password, which cannot be null
    name = db.Column(db.String(80))  # Column to store the user's name
    notes = db.relationship('Note', backref='user', lazy=True)  # Establish a one-to-many relationship with the Note model; 'backref' creates a virtual column in the Note model to reference the User, and 'lazy=True' indicates that related objects should be loaded only when accessed
