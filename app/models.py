from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

# ---------- User Model ----------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Unique user ID
    username = db.Column(db.String(64), unique=True, nullable=False)  # Username
    email = db.Column(db.String(120), unique=True, nullable=False)    # Email address
    password_hash = db.Column(db.String(128), nullable=False)         # Hashed password

    favorite_team = db.Column(db.String(64))      # User's favorite F1 team
    favorite_driver = db.Column(db.String(64))    # User's favorite F1 driver
    bio = db.Column(db.Text, default='')          # User bio
    profile_pic = db.Column(db.String(256), default='default.jpg')  # Profile picture filename

    # Relationship to user's predictions
    predictions = db.relationship('Prediction', backref='user', lazy=True)
    # Relationship to user's blog posts
    blog_posts = db.relationship('BlogPost', backref='author', lazy=True)

    # Friend system: users this user is following
    following = db.relationship(
        'Friendship',
        foreign_keys='Friendship.follower_id',
        backref='follower',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    # Friend system: users following this user
    followers = db.relationship(
        'Friendship',
        foreign_keys='Friendship.followed_id',
        backref='followed',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    # Sent chat messages (avoid backref conflict)
    sent_messages = db.relationship(
        'ChatMessage',
        foreign_keys='ChatMessage.sender_id',
        back_populates='sender',
        lazy='dynamic'
    )
    # Received chat messages (avoid backref conflict)
    received_messages = db.relationship(
        'ChatMessage',
        foreign_keys='ChatMessage.receiver_id',
        back_populates='receiver',
        lazy='dynamic'
    )

    # Set the user's password (hashed)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    # Check if the password matches the stored hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Check if this user is following another user
    def is_following(self, user):
        return self.following.filter_by(followed_id=user.id).first() is not None

    # Check if this user is followed by another user
    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    # Check if this user and another user are friends (mutual following)
    def is_friends_with(self, user):
        return self.is_following(user) and self.is_followed_by(user)

    # Get a list of users this user is following
    def get_following_list(self):
        return [f.followed for f in self.following]
    
    def __repr__(self):
        return f"<User {self.username}>"

# ---------- Prediction Model ----------
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique prediction ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User who made the prediction
    race_name = db.Column(db.String(120))         # Name of the race
    predicted_winner = db.Column(db.String(80))   # Predicted winner
    fastest_lap = db.Column(db.String(80))        # Predicted fastest lap driver
    actual_winner = db.Column(db.String(80))      # Actual winner (filled after race)
    points = db.Column(db.Integer)                # Points earned for this prediction

# ---------- BlogPost Model ----------
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique blog post ID
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Author (user)
    title = db.Column(db.String(100), nullable=False)  # Blog post title
    content = db.Column(db.Text, nullable=False)       # Blog post content
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Time posted
    is_public = db.Column(db.Boolean, default=True)    # Public or followers-only

# ---------- Friendship Model ----------
class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique friendship ID
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User who follows
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User being followed

    # Ensure unique follower-followed pairs
    __table_args__ = (db.UniqueConstraint('follower_id', 'followed_id', name='unique_friendship'),)

# ---------- ChatMessage Model ----------
class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique message ID
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)    # Sender user ID
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Receiver user ID
    content = db.Column(db.Text, nullable=False)   # Message content
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)  # Time sent

    # Explicit relationships to avoid backref name collision
    sender = db.relationship('User', foreign_keys=[sender_id], back_populates='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], back_populates='received_messages')
    
    is_read = db.Column(db.Boolean, default=False)  # Message read status