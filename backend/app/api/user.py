from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app.services.user_service import UserService
from app import db
import datetime
import json

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print(f"Register request data: {json.dumps(data)}")
    
    # Extract registration data
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone')
    email = data.get('email')
    
    print(f"Extracted data - username: {username}, phone: {phone}, email: {email}, password length: {len(password) if password else 0}")
    
    # Use service to handle registration
    result = UserService.register(username, password, email, phone)
    
    if not result['success']:
        print(f"Registration failed: {result['message']}")
        return jsonify({'error': result['message']}), 400
    
    # Get basic user information
    user = User.query.get(result['user_id'])
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'phone': user.phone,
        'created_at': user.created_at.isoformat() if user.created_at else None
    }
    
    return jsonify({
        'success': True,
        'message': result['message'],
        'user': user_data
    }), 201

@user_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    # Validate input
    identifier = None
    is_email = False
    
    if 'email' in data and data['email']:
        identifier = data.get('email')
        is_email = True
    elif 'phone' in data and data['phone']:
        identifier = data.get('phone')
    elif 'username' in data and data['username']:
        identifier = data.get('username')
    else:
        return jsonify({
            'success': False,
            'error': 'At least one of email, phone, or username is required'
        }), 400
    
    password = data.get('password')
    if not password:
        return jsonify({
            'success': False,
            'error': 'Password is required'
        }), 400
    
    # Call service to handle login
    result = UserService.login(identifier, password, is_email)
    
    if not result['success']:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 401
    
    # Create access token
    expires = datetime.timedelta(days=7)
    access_token = create_access_token(
        identity=result['user_id'],
        additional_claims={'role': result['role']},
        expires_delta=expires
    )
    
    # Return response with token and user info
    return jsonify({
        'success': True,
        'access_token': access_token,
        'user': result['user']
    }), 200

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    
    # Use service to get profile
    result = UserService.get_profile(user_id)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    
    return jsonify(result['user']), 200

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Use service to update profile
    result = UserService.update_profile(user_id, data)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({
        'success': True,
        'message': result['message'],
        'user': result['user']
    }), 200

@user_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not current_password or not new_password:
        return jsonify({'error': 'Both current and new password are required'}), 400
    
    # Use service to change password
    result = UserService.change_password(user_id, current_password, new_password)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({'message': result['message']}), 200

@user_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def list_users():
    admin_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Use service to list users (admin only)
    result = UserService.list_users(admin_id, page, per_page)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 403
    
    return jsonify({
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'users': result['users']
    }), 200

@user_bp.route('/admin/users/<int:target_user_id>/status', methods=['PUT'])
@jwt_required()
def toggle_user_status(target_user_id):
    admin_id = get_jwt_identity()
    data = request.get_json()
    status = data.get('status', False)
    
    # Use service to change user status (admin only)
    result = UserService.manage_user_status(admin_id, target_user_id, status)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 403 if 'Admin privileges' in result['error'] else 404
    
    return jsonify({
        'message': result['message'],
        'user': result['user']
    }), 200

@user_bp.route('/admin/users/<int:target_user_id>/role', methods=['PUT'])
@jwt_required()
def update_user_role(target_user_id):
    """Update a user's role (admin only)"""
    admin_id = get_jwt_identity()
    data = request.get_json()
    new_role = data.get('role')
    
    if not new_role or new_role not in ['user', 'author', 'admin']:
        return jsonify({'error': 'Invalid role'}), 400
    
    # Use service to update role
    result = UserService.update_user_role(admin_id, target_user_id, new_role)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({
        'message': result['message'],
        'user': result['user']
    }), 200

@user_bp.route('/deactivate', methods=['POST'])
@jwt_required()
def deactivate_account():
    """Deactivate (delete) current user's account"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Check password
    password = data.get('password')
    if not password:
        return jsonify({'error': 'Password is required for account deactivation'}), 400
    
    # Call service to handle account deactivation
    result = UserService.deactivate_account(user_id, password)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({
        'success': True,
        'message': result['message']
    }), 200

@user_bp.route('/resign-author', methods=['POST'])
@jwt_required()
def resign_author():
    """Resign author status (convert from author to regular user)"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Check password
    password = data.get('password')
    if not password:
        return jsonify({'error': 'Password is required to resign author status'}), 400
    
    # Call service to handle author resignation
    result = UserService.resign_author_status(user_id, password)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({
        'success': True,
        'message': result['message'],
        'has_works': result.get('has_works', False)
    }), 200 