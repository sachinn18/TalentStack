from flask import Blueprint, render_template, request
from sqlalchemy import or_
from models.job import Job

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
def index():
    jobs = Job.query.order_by(Job.date_posted.desc()).limit(15).all()
    return render_template('index.html', jobs=jobs)

@main_bp.route('/search')
def search():
    job_query = request.args.get('job', '')
    location_query = request.args.get('location', '')
    
    # Build the search query
    query = Job.query
    
    if job_query:
        query = query.filter(
            or_(
                Job.title.ilike(f'%{job_query}%'),
                Job.description.ilike(f'%{job_query}%')
            )
        )
    
    if location_query:
        query = query.filter(Job.location.ilike(f'%{location_query}%'))
    
    # Order by most recent and execute query
    jobs = query.order_by(Job.date_posted.desc()).all()
    
    return render_template('index.html', 
                           jobs=jobs,
                           job_query=job_query,
                           location_query=location_query)