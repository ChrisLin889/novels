from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db
import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    if not all(key in data for key in ['username', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check for existing user
    phone = data.get('phone')
    email = data.get('email')
    
    if not phone and not email:
        return jsonify({'error': 'Either phone or email is required'}), 400
    
    if phone and User.query.filter_by(phone=phone).first():
        return jsonify({'error': 'Phone number already registered'}), 400
    
    if email and User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create new user
    user = User(
        username=data['username'],
        phone=phone,
        email=email
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict()
    }), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Check for login credentials
    if 'phone' in data:
        user = User.query.filter_by(phone=data['phone']).first()
    elif 'email' in data:
        user = User.query.filter_by(email=data['email']).first()
    else:
        return jsonify({'error': 'Either phone or email is required'}), 400
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not user.status:
        return jsonify({'error': 'Account is disabled'}), 403
    
    # Create access token
    expires = datetime.timedelta(days=7)
    access_token = create_access_token(
        identity=user.id,
        additional_claims={'role': user.role},
        expires_delta=expires
    )
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Fields that can be updated
    if 'username' in data:
        user.username = data['username']
    
    if 'avatar' in data:
        user.avatar = data['avatar']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': user.to_dict()
    }), 200 