from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def get_database_uri():
    return os.environ.get('DATABASE_URL', 'sqlite:///prompts.db')

def configure_app(app):
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

def setup_user_loader():
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

def register_blueprints(app):
    from app.routes import main_bp
    app.register_blueprint(main_bp)

def create_app():
    app = Flask(__name__)
    configure_app(app)
    initialize_extensions(app)
    setup_user_loader()
    register_blueprints(app)
    
    with app.app_context():
        db.create_all()
    
    return app
