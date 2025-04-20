from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.author_service import AuthorService
from app.utils.auth import admin_required

author_bp = Blueprint('author', __name__)

@author_bp.route('/application', methods=['POST'])
@jwt_required()
def submit_application():
    """提交作者申请"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # 验证必要字段
    pen_name = data.get('pen_name')
    bio = data.get('bio')
    reason = data.get('reason')
    
    if not all([pen_name, bio, reason]):
        return jsonify({'error': '笔名、简介和申请理由为必填项'}), 400
        
    # 调用服务提交申请
    result = AuthorService.submit_application(user_id, pen_name, bio, reason)
    
    if not result['success']:
        return jsonify({'error': result['message']}), 400
        
    return jsonify({
        'message': result['message'],
        'application': result['application']
    }), 201

@author_bp.route('/applications', methods=['GET'])
@jwt_required()
def get_user_applications():
    """获取用户的作者申请历史"""
    user_id = get_jwt_identity()
    
    # 调用服务获取申请历史
    result = AuthorService.get_user_applications(user_id)
    
    if not result['success']:
        return jsonify({'error': result['message']}), 400
        
    return jsonify({'applications': result['applications']}), 200

@author_bp.route('/admin/applications', methods=['GET'])
@jwt_required()
@admin_required
def get_pending_applications():
    """获取待处理的作者申请列表（管理员使用）"""
    page = request.args.get('page', 1, type=int)
    per_page = min(int(request.args.get('per_page', 20)), 100)
    
    # 调用服务获取待处理申请
    result = AuthorService.get_pending_applications(page, per_page)
    
    if not result['success']:
        return jsonify({'error': result['message']}), 400
        
    return jsonify({
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'applications': result['applications']
    }), 200

@author_bp.route('/admin/applications/<int:application_id>', methods=['POST'])
@jwt_required()
@admin_required
def process_application(application_id):
    """处理作者申请（管理员使用）"""
    admin_id = get_jwt_identity()
    data = request.get_json()
    
    # 验证必要字段
    action = data.get('action')
    comment = data.get('comment')
    
    if not action or action not in ['approve', 'reject']:
        return jsonify({'error': '无效的操作，必须是 approve 或 reject'}), 400
        
    if action == 'reject' and not comment:
        return jsonify({'error': '拒绝申请时必须提供原因'}), 400
        
    # 调用服务处理申请
    result = AuthorService.process_application(application_id, admin_id, action, comment)
    
    if not result['success']:
        return jsonify({'error': result['message']}), 400
        
    return jsonify({
        'message': result['message'],
        'application': result['application']
    }), 200

@author_bp.route('/resign', methods=['POST'])
@jwt_required()
def resign_author():
    """放弃作者身份"""
    user_id = get_jwt_identity()
    
    # 调用服务处理注销
    result = AuthorService.resign_author(user_id)
    
    if not result['success']:
        return jsonify({'error': result['message']}), 400
        
    return jsonify({
        'success': True,
        'message': result['message']
    }), 200

@author_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """更新作者资料"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # 调用服务更新资料
    result = AuthorService.update_author_profile(user_id, data)
    
    if not result['success']:
        return jsonify({'error': result['message']}), 400
        
    return jsonify({
        'success': True,
        'message': result['message'],
        'author': result['author']
    }), 200 