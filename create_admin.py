import os
from app import create_app, db
from models.user import User

# Create a Flask app context
app = create_app()
app.app_context().push()

# --- Admin User Details ---
# IMPORTANT: Change these values before running the script
ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "your_strong_password" # Change this!

def create_admin_user():
    """Creates an admin user if one doesn't already exist."""
    
    # Check if an admin user already exists
    if User.query.filter_by(role='admin').first():
        print("An admin user already exists.")
        return

    # Check if the username or email is already taken
    if User.query.filter_by(username=ADMIN_USERNAME).first():
        print(f"Username '{ADMIN_USERNAME}' is already taken.")
        return
    
    if User.query.filter_by(email=ADMIN_EMAIL).first():
        print(f"Email '{ADMIN_EMAIL}' is already taken.")
        return

    # Create the new admin user
    admin = User(
        username=ADMIN_USERNAME,
        email=ADMIN_EMAIL,
        role='admin'
    )
    admin.password = ADMIN_PASSWORD
    
    db.session.add(admin)
    db.session.commit()
    
    print(f"Admin user '{ADMIN_USERNAME}' created successfully!")

if __name__ == '__main__':
    print("Creating admin user...")
    create_admin_user()
    print("Script finished.") 