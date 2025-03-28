import re
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request

def admin_required():
    """
    Decorator to verify the JWT has an admin role claim
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") != "admin":
                return jsonify({"error": "Admin privileges required"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def author_required():
    """
    Decorator to verify the JWT has an author or admin role claim
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") not in ["author", "admin"]:
                return jsonify({"error": "Author privileges required"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def filter_sensitive_words(content, blocked_words=None):
    """
    Filter sensitive words from content
    """
    if blocked_words is None:
        # Default list of sensitive words, should be loaded from database in real app
        blocked_words = ['敏感词1', '敏感词2', '敏感词3']
    
    filtered_content = content
    for word in blocked_words:
        # Replace sensitive words with asterisks
        filtered_content = re.sub(word, '*' * len(word), filtered_content)
    
    return filtered_content

def validate_password(password):
    """
    Validates the password meets minimum requirements
    """
    # Check if password length is at least 8 characters
    if len(password) < 8:
        return False
    
    # Check if password contains at least one digit
    if not re.search(r'\d', password):
        return False
    
    # Check if password contains at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False
    
    return True 