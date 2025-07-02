import random
from faker import Faker
from app import create_app, db
from models.user import User
from models.job import Job

# --- Configuration ---
NUM_EMPLOYERS = 20
NUM_JOBS = 20
JOB_TYPES = ['Full-time', 'Part-time', 'Contract', 'Internship', 'Temporary']

# Indian and International Companies
COMPANIES = [
    'TCS', 'Infosys', 'Wipro', 'HCL Technologies', 'Tech Mahindra',
    'Google', 'Amazon', 'Microsoft', 'JP Morgan', 'Goldman Sachs',
    'Reliance Digital', 'Bharti Airtel', 'HDFC Bank', 'ICICI Bank', 'Axis Bank',
    'IBM', 'Accenture', 'Deloitte', 'Oracle', 'Adobe'
]

# Indian Cities
CITIES = [
    'Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Chennai', 'Pune', 'Gurgaon', 
    'Noida', 'Kolkata', 'Ahmedabad'
]

# --- Initialization ---
app = create_app()
app.app_context().push()
fake = Faker(['en_IN'])  # Use Indian locale

def clear_data():
    """Clears existing jobs and non-admin users."""
    print("Clearing old data...")
    # Delete applications first due to dependencies
    # from models.application import Application
    # Application.query.delete()
    Job.query.delete()
    User.query.filter(User.role != 'admin').delete()
    db.session.commit()
    print("Old data cleared.")

def create_employers():
    """Creates a specified number of employer users."""
    print(f"Creating {NUM_EMPLOYERS} employer accounts...")
    employers = []
    for company in COMPANIES:
        employer = User(
            username=company,
            email=f"careers@{company.lower().replace(' ', '').replace(',', '')}.com",
            role='employer'
        )
        employer.password = 'password123'  # Set a default password
        employers.append(employer)
    
    db.session.add_all(employers)
    db.session.commit()
    print("Employer accounts created.")
    return employers

def create_jobs(employers):
    """Creates a specified number of jobs and assigns them to employers."""
    print(f"Creating {NUM_JOBS} job listings...")
    jobs = []
    
    # Job titles for different companies
    job_titles = {
        'Google': [
            'Software Engineer', 'Senior Software Engineer', 'Machine Learning Engineer',
            'Data Scientist', 'Cloud Architect', 'Product Manager', 'Site Reliability Engineer'
        ],
        'Amazon': [
            'Software Development Engineer', 'Solutions Architect', 'Data Engineer',
            'Product Manager', 'Cloud Support Engineer', 'DevOps Engineer'
        ],
        'Microsoft': [
            'Software Engineer', 'Program Manager', 'Cloud Solutions Architect',
            'Data & Applied Scientist', 'Security Engineer', 'Full Stack Developer'
        ],
        'TCS': [
            'Software Developer', 'Technical Lead', 'Project Manager',
            'Business Analyst', 'System Architect', 'Quality Engineer'
        ],
        'Infosys': [
            'Technology Analyst', 'Senior Systems Engineer', 'Technical Architect',
            'Project Manager', 'Digital Specialist Engineer', 'Data Scientist'
        ],
        'Wipro': [
            'Project Engineer', 'Technical Lead', 'Delivery Manager',
            'Cloud Engineer', 'Full Stack Developer', 'DevOps Specialist'
        ],
        'JP Morgan': [
            'Software Engineer', 'Quantitative Analyst', 'Technology Analyst',
            'Investment Banking Technologist', 'Application Developer', 'Cloud Engineer'
        ],
        'Goldman Sachs': [
            'Technology Analyst', 'Software Engineer', 'Quantitative Strategist',
            'Financial Software Developer', 'Cloud Infrastructure Engineer', 'Security Engineer'
        ]
    }

    # Default job titles for other companies
    default_titles = [
        'Software Engineer', 'Senior Developer', 'Full Stack Developer',
        'Project Manager', 'Business Analyst', 'System Architect',
        'DevOps Engineer', 'Quality Assurance Engineer', 'Technical Lead'
    ]

    # Company-specific job descriptions
    company_descriptions = {
        'Google': [
            'Join our team to work on cutting-edge search algorithms and AI technologies. You will collaborate with world-class engineers to solve complex technical challenges.',
            'Help build the next generation of cloud infrastructure. Work with distributed systems at massive scale.',
            'Develop innovative solutions for Google\'s advertising platforms. Impact billions of users worldwide.'
        ],
        'Amazon': [
            'Build scalable e-commerce solutions that serve millions of customers. Work with microservices architecture and AWS.',
            'Develop and optimize warehouse automation systems. Use machine learning to improve logistics.',
            'Create innovative solutions for Amazon Prime Video streaming services.'
        ],
        'Microsoft': [
            'Work on the Azure cloud platform. Design and implement enterprise-scale solutions.',
            'Develop next-generation features for Microsoft 365. Impact productivity tools used globally.',
            'Join the Xbox gaming division to create immersive gaming experiences.'
        ],
        'TCS': [
            'Work with leading global clients on digital transformation projects. Implement enterprise solutions.',
            'Develop banking and financial solutions for major institutions. Focus on secure transaction systems.',
            'Build innovative healthcare IT solutions. Impact patient care through technology.'
        ],
        'Infosys': [
            'Join our digital innovation team. Work on AI and blockchain solutions for enterprise clients.',
            'Develop fintech solutions for global banking clients. Focus on secure payment systems.',
            'Create cloud migration strategies and implement solutions for Fortune 500 companies.'
        ],
        'Wipro': [
            'Build enterprise-grade cloud solutions. Work with leading cloud platforms and technologies.',
            'Develop IoT solutions for industrial automation. Impact manufacturing efficiency.',
            'Create digital transformation solutions for healthcare and retail sectors.'
        ],
        'JP Morgan': [
            'Develop high-frequency trading systems. Work with real-time market data and analytics.',
            'Build secure banking applications. Implement robust financial transaction systems.',
            'Create risk management solutions using advanced analytics and machine learning.'
        ],
        'Goldman Sachs': [
            'Develop algorithmic trading platforms. Work with financial markets technology.',
            'Build risk assessment and portfolio management systems. Use quantitative analysis.',
            'Create secure financial reporting and compliance systems.'
        ]
    }

    # Default descriptions for other companies
    default_descriptions = [
        'Join our innovative team to develop cutting-edge solutions. Work with modern technologies and methodologies.',
        'Help build scalable enterprise solutions. Impact business operations through technology.',
        'Create innovative digital solutions. Work with a talented team on challenging projects.'
    ]

    for _ in range(NUM_JOBS):
        employer = random.choice(employers)
        company_name = employer.username
        
        # Get company-specific titles and descriptions or use default
        available_titles = job_titles.get(company_name, default_titles)
        available_descriptions = company_descriptions.get(company_name, default_descriptions)
        
        job = Job(
            title=random.choice(available_titles),
            description=random.choice(available_descriptions),
            location=random.choice(CITIES),
            salary=f"₹{random.randrange(5, 75)} LPA",  # Indian salary format
            job_type=random.choice(JOB_TYPES),
            employer_id=employer.id
        )
        jobs.append(job)

    db.session.add_all(jobs)
    db.session.commit()
    print("Job listings created.")

def seed_database():
    """Main function to run the seeding process."""
    clear_data()
    created_employers = create_employers()
    create_jobs(created_employers)
    print("\nDatabase seeding complete!")
    print(f"-> Created {NUM_EMPLOYERS} employers.")
    print(f"-> Created {NUM_JOBS} jobs.")

if __name__ == '__main__':
    seed_database()