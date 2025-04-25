from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.admin_service import AdminService
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ====== 回收站功能 ======

@admin_bp.route('/recycle-bin/novels', methods=['GET'])
@jwt_required()
@admin_required
def get_recycled_novels():
    """
    获取回收站中的所有小说（分页）
    
    GET参数:
    - page: 页码（默认: 1）
    - per_page: 每页数量（默认: 20）
    - title: 标题筛选（可选）
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
    except ValueError:
        return jsonify({
            'error': '无效的分页参数'
        }), 400
    
    title_filter = request.args.get('title')
    
    result = AdminService.get_recycled_novels(page=page, per_page=per_page, title_filter=title_filter)
    
    return jsonify(result)

@admin_bp.route('/recycle-bin/chapters', methods=['GET'])
@jwt_required()
@admin_required
def get_recycled_chapters():
    """
    获取回收站中的所有章节（分页）
    
    GET参数:
    - novel_id: 小说ID筛选（可选）
    - page: 页码（默认: 1）
    - per_page: 每页数量（默认: 20）
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
        novel_id = request.args.get('novel_id')
        if novel_id:
            novel_id = int(novel_id)
    except ValueError:
        return jsonify({
            'error': '无效的参数'
        }), 400
    
    result = AdminService.get_recycled_chapters(novel_id=novel_id, page=page, per_page=per_page)
    
    return jsonify(result)

@admin_bp.route('/recycle-bin/comments', methods=['GET'])
@jwt_required()
@admin_required
def get_recycled_comments():
    """
    获取回收站中的所有评论（分页）
    
    GET参数:
    - novel_id: 小说ID筛选（可选）
    - chapter_id: 章节ID筛选（可选）
    - page: 页码（默认: 1）
    - per_page: 每页数量（默认: 20）
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
            'error': '无效的参数'
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
    从回收站还原小说及其关联内容
    """
    # 从认证中获取管理员用户ID
    admin_id = g.user_id
    
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
    从回收站还原章节及其关联评论
    """
    # 从认证中获取管理员用户ID
    admin_id = g.user_id
    
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
    从回收站还原评论
    """
    # 从认证中获取管理员用户ID
    admin_id = g.user_id
    
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
    永久删除回收站中的小说
    """
    # 从认证中获取管理员用户ID
    admin_id = g.user_id
    
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
    永久删除回收站中的章节
    """
    # 从认证中获取管理员用户ID
    admin_id = g.user_id
    
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
    永久删除回收站中的评论
    """
    # 从认证中获取管理员用户ID
    admin_id = g.user_id
    
    result = AdminService.permanently_delete_comment(admin_id, comment_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

# 修改现有的删除路由，使用软删除而不是永久删除

@admin_bp.route('/novels/<int:novel_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_novel(novel_id):
    """
    软删除小说（移至回收站）
    """
    # 从认证中获取管理员用户ID
    admin_id = g.user_id
    
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
    软删除章节（移至回收站）
    """
    # 从认证中获取管理员用户ID
    admin_id = g.user_id
    
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
    软删除评论（移至回收站）
    """
    # 从认证中获取管理员用户ID
    admin_id = g.user_id
    
    result = AdminService.delete_comment(admin_id, comment_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result) 