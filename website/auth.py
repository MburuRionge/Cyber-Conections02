# Import necessary modules and functions from Flask and other dependencies
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User  # Import User model from the models module
from .models import Note  # Import Note model from the models module
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # Import the db instance from the current package (__init__.py)
from flask_login import login_user, login_required, logout_user, current_user

# Create a Blueprint named 'auth'. This helps in organizing the authentication-related routes.
auth = Blueprint('auth', __name__)

# Define the login route which handles both GET and POST requests
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Check if the request method is POST
        email = request.form.get('email')  # Get the email from the form
        password = request.form.get('password')  # Get the password from the form

        # Query the database for a user with the provided email
        user = User.query.filter_by(email=email).first()
        if user:
            # Check if the provided password matches the stored password hash
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')  # Flash a success message
                login_user(user, remember=True)  # Log the user in
                return redirect(url_for('views.home'))  # Redirect to the home page
            else:
                flash('Incorrect password, try again.', category='error')  # Flash an error message
        else:
            flash('Email does not exist.', category='error')  # Flash an error message

    return render_template("login.html", user=current_user)  # Render the login template

# Define the logout route which requires the user to be logged in
@auth.route('/logout')
@login_required
def logout():
    logout_user()  # Log the user out
    return redirect(url_for('auth.login'))  # Redirect to the login page

# Define the sign-up route which handles both GET and POST requests
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':  # Check if the request method is POST
        email = request.form.get('email')  # Get the email from the form
        name = request.form.get('name')  # Get the name from the form
        password1 = request.form.get('password1')  # Get the first password from the form
        password2 = request.form.get('password2')  # Get the second password from the form

        # Query the database for a user with the provided email
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')  # Flash an error message
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')  # Flash an error message
        elif len(name) < 2:
            flash('Organization name must be greater than 1 character.', category='error')  # Flash an error message
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')  # Flash an error message
        elif len(password1) < 3:
            flash('Password must be at least 3 characters.', category='error')  # Flash an error message
        else:
            # Create a new user with the provided data and hashed password
            new_user = User(email=email, name=name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)  # Add the new user to the database session
            db.session.commit()  # Commit the session to save the user
            login_user(new_user, remember=True)  # Log the new user in
            flash('Account created!', category='success')  # Flash a success message
            return redirect(url_for('views.home'))  # Redirect to the home page

    return render_template("sign_up.html", user=current_user)  # Render the sign-up template

# Define the search route which requires the user to be logged in and handles GET requests
@auth.route("/search", methods=['GET'])
@login_required
def search():
    q = request.args.get("q")  # Get the search query from the request arguments
    results = []
    user_notes = []

    if q:
        # Use ILIKE for case-insensitive search and partial matches
        results = db.session.query(User).join(Note).filter(
            (User.name.ilike(f'%{q}%')) |
            (User.email.ilike(f'%{q}%'))
        ).all()  # Execute the query and get the results
        print("Query executed, results:", results)  # Print the results for debugging

    # Get current user's notes if the user is authenticated
    if current_user.is_authenticated:
        user_notes = current_user.notes

    return render_template("search.html", user=current_user, results=results, user_notes=user_notes)  # Render the search template
