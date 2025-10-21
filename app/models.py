from app import db
from datetime import datetime
from flask_login import UserMixin

def get_current_timestamp():
    return datetime.utcnow()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=get_current_timestamp)

class Prompt(db.Model):
    __tablename__ = 'prompts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    examples = db.Column(db.Text)
    rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=get_current_timestamp)
    updated_at = db.Column(db.DateTime, default=get_current_timestamp, onupdate=get_current_timestamp)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'content': self.content,
            'examples': self.examples,
            'rating': self.rating,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
