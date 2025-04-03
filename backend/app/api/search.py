from flask import Blueprint, request, jsonify
from app.services.search_service import SearchService

# Create blueprint
search_bp = Blueprint('search', __name__)

@search_bp.route('/novels', methods=['GET'])
def search_novels():
    """
    Search novels by keyword
    
    GET params:
    - q: Search query/keyword
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    """
    # Get parameters
    q = request.args.get('q', '')
    
    # Parse numeric parameters
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 50)  # Limit max per_page
    except ValueError:
        return jsonify({
            'error': 'Invalid pagination parameters'
        }), 400
    
    # Call service to search novels
    results = SearchService.search_novels(
        q=q,
        page=page,
        per_page=per_page
    )
    
    return jsonify(results)

@search_bp.route('/novels/tag/<tag>', methods=['GET'])
def search_by_tag(tag):
    """
    Search novels by tag
    
    GET params:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 50)
    except ValueError:
        return jsonify({
            'error': 'Invalid pagination parameters'
        }), 400
    
    results = SearchService.search_by_tag(
        tag=tag,
        page=page,
        per_page=per_page
    )
    
    return jsonify(results)

@search_bp.route('/similar/<int:novel_id>', methods=['GET'])
def get_similar_novels(novel_id):
    """
    Get novels similar to the specified novel
    
    GET params:
    - limit: Number of similar novels to return (default: 5)
    """
    try:
        limit = min(int(request.args.get('limit', 5)), 20)
    except ValueError:
        return jsonify({
            'error': 'Invalid limit parameter'
        }), 400
    
    similar_novels = SearchService.suggest_similar_novels(
        novel_id=novel_id,
        limit=limit
    )
    
    return jsonify({
        'similar_novels': similar_novels
    }) 