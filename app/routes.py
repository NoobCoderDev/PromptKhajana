from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from datetime import datetime
from app.models import Prompt

main_bp = Blueprint('main', __name__)

def get_all_prompts():
    return Prompt.query.order_by(Prompt.created_at.desc()).all()

def get_prompt_by_id(prompt_id):
    return Prompt.query.get_or_404(prompt_id)

def extract_form_data():
    return {
        'title': request.form.get('title'),
        'category': request.form.get('category'),
        'content': request.form.get('content'),
        'examples': request.form.get('examples'),
        'rating': float(request.form.get('rating', 0.0))
    }

def create_prompt_from_data(data):
    prompt = Prompt(
        title=data['title'],
        category=data['category'],
        content=data['content'],
        examples=data['examples'],
        rating=data['rating']
    )
    return prompt

def update_prompt_fields(prompt, data):
    prompt.title = data['title']
    prompt.category = data['category']
    prompt.content = data['content']
    prompt.examples = data['examples']
    prompt.rating = data['rating']
    prompt.updated_at = datetime.utcnow()
    return prompt

def save_to_database(obj):
    db.session.add(obj)
    db.session.commit()

def delete_from_database(obj):
    db.session.delete(obj)
    db.session.commit()

@main_bp.route('/')
def index():
    prompts = get_all_prompts()
    return render_template('index.html', prompts=prompts)

@main_bp.route('/prompt/<int:id>')
def view_prompt(id):
    prompt = get_prompt_by_id(id)
    return render_template('view_prompt.html', prompt=prompt)

@main_bp.route('/add', methods=['GET', 'POST'])
def add_prompt():
    if request.method == 'POST':
        data = extract_form_data()
        prompt = create_prompt_from_data(data)
        save_to_database(prompt)
        flash('Prompt added successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('add_prompt.html')

@main_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_prompt(id):
    prompt = get_prompt_by_id(id)
    if request.method == 'POST':
        data = extract_form_data()
        updated_prompt = update_prompt_fields(prompt, data)
        save_to_database(updated_prompt)
        flash('Prompt updated successfully!', 'success')
        return redirect(url_for('main.view_prompt', id=id))
    return render_template('edit_prompt.html', prompt=prompt)

@main_bp.route('/delete/<int:id>')
def delete_prompt(id):
    prompt = get_prompt_by_id(id)
    delete_from_database(prompt)
    flash('Prompt deleted successfully!', 'success')
    return redirect(url_for('main.index'))
