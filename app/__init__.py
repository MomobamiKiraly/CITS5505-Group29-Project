from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///f1predictor.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app