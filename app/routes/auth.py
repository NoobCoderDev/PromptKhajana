from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.utils.otp import create_otp, verify_otp, cleanup_expired_otps
from app.utils.email import send_otp_email
from app.utils.validators import validate_email_format, validate_password_strength, validate_username, sanitize_input
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

OTP_RATE_LIMIT_MINUTES = 2

def check_rate_limit(email, action):
    key = f"{action}_{email}"
    last_sent = session.get(key)
    
    if last_sent:
        last_sent_time = datetime.fromisoformat(last_sent)
        time_diff = datetime.utcnow() - last_sent_time
        
        if time_diff < timedelta(minutes=OTP_RATE_LIMIT_MINUTES):
            remaining = OTP_RATE_LIMIT_MINUTES * 60 - time_diff.total_seconds()
            return False, f"Please wait {int(remaining)} seconds before requesting another OTP"
    
    session[key] = datetime.utcnow().isoformat()
    return True, ""

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = sanitize_input(request.form.get('email'))
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('auth/login.html')
        
        if not validate_email_format(email):
            flash('Invalid email format', 'error')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            flash('Invalid email or password', 'error')
            return render_template('auth/login.html')
        
        can_send, message = check_rate_limit(email, 'login')
        if not can_send:
            flash(message, 'error')
            return render_template('auth/login.html')
        
        cleanup_expired_otps()
        otp_code = create_otp(email, 'login')
        
        if send_otp_email(email, otp_code, 'login'):
            session['login_email'] = email
            session['login_verified'] = False
            flash('OTP sent to your email. Please verify to continue.', 'success')
            return redirect(url_for('auth.verify_login_otp'))
        else:
            flash('Failed to send OTP. Please try again.', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/verify-login-otp', methods=['GET', 'POST'])
def verify_login_otp():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    email = session.get('login_email')
    if not email:
        flash('Session expired. Please login again.', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        otp_code = sanitize_input(request.form.get('otp'))
        
        if not otp_code:
            flash('OTP is required', 'error')
            return render_template('auth/verify_otp.html', purpose='login')
        
        success, message = verify_otp(email, otp_code, 'login')
        
        if success:
            user = User.query.filter_by(email=email).first()
            if user:
                login_user(user)
                session.pop('login_email', None)
                session.pop('login_verified', None)
                next_page = request.args.get('next')
                flash('Login successful!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash(message, 'error')
    
    return render_template('auth/verify_otp.html', purpose='login', email=email)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = sanitize_input(request.form.get('username'))
        email = sanitize_input(request.form.get('email'))
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        errors = []
        
        if not all([username, email, password, confirm_password]):
            flash('All fields are required', 'error')
            return render_template('auth/register.html')
        
        if not validate_email_format(email):
            errors.append('Invalid email format')
        
        valid_username, username_msg = validate_username(username)
        if not valid_username:
            errors.append(username_msg)
        
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        valid_password, password_msg = validate_password_strength(password)
        if not valid_password:
            errors.append(password_msg)
        
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')
        
        if User.query.filter_by(username=username).first():
            errors.append('Username already taken')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('auth/register.html')
        
        can_send, message = check_rate_limit(email, 'signup')
        if not can_send:
            flash(message, 'error')
            return render_template('auth/register.html')
        
        cleanup_expired_otps()
        otp_code = create_otp(email, 'signup')
        
        if send_otp_email(email, otp_code, 'signup'):
            session['signup_username'] = username
            session['signup_email'] = email
            session['signup_password'] = password
            flash('OTP sent to your email. Please verify to complete registration.', 'success')
            return redirect(url_for('auth.verify_signup_otp'))
        else:
            flash('Failed to send OTP. Please try again.', 'error')
    
    return render_template('auth/register.html')

@auth_bp.route('/verify-signup-otp', methods=['GET', 'POST'])
def verify_signup_otp():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    email = session.get('signup_email')
    username = session.get('signup_username')
    password = session.get('signup_password')
    
    if not all([email, username, password]):
        flash('Session expired. Please register again.', 'error')
        return redirect(url_for('auth.register'))
    
    if request.method == 'POST':
        otp_code = sanitize_input(request.form.get('otp'))
        
        if not otp_code:
            flash('OTP is required', 'error')
            return render_template('auth/verify_otp.html', purpose='signup')
        
        success, message = verify_otp(email, otp_code, 'signup')
        
        if success:
            user = User(username=username, email=email, email_verified=True)
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            session.pop('signup_username', None)
            session.pop('signup_email', None)
            session.pop('signup_password', None)
            
            login_user(user)
            flash('Registration successful! Welcome to Prompt Khajana.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash(message, 'error')
    
    return render_template('auth/verify_otp.html', purpose='signup', email=email)

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = sanitize_input(request.form.get('email'))
        
        if not email:
            flash('Email is required', 'error')
            return render_template('auth/forgot_password.html')
        
        if not validate_email_format(email):
            flash('Invalid email format', 'error')
            return render_template('auth/forgot_password.html')
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('If this email exists, an OTP has been sent.', 'success')
            return render_template('auth/forgot_password.html')
        
        can_send, message = check_rate_limit(email, 'reset')
        if not can_send:
            flash(message, 'error')
            return render_template('auth/forgot_password.html')
        
        cleanup_expired_otps()
        otp_code = create_otp(email, 'reset')
        
        if send_otp_email(email, otp_code, 'reset'):
            session['reset_email'] = email
            flash('OTP sent to your email. Please verify to reset your password.', 'success')
            return redirect(url_for('auth.verify_reset_otp'))
        else:
            flash('Failed to send OTP. Please try again.', 'error')
    
    return render_template('auth/forgot_password.html')

@auth_bp.route('/verify-reset-otp', methods=['GET', 'POST'])
def verify_reset_otp():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    email = session.get('reset_email')
    if not email:
        flash('Session expired. Please try again.', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        otp_code = sanitize_input(request.form.get('otp'))
        
        if not otp_code:
            flash('OTP is required', 'error')
            return render_template('auth/verify_otp.html', purpose='reset')
        
        success, message = verify_otp(email, otp_code, 'reset')
        
        if success:
            session['reset_verified'] = True
            flash('OTP verified. Please set your new password.', 'success')
            return redirect(url_for('auth.reset_password'))
        else:
            flash(message, 'error')
    
    return render_template('auth/verify_otp.html', purpose='reset', email=email)

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    email = session.get('reset_email')
    verified = session.get('reset_verified')
    
    if not email or not verified:
        flash('Unauthorized access. Please verify OTP first.', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not password or not confirm_password:
            flash('All fields are required', 'error')
            return render_template('auth/reset_password.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth/reset_password.html')
        
        valid_password, password_msg = validate_password_strength(password)
        if not valid_password:
            flash(password_msg, 'error')
            return render_template('auth/reset_password.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            if user.check_password(password):
                flash('New password cannot be the same as old password', 'error')
                return render_template('auth/reset_password.html')
            
            user.set_password(password)
            db.session.commit()
            
            session.pop('reset_email', None)
            session.pop('reset_verified', None)
            
            flash('Password reset successful! Please login with your new password.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('User not found', 'error')
            return redirect(url_for('auth.forgot_password'))
    
    return render_template('auth/reset_password.html')

@auth_bp.route('/resend-otp/<purpose>')
def resend_otp(purpose):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    email_key_map = {
        'signup': 'signup_email',
        'login': 'login_email',
        'reset': 'reset_email'
    }
    
    email_key = email_key_map.get(purpose)
    if not email_key:
        flash('Invalid request', 'error')
        return redirect(url_for('main.index'))
    
    email = session.get(email_key)
    if not email:
        flash('Session expired. Please try again.', 'error')
        return redirect(url_for(f'auth.{purpose if purpose != "signup" else "register"}'))
    
    can_send, message = check_rate_limit(email, purpose)
    if not can_send:
        flash(message, 'error')
        return redirect(url_for(f'auth.verify_{purpose}_otp'))
    
    cleanup_expired_otps()
    otp_code = create_otp(email, purpose)
    
    if send_otp_email(email, otp_code, purpose):
        flash('New OTP sent to your email', 'success')
    else:
        flash('Failed to send OTP. Please try again.', 'error')
    
    return redirect(url_for(f'auth.verify_{purpose}_otp'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('main.index'))
