from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

# ---------- User Model ----------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    favorite_team = db.Column(db.String(64))
    favorite_driver = db.Column(db.String(64))
    bio = db.Column(db.Text, default='')
    profile_pic = db.Column(db.String(256), default='default.jpg')

    predictions = db.relationship('Prediction', backref='user', lazy=True)
    blog_posts = db.relationship('BlogPost', backref='author', lazy=True)

    # Friend system
    following = db.relationship(
        'Friendship',
        foreign_keys='Friendship.follower_id',
        backref='follower',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    followers = db.relationship(
        'Friendship',
        foreign_keys='Friendship.followed_id',
        backref='followed',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    # ✅ Fixed: Use back_populates to avoid backref conflict
    sent_messages = db.relationship(
        'ChatMessage',
        foreign_keys='ChatMessage.sender_id',
        back_populates='sender',
        lazy='dynamic'
    )
    received_messages = db.relationship(
        'ChatMessage',
        foreign_keys='ChatMessage.receiver_id',
        back_populates='receiver',
        lazy='dynamic'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_following(self, user):
        return self.following.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    def is_friends_with(self, user):
        return self.is_following(user) and self.is_followed_by(user)

    def get_following_list(self):
        return [f.followed for f in self.following]
    
    def __repr__(self):
        return f"<User {self.username}>"

# ---------- Prediction Model ----------
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    race_name = db.Column(db.String(120))
    predicted_winner = db.Column(db.String(80))
    fastest_lap = db.Column(db.String(80))
    actual_winner = db.Column(db.String(80))
    points = db.Column(db.Integer)

# ---------- BlogPost Model ----------
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_public = db.Column(db.Boolean, default=True)

# ---------- Friendship Model ----------
class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    __table_args__ = (db.UniqueConstraint('follower_id', 'followed_id', name='unique_friendship'),)

# ---------- ChatMessage Model ----------
class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # ✅ Explicit relationships to avoid backref name collision
    sender = db.relationship('User', foreign_keys=[sender_id], back_populates='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], back_populates='received_messages')
    
    is_read = db.Column(db.Boolean, default=False)