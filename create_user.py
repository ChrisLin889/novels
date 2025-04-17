import os
import sys
import bcrypt

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from backend.app import create_app, db
    from backend.app.models.user import User
    from backend.app.models.admin import Admin
except ImportError:
    print("Failed to import modules. Make sure you're running this script from the project root.")
    sys.exit(1)

def create_test_admin():
    """Create a test admin user for login testing"""
    print("Creating Flask application context...")
    app = create_app()
    with app.app_context():
        print("Checking if test admin already exists...")
        existing_user = User.query.filter_by(username='admintest').first()
        if existing_user:
            print(f"User admintest already exists with id {existing_user.id}")
            return
        
        print("Creating new admin user...")
        password = 'admin123'
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
        
        # Create user
        user = User(
            username='admintest',
            email='admintest@example.com',
            password_hash=password_hash,
            status=0  # active
        )
        
        # Save user to get ID
        db.session.add(user)
        db.session.commit()
        print(f"Created user with id {user.id}")
        
        # Create admin record
        admin = Admin(
            user_id=user.id,
            admin_level=1,
            permissions={"user": True, "content": True}
        )
        
        # Save admin record
        db.session.add(admin)
        db.session.commit()
        print(f"Created admin record with id {admin.id}")
        
        print(f"Test admin created successfully:")
        print(f"  Username: admintest")
        print(f"  Password: {password}")
        print(f"  Email: admintest@example.com")

if __name__ == "__main__":
    create_test_admin() 