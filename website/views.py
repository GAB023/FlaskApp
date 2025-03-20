from flask import Blueprint, jsonify, render_template, request, flash
from flask_login import login_required, current_user
from .models import Note
from . import db
import json


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')


    return render_template("home.html", user=current_user)

#mit user=user-


@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note_data = request.get_json()
    print("Received request data:", note_data)  # Debugging
    
    note_id = note_data.get('id')  # Sicherstellen dass nur "id" geholt wird!

    if not note_id or not isinstance(note_id, int):  # Prüfen, ob ID eine Zahl ist
        return jsonify({"error": "Invalid note ID"}), 400

    note = Note.query.get(note_id)
    
    if not note:
        return jsonify({"error": "Note not found"}), 404

    if note.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(note)
    db.session.commit()

    return jsonify({"message": "Note deleted successfully"}), 200


 