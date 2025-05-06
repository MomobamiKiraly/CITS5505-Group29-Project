import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()  

def create_app():
    
    app = Flask(
        __name__,
        static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    )

    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your-database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  

    login_manager.login_view = 'main.login'

    from app.routes import main
    app.register_blueprint(main)

    from app.models import User  
    from app import models       

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.config['UPLOAD_FOLDER'] = 'app/static/profile_pics'
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  

    return app