from flask import Blueprint, request, jsonify, g
from app.services.admin_service import AdminService
from app.services.author_service import AuthorService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.security import admin_required
from app.config.settings import update_setting, get_settings
from app.dao.admin_dao import AdminDAO
from app.dao.novel_dao import NovelDAO
from app.models.admin import Admin

# Create blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ====== User Management ======

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required()
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
@jwt_required()
@admin_required()
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
@jwt_required()
@admin_required()
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
@jwt_required()
@admin_required()
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

@admin_bp.route('/content/<string:content_type>', methods=['GET'])
@jwt_required()
@admin_required()
def get_pending_content(content_type):
    """
    Get content pending review
    
    content_type: 'novel' or 'chapter'
    """
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Get pending content by type
        result = AdminService.get_pending_content(content_type, page, per_page)
        
        if not result['success']:
            return jsonify({'error': result['error']}), 400
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/content', methods=['GET'])
@jwt_required()
@admin_required()
def get_pending_content_summary():
    """Get summary of all pending content"""
    try:
        result = AdminService.get_pending_content()
        
        if not result['success']:
            return jsonify({'error': result['error']}), 400
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/content/audit/<string:content_type>/<int:content_id>', methods=['POST'])
@jwt_required()
@admin_required()
def audit_content(content_type, content_id):
    """
    Review and update content status
    
    content_type: 'novel' or 'chapter'
    content_id: ID of the content
    """
    try:
        # Validate content type
        if content_type not in ['novel', 'chapter']:
            return jsonify({'error': 'Invalid content type'}), 400
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing request data'}), 400
        
        # Get status and comment from request
        status = data.get('status')
        comment = data.get('comment')
        
        if not status or status not in ['approved', 'rejected']:
            return jsonify({'error': 'Invalid status'}), 400
        
        # Get admin ID
        admin_id = get_jwt_identity()
        
        # Process audit action
        result = AdminService.audit_content(content_type, content_id, status, admin_id, comment)
        
        if not result['success']:
            return jsonify({'error': result['error']}), 400
        
        return jsonify({'message': f'{content_type.capitalize()} has been {status}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/settings/content_audit', methods=['GET'])
@jwt_required()
@admin_required()
def get_content_audit_setting():
    """Get content audit setting"""
    try:
        settings = get_settings()
        enable_content_audit = settings.get('enable_content_audit', True)
        
        return jsonify({'enable_content_audit': enable_content_audit})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/settings/content_audit', methods=['POST'])
@jwt_required()
@admin_required()
def update_content_audit_setting():
    """Update content audit setting"""
    try:
        # Get request data
        data = request.get_json()
        if data is None or 'enable' not in data:
            return jsonify({'error': 'Missing enable parameter'}), 400
        
        # Get enable value
        enable = data.get('enable')
        if not isinstance(enable, bool):
            return jsonify({'error': 'Enable parameter must be a boolean'}), 400
        
        # Update setting
        success = update_setting('enable_content_audit', enable)
        if not success:
            return jsonify({'error': 'Failed to update setting'}), 500
        
        return jsonify({'enable_content_audit': enable})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/author/<int:author_id>/exempt', methods=['POST'])
@jwt_required()
@admin_required()
def toggle_author_exempt_status(author_id):
    """Toggle author exempt from audit status"""
    try:
        # Get request data
        data = request.get_json()
        if data is None or 'exempt' not in data:
            return jsonify({'error': 'Missing exempt parameter'}), 400
        
        # Get exempt value
        exempt = data.get('exempt')
        if not isinstance(exempt, bool):
            return jsonify({'error': 'Exempt parameter must be a boolean'}), 400
        
        # Update author exempt status
        result = AdminService.toggle_exempt_from_audit(author_id, exempt)
        
        if not result['success']:
            return jsonify({'error': result['error']}), 400
        
        return jsonify({'exempt_from_audit': exempt})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ====== Sensitive Words Management ======

@admin_bp.route('/sensitive-words', methods=['GET'])
@jwt_required()
@admin_required()
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
@jwt_required()
@admin_required()
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
@jwt_required()
@admin_required()
def get_dashboard_stats():
    """
    Get statistics for admin dashboard
    """
    result = AdminService.get_dashboard_stats()
    
    return jsonify(result)

# ====== Author Management ======

@admin_bp.route('/author-applications', methods=['GET'])
@jwt_required()
@admin_required()
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
@admin_required()
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
@jwt_required()
@admin_required()
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
@admin_required()
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
@admin_required()
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
@admin_required()
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
@admin_required()
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
@admin_required()
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
@admin_required()
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
@admin_required()
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
@admin_required()
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
@admin_required()
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
@admin_required()
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
@admin_required()
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
@admin_required()
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

@admin_bp.route('/content/audit/<int:audit_id>', methods=['POST'])
@jwt_required()
@admin_required()
def audit_content_by_id(audit_id):
    """
    Review and update content status by audit ID
    
    audit_id: ID of the ContentAudit record
    """
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing request data'}), 400
        
        # Get status and reason from request
        status = data.get('status')
        reason = data.get('reason')
        
        if not status or status not in ['approved', 'rejected']:
            return jsonify({'error': 'Invalid status'}), 400
        
        # Get admin ID - 修复：获取正确的管理员ID
        user_id = get_jwt_identity()
        admin = Admin.query.filter_by(user_id=user_id).first()
        if not admin:
            return jsonify({'error': 'Admin record not found for the current user'}), 400
        admin_id = admin.id
        
        # Process audit action
        audit = AdminDAO.audit_content(audit_id, admin_id, status, reason)
        
        # Get content type and ID 
        content_type = audit.content_type
        content_id = audit.content_id
        
        # Update the content status too
        NovelDAO.update_audit_status(content_type, content_id, status)
        
        return jsonify({'success': True, 'message': f'Content has been {status}'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ====== 内容管理 ======

@admin_bp.route('/novels', methods=['GET'])
@jwt_required()
@admin_required()
def get_admin_novels():
    """
    获取所有小说（带分页和筛选）
    
    GET params:
    - page: 页码 (默认: 1)
    - per_page: 每页条数 (默认: 20)
    - title: 标题筛选 (可选)
    - category: 分类筛选 (可选)
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
    except ValueError:
        return jsonify({
            'error': 'Invalid pagination parameters'
        }), 400
    
    title_filter = request.args.get('title')
    category = request.args.get('category')
    
    result = AdminService.get_novels(
        page=page, 
        per_page=per_page, 
        title_filter=title_filter, 
        category=category
    )
    
    return jsonify(result)

@admin_bp.route('/chapters', methods=['GET'])
@jwt_required()
@admin_required()
def get_admin_chapters():
    """
    获取所有章节（带分页和筛选）
    
    GET params:
    - novel_id: 小说ID筛选 (可选)
    - title: 标题筛选 (可选)
    - page: 页码 (默认: 1)
    - per_page: 每页条数 (默认: 20)
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
    
    title_filter = request.args.get('title')
    
    result = AdminService.get_chapters(
        page=page, 
        per_page=per_page, 
        novel_id=novel_id,
        title_filter=title_filter
    )
    
    return jsonify(result)

@admin_bp.route('/comments', methods=['GET'])
@jwt_required()
@admin_required()
def get_admin_comments():
    """
    获取所有评论（带分页和筛选）
    
    GET params:
    - novel_id: 小说ID筛选 (可选)
    - chapter_id: 章节ID筛选 (可选)
    - page: 页码 (默认: 1)
    - per_page: 每页条数 (默认: 20)
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
    
    result = AdminService.get_comments(
        page=page, 
        per_page=per_page, 
        novel_id=novel_id,
        chapter_id=chapter_id
    )
    
    return jsonify(result)

@admin_bp.route('/trash/<string:content_type>/<int:content_id>', methods=['POST'])
@jwt_required()
@admin_required()
def move_to_trash(content_type, content_id):
    """
    将内容移至回收站
    
    content_type: 'novel'(小说), 'chapter'(章节), 'comment'(评论)
    content_id: 内容ID
    """
    if content_type not in ['novel', 'chapter', 'comment']:
        return jsonify({'error': 'Invalid content type'}), 400
        
    # 获取管理员ID
    admin_id = get_jwt_identity()
    
    if content_type == 'novel':
        result = AdminService.delete_novel(admin_id, content_id)
    elif content_type == 'chapter':
        result = AdminService.delete_chapter(admin_id, content_id)
    elif content_type == 'comment':
        result = AdminService.delete_comment(admin_id, content_id)
    
    if not result['success']:
        return jsonify({'error': result['message']}), 400
        
    return jsonify({'success': True, 'message': f'{content_type.capitalize()} has been moved to trash'}) 