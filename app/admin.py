from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Prompt, Category, Tag
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please login to access this page', 'error')
            return redirect(url_for('auth.login'))
        if not current_user.is_superadmin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@superadmin_required
def dashboard():
    total_prompts = Prompt.query.count()
    total_categories = Category.query.count()
    total_tags = Tag.query.count()
    recent_prompts = Prompt.query.order_by(Prompt.created_at.desc()).limit(5).all()
    
    return render_template(
        'admin/dashboard.html',
        total_prompts=total_prompts,
        total_categories=total_categories,
        total_tags=total_tags,
        recent_prompts=recent_prompts
    )

@admin_bp.route('/prompts')
@superadmin_required
def manage_prompts():
    prompts = Prompt.query.order_by(Prompt.created_at.desc()).all()
    return render_template('admin/manage_prompts.html', prompts=prompts)

@admin_bp.route('/categories', methods=['GET', 'POST'])
@superadmin_required
def manage_categories():
    if request.method == 'POST':
        name = request.form.get('name')
        slug = request.form.get('slug')
        description = request.form.get('description')
        icon = request.form.get('icon')
        
        category = Category(name=name, slug=slug, description=description, icon=icon)
        db.session.add(category)
        db.session.commit()
        
        flash('Category created successfully', 'success')
        return redirect(url_for('admin.manage_categories'))
    
    categories = Category.query.order_by(Category.name).all()
    return render_template('admin/manage_categories.html', categories=categories)

@admin_bp.route('/categories/delete/<int:id>', methods=['POST'])
@superadmin_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully', 'success')
    return redirect(url_for('admin.manage_categories'))

@admin_bp.route('/tags', methods=['GET', 'POST'])
@superadmin_required
def manage_tags():
    if request.method == 'POST':
        name = request.form.get('name')
        slug = request.form.get('slug')
        
        tag = Tag(name=name, slug=slug)
        db.session.add(tag)
        db.session.commit()
        
        flash('Tag created successfully', 'success')
        return redirect(url_for('admin.manage_tags'))
    
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('admin/manage_tags.html', tags=tags)

@admin_bp.route('/tags/delete/<int:id>', methods=['POST'])
@superadmin_required
def delete_tag(id):
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tag deleted successfully', 'success')
    return redirect(url_for('admin.manage_tags'))
