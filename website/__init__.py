# Import necessary modules from Flask and other dependencies
from flask import Flask  # Flask is the main class for creating a Flask web application
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy is an ORM for database interactions
from os import path  # Used for file path operations
from flask_login import LoginManager  # LoginManager is used for managing user login sessions
from flask_migrate import Migrate  # Migrate handles database migrations

# Create an instance of SQLAlchemy to manage database operations
db = SQLAlchemy()
# Create an instance of Migrate to handle database migrations
migrate = Migrate()
# Define the name of the database file
DB_NAME = "database.db"

# Function to create and configure the Flask application
def create_app():
    app = Flask(__name__)  # Initialize the Flask application
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'  # Set the secret key for session management and security
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Set the database URI for SQLAlchemy

    db.init_app(app)  # Initialize the database with the app
    migrate.init_app(app, db)  # Initialize migration support with the app and database

    # Import the blueprints from the views and auth modules
    from .views import views
    from .auth import auth

    # Register the blueprints with the app
    # Blueprints help in organizing the application into modules
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import the models to ensure they are registered with SQLAlchemy
    from .models import User, Note

    # Create the database tables if they don't exist already
    with app.app_context():
        db.create_all()

    # Set up the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Specify the login view
    login_manager.init_app(app)  # Initialize the login manager with the app

    # User loader function for Flask-Login
    # This function loads a user by their ID
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Query the database for the user with the given ID

    return app  # Return the configured Flask app instance

# Function to create the database file if it doesn't exist
def create_database(app):
    if not path.exists('website/' + DB_NAME):  # Check if the database file already exists
        db.create_all(app=app)  # Create all the database tables
        print('Created Database!')  # Print a message indicating the database was created
