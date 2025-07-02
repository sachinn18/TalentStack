from flask import Blueprint, render_template, url_for, flash, redirect, abort
from flask_login import current_user, login_required
from app import db
from models.user import User
from models.job import Job

admin_bp = Blueprint('admin', __name__)

def check_admin():
    if not current_user.is_authenticated or current_user.role != 'admin':
        abort(403)

@admin_bp.before_request
@login_required
def before_request():
    check_admin()

@admin_bp.route('/dashboard')
def admin_dashboard():
    users = User.query.all()
    jobs = Job.query.all()
    return render_template('admin_dashboard.html', title='Admin Dashboard', users=users, jobs=jobs)

@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash('Cannot delete an admin user.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))
    
    # Also delete user's job postings if they are an employer
    if user.role == 'employer':
        Job.query.filter_by(employer_id=user.id).delete()

    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted.', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/job/<int:job_id>/delete', methods=['POST'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('Job has been deleted.', 'success')
    return redirect(url_for('admin.admin_dashboard')) 