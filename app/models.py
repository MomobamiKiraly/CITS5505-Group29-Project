from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    favorite_team = db.Column(db.String(100))
    favorite_driver = db.Column(db.String(100))

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    race_name = db.Column(db.String(120))
    predicted_winner = db.Column(db.String(80))
    actual_winner = db.Column(db.String(80))
    points = db.Column(db.Integer)