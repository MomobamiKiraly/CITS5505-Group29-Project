import openai
import os
import requests
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify, current_app
from flask_login import login_user, logout_user
from werkzeug.utils import secure_filename
from app.forms import LoginForm
from app.models import User, Prediction
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

        new_user= User(username=username, email=email)
        new_user.set_password(password)
        new_user.profile_pic = url_for('static', filename='profile_pics/default.jpg')
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
        user.username = request.form.get('username', user.username)
        user.email = request.form.get('email', user.email)
        user.favorite_team = request.form.get('favorite_team')
        user.favorite_driver = request.form.get('favorite_driver')
        user.bio = request.form.get('bio')

        # Handle profile picture upload
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename:
                filename = secure_filename(file.filename)
                upload_folder = os.path.join(current_app.root_path, 'static', 'profile_pics')
                os.makedirs(upload_folder, exist_ok=True)
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                user.profile_pic = f'/static/profile_pics/{filename}'

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

    if 'driver' in user_message.lower():
        reply = "Your team's main driver is Max Verstappen."
    elif 'car' in user_message.lower():
        reply = "Your team has 2 race cars for the season."
    elif 'score' in user_message.lower():
        reply = "The last race score was 1st place!"
    else:
        reply = "I'm still learning! Try asking about drivers, cars, or scores."

    return jsonify({'reply': reply})

@main.route('/logout')
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main.route('/upload', methods=['GET', 'POST'])
def upload():
    teams = [
        {"name": "Ferrari", "image_url": "..."},
        {"name": "Red Bull", "image_url": "..."},
        {"name": "Mercedes", "image_url": "..."},
        {"name": "McLaren", "image_url": "..."}
    ]

    drivers_by_team = {
        "Ferrari": [...],
        "Red Bull": [...],
        "Mercedes": [...],
        "McLaren": [...]
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

@main.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": "Bearer sk-840cc1a0773847b58044106e33e2119d",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": user_message}]
            },
            timeout=30
        )

        output = response.json()
        if "choices" in output and output["choices"]:
            reply = output["choices"][0]["message"]["content"]
        else:
            reply = "Sorry, DeepSeek did not return a valid response."

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": f"DeepSeek API error: {str(e)}"}), 500








