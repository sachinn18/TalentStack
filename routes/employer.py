from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from models.job import Job
from models.application import Application
from models.user import User

employer_bp = Blueprint('employer', __name__)

def check_employer():
    if not current_user.is_authenticated or current_user.role != 'employer':
        abort(403)

@employer_bp.before_request
@login_required
def before_request():
    check_employer()

@employer_bp.route('/dashboard')
def employer_dashboard():
    jobs = Job.query.filter_by(employer_id=current_user.id).order_by(Job.date_posted.desc()).all()
    return render_template('employer_dashboard.html', title='Employer Dashboard', jobs=jobs)

@employer_bp.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')
        salary = request.form.get('salary')
        job_type = request.form.get('job_type')
        
        job = Job(title=title, description=description, location=location, salary=salary, job_type=job_type, employer_id=current_user.id)
        db.session.add(job)
        db.session.commit()
        flash('Your job has been posted!', 'success')
        return redirect(url_for('employer.employer_dashboard'))
    return render_template('post_job.html', title='Post a New Job')

@employer_bp.route('/job/<int:job_id>/applicants')
def view_applicants(job_id):
    job = Job.query.get_or_404(job_id)
    if job.author != current_user:
        abort(403)
    
    applications = Application.query.filter_by(job_id=job.id).all()
    applicant_ids = [app.user_id for app in applications]
    applicants = User.query.filter(User.id.in_(applicant_ids)).all()

    return render_template('view_applicants.html', title=f"Applicants for {job.title}", applicants=applicants, job=job)

@employer_bp.route('/job/<int:job_id>/delete', methods=['POST'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.author != current_user:
        abort(403)
    db.session.delete(job)
    db.session.commit()
    flash('The job has been deleted.', 'success')
    return redirect(url_for('employer.employer_dashboard')) 