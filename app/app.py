# app.py

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///f1predictor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Example User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    favorite_team = db.Column(db.String(80))

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    race_name = db.Column(db.String(120))
    predicted_winner = db.Column(db.String(80))
    actual_winner = db.Column(db.String(80))
    points = db.Column(db.Integer)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    predictions = Prediction.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, predictions=predictions)

@app.route('/chatbot')
def chatbot():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('chatbot.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_message = data['message']

    # For now, dummy AI response
    if 'driver' in user_message.lower():
        reply = "Your team's main driver is Max Verstappen."
    elif 'car' in user_message.lower():
        reply = "Your team has 2 race cars for the season."
    elif 'score' in user_message.lower():
        reply = "The last race score was 1st place!"
    else:
        reply = "I'm still learning! Try asking about drivers, cars, or scores."

    return jsonify({ 'reply': reply })

if __name__ == '__main__':
    app.run(debug=True)