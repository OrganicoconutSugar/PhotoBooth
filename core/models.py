# Database Models Definition
from core.database import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='consumer') # 'consumer' atau 'admin'
    phone = db.Column(db.String(20), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    profile_pic = db.Column(db.String(200), nullable=True)
    photos = db.relationship('Photo', backref='owner', lazy=True)

    def __init__(self, username=None, email=None, password=None, role='consumer', phone=None, bio=None, profile_pic=None):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.phone = phone
        self.bio = bio
        self.profile_pic = profile_pic

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    smile_score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, user_id=None, file_path=None, smile_score=None):
        self.user_id = user_id
        self.file_path = file_path
        self.smile_score = smile_score
