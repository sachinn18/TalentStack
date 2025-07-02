from flask import Blueprint, render_template, url_for, flash, redirect, abort
from flask_login import current_user, login_required
from app import db
from models.job import Job
from models.application import Application
from models.user import User

job_seeker_bp = Blueprint('job_seeker', __name__)

@job_seeker_bp.route('/job/<int:job_id>')
def job_details(job_id):
    job = Job.query.get_or_404(job_id)
    applied = False
    if current_user.is_authenticated and current_user.role == 'job_seeker':
        application = Application.query.filter_by(user_id=current_user.id, job_id=job.id).first()
        if application:
            applied = True
    return render_template('job_details.html', title=job.title, job=job, applied=applied)

@job_seeker_bp.route('/job/<int:job_id>/apply', methods=['POST'])
@login_required
def apply_to_job(job_id):
    if current_user.role != 'job_seeker':
        flash('Only job seekers can apply for jobs.', 'danger')
        return redirect(url_for('main.index'))

    job = Job.query.get_or_404(job_id)
    application = Application.query.filter_by(user_id=current_user.id, job_id=job.id).first()

    if application:
        flash('You have already applied for this job.', 'info')
        return redirect(url_for('job_seeker.job_details', job_id=job.id))
    
    new_application = Application(user_id=current_user.id, job_id=job.id)
    db.session.add(new_application)
    db.session.commit()
    flash('You have successfully applied for the job!', 'success')
    return redirect(url_for('job_seeker.job_details', job_id=job.id))

@job_seeker_bp.route('/dashboard')
@login_required
def job_seeker_dashboard():
    if current_user.role != 'job_seeker':
        abort(403)
    
    applications = Application.query.filter_by(user_id=current_user.id).all()
    job_ids = [app.job_id for app in applications]
    applied_jobs = Job.query.filter(Job.id.in_(job_ids)).all()
    
    return render_template('job_seeker_dashboard.html', title='My Applications', jobs=applied_jobs) 