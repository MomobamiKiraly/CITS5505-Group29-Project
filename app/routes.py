import openai
import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from app.forms import LoginForm
from app.models import User, Prediction
from flask_login import login_user
from app import db


main = Blueprint('main', __name__)

@main.route('/')
def home():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('main.profile'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('main.register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)  # 用加密密码存储
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

@main.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Password reset link would be sent (simulation).', 'info')
        else:
            flash('Email not found.', 'danger')
        return redirect(url_for('main.login'))
    return render_template('forgot_password.html')

@main.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.favorite_team = request.form.get('favorite_team')
        user.favorite_driver = request.form.get('favorite_driver')
        db.session.commit()

        flash('Profile updated successfully.', 'success')
        return redirect(url_for('main.profile'))

    return render_template('edit_profile.html', user=user)

@main.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    user = User.query.get(session['user_id'])
    predictions = Prediction.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, predictions=predictions)

@main.route('/chatbot')
def chatbot():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    return render_template('chatbot.html')

@main.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_message = data['message']

    # Dummy AI response
    if 'driver' in user_message.lower():
        reply = "Your team's main driver is Max Verstappen."
    elif 'car' in user_message.lower():
        reply = "Your team has 2 race cars for the season."
    elif 'score' in user_message.lower():
        reply = "The last race score was 1st place!"
    else:
        reply = "I'm still learning! Try asking about drivers, cars, or scores."

    return jsonify({'reply': reply})

from flask_login import logout_user

@main.route('/logout')
def logout():
    logout_user()  # 调用 Flask-Login 的 logout
    session.clear()  # 清除 session
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main.route('/upload', methods=['GET', 'POST'])
def upload():
    teams = [
     {"name": "Ferrari", "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/team%20logos/ferrari.jpg"},
    {"name": "Red Bull", "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/team%20logos/red%20bull.jpg"},
    {"name": "Mercedes", "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/team%20logos/mercedes.jpg"},
    {"name": "McLaren", "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/team%20logos/mclaren.jpg"}
    ]

    drivers_by_team = {
    "Ferrari": [
        {"name": "Charles Leclerc", "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/leclerc.jpg"},
        {"name": "Lewis Hamilton", "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/hamilton.jpg"}
    ],
    "Red Bull": [
        {"name": "Max Verstappen", "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/verstappen.jpg"},
        {"name": "Liam Lawson", "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/lawson.jpg"}
    ],
    "Mercedes": [
        {"name": "George Russell", "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/russell.jpg"},
        {"name": "Andrea Kimi Antonelli", "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/antonelli.jpg"}
    ],
    "McLaren": [
        {"name": "Lando Norris", "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/norris.jpg"},
        {"name": "Oscar Piastri", "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/piastri.jpg"}
    ]
    }

    if request.method == 'POST':
        user = User(
            full_name=request.form['full_name'],
            age=request.form['age'],
            team=request.form['team'],
            driver=request.form['driver']
        )
        db.session.add(user)
        db.session.commit()

        prediction = Prediction(
            user_id=user.id,
            race_winner=request.form['race_winner'],
            top_3=request.form['top_3'],
            fastest_lap=request.form['fastest_lap']
        )
        db.session.add(prediction)
        db.session.commit()

        flash('Data successfully uploaded!', 'success')
        return redirect(url_for('main.upload'))

    return render_template('upload.html', teams=teams, drivers_by_team=drivers_by_team)

from flask import request, jsonify
import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

@main.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    print("Received message:", user_message)

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message["content"]
        print("OpenAI reply:", reply)
        return jsonify({"reply": reply})
    except Exception as e:
        print("OpenAI Error:", e)  
        return jsonify({"error": str(e)}), 500







