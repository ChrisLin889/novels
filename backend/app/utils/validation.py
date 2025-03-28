from flask import request, jsonify
from functools import wraps

def validate_params(required_params, location='json'):
    """
    Decorator to validate required parameters in request
    
    Args:
        required_params (list): List of required parameter names
        location (str): Where to look for params ('json', 'args', 'form')
        
    Returns:
        Decorated function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get data from appropriate location
            if location == 'json':
                data = request.json
            elif location == 'args':
                data = request.args
            elif location == 'form':
                data = request.form
            else:
                return jsonify({'error': 'Invalid parameter location'}), 400
                
            # Check if data exists
            if not data and required_params:
                return jsonify({
                    'error': f'Missing request data in {location}'
                }), 400
                
            # Check for required parameters
            missing = []
            for param in required_params:
                if param not in data or data[param] is None:
                    missing.append(param)
                    
            if missing:
                return jsonify({
                    'error': f'Missing required parameters: {", ".join(missing)}'
                }), 400
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator 