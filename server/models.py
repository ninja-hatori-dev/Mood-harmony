from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    mood_records = db.relationship('MoodRecord', backref='user', lazy=True)

class MoodRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood = db.Column(db.String(100), nullable=False)
    cuisine = db.Column(db.String(200))
    explanation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    songs = db.relationship('Song', backref='mood_record', lazy=True)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood_record_id = db.Column(db.Integer, db.ForeignKey('mood_record.id'), nullable=False)
    title = db.Column(db.String(200))
    youtube_link = db.Column(db.String(300))
    spotify_link = db.Column(db.String(300))