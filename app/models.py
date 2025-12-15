from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

def get_current_timestamp():
    return datetime.utcnow()

prompt_tags = db.Table('prompt_tags',
    db.Column('prompt_id', db.Integer, db.ForeignKey('prompts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=get_current_timestamp)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_superadmin(self):
        return self.is_admin

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=get_current_timestamp)
    
    prompts = db.relationship('Prompt', backref='category_obj', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=get_current_timestamp)
    
    def __repr__(self):
        return f'<Tag {self.name}>'

class Prompt(db.Model):
    __tablename__ = 'prompts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    content = db.Column(db.Text, nullable=False)
    use_case = db.Column(db.Text)
    examples = db.Column(db.Text)
    difficulty = db.Column(db.String(20), default='Intermediate')
    rating = db.Column(db.Float, default=0.0)
    views = db.Column(db.Integer, default=0)
    
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    tags = db.relationship('Tag', secondary=prompt_tags, lazy='subquery',
                          backref=db.backref('prompts', lazy=True))
    
    created_at = db.Column(db.DateTime, default=get_current_timestamp)
    updated_at = db.Column(db.DateTime, default=get_current_timestamp, onupdate=get_current_timestamp)
    
    def __repr__(self):
        return f'<Prompt {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'use_case': self.use_case,
            'examples': self.examples,
            'difficulty': self.difficulty,
            'rating': self.rating,
            'views': self.views,
            'category': self.category_obj.name if self.category_obj else None,
            'tags': [tag.name for tag in self.tags],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
