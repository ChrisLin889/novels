from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.cache_service import CacheService
from app.models.user import User

cache_bp = Blueprint('cache', __name__)

@cache_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh_cache():
    """Refresh all cache (admin only)"""
    user_id = get_jwt_identity()
    
    # Check if user is admin
    user = User.query.get(user_id)
    if not user or user.role != 'admin':
        return jsonify({'error': 'Only admin can perform this operation'}), 403
    
    CacheService.refresh_novel_cache()
    return jsonify({'message': 'Cache refreshed successfully'}), 200

@cache_bp.route('/clear', methods=['POST'])
@jwt_required()
def clear_cache():
    """Clear all cache (admin only)"""
    user_id = get_jwt_identity()
    
    # Check if user is admin
    user = User.query.get(user_id)
    if not user or user.role != 'admin':
        return jsonify({'error': 'Only admin can perform this operation'}), 403
    
    CacheService.clear_all()
    return jsonify({'message': 'Cache cleared successfully'}), 200

@cache_bp.route('/novel/<int:novel_id>', methods=['DELETE'])
@jwt_required()
def clear_novel_cache(novel_id):
    """Clear cache for a specific novel (admin or author)"""
    user_id = get_jwt_identity()
    
    # Check if user is admin or author of the novel
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get novel from database to check if user is author
    from app.models.novel import Novel
    novel = Novel.query.get(novel_id)
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    # Check permissions
    if user.role != 'admin' and novel.author != user.username:
        return jsonify({'error': 'Permission denied'}), 403
    
    # Delete novel cache
    CacheService.delete(f"novel:{novel_id}")
    CacheService.delete_pattern(f"chapter:{novel_id}:*")
    
    return jsonify({'message': 'Novel cache cleared successfully'}), 200

@cache_bp.route('/rankings/<string:ranking_type>', methods=['DELETE'])
@jwt_required()
def clear_ranking_cache(ranking_type):
    """Clear ranking cache (admin only)"""
    user_id = get_jwt_identity()
    
    # Check if user is admin
    user = User.query.get(user_id)
    if not user or user.role != 'admin':
        return jsonify({'error': 'Only admin can perform this operation'}), 403
    
    # Valid ranking types
    valid_types = ['hot', 'latest', 'popular', 'all']
    
    if ranking_type not in valid_types and ranking_type != 'all':
        return jsonify({'error': 'Invalid ranking type'}), 400
    
    if ranking_type == 'all':
        CacheService.delete_pattern("ranking:*")
        return jsonify({'message': 'All ranking caches cleared successfully'}), 200
    else:
        CacheService.delete(f"ranking:{ranking_type}")
        return jsonify({'message': f'{ranking_type} ranking cache cleared successfully'}), 200

@cache_bp.route('/categories', methods=['DELETE'])
@jwt_required()
def clear_categories_cache():
    """Clear categories cache (admin only)"""
    user_id = get_jwt_identity()
    
    # Check if user is admin
    user = User.query.get(user_id)
    if not user or user.role != 'admin':
        return jsonify({'error': 'Only admin can perform this operation'}), 403
    
    CacheService.delete("category:all")
    return jsonify({'message': 'Categories cache cleared successfully'}), 200

@cache_bp.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def clear_user_cache(user_id):
    """Clear cache for a specific user (admin or the user themselves)"""
    current_user_id = get_jwt_identity()
    
    # Check permissions
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({'error': 'User not found'}), 404
    
    if current_user.role != 'admin' and current_user_id != user_id:
        return jsonify({'error': 'Permission denied'}), 403
    
    # Clear user cache
    CacheService.invalidate_user_cache(user_id)
    return jsonify({'message': 'User cache cleared successfully'}), 200 