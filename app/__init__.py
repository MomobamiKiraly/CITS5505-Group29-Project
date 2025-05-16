import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask extensions (but not bound to app yet)
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    # Create Flask app instance with custom static folder path
    app = Flask(
        __name__,
        static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    )

    # Load configuration from environment variables or use defaults
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "your-secret-key")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your-database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Flask extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)  # ✅ CSRF protection initialized

    # Set the login view for Flask-Login
    login_manager.login_view = 'main.login'

    # Register the main blueprint containing routes
    from app.routes import main
    app.register_blueprint(main)

    # Import models to ensure they are registered with SQLAlchemy
    from app.models import User  
    from app import models       

    # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Set upload folder and max upload size for profile pictures
    app.config['UPLOAD_FOLDER'] = 'app/static/profile_pics'
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2 MB

    return app