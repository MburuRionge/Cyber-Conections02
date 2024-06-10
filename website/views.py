# Import necessary modules and functions from Flask and other dependencies
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note  # Import the Note model from the models module
from . import db  # Import the db instance from the current package (__init__.py)
import json  # Import the json module to handle JSON data
from .models import User  # Import the User model from the models module

# Create a Blueprint named 'views'. This helps in organizing the view-related routes.
views = Blueprint('views', __name__)

# Define the home route which handles both GET and POST requests
@views.route('/', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in to access this route
def home():
    if request.method == 'POST':  # Check if the request method is POST
        note = request.form.get('note')  # Get the note data from the form

        if len(note) < 1:  # Check if the note is too short
            flash('Note is too short!', category='error')  # Flash an error message
        else:
            # Create a new note with the provided data and the current user's ID
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)  # Add the new note to the database session
            db.session.commit()  # Commit the session to save the note
            flash('Note added!', category='success')  # Flash a success message

    return render_template("home.html", user=current_user)  # Render the home template with the current user

# Define the delete-note route which handles POST requests
@views.route('/delete-note', methods=['POST'])
def delete_note():
    # Load the note data from the request's JSON payload
    note = json.loads(request.data)
    noteId = note['noteId']  # Extract the note ID from the JSON data
    note = Note.query.get(noteId)  # Query the database for the note with the given ID
    if note:
        if note.user_id == current_user.id:  # Check if the current user is the owner of the note
            db.session.delete(note)  # Delete the note from the database session
            db.session.commit()  # Commit the session to remove the note from the database

    return jsonify({})  # Return an empty JSON response

