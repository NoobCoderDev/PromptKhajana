from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user
from app import db
from datetime import datetime
from app.models import Prompt, Category, Tag
from sqlalchemy import or_, func
import markdown2

main_bp = Blueprint('main', __name__)

# Markdown configuration with extras
MARKDOWN_EXTRAS = ['fenced-code-blocks', 'tables', 'break-on-newline', 'code-friendly']

def render_markdown(text):
    """Convert markdown text to HTML"""
    if not text:
        return ''
    return markdown2.markdown(text, extras=MARKDOWN_EXTRAS)

# Template filter for markdown
@main_bp.app_template_filter('markdown')
def markdown_filter(text):
    return render_markdown(text)

def get_all_categories():
    """Get all categories ordered by name"""
    return Category.query.order_by(Category.name).all()

def get_all_tags():
    """Get all tags ordered by name"""
    return Tag.query.order_by(Tag.name).all()

def get_filtered_prompts(search_query=None, category_slug=None, tag_slug=None, 
                         difficulty=None, sort_by='newest'):
    """Get prompts with filters applied"""
    query = Prompt.query
    
    # Search filter
    if search_query:
        search_pattern = f'%{search_query}%'
        query = query.filter(
            or_(
                Prompt.title.ilike(search_pattern),
                Prompt.description.ilike(search_pattern),
                Prompt.content.ilike(search_pattern),
                Prompt.use_case.ilike(search_pattern)
            )
        )
    
    # Category filter
    if category_slug:
        category = Category.query.filter_by(slug=category_slug).first()
        if category:
            query = query.filter(Prompt.category_id == category.id)
    
    # Tag filter
    if tag_slug:
        tag = Tag.query.filter_by(slug=tag_slug).first()
        if tag:
            query = query.filter(Prompt.tags.contains(tag))
    
    # Difficulty filter
    if difficulty:
        query = query.filter(Prompt.difficulty == difficulty)
    
    # Sorting
    if sort_by == 'newest':
        query = query.order_by(Prompt.created_at.desc())
    elif sort_by == 'popular':
        query = query.order_by(Prompt.views.desc())
    elif sort_by == 'rating':
        query = query.order_by(Prompt.rating.desc())
    else:
        query = query.order_by(Prompt.created_at.desc())
    
    return query.all()

def get_prompt_by_id(prompt_id):
    """Get prompt by ID or 404"""
    return Prompt.query.get_or_404(prompt_id)

def increment_prompt_views(prompt):
    """Increment view count for a prompt"""
    prompt.views += 1
    db.session.commit()

def extract_form_data():
    """Extract form data for prompt creation/update"""
    return {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'content': request.form.get('content'),
        'use_case': request.form.get('use_case'),
        'examples': request.form.get('examples'),
        'difficulty': request.form.get('difficulty', 'Intermediate'),
        'category_id': int(request.form.get('category_id')),
        'tag_ids': request.form.getlist('tags')  # Multiple tags
    }

def create_prompt_from_data(data):
    """Create new prompt from form data"""
    tag_ids = data.pop('tag_ids', [])
    prompt = Prompt(**data)
    
    # Add tags
    if tag_ids:
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        prompt.tags = tags
    
    return prompt

def update_prompt_fields(prompt, data):
    """Update prompt fields from form data"""
    tag_ids = data.pop('tag_ids', [])
    
    for key, value in data.items():
        setattr(prompt, key, value)
    
    # Update tags
    if tag_ids:
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        prompt.tags = tags
    
    prompt.updated_at = datetime.utcnow()
    return prompt

def save_to_database(obj):
    """Save object to database"""
    db.session.add(obj)
    db.session.commit()

def delete_from_database(obj):
    """Delete object from database"""
    db.session.delete(obj)
    db.session.commit()

@main_bp.route('/')
def index():
    """Homepage with search and filtering"""
    # Get filter parameters
    search_query = request.args.get('search', '')
    category_slug = request.args.get('category', '')
    tag_slug = request.args.get('tag', '')
    difficulty = request.args.get('difficulty', '')
    sort_by = request.args.get('sort', 'newest')
    
    # Get filtered prompts
    prompts = get_filtered_prompts(
        search_query=search_query if search_query else None,
        category_slug=category_slug if category_slug else None,
        tag_slug=tag_slug if tag_slug else None,
        difficulty=difficulty if difficulty else None,
        sort_by=sort_by
    )
    
    # Get all categories and tags for filters
    categories = get_all_categories()
    tags = get_all_tags()
    
    # Difficulty options
    difficulties = ['Beginner', 'Intermediate', 'Advanced']
    
    return render_template(
        'index.html',
        prompts=prompts,
        categories=categories,
        tags=tags,
        difficulties=difficulties,
        current_search=search_query,
        current_category=category_slug,
        current_tag=tag_slug,
        current_difficulty=difficulty,
        current_sort=sort_by
    )


@main_bp.route('/prompt/<int:id>')
@login_required
def view_prompt(id):
    prompt = get_prompt_by_id(id)
    increment_prompt_views(prompt)
    
    related_prompts = Prompt.query.filter(
        Prompt.category_id == prompt.category_id,
        Prompt.id != prompt.id
    ).order_by(func.random()).limit(3).all()
    
    return render_template(
        'view_prompt.html',
        prompt=prompt,
        related_prompts=related_prompts
    )

@main_bp.route('/category/<slug>')
def category(slug):
    """View prompts by category"""
    category = Category.query.filter_by(slug=slug).first_or_404()
    prompts = Prompt.query.filter_by(category_id=category.id).order_by(Prompt.created_at.desc()).all()
    
    return render_template(
        'category.html',
        category=category,
        prompts=prompts
    )

@main_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_prompt():
    if not current_user.is_superadmin():
        abort(403)
    
    if request.method == 'POST':
        data = extract_form_data()
        prompt = create_prompt_from_data(data)
        save_to_database(prompt)
        flash('Prompt added successfully!', 'success')
        return redirect(url_for('main.view_prompt', id=prompt.id))
    
    categories = get_all_categories()
    tags = get_all_tags()
    difficulties = ['Beginner', 'Intermediate', 'Advanced']
    
    return render_template(
        'add_prompt.html',
        categories=categories,
        tags=tags,
        difficulties=difficulties
    )

@main_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_prompt(id):
    if not current_user.is_superadmin():
        abort(403)
    
    prompt = get_prompt_by_id(id)
    
    if request.method == 'POST':
        data = extract_form_data()
        updated_prompt = update_prompt_fields(prompt, data)
        save_to_database(updated_prompt)
        flash('Prompt updated successfully!', 'success')
        return redirect(url_for('main.view_prompt', id=id))
    
    categories = get_all_categories()
    tags = get_all_tags()
    difficulties = ['Beginner', 'Intermediate', 'Advanced']
    
    return render_template(
        'edit_prompt.html',
        prompt=prompt,
        categories=categories,
        tags=tags,
        difficulties=difficulties
    )

@main_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_prompt(id):
    if not current_user.is_superadmin():
        abort(403)
    
    prompt = get_prompt_by_id(id)
    delete_from_database(prompt)
    flash('Prompt deleted successfully!', 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/api/prompts')
def api_prompts():
    """API endpoint for prompts (JSON)"""
    prompts = Prompt.query.all()
    return jsonify([prompt.to_dict() for prompt in prompts])

@main_bp.route('/api/categories')
def api_categories():
    """API endpoint for categories (JSON)"""
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'slug': c.slug,
        'icon': c.icon,
        'prompt_count': c.prompts.count()
    } for c in categories])
