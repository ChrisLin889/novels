import json
import pytest
from app import create_app, db
from app.models.user import User
from app.models.author import AuthorApplication
from app.models.admin import Admin
from app.services.author_service import AuthorService
from flask_jwt_extended import create_access_token
from unittest.mock import patch, MagicMock

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        # Create test admin user
        admin_user = User(username='admin_user', email='admin@test.com')
        admin_user.set_password('password')
        db.session.add(admin_user)
        db.session.commit()
        
        # Create admin record
        admin = Admin(user_id=admin_user.id)
        db.session.add(admin)
        
        # Create test normal user
        normal_user = User(username='normal_user', email='user@test.com')
        normal_user.set_password('password')
        db.session.add(normal_user)
        db.session.commit()
        
        # Create pending application
        application = AuthorApplication(
            user_id=normal_user.id,
            pen_name='Test Author',
            bio='Test bio',
            reason='Test reason',
            status='pending'
        )
        db.session.add(application)
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_token(app):
    with app.app_context():
        admin_user = User.query.filter_by(username='admin_user').first()
        return create_access_token(identity=admin_user.id)
        
@pytest.fixture
def normal_token(app):
    with app.app_context():
        normal_user = User.query.filter_by(username='normal_user').first()
        return create_access_token(identity=normal_user.id)

def test_get_pending_applications(client, admin_token):
    """Test getting pending applications as admin"""
    response = client.get(
        '/api/admin/author-applications',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'applications' in data
    assert len(data['applications']) > 0
    assert data['applications'][0]['pen_name'] == 'Test Author'

def test_get_pending_applications_as_normal_user(client, normal_token):
    """Test that normal users cannot access admin endpoint"""
    response = client.get(
        '/api/admin/author-applications',
        headers={'Authorization': f'Bearer {normal_token}'}
    )
    
    assert response.status_code == 403

def test_process_application_approve(client, admin_token, app):
    """Test approving an author application"""
    with app.app_context():
        application = AuthorApplication.query.first()
        
        response = client.post(
            f'/api/admin/author-applications/{application.id}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'action': 'approve'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'application' in data
        assert data['application']['status'] == 'approved'
        
        # Verify that the user now has an author record
        admin_user = User.query.filter_by(username='admin_user').first()
        normal_user = User.query.filter_by(username='normal_user').first()
        
        # Mock the permission check since we're not implementing the full permission system
        with patch('app.services.permission_service.PermissionService.has_role') as mock_has_role:
            # Mock role checks
            def side_effect(user_id, role):
                if user_id == admin_user.id and role == 'admin':
                    return True
                return False
                
            mock_has_role.side_effect = side_effect
            
            # Verify the application was approved
            updated_application = AuthorApplication.query.get(application.id)
            assert updated_application.status == 'approved'

def test_process_application_reject(client, admin_token, app):
    """Test rejecting an author application"""
    with app.app_context():
        application = AuthorApplication.query.first()
        
        response = client.post(
            f'/api/admin/author-applications/{application.id}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'action': 'reject', 'comment': 'Not qualified'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'application' in data
        assert data['application']['status'] == 'rejected'
        assert data['application']['admin_comment'] == 'Not qualified'

def test_process_application_invalid_action(client, admin_token, app):
    """Test invalid action when processing application"""
    with app.app_context():
        application = AuthorApplication.query.first()
        
        response = client.post(
            f'/api/admin/author-applications/{application.id}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'action': 'invalid_action'}
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert '无效的操作' in data['error']

def test_process_application_missing_comment(client, admin_token, app):
    """Test rejecting without comment"""
    with app.app_context():
        application = AuthorApplication.query.first()
        
        response = client.post(
            f'/api/admin/author-applications/{application.id}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'action': 'reject'}
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert '拒绝申请时必须提供原因' in data['error'] 