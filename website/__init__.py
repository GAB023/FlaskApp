from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()  
# Diese Zeile lädt die .env Datei


db = SQLAlchemy()
mail = Mail()  
migrate = Migrate() 
jwt = JWTManager()

# Hier wurde aufgrund dem Hochladen auf GitHub die Zugangsdaten der DB entfert.
# Diese muss beim Deployment manuell erstellt werden. 


def create_app():
    app = Flask(__name__)

    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    
    app.config['SECRET_KEY'] = 'abc'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # JWT Schlüssel für Tokens

    # Code für E-Mail-Versand
    # app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
    # app.config['MAIL_PORT'] = 2525
    # app.config['MAIL_USERNAME'] = 'd0a66c57318c82'  # Benutzername von Mailtrap
    # app.config['MAIL_PASSWORD'] = 'e0a6dea2a18664'
    # app.config['MAIL_USE_TLS'] = True
    # app.config['MAIL_USE_SSL'] = False

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)  # **Mail initialisieren**
    migrate.init_app(app, db)  # **Flask-Migrate initialisieren**

    from .views import views
    from .auth import auth
    from .models import User, Note  # **Modelle importieren**
    from .api import api  # **API zuletzt importieren**

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api, url_prefix='/')

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    with app.app_context():
        db.create_all()
        print("Created MySQL-Datenbank")

# Bei erfolgreicher Erstellung von DB erhalten wir print-Ausgabe.
