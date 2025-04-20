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
    
    if not result['success']:
        return jsonify({'error': result.get('error', 'Failed to get collections')}), 400
    
    # 返回格式保持与API文档一致
    return jsonify({
        'success': True,
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'novels': result['collections']  # 重命名collections为novels以提供一致的响应格式
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

# New routes for following functionality
@interaction_bp.route('/follow', methods=['POST'])
@jwt_required()
def toggle_follow():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if 'user_id' not in data:
        return jsonify({'error': 'User ID to follow is required'}), 400
    
    followed_id = data.get('user_id')
    
    # Use service to toggle follow
    result = InteractionService.toggle_follow(user_id, followed_id)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    
    return jsonify({
        'message': result['message'],
        'is_following': result['is_following']
    }), 200

@interaction_bp.route('/follow/status/<int:user_id>', methods=['GET'])
@jwt_required()
def get_follow_status(user_id):
    follower_id = get_jwt_identity()
    
    # Use service to check follow status
    result = InteractionService.get_follow_status(follower_id, user_id)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    
    return jsonify({'is_following': result['is_following']}), 200

@interaction_bp.route('/followers/<int:user_id>', methods=['GET'])
def get_followers(user_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Use service to get followers
    result = InteractionService.get_followers(user_id, page, per_page)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    
    return jsonify({
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'followers': result['followers']
    }), 200

@interaction_bp.route('/following/<int:user_id>', methods=['GET'])
def get_following(user_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Use service to get following
    result = InteractionService.get_following(user_id, page, per_page)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    
    return jsonify({
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'following': result['following']
    }), 200

# New routes for messaging functionality
@interaction_bp.route('/message', methods=['POST'])
@jwt_required()
def send_message():
    sender_id = get_jwt_identity()
    data = request.get_json()
    
    if not all(key in data for key in ['recipient_id', 'content']):
        return jsonify({'error': 'Recipient ID and content are required'}), 400
    
    recipient_id = data.get('recipient_id')
    content = data.get('content')
    
    # Use service to send message
    result = InteractionService.send_message(sender_id, recipient_id, content)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({
        'message': result['message'],
        'data': result['data']
    }), 201

@interaction_bp.route('/conversation/<int:user_id>', methods=['GET'])
@jwt_required()
def get_conversation(user_id):
    current_user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    # Use service to get conversation
    result = InteractionService.get_conversation(current_user_id, user_id, page, per_page)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    
    return jsonify({
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'messages': result['messages']
    }), 200

@interaction_bp.route('/inbox', methods=['GET'])
@jwt_required()
def get_inbox():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Use service to get inbox
    result = InteractionService.get_inbox(user_id, page, per_page)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    
    return jsonify({
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'messages': result['messages'],
        'unread_count': result['unread_count']
    }), 200

@interaction_bp.route('/message/<int:message_id>/read', methods=['POST'])
@jwt_required()
def mark_message_read(message_id):
    user_id = get_jwt_identity()
    
    # Use service to mark message as read
    result = InteractionService.mark_message_read(user_id, message_id)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    
    return jsonify({'message': result['message']}), 200

# New routes for tipping functionality
@interaction_bp.route('/tip', methods=['POST'])
@jwt_required()
def send_tip():
    tipper_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ['author_id', 'novel_id', 'amount']
    if not all(key in data for key in required_fields):
        return jsonify({'error': 'Author ID, novel ID, and amount are required'}), 400
    
    author_id = data.get('author_id')
    novel_id = data.get('novel_id')
    amount = data.get('amount')
    message = data.get('message')
    chapter_id = data.get('chapter_id')
    
    # Use service to send tip
    result = InteractionService.send_tip(tipper_id, author_id, novel_id, amount, message, chapter_id)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({
        'message': result['message'],
        'tip': result['tip']
    }), 201

@interaction_bp.route('/tips/received', methods=['GET'])
@jwt_required()
def get_tips_received():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Use service to get tips received
    result = InteractionService.get_tips_received(user_id, page, per_page)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    
    return jsonify({
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'tips': result['tips'],
        'total_amount': result['total_amount']
    }), 200

@interaction_bp.route('/tips/sent', methods=['GET'])
@jwt_required()
def get_tips_sent():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Use service to get tips sent
    result = InteractionService.get_tips_sent(user_id, page, per_page)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    
    return jsonify({
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'tips': result['tips'],
        'total_amount': result['total_amount']
    }), 200

@interaction_bp.route('/user-comments', methods=['GET'])
@jwt_required()
def get_user_comments():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Use service to get user comments
    result = InteractionService.get_user_comments(user_id, page, per_page)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    
    return jsonify({
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'comments': result['comments']
    }), 200 