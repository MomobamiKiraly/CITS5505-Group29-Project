import openai 
import os
import requests
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy import or_
from app.forms import LoginForm
from app.models import User, Prediction, BlogPost, Friendship
from app import db,csrf
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend to avoid Tkinter issues
import matplotlib.pyplot as plt
from app.utils import fetch_teams, get_drivers_by_team, get_next_race_name


main = Blueprint('main', __name__)

# ---------- Home ----------
@main.route('/')
def home():
    return redirect(url_for('main.login'))

# ---------- Friend List ----------
@main.route('/friends')
@login_required
def friends():
    following = current_user.get_following_list()
    return render_template('friends.html', friends=following)

# ---------- Login ----------
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

# ---------- Register ----------
from app.forms import LoginForm, RegisterForm  # 🔄 确保导入 RegisterForm

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    teams = fetch_teams()
    drivers_by_team = get_drivers_by_team()

    if form.validate_on_submit():
        # Get values from regular request.form, not from WTForms
        favorite_team = request.form.get('favorite_team')
        favorite_driver = request.form.get('favorite_driver')

        print("Favorite team from request:", favorite_team)
        print("Favorite driver from request:", favorite_driver)

        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()

        if existing_user:
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('main.register'))

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            favorite_team=favorite_team,
            favorite_driver=favorite_driver,
            profile_pic='default.jpg'
        )
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template(
        'register.html',
        form=form,
        teams=teams,
        drivers_by_team=drivers_by_team
    )


# ---------- Dashboard ----------
def generate_standings_chart(standings):
    import matplotlib.pyplot as plt
    import os
    from flask import current_app

    print("📊 generate_standings_chart called")
    print("Driver names:", [item['driver']['name'] for item in standings[:5]])

    names = [item['driver']['name'] for item in standings[:5]]
    points = [item['points'] for item in standings[:5]]
    colors = ['red', 'orange', 'blue', 'green', 'purple']

    fig, ax = plt.subplots(figsize=(8, 4))
    for i, (name, point) in enumerate(zip(names, points)):
        ax.plot([0, point], [i, i], lw=8, color=colors[i])
        ax.text(point + 1, i, f"{name} ({point})", va='center')

    ax.set_xlim(0, max(points) + 10)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title("F1 Driver Standings")

    # 🔧 改为项目根目录/static/charts/
    chart_dir = os.path.join(os.path.dirname(current_app.root_path), 'static', 'charts')
    os.makedirs(chart_dir, exist_ok=True)
    chart_path = os.path.join(chart_dir, 'standings.png')
    print("✅ Saving chart to:", chart_path)

    plt.savefig(chart_path, bbox_inches='tight')
    plt.close()

    return '/static/charts/standings.png'

@main.route('/dashboard')
@login_required
def dashboard():
    try:
        standings_url = "http://api.jolpi.ca/ergast/f1/current/driverStandings.json"
        next_race_url = "http://api.jolpi.ca/ergast/f1/current/next.json"

        standings_resp = requests.get(standings_url, timeout=10)
        next_race_resp = requests.get(next_race_url, timeout=10)

        if standings_resp.ok and next_race_resp.ok:
            standings_data = standings_resp.json()
            next_race_data = next_race_resp.json()

            standings_list = standings_data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

            standings = [
                {
                    'driver': {
                        'name': f"{d['Driver']['givenName']} {d['Driver']['familyName']}"
                    },
                    'points': int(d['points'])
                }
                for d in standings_list
            ]

            next_race = next_race_data['MRData']['RaceTable']['Races'][0] if next_race_data['MRData']['RaceTable']['Races'] else None
            next_race_parsed = {
                'race': {
                    'raceName': next_race['raceName'],
                    'date': next_race['date'],
                    'circuit': {
                        'location': {
                            'locality': next_race['Circuit']['Location']['locality']
                        }
                    }
                }
            } if next_race else None

            chart_path = generate_standings_chart(standings)
        else:
            flash("Unable to fetch F1 data.", "danger")
            standings, next_race_parsed, chart_path = [], None, None

    except Exception as e:
        flash(f"Error fetching F1 data: {str(e)}", "danger")
        standings, next_race_parsed, chart_path = [], None, None

    return render_template("dashboard.html", standings=standings, next_race=next_race_parsed, chart_path=chart_path)


# ---------- Forgot Password ----------
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

# ---------- Edit Profile ----------
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

# ---------- Current User Profile ----------
@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get_or_404(session['user_id'])

    # --- Handle blog post submission ---
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        is_public = request.form.get('is_public') == 'on'

        post = BlogPost(
            author=user,
            title=title,
            content=content,
            is_public=is_public,
            timestamp=datetime.utcnow()
        )
        db.session.add(post)
        db.session.commit()
        flash("Blog post published!", "success")
        return redirect(url_for('main.profile'))

    # --- Prepare page content ---
    predictions = Prediction.query.filter_by(user_id=user.id).all()
    posts = BlogPost.query.filter_by(author_id=user.id).all()

    return render_template(
        'profile.html',
        user=user,
        predictions=predictions,
        posts=posts,
        is_following=None  # Not relevant for self-profile
    )

# ---------- Any User Profile + Blog ----------
@main.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def view_profile(user_id):
    target_user = User.query.get_or_404(user_id)

    if request.method == 'POST' and current_user.id == target_user.id:
        title = request.form['title']
        content = request.form['content']
        is_public = request.form.get('is_public') == 'on'

        new_post = BlogPost(
            author=current_user,
            title=title,
            content=content,
            is_public=is_public,
            timestamp=datetime.utcnow()
        )
        db.session.add(new_post)
        db.session.commit()
        flash("Blog post published!", "success")
        return redirect(url_for('main.view_profile', user_id=user_id))

    if current_user.id == target_user.id:
        posts = target_user.blog_posts
    elif Friendship.query.filter_by(follower_id=current_user.id, followed_id=target_user.id).first():
        posts = BlogPost.query.filter_by(author_id=target_user.id).all()
    else:
        posts = BlogPost.query.filter_by(author_id=target_user.id, is_public=True).all()

    is_following = Friendship.query.filter_by(
        follower_id=current_user.id, followed_id=target_user.id
    ).first() is not None

    return render_template("profile.html", user=target_user, posts=posts, is_following=is_following)

# ---------- Follow ----------
@main.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    if user_id == current_user.id:
        flash("You can't follow yourself.", "warning")
        return redirect(url_for('main.view_profile', user_id=user_id))

    existing = Friendship.query.filter_by(
        follower_id=current_user.id, followed_id=user_id
    ).first()

    if not existing:
        new_friend = Friendship(follower_id=current_user.id, followed_id=user_id)
        db.session.add(new_friend)
        db.session.commit()
        flash("Followed successfully.", "success")
    else:
        flash("You're already following this user.", "info")

    return redirect(url_for('main.view_profile', user_id=user_id))

# ---------- Unfollow ----------
@main.route('/unfollow/<int:user_id>')
@login_required
def unfollow(user_id):
    friend = Friendship.query.filter_by(
        follower_id=current_user.id, followed_id=user_id
    ).first()

    if friend:
        db.session.delete(friend)
        db.session.commit()
        flash("Unfollowed.", "info")

    return redirect(url_for('main.view_profile', user_id=user_id))

# ---------- Search Users ----------
@main.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    results = []

    if query:
        results = User.query.filter(
            or_(
                User.username.ilike(f"%{query}%"),
                User.email.ilike(f"%{query}%")
            )
        ).all()

    return render_template('search.html', query=query, results=results)

# ---------- Chatbot ----------
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

# ---------- Upload (Prediction?) ----------
@main.route('/upload', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def upload():

    # --- Fetch Driver-Team Mapping ---
    ergast_url = "https://ergast.com/api/f1/current/driverStandings.json"
    drivers_by_team = {}

    try:
        response = requests.get(ergast_url)
        data = response.json()
        standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        for driver_info in standings:
            driver = driver_info['Driver']
            team = driver_info['Constructors'][0]['name']
            driver_name = f"{driver['givenName']} {driver['familyName']}"
            drivers_by_team.setdefault(team, []).append({"name": driver_name})
    except (KeyError, IndexError, requests.exceptions.RequestException):
        flash("Failed to fetch driver/team data from the API.", "danger")
        drivers_by_team = {}

    # --- Fetch Next Race Name ---
    race_name = "Upcoming Race"
    try:
        next_race_url = "http://api.jolpi.ca/ergast/f1/current/next.json"
        race_response = requests.get(next_race_url)
        race_data = race_response.json()
        race_name = race_data['MRData']['RaceTable']['Races'][0]['raceName']
    except (KeyError, IndexError, requests.exceptions.RequestException):
        flash("Could not retrieve race name.", "warning")

    # --- Handle Form Submission ---
    if request.method == 'POST':
        predicted_winner = request.form['predicted_winner']
        fastest_lap = request.form['fastest_lap']

        existing_prediction = Prediction.query.filter_by(user_id=current_user.id, race_name=race_name).first()

        if existing_prediction:
            existing_prediction.predicted_winner = predicted_winner
            existing_prediction.fastest_lap = fastest_lap
        else:
            new_prediction = Prediction(
                user_id=current_user.id,
                predicted_winner=predicted_winner,
                fastest_lap=fastest_lap,
                race_name=race_name
            )
            db.session.add(new_prediction)

        db.session.commit()
        flash('Prediction saved successfully!', 'success')
        return redirect(url_for('main.profile'))

    # --- Render Form ---
    return render_template('upload.html', drivers_by_team=drivers_by_team, race_name=race_name)


# ---------- DeepSeek Chat API ----------
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

# ---------- Logout ----------
@main.route('/logout')
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))
