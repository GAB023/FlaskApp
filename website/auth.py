from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, mail
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
import jwt
import datetime
from datetime import datetime, timedelta


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.account_locked_until:
            if datetime.utcnow() < user.account_locked_until:
                flash('Your account is locked due to multiple failed login attempts. Try again later.', category='error')
                return redirect(url_for('auth.login'))
            else:
                user.account_locked_until = None
                user.failed_login_attempts = 0
                db.session.commit()
        #Prüft, ob das Konto gesperrt ist und mit else Sperre aufheben, falls die Zeit abgelaufen ist

        if user:
        # Für spätere Implementation stehen gelassen.
        #     if not user.is_verified:
        #         flash('Please verify your email before logging in.', category='error')
        #         return redirect(url_for('auth.login'))
            
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)

                user.failed_login_attempts = 0
                db.session.commit()
                #Erfolgreicher Login → Fehlversuche zurücksetzen

                return redirect(url_for('views.home'))
            else:
                #Fehlversuch zählen
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 3:
                    user.account_locked_until = datetime.utcnow() + timedelta(hours=24)  # 24h Sperrung
                    flash('Too many failed login attempts. Your account is locked for 24 hours.', category='error')
                else:
                    flash(f'Incorrect password, {3 - user.failed_login_attempts} attempts remaining.', category='error')

                db.session.commit()
        else:
            flash('Email does not exist. Please Sign Up to access.', category='error')

    return render_template("login.html", user=current_user)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('auth.login'))  


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user_count = User.query.count()
        if user_count >= 6:
            flash('Max Amount of User reached.', category='error')
            return redirect(url_for('auth.sign_up')) 
        # Prüft ob Grenze von 6 Benutzer erreicht wurde bevor User erstellt wird.
        # Blockiert weitere Registrierungen, fall Max Anzahl User erreicht wurde.


        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First Name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(
                email=email, 
                first_name=first_name, 
                password=generate_password_hash(password1, method='pbkdf2:sha256'),
                failed_login_attempts=0,  # Anzahl Fehlversuche wird auf 0 gesetzt
                account_locked_until=None  # Kein Sperrzeitpunkt initial
            )
            
            db.session.add(new_user)
            db.session.commit()

#            send_verification_email(new_user)  # E-Mail senden
            
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))  # Direkt zur Login-Seite

    return render_template("sign_up.html", user=current_user)





#Untenstehend befindet sich code für die E-Mail Verifizierung beim Login, welcher auskommentiert wurde, da nicht funktioniert und keine Zeit vorhanden um noch einzurichten.
#Wird für spätere einrichtung auskommentiert. 

# def generate_verification_token(email):
#     return jwt.encode({'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, 
#                      "secret", algorithm="HS256")

# def send_verification_email(user):
#     token = generate_verification_token(user.email)
#     verify_url = url_for('auth.verify_email', token=token, _external=True)
#     
#     msg = Message("Verify Your Email", sender='your-email@gmail.com', recipients=[user.email])
#     msg.body = f"Click the link to verify your email: {verify_url}"
#     
#     mail.send(msg)
#     print(f"Verification email sent to {user.email}!")


# @auth.route('/verify-email/<token>')
# def verify_email(token):
#     try:
#         data = jwt.decode(token, "secret", algorithms=["HS256"])
#         user = User.query.filter_by(email=data["email"]).first()
#         if user and not user.is_verified:
#             user.is_verified = True
#             db.session.commit()
#             flash("Your email has been verified. You can now log in.", category="success")
#             return redirect(url_for('auth.login'))
#         else:
#             flash("Invalid or expired token.", category="error")
#             return redirect(url_for('auth.login'))
#     except jwt.ExpiredSignatureError:
#         flash("Verification link has expired.", category="error")
#         return redirect(url_for('auth.sign_up'))
#     except jwt.InvalidTokenError:
#         flash("Invalid token.", category="error")
#         return redirect(url_for('auth.sign_up'))
