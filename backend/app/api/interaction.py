from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.interaction_service import InteractionService

interaction_bp = Blueprint('interaction', __name__)

@interaction_bp.route('/collection', methods=['POST'])
@jwt_required()
def toggle_collection():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if 'novel_id' not in data:
        return jsonify({'error': 'Novel ID is required'}), 400
    
    novel_id = data.get('novel_id')
    
    # Use service to toggle collection
    result = InteractionService.toggle_collection(user_id, novel_id)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    
    return jsonify({
        'message': result['message'],
        'is_collected': result['is_collected']
    }), 200

@interaction_bp.route('/collection/status/<int:novel_id>', methods=['GET'])
@jwt_required()
def get_collection_status(novel_id):
    user_id = get_jwt_identity()
    
    # Use service to check collection status
    result = InteractionService.get_collection_status(user_id, novel_id)
    
    return jsonify({'is_collected': result['is_collected']}), 200

@interaction_bp.route('/collection', methods=['GET'])
@jwt_required()
def get_collections():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Use service to get collections
    result = InteractionService.get_user_collections(user_id, page, per_page)
    
    return jsonify({
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'collections': result['collections']
    }), 200

@interaction_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Use service to get reading history
    result = InteractionService.get_reading_history(user_id, page, per_page)
    
    return jsonify({
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'history': result['history']
    }), 200

@interaction_bp.route('/progress/<int:novel_id>', methods=['GET'])
@jwt_required()
def get_reading_progress(novel_id):
    user_id = get_jwt_identity()
    
    # Use service to get reading progress
    result = InteractionService.get_reading_progress(user_id, novel_id)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    
    return jsonify(result), 200

@interaction_bp.route('/comment', methods=['POST'])
@jwt_required()
def add_comment():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not all(key in data for key in ['novel_id', 'content']):
        return jsonify({'error': 'Novel ID and content are required'}), 400
    
    novel_id = data.get('novel_id')
    content = data.get('content')
    chapter_id = data.get('chapter_id')
    
    # Use service to add comment
    result = InteractionService.add_comment(user_id, novel_id, content, chapter_id)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({
        'message': result['message'],
        'comment': result['comment']
    }), 201

@interaction_bp.route('/comments/<int:novel_id>', methods=['GET'])
def get_novel_comments(novel_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Use service to get novel comments
    result = InteractionService.get_comments(novel_id, None, page, per_page)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    
    return jsonify({
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'comments': result['comments']
    }), 200

@interaction_bp.route('/comments/<int:novel_id>/chapter/<int:chapter_id>', methods=['GET'])
def get_chapter_comments(novel_id, chapter_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Use service to get chapter comments
    result = InteractionService.get_comments(novel_id, chapter_id, page, per_page)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    
    return jsonify({
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'comments': result['comments']
    }), 200

@interaction_bp.route('/comment/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    user_id = get_jwt_identity()
    
    # Use service to delete comment
    result = InteractionService.delete_comment(user_id, comment_id)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 403 if 'Permission denied' in result['error'] else 404
    
    return jsonify({'message': result['message']}), 200 