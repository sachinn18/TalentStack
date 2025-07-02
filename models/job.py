from datetime import datetime
from app import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(100), nullable=True)
    job_type = db.Column(db.String(50), nullable=False, default='Full-time')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    applications = db.relationship('Application', backref='job', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"Job('{self.title}', '{self.date_posted}')" 