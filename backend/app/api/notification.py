from flask import Blueprint, jsonify, request, g
from app.services.notification_service import NotificationService
from flask_jwt_extended import jwt_required, get_jwt_identity

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('', methods=['GET'])
@jwt_required()
def get_notifications():
    """获取用户通知列表"""
    user_id = get_jwt_identity()
    
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
    except ValueError:
        return jsonify({
            'error': 'Invalid pagination parameters'
        }), 400
    
    result = NotificationService.get_user_notifications(
        user_id=user_id,
        page=page,
        per_page=per_page
    )
    
    if not result['success']:
        return jsonify({
            'error': result['error']
        }), 400
    
    return jsonify(result), 200

@notification_bp.route('/<int:notification_id>/read', methods=['POST'])
@jwt_required()
def mark_notification_read(notification_id):
    """将通知标记为已读"""
    user_id = get_jwt_identity()
    
    result = NotificationService.mark_notification_read(
        user_id=user_id,
        notification_id=notification_id
    )
    
    if not result['success']:
        return jsonify({
            'error': result['error']
        }), 400
    
    return jsonify(result), 200

@notification_bp.route('/read-all', methods=['POST'])
@jwt_required()
def mark_all_read():
    """将所有通知标记为已读"""
    user_id = get_jwt_identity()
    
    result = NotificationService.mark_all_read(user_id=user_id)
    
    if not result['success']:
        return jsonify({
            'error': result['error']
        }), 400
    
    return jsonify(result), 200 