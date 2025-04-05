from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.novel_service import NovelService
from app.utils.security import author_required, admin_required

novel_bp = Blueprint('novel', __name__)

@novel_bp.route('/list', methods=['GET'])
def get_novel_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category')
    sort_by = request.args.get('sort_by', 'updated_at')
    
    # Use service to get novel list
    result = NovelService.get_novel_list(category, page, per_page, sort_by)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'novels': result['novels']
    }), 200

@novel_bp.route('/detail/<int:novel_id>', methods=['GET'])
def get_novel_detail(novel_id):
    # Use service to get novel detail
    result = NovelService.get_novel_detail(novel_id)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    
    return jsonify({
        'novel': result['novel'],
        'chapters': result.get('chapters', [])
    }), 200

@novel_bp.route('/chapter/<int:chapter_id>', methods=['GET'])
def get_chapter(chapter_id):
    # Get user ID if logged in
    user_id = None
    if request.headers.get('Authorization'):
        try:
            user_id = get_jwt_identity()
        except:
            pass
    
    # Use service to get chapter
    result = NovelService.get_chapter(chapter_id, True, user_id)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    
    return jsonify({
        'chapter': result['chapter'],
        'prev_chapter': result['prev_chapter'],
        'next_chapter': result['next_chapter']
    }), 200

@novel_bp.route('/search', methods=['GET'])
def search_novels():
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    if not keyword:
        return jsonify({'error': 'Search keyword is required'}), 400
    
    # Use service to search novels
    result = NovelService.search_novels(keyword, page, per_page)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page'],
        'novels': result['novels']
    }), 200

@novel_bp.route('/categories', methods=['GET'])
def get_categories():
    # Use service to get categories
    result = NovelService.get_categories()
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({'categories': result['categories']}), 200

@novel_bp.route('/popular', methods=['GET'])
def get_popular_novels():
    limit = request.args.get('limit', 10, type=int)
    
    # Use service to get popular novels
    result = NovelService.get_popular_novels(limit)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({'novels': result['novels']}), 200

@novel_bp.route('/latest', methods=['GET'])
def get_latest_novels():
    limit = request.args.get('limit', 10, type=int)
    
    # Use service to get latest novels
    result = NovelService.get_latest_novels(limit)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({'novels': result['novels']}), 200

@novel_bp.route('/add', methods=['POST'])
@jwt_required()
@author_required()
def add_novel():
    """Add a new novel (author only)"""
    data = request.get_json()
    
    # 获取必要字段
    title = data.get('title')
    author_name = data.get('author')  # 可以使用自定义作者名
    category = data.get('category')
    intro = data.get('intro')
    cover = data.get('cover', 'default_cover.jpg')
    status = data.get('status', 'ongoing')
    
    # 验证必要字段
    if not all([title, author_name, category, intro]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # 获取当前用户ID作为内部作者ID
    author_id = get_jwt_identity()
    
    # 使用服务添加小说
    result = NovelService.add_novel(
        title=title,
        author_name=author_name,
        category=category,
        intro=intro,
        author_id=author_id,
        cover=cover,
        status=status
    )
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({
        'message': result['message'],
        'novel': result['novel']
    }), 201

@novel_bp.route('/<int:novel_id>/chapter/add', methods=['POST'])
@jwt_required()
@author_required()
def add_chapter(novel_id):
    author_id = get_jwt_identity()
    data = request.get_json()
    
    # Extract chapter data
    title = data.get('title')
    content = data.get('content')
    chapter_number = data.get('chapter_number')
    
    # Use service to add chapter
    result = NovelService.add_chapter(author_id, novel_id, title, content, chapter_number)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({
        'message': result['message'],
        'chapter': result['chapter']
    }), 201

@novel_bp.route('/<int:novel_id>', methods=['PUT'])
@jwt_required()
def update_novel(novel_id):
    """Update novel information (author or admin only)"""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    # 使用服务更新小说
    result = NovelService.update_novel(novel_id, data, user_id)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({
        'message': result['message'],
        'novel': result['novel']
    }), 200

@novel_bp.route('/chapter/<int:chapter_id>/update', methods=['PUT'])
@jwt_required()
@author_required()
def update_chapter(chapter_id):
    author_id = get_jwt_identity()
    data = request.get_json()
    
    # Use service to update chapter
    result = NovelService.update_chapter(author_id, chapter_id, data)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({
        'message': result['message'],
        'chapter': result['chapter']
    }), 200

@novel_bp.route('/<int:novel_id>/delete', methods=['DELETE'])
@jwt_required()
@admin_required()
def delete_novel(novel_id):
    admin_id = get_jwt_identity()
    
    # Use service to delete novel
    result = NovelService.delete_novel(admin_id, novel_id)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({'message': result['message']}), 200

@novel_bp.route('/chapter/<int:chapter_id>/delete', methods=['DELETE'])
@jwt_required()
@author_required()
def delete_chapter(chapter_id):
    author_id = get_jwt_identity()
    
    # Use service to delete chapter
    result = NovelService.delete_chapter(author_id, chapter_id)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({'message': result['message']}), 200

@novel_bp.route('/refresh-cache', methods=['POST'])
@jwt_required()
@admin_required()
def refresh_cache():
    # Use service to refresh cache
    result = NovelService.refresh_cache()
    
    if not result['success']:
        return jsonify({'error': result['error']}), 500
    
    return jsonify({'message': result['message']}), 200

@novel_bp.route('/my', methods=['GET'])
@jwt_required()
@author_required()
def get_my_novels():
    """Get novels created by the current author"""
    try:
        author_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用服务获取作者的小说
        result = NovelService.get_author_novels(author_id, page, per_page)
        
        if not result['success']:
            return jsonify({'error': result['error']}), 400
        
        return jsonify({
            'novels': result['novels'],
            'total': result['total'],
            'total_pages': result['total_pages'],
            'current_page': result['current_page']
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@novel_bp.route('/author/stats', methods=['GET'])
@jwt_required()
@author_required()
def get_author_stats():
    """Get author statistics"""
    try:
        author_id = get_jwt_identity()
        
        # 使用服务获取作者统计信息
        result = NovelService.get_author_stats(author_id)
        
        if not result['success']:
            return jsonify({'error': result['error']}), 400
        
        return jsonify(result['stats']), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@novel_bp.route('/<int:novel_id>/chapters', methods=['GET'])
def get_novel_chapters(novel_id):
    """Get all chapters for a novel"""
    try:
        # Use service to get chapters
        result = NovelService.get_novel_detail(novel_id)
        
        if not result['success']:
            return jsonify({'error': result['error']}), 404
        
        return jsonify({
            'novel': result['novel'],
            'chapters': result.get('chapters', [])
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400 