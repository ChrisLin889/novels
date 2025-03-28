from flask import Blueprint, request, jsonify, current_app, g
from app.services.search_service import SearchService
from datetime import datetime, timedelta
from app.utils.auth import token_required
from app.utils.validation import validate_params

# Create blueprint
search_bp = Blueprint('search', __name__)

@search_bp.route('/novels', methods=['GET'])
def search_novels():
    """
    Search novels with advanced filters
    
    GET params:
    - q: Search query/keyword
    - category: Optional category filter
    - status: Optional status filter (ongoing, completed)
    - min_words: Minimum word count
    - max_words: Maximum word count
    - updated_since: Number of days (novels updated in last X days)
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    """
    # Get parameters
    keyword = request.args.get('q', '')
    category = request.args.get('category')
    status = request.args.get('status')
    
    # Parse numeric parameters
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 50)  # Limit max per_page
        min_words = request.args.get('min_words')
        min_words = int(min_words) if min_words else None
        max_words = request.args.get('max_words')
        max_words = int(max_words) if max_words else None
        updated_since = request.args.get('updated_since')
    except ValueError:
        return jsonify({
            'error': 'Invalid numeric parameter'
        }), 400
    
    # Convert updated_since days to datetime
    updated_after = None
    if updated_since:
        try:
            days = int(updated_since)
            updated_after = datetime.utcnow() - timedelta(days=days)
        except ValueError:
            return jsonify({
                'error': 'Invalid updated_since parameter'
            }), 400
    
    # Call service to search novels
    results = SearchService.search_novels(
        keyword=keyword,
        category=category,
        min_words=min_words,
        max_words=max_words,
        status=status,
        updated_after=updated_after,
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

@search_bp.route('/trending', methods=['GET'])
def get_trending_keywords():
    """
    Get trending search keywords
    
    GET params:
    - limit: Number of keywords to return (default: 10)
    """
    try:
        limit = min(int(request.args.get('limit', 10)), 50)
    except ValueError:
        return jsonify({
            'error': 'Invalid limit parameter'
        }), 400
    
    trending_keywords = SearchService.get_trending_keywords(limit=limit)
    
    return jsonify({
        'trending_keywords': trending_keywords
    })

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