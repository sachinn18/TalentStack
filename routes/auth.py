from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'job_seeker')

        user_by_email = User.query.filter_by(email=email).first()
        user_by_name = User.query.filter_by(username=username).first()

        if user_by_email:
            flash('Email already exists.', 'danger')
            return redirect(url_for('auth.register'))
        
        if user_by_name:
            flash('Username already exists.', 'danger')
            return redirect(url_for('auth.register'))

        user = User(username=username, email=email, role=role)
        user.password = password
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register')

@auth_bp.route('/register_employer', methods=['GET', 'POST'])
def register_employer():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user_by_email = User.query.filter_by(email=email).first()
        user_by_name = User.query.filter_by(username=username).first()

        if user_by_email:
            flash('Email already exists.', 'danger')
            return redirect(url_for('auth.register_employer'))
        
        if user_by_name:
            flash('Username already exists.', 'danger')
            return redirect(url_for('auth.register_employer'))

        user = User(username=username, email=email, role='employer')
        user.password = password
        db.session.add(user)
        db.session.commit()
        flash('Your employer account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register_employer.html', title='Register as Employer')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.verify_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash('Login successful.', 'success')
            if user.role == 'employer':
                return redirect(url_for('employer.employer_dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            else:
                 return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index')) 