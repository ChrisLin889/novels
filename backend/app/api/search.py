from flask import Blueprint, request, jsonify
from app.services.search_service import SearchService

# Create blueprint
search_bp = Blueprint('search', __name__)

# Error response standardization function
def error_response(message, status_code=400):
    """
    Create standardized error response
    
    Args:
        message: Error message
        status_code: HTTP status code
        
    Returns:
        JSON response with error and status code
    """
    return jsonify({'success': False, 'error': message}), status_code

# Success response standardization function
def success_response(data, status_code=200):
    """
    Create standardized success response
    
    Args:
        data: Response data
        status_code: HTTP status code
        
    Returns:
        JSON response with data and status code
    """
    response_data = {'success': True}
    response_data.update(data)
    return jsonify(response_data), status_code

@search_bp.route('/novels', methods=['GET'])
def search_novels():
    """
    Search novels by keyword
    
    GET params:
    - q: Search query/keyword
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    """
    try:
        # Get parameters
        q = request.args.get('q', '')
        
        # Parse numeric parameters
        try:
            page = int(request.args.get('page', 1))
            per_page = min(int(request.args.get('per_page', 20)), 50)  # Limit max per_page
        except ValueError:
            return error_response('Invalid pagination parameters', 400)
        
        # Call service to search novels
        result = SearchService.search_novels(
            q=q,
            page=page,
            per_page=per_page
        )
        
        # Handle error response
        if not result['success']:
            return error_response(result['error'], 400)
        
        # Return success response
        return success_response({
            'total': result['total'],
            'page': result['page'],
            'per_page': result['per_page'],
            'total_pages': result['total_pages'],
            'results': result['results']
        })
    except Exception as e:
        return error_response(str(e), 500)

@search_bp.route('/by-tag', methods=['GET'])
def search_by_tag():
    """
    Search novels by tag
    
    GET params:
    - tag: Tag to search for
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    """
    try:
        # Get parameters
        tag = request.args.get('tag', '')
        if not tag:
            return error_response('Tag parameter is required', 400)
        
        # Parse numeric parameters
        try:
            page = int(request.args.get('page', 1))
            per_page = min(int(request.args.get('per_page', 20)), 50)  # Limit max per_page
        except ValueError:
            return error_response('Invalid pagination parameters', 400)
        
        # Call service to search by tag
        result = SearchService.search_by_tag(
            tag=tag,
            page=page,
            per_page=per_page
        )
        
        # Handle error response
        if not result['success']:
            return error_response(result['error'], 400)
        
        # Return success response
        return success_response({
            'total': result['total'],
            'page': result['page'],
            'per_page': result['per_page'],
            'total_pages': result['total_pages'],
            'results': result['results']
        })
    except Exception as e:
        return error_response(str(e), 500)

@search_bp.route('/novels/tag/<string:tag>', methods=['GET'])
def search_by_tag_path(tag):
    """
    Search novels by tag
    
    GET params:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    """
    try:
        # Tag is now a path parameter, not a query parameter
        if not tag:
            return error_response('Tag parameter is required', 400)
        
        # Parse numeric parameters
        try:
            page = int(request.args.get('page', 1))
            per_page = min(int(request.args.get('per_page', 20)), 50)  # Limit max per_page
        except ValueError:
            return error_response('Invalid pagination parameters', 400)
        
        # Call service to search by tag
        result = SearchService.search_by_tag(
            tag=tag,
            page=page,
            per_page=per_page
        )
        
        # Handle error response
        if not result['success']:
            return error_response(result['error'], 400)
        
        # Return success response
        return success_response({
            'total': result['total'],
            'page': result['page'],
            'per_page': result['per_page'],
            'total_pages': result['total_pages'],
            'results': result['results']
        })
    except Exception as e:
        return error_response(str(e), 500)

@search_bp.route('/similar/<int:novel_id>', methods=['GET'])
def get_similar_novels(novel_id):
    """
    Get similar novels based on a specific novel
    
    GET params:
    - limit: Maximum number of similar novels to return (default: 5)
    """
    try:
        # Get parameters
        limit = min(int(request.args.get('limit', 5)), 20)  # Limit max results
        
        # Call service to get similar novels
        result = SearchService.suggest_similar_novels(
            novel_id=novel_id,
            limit=limit
        )
        
        # Handle error response
        if not result['success']:
            return error_response(result['error'], 404 if 'not found' in result['error'].lower() else 400)
        
        # Change 'results' key to 'similar_novels' to match API documentation
        return success_response({'similar_novels': result['results']})
    except Exception as e:
        return error_response(str(e), 500)

@search_bp.route('/tags/hot', methods=['GET'])
def get_hot_tags():
    """
    Get hot tags
    
    GET params:
    - limit: Number of tags to return (default: 20)
    - category_id: Category ID (optional)
    """
    try:
        # Get parameters
        try:
            limit = min(int(request.args.get('limit', 20)), 100)  # Limit max results
        except ValueError:
            return error_response('Invalid limit parameter', 400)
            
        # Get optional category_id parameter
        category_id = request.args.get('category_id')
        if category_id:
            try:
                category_id = int(category_id)
            except ValueError:
                return error_response('Invalid category_id parameter', 400)
        
        # Call service to get hot tags
        result = SearchService.get_hot_tags(
            limit=limit,
            category_id=category_id
        )
        
        # Handle error response
        if not result['success']:
            return error_response(result['error'], 400)
        
        # Return success response
        return success_response({'tags': result['tags']})
    except Exception as e:
        return error_response(str(e), 500) 