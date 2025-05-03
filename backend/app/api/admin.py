from flask import Blueprint, request, jsonify, g
from app.services.admin_service import AdminService
from app.services.author_service import AuthorService
from app.utils.auth import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create blueprint
admin_bp = Blueprint('admin', __name__)

# ====== User Management ======

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    """
    Get users with pagination
    
    GET params:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    - role: Filter by role (optional)
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
    except ValueError:
        return jsonify({
            'error': 'Invalid pagination parameters'
        }), 400
    
    role = request.args.get('role')
    
    result = AdminService.get_users(page=page, per_page=per_page, role=role)
    
    return jsonify(result)

@admin_bp.route('/users/<int:user_id>', methods=['POST'])
@admin_required
def manage_user(user_id):
    """
    Manage a user (ban, unban)
    
    POST params:
    - action: "ban" or "unban"
    - reason: Reason for action
    - duration: Ban duration in days (only for "ban" action)
    """
    # Get admin user ID from auth
    admin_id = g.user.id
    
    # Get request data
    data = request.json
    if not data:
        return jsonify({
            'error': 'Missing request data'
        }), 400
    
    action = data.get('action')
    reason = data.get('reason')
    duration = data.get('duration')
    
    if not action or not reason:
        return jsonify({
            'error': 'Missing required parameters'
        }), 400
    
    # Convert duration to int if present
    if duration:
        try:
            duration = int(duration)
        except ValueError:
            return jsonify({
                'error': 'Invalid duration'
            }), 400
    
    result = AdminService.manage_user(
        admin_id=admin_id,
        user_id=user_id,
        action=action,
        reason=reason,
        duration=duration
    )
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

@admin_bp.route('/user-actions', methods=['GET'])
@admin_required
def get_user_actions():
    """
    Get user management actions
    
    GET params:
    - user_id: Filter by target user ID (optional)
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
        user_id = request.args.get('user_id')
        if user_id:
            user_id = int(user_id)
    except ValueError:
        return jsonify({
            'error': 'Invalid parameters'
        }), 400
    
    result = AdminService.get_user_actions(user_id=user_id, page=page, per_page=per_page)
    
    return jsonify(result)

@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@admin_required
def update_user_role(user_id):
    """
    Update a user's role
    
    PUT params:
    - role: New role for the user
    """
    # Get admin user ID from auth
    admin_id = g.user.id
    
    # Get request data
    data = request.json
    if not data:
        return jsonify({
            'error': 'Missing request data'
        }), 400
    
    role = data.get('role')
    if not role:
        return jsonify({
            'error': 'Missing role parameter'
        }), 400
    
    result = AdminService.update_user_role(
        admin_id=admin_id,
        user_id=user_id,
        role=role
    )
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

# ====== Content Management ======

@admin_bp.route('/content/<content_type>', methods=['GET'])
@admin_required
def get_pending_content(content_type):
    """
    Get pending content for moderation
    
    URL params:
    - content_type: Type of content ("novel", "chapter", "comment")
    
    GET params:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    """
    # Validate content type
    if content_type not in ['novel', 'chapter', 'comment']:
        return jsonify({
            'error': f"Invalid content type: {content_type}"
        }), 400
    
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 50)
    except ValueError:
        return jsonify({
            'error': 'Invalid pagination parameters'
        }), 400
    
    result = AdminService.get_pending_content(content_type=content_type, page=page, per_page=per_page)
    
    return jsonify(result)

@admin_bp.route('/content/audit/<int:audit_id>', methods=['POST'])
@admin_required
def audit_content(audit_id):
    """
    Approve or reject content
    
    POST params:
    - status: "approved" or "rejected"
    - reason: Reason for rejection (required for "rejected" status)
    """
    # Get admin user ID from auth
    admin_id = g.user.id
    
    # Get request data
    data = request.json
    if not data:
        return jsonify({
            'error': 'Missing request data'
        }), 400
    
    status = data.get('status')
    reason = data.get('reason')
    
    if not status or status not in ['approved', 'rejected']:
        return jsonify({
            'error': 'Invalid status'
        }), 400
    
    if status == 'rejected' and not reason:
        return jsonify({
            'error': 'Reason is required for rejection'
        }), 400
    
    result = AdminService.audit_content(
        audit_id=audit_id,
        admin_id=admin_id,
        status=status,
        reason=reason
    )
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

# ====== Sensitive Words Management ======

@admin_bp.route('/sensitive-words', methods=['GET'])
@admin_required
def get_sensitive_words():
    """
    Get sensitive words
    
    GET params:
    - category: Filter by category (optional)
    - page: Page number (default: 1)
    - per_page: Items per page (default: 50)
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 50)), 200)
    except ValueError:
        return jsonify({
            'error': 'Invalid pagination parameters'
        }), 400
    
    category = request.args.get('category')
    
    result = AdminService.get_sensitive_words(category=category, page=page, per_page=per_page)
    
    return jsonify(result)

@admin_bp.route('/sensitive-words', methods=['POST'])
@admin_required
def manage_sensitive_word():
    """
    Add or delete a sensitive word
    
    POST params:
    - action: "add" or "delete"
    - word: The sensitive word (for "add" action)
    - level: Sensitivity level (for "add" action)
    - category: Word category (for "add" action)
    - word_id: ID of word to delete (for "delete" action)
    """
    # Get admin user ID from auth
    admin_id = g.user.id
    
    # Get request data
    data = request.json
    if not data:
        return jsonify({
            'error': 'Missing request data'
        }), 400
    
    action = data.get('action')
    
    if action == 'add':
        word = data.get('word')
        level = data.get('level')
        category = data.get('category')
        
        if not word or not level or not category:
            return jsonify({
                'error': 'Missing required parameters for add'
            }), 400
        
        try:
            level = int(level)
            if level < 1 or level > 3:
                raise ValueError("Level must be between 1 and 3")
        except ValueError:
            return jsonify({
                'error': 'Invalid level'
            }), 400
        
        result = AdminService.manage_sensitive_word(
            word=word,
            level=level,
            category=category,
            admin_id=admin_id,
            action='add'
        )
    elif action == 'delete':
        word_id = data.get('word_id')
        
        if not word_id:
            return jsonify({
                'error': 'Missing word_id for delete'
            }), 400
        
        try:
            word_id = int(word_id)
        except ValueError:
            return jsonify({
                'error': 'Invalid word_id'
            }), 400
        
        result = AdminService.manage_sensitive_word(
            word="",  # Not used for delete
            level=0,  # Not used for delete
            category="",  # Not used for delete
            admin_id=admin_id,
            action='delete',
            word_id=word_id
        )
    else:
        return jsonify({
            'error': f"Invalid action: {action}"
        }), 400
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

# ====== Dashboard ======

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard_stats():
    """
    Get statistics for admin dashboard
    """
    result = AdminService.get_dashboard_stats()
    
    return jsonify(result)

# ====== Author Management ======

@admin_bp.route('/author-applications', methods=['GET'])
@jwt_required()
@admin_required
def get_pending_applications():
    """获取待处理的作者申请列表"""
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
    except ValueError:
        return jsonify({
            'error': '无效的分页参数'
        }), 400
    
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

@admin_bp.route('/author-applications/<int:application_id>', methods=['POST'])
@jwt_required()
@admin_required
def process_application(application_id):
    """处理作者申请"""
    # Get admin user ID from auth
    admin_id = get_jwt_identity()
    
    # Get request data
    data = request.json
    if not data:
        return jsonify({
            'error': '缺少请求数据'
        }), 400
    
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

@admin_bp.route('/content-scan', methods=['POST'])
@admin_required
def scan_content():
    """
    手动触发内容敏感词扫描和替换
    """
    from app.utils.tasks import scan_and_update_content
    
    # 执行扫描
    result = scan_and_update_content()
    
    if not result['success']:
        return jsonify({
            'error': result['error']
        }), 500
    
    return jsonify(result), 200

# ====== Recycle Bin ======

@admin_bp.route('/recycle-bin/novels', methods=['GET'])
@jwt_required()
@admin_required
def get_recycled_novels():
    """
    Get all novels in recycle bin (paginated)
    
    GET params:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    - title: Title filter (optional)
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
    except ValueError:
        return jsonify({
            'error': 'Invalid pagination parameters'
        }), 400
    
    title_filter = request.args.get('title')
    
    result = AdminService.get_recycled_novels(page=page, per_page=per_page, title_filter=title_filter)
    
    return jsonify(result)

@admin_bp.route('/recycle-bin/chapters', methods=['GET'])
@jwt_required()
@admin_required
def get_recycled_chapters():
    """
    Get all chapters in recycle bin (paginated)
    
    GET params:
    - novel_id: Novel ID filter (optional)
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
        novel_id = request.args.get('novel_id')
        if novel_id:
            novel_id = int(novel_id)
    except ValueError:
        return jsonify({
            'error': 'Invalid parameters'
        }), 400
    
    result = AdminService.get_recycled_chapters(novel_id=novel_id, page=page, per_page=per_page)
    
    return jsonify(result)

@admin_bp.route('/recycle-bin/comments', methods=['GET'])
@jwt_required()
@admin_required
def get_recycled_comments():
    """
    Get all comments in recycle bin (paginated)
    
    GET params:
    - novel_id: Novel ID filter (optional)
    - chapter_id: Chapter ID filter (optional)
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
        
        novel_id = request.args.get('novel_id')
        if novel_id:
            novel_id = int(novel_id)
            
        chapter_id = request.args.get('chapter_id')
        if chapter_id:
            chapter_id = int(chapter_id)
    except ValueError:
        return jsonify({
            'error': 'Invalid parameters'
        }), 400
    
    result = AdminService.get_recycled_comments(
        novel_id=novel_id, 
        chapter_id=chapter_id, 
        page=page, 
        per_page=per_page
    )
    
    return jsonify(result)

@admin_bp.route('/recycle-bin/novels/<int:novel_id>/restore', methods=['POST'])
@jwt_required()
@admin_required
def restore_novel(novel_id):
    """
    Restore a novel and its associated content from recycle bin
    """
    # Get admin user ID from auth
    admin_id = g.user.id
    
    result = AdminService.restore_novel(admin_id, novel_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

@admin_bp.route('/recycle-bin/chapters/<int:chapter_id>/restore', methods=['POST'])
@jwt_required()
@admin_required
def restore_chapter(chapter_id):
    """
    Restore a chapter and its associated comments from recycle bin
    """
    # Get admin user ID from auth
    admin_id = g.user.id
    
    result = AdminService.restore_chapter(admin_id, chapter_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

@admin_bp.route('/recycle-bin/comments/<int:comment_id>/restore', methods=['POST'])
@jwt_required()
@admin_required
def restore_comment(comment_id):
    """
    Restore a comment from recycle bin
    """
    # Get admin user ID from auth
    admin_id = g.user.id
    
    result = AdminService.restore_comment(admin_id, comment_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

@admin_bp.route('/recycle-bin/novels/<int:novel_id>/permanent', methods=['DELETE'])
@jwt_required()
@admin_required
def permanently_delete_novel(novel_id):
    """
    Permanently delete a novel from recycle bin
    """
    # Get admin user ID from auth
    admin_id = g.user.id
    
    result = AdminService.permanently_delete_novel(admin_id, novel_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

@admin_bp.route('/recycle-bin/chapters/<int:chapter_id>/permanent', methods=['DELETE'])
@jwt_required()
@admin_required
def permanently_delete_chapter(chapter_id):
    """
    Permanently delete a chapter from recycle bin
    """
    # Get admin user ID from auth
    admin_id = g.user.id
    
    result = AdminService.permanently_delete_chapter(admin_id, chapter_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

@admin_bp.route('/recycle-bin/comments/<int:comment_id>/permanent', methods=['DELETE'])
@jwt_required()
@admin_required
def permanently_delete_comment(comment_id):
    """
    Permanently delete a comment from recycle bin
    """
    # Get admin user ID from auth
    admin_id = g.user.id
    
    result = AdminService.permanently_delete_comment(admin_id, comment_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

# Modify existing delete routes to use soft delete instead of permanent delete

@admin_bp.route('/novels/<int:novel_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_novel(novel_id):
    """
    Soft delete a novel (move to recycle bin)
    """
    # Get admin user ID from auth
    admin_id = g.user.id
    
    result = AdminService.delete_novel(admin_id, novel_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

@admin_bp.route('/chapters/<int:chapter_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_chapter(chapter_id):
    """
    Soft delete a chapter (move to recycle bin)
    """
    # Get admin user ID from auth
    admin_id = g.user.id
    
    result = AdminService.delete_chapter(admin_id, chapter_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

@admin_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_comment(comment_id):
    """
    Soft delete a comment (move to recycle bin)
    """
    # Get admin user ID from auth
    admin_id = g.user.id
    
    result = AdminService.delete_comment(admin_id, comment_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result) 