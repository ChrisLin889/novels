from functools import wraps
from flask import jsonify, g
from flask_jwt_extended import get_jwt, verify_jwt_in_request, get_jwt_identity
from app.models.user import User

def token_required(f):
    """
    Decorator to verify a valid JWT token is present in the request
    Also injects the user object into Flask's g object
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        
        # Get user from database and add to request context
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Add user to Flask's g object for use in the route
        g.user = user
        
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """
    Decorator to verify the JWT has an admin role claim
    Also injects the user object into Flask's g object
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        
        if claims.get("role") != "admin":
            return jsonify({"error": "Admin privileges required"}), 403
            
        # Get user from database and add to request context
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != "admin":
            return jsonify({"error": "Admin privileges required"}), 403
            
        # Add user to Flask's g object for use in the route
        g.user = user
        
        return f(*args, **kwargs)
    return decorated 