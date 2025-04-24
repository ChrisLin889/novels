from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.interaction_service import InteractionService
from app.models.user import User

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
    
    print(f"DEBUG - 获取阅读历史API: user_id={user_id}, page={page}, per_page={per_page}")
    
    # Use service to get reading history
    result = InteractionService.get_reading_history(user_id, page, per_page)
    
    print(f"DEBUG - 阅读历史服务返回结果: total={result.get('total', 0)}, history_count={len(result.get('history', []))}")
    
    response = {
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'history': result['history']
    }
    
    return jsonify(response), 200

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
    
    # 确保chapter_id为None或有效值
    if chapter_id == '' or chapter_id == 0 or chapter_id is None:
        chapter_id = None
    
    # Use service to add comment - 修正参数顺序以匹配服务层
    result = InteractionService.add_comment(user_id, novel_id, chapter_id, content)
    
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
    
    if 'target_user_id' not in data:
        return jsonify({'error': 'User ID to follow is required'}), 400
    
    followed_id = data.get('target_user_id')
    
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
    
    # 修改返回结构，符合API文档
    return jsonify({
        'message': 'Message sent successfully',
        'message_id': result['data']['id']  # 假设data包含消息ID
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
    
    # Use directly from service layer which now includes the conversation_with field
    return jsonify({
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'conversation_with': result['conversation_with'],
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
    
    # Return using consistent field names from the service layer
    return jsonify({
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'conversations': result['conversations'],  # Now directly use the correct field name
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

@interaction_bp.route('/user/comments', methods=['GET'])
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