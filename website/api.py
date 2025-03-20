from flask import Blueprint, request, jsonify, url_for, redirect
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import jwt
import datetime
from .models import Note, User
from . import db, mail


api = Blueprint('api', __name__)

@api.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()  # Holt JSON-Daten aus der Anfrage
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Ungültige Anfrage"}), 400
    
    user = User.query.filter_by(email=data["email"]).first()
    if user and check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"error": "Falsche Login-Daten"}), 401

# API-Login-Route welche bei erfolgreicher Anmeldung einen JSON-Token zurückgibt. 
# JSON-Token für weitere API-Routen nötig.


@api.route('/api/notes', methods=['GET'])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    notes = Note.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": note.id, "data": note.data, "date": note.date} for note in notes]), 200

# API-Route-Get um Notizen von Benutzer abzurufen


@api.route('/api/notes', methods=['POST'])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.json.get('data', '')

    if not data:
        return jsonify({"error": "Notizinhalt darf nicht leer sein"}), 400

    new_note = Note(data=data, user_id=user_id)
    db.session.add(new_note)
    db.session.commit()
    
    return jsonify({"message": "Notiz erfolgreich erstellt", "note_id": new_note.id}), 201

# API-Route-Post um neue Notiz zu erstellen


@api.route('/api/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()

    if not note:
        return jsonify({"error": "Notiz nicht gefunden"}), 404

    db.session.delete(note)
    db.session.commit()
    
    return jsonify({"message": "Notiz erfolgreich gelöscht"}), 200

# API-Route-Delete um Notiz zu löschen




# Hier befindet sich ebenfalls code für die E-Mail-Verifizierung, welcher aus Zeitgründen für später aufgehoben wird.
""" # E-Mail-Verifizierung Token generieren
def generate_verification_token(email):
    return jwt.encode({'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, "secret", algorithm="HS256")

# E-Mail senden mit Bestätigungslink
def send_verification_email(user):
    token = generate_verification_token(user.email)
    verify_url = url_for('auth.verify_email', token=token, _external=True)
    msg = Message("Verify Your Email", sender='your-email@gmail.com', recipients=[user.email])
    msg.body = f"Click the link to verify your email: {verify_url}"
    mail.send(msg)
    print("Verification email sent!") """

""" 
# Route für E-Mail-Verifizierung
@api.route('/verify-email/<token>')
def verify_email(token):
    try:
        data = jwt.decode(token, "secret", algorithms=["HS256"])
        user = User.query.filter_by(email=data["email"]).first()
        if user:
            user.is_verified = True
            db.session.commit()
            return redirect(url_for('auth.login'))
        return jsonify({"error": "Invalid token"}), 400
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 400
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 400
 """
