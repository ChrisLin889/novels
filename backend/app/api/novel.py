from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.novel_service import NovelService
from app.utils.security import author_required, admin_required
from app.models.author import Author
from app.services.permission_service import PermissionService
from app.dao.novel_dao import NovelDAO
import sys
import datetime

novel_bp = Blueprint('novel', __name__)

# 辅助函数，用于统一响应格式
def success_response(data, status_code=200):
    response = {'success': True}
    response.update(data)
    return jsonify(response), status_code

def error_response(message, status_code=400):
    return jsonify({'success': False, 'error': message}), status_code

@novel_bp.route('/<int:novel_id>', methods=['GET'])
def get_novel(novel_id):
    try:
        # 获取小说详情
        result = NovelService.get_novel_by_id(novel_id)
        
        if not result['success']:
            if 'not found' in result['error'].lower():
                return error_response(result['error'], 404)
            return error_response(result['error'], 400)
        
        return success_response({'novel': result['novel']})
    except Exception as e:
        return error_response(str(e))

@novel_bp.route('/list', methods=['GET'])
def get_novel_list():
    """Get paginated list of novels with optional filtering"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        category = request.args.get('category')
        status = request.args.get('status')
        sort_by = request.args.get('sort_by', 'updated_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        # Get novel list from service
        result = NovelService.get_novel_list(
            page=page,
            per_page=per_page,
            category=category,
            status=status,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        # Handle error response
        if not result['success']:
            return error_response(result['error'], 400)
        
        # Return success response
        return success_response({
            'novels': result['novels'],
            'total': result['total'],
            'pages': result['pages'],
            'current_page': page
        })
    except Exception as e:
        return error_response(str(e), 500)

@novel_bp.route('/detail/<int:novel_id>', methods=['GET'])
def get_novel_detail(novel_id):
    """Get detailed information about a novel including its chapters"""
    try:
        # Use service to get novel detail
        result = NovelService.get_novel_detail(novel_id)
        
        # Handle error response
        if not result['success']:
            return error_response(result['error'], 404)
        
        # Return success response
        return success_response({
            'novel': result['novel'],
            'chapters': result.get('chapters', [])
        })
    except Exception as e:
        return error_response(str(e), 500)

@novel_bp.route('/chapters/<int:chapter_id>', methods=['GET'])
def get_chapter(chapter_id):
    """获取章节内容"""
    # Get user ID if logged in
    user_id = None
    auth_header = request.headers.get('Authorization')
    
    print(f"\n\n==== 章节请求调试信息 ====")
    print(f"章节ID: {chapter_id}")
    print(f"请求头: {dict(request.headers)}")
    print(f"当前时间: {datetime.datetime.now()}")
    
    try:
        # 处理认证逻辑
        if auth_header:
            print(f"Authorization头: {auth_header[:30]}...")
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                print(f"提取token: {token[:15]}...")
                
                try:
                    # 明确解码和验证token
                    from flask_jwt_extended import decode_token
                    decoded = decode_token(token)
                    print(f"Token解码成功: {decoded}")
                    
                    # 获取用户ID（sub字段）
                    if 'sub' in decoded:
                        user_id = decoded['sub']
                        print(f"用户ID: {user_id}, 类型: {type(user_id)}")
                        
                        # 验证用户是否存在
                        from app.models.user import User
                        user = User.query.get(user_id)
                        if user:
                            print(f"用户存在: {user.username} (ID: {user_id})")
                        else:
                            print(f"警告: 用户ID {user_id} 在数据库中不存在!")
                    else:
                        print(f"错误: Token中没有sub字段!")
                except Exception as token_err:
                    print(f"Token解析错误: {str(token_err)}")
            else:
                print(f"Authorization头格式错误: {auth_header[:15]}...")
        else:
            print("请求中没有Authorization头")
    except Exception as auth_err:
        import traceback
        print(f"处理认证时出错: {str(auth_err)}")
        print(f"错误类型: {type(auth_err).__name__}")
        print(f"错误跟踪: {traceback.format_exc()}")
    
    # 确保user_id为整数而非字符串
    if user_id is not None:
        try:
            user_id = int(user_id)
            print(f"转换后的用户ID (整数): {user_id}")
        except (ValueError, TypeError):
            print(f"警告: 无法将用户ID {user_id} 转换为整数，将其设为None")
            user_id = None
    
    # Use service to get chapter with extensive logging
    print(f"调用NovelService.get_chapter, 参数: chapter_id={chapter_id}, user_id={user_id}")
    result = NovelService.get_chapter(chapter_id, True, user_id)
    print(f"NovelService.get_chapter返回结果: success={result.get('success', False)}")
    print(f"==== 章节请求调试信息结束 ====\n\n")
    
    if not result['success']:
        return error_response(result['error'], 404)
    
    return success_response({
        'chapter': result['chapter'],
        'prev_chapter': result['prev_chapter'],
        'next_chapter': result['next_chapter']
    })

@novel_bp.route('/search', methods=['GET'])
def search_novels():
    try:
        # Get search parameters
        keyword = request.args.get('keyword', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        category = request.args.get('category', type=str)
        
        if not keyword:
            return error_response('Search keyword is required', 400)
        
        # Search novels
        result = NovelService.search_novels(
            keyword=keyword,
            page=page,
            per_page=per_page,
            category=category
        )
        
        if not result['success']:
            return error_response(result['error'], 400)
        
        return success_response({
            'novels': result['novels'],
            'total': result['total'],
            'pages': result['pages'],
            'current_page': page
        })
    except Exception as e:
        return error_response(str(e))

@novel_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get list of novel categories with counts"""
    try:
        # Use service to get categories
        result = NovelService.get_categories()
        
        # Handle error response
        if not result['success']:
            return error_response(result['error'], 400)
        
        # Return success response
        return success_response({'categories': result['categories']})
    except Exception as e:
        return error_response(str(e), 500)

@novel_bp.route('/popular', methods=['GET'])
def get_popular_novels():
    """Get popular novels with pagination and category filtering"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        category = request.args.get('category', None, type=str)
        
        # Get popular novels from service
        result = NovelService.get_popular_novels(page=page, per_page=per_page, category=category)
        
        # Handle error response
        if not result['success']:
            return error_response(result['error'], 400)
        
        # Return success response
        return success_response({
            'novels': result['novels'],
            'total': result['total'],
            'pages': result['pages'],
            'current_page': page
        })
    except Exception as e:
        return error_response(str(e), 500)

@novel_bp.route('/latest', methods=['GET'])
def get_latest_novels():
    """Get latest novels"""
    try:
        # Get query parameters
        limit = request.args.get('limit', 10, type=int)
        
        # Use service to get latest novels
        result = NovelService.get_latest_novels(limit)
        
        # Handle error response
        if not result['success']:
            return error_response(result['error'], 400)
        
        # Return success response
        return success_response({'novels': result['novels']})
    except Exception as e:
        return error_response(str(e), 500)

@novel_bp.route('/add', methods=['POST'])
@jwt_required()
def add_novel():
    """Add a new novel (author only)"""
    try:
        # Get user ID from JWT
        user_id = get_jwt_identity()
        
        # Get request data
        data = request.get_json()
        
        # Required fields validation
        required_fields = ['title', 'category', 'intro']
        if not all(key in data for key in required_fields):
            return error_response(f'Missing required fields: {", ".join(required_fields)}', 400)
            
        # Use service to add novel
        result = NovelService.add_novel(
            title=data.get('title'),
            category=data.get('category'),
            intro=data.get('intro'),
            cover=data.get('cover', 'default_cover.jpg'),
            tags=data.get('tags', []),
            user_id=user_id
        )
        
        # Handle error response
        if not result['success']:
            error_msg = result['error']
            status_code = 403 if 'permission' in error_msg.lower() else 400
            return error_response(error_msg, status_code)
        
        # Return success response
        return success_response({
            'message': 'Novel added successfully', 
            'novel_id': result.get('novel_id', result.get('novel', {}).get('id'))
        }, 201)
    except Exception as e:
        return error_response(str(e), 500)

@novel_bp.route('/<int:novel_id>/chapters', methods=['GET'])
def get_novel_chapters(novel_id):
    """Get all chapters for a novel"""
    try:
        # Use service to get novel chapters
        result = NovelService.get_novel_chapters(novel_id)
        
        # Handle error response
        if not result['success']:
            error_msg = result['error']
            status_code = 404 if 'not found' in error_msg.lower() else 400
            return error_response(error_msg, status_code)
        
        # Return success response
        return success_response({'chapters': result['chapters']})
    except Exception as e:
        return error_response(str(e), 500)

@novel_bp.route('/<int:novel_id>/chapters/all', methods=['GET'])
def get_all_chapters(novel_id):
    """获取小说的所有章节"""
    # Use service to get all chapters
    result = NovelService.get_all_chapters(novel_id)
    
    if not result['success']:
        # 判断错误类型并返回适当的状态码
        error_msg = result['error']
        if 'not found' in error_msg.lower():
            return error_response(error_msg, 404)
        else:
            return error_response(error_msg)
    
    return success_response({'chapters': result['chapters']})

# 标签管理API
@novel_bp.route('/<int:novel_id>/tags', methods=['GET'])
def get_novel_tags(novel_id):
    """获取小说的所有标签"""
    result = NovelService.get_novel_tags(novel_id)
    
    if not result['success']:
        error_msg = result['error']
        if 'not found' in error_msg.lower():
            return error_response(error_msg, 404)
        else:
            return error_response(error_msg)
    
    return success_response({'tags': result['tags']})

@novel_bp.route('/<int:novel_id>/tags', methods=['POST'])
@jwt_required()
@author_required()
def add_tags_to_novel(novel_id):
    """为小说添加标签"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # 验证必要参数
        if not data or 'tags' not in data or not isinstance(data['tags'], list):
            return error_response('Tags list is required', 400)
        
        # 获取小说详情
        novel = NovelService.get_novel_by_id(novel_id)
        if not novel['success']:
            return error_response(novel['error'], 404)
        
        # 获取用户的作者记录
        author = Author.query.filter_by(user_id=user_id).first()
        if not author:
            return error_response('Author not found', 404)
        
        # 验证权限：只有小说作者可以添加标签
        if novel['novel']['author_id'] != author.id:
            return error_response('Permission denied - only the novel author can add tags', 403)
        
        # 添加标签
        result = NovelService.add_tags_to_novel(novel_id, data['tags'])
        
        if not result['success']:
            return error_response(result['error'])
        
        return success_response({
            'message': result['message'],
            'added_tags': result.get('added_tags', [])
        })
    except Exception as e:
        return error_response(str(e))

@novel_bp.route('/<int:novel_id>/tags/<int:tag_id>', methods=['DELETE'])
@jwt_required()
@author_required()
def remove_tag_from_novel(novel_id, tag_id):
    """从小说中移除标签"""
    try:
        user_id = get_jwt_identity()
        
        # 获取小说详情
        novel = NovelService.get_novel_by_id(novel_id)
        if not novel['success']:
            return error_response(novel['error'], 404)
        
        # 获取用户的作者记录
        author = Author.query.filter_by(user_id=user_id).first()
        if not author:
            return error_response('Author not found', 404)
        
        # 验证权限：只有小说作者可以移除标签
        if novel['novel']['author_id'] != author.id:
            return error_response('Permission denied - only the novel author can remove tags', 403)
        
        # 移除标签
        result = NovelService.remove_tag_from_novel(novel_id, tag_id)
        
        if not result['success']:
            error_msg = result['error']
            if 'not found' in error_msg.lower():
                return error_response(error_msg, 404)
            else:
                return error_response(error_msg)
        
        return success_response({'message': result['message']})
    except Exception as e:
        return error_response(str(e))

@novel_bp.route('/tags', methods=['GET'])
def get_all_tags():
    """获取所有标签列表"""
    result = NovelService.get_all_tags()
    
    if not result['success']:
        return error_response(result['error'])
    
    return success_response({'tags': result['tags']})

@novel_bp.route('/author/novels', methods=['GET'])
@jwt_required()
@author_required()
def get_author_novels():
    """作者获取自己的所有小说"""
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Use service to get author novels
    result = NovelService.get_author_novels(user_id, page, per_page)
    
    if not result['success']:
        return error_response(result['error'])
    
    return success_response({
        'novels': result['novels'],
        'total': result['total'],
        'pages': result.get('pages', 1),
        'current_page': page
    })

@novel_bp.route('/author/stats', methods=['GET'])
@jwt_required()
@author_required()
def get_author_stats():
    """获取作者统计数据"""
    user_id = get_jwt_identity()
    
    # Use service to get author stats
    result = NovelService.get_author_stats(user_id)
    
    if not result['success']:
        # 判断错误类型并返回适当的状态码
        error_msg = result['error']
        if 'not found' in error_msg.lower():
            return error_response(error_msg, 404)
        else:
            return error_response(error_msg)
    
    return success_response(result['stats'])

@novel_bp.route('/<int:novel_id>/chapters', methods=['POST'])
@jwt_required()
@author_required()
def add_chapter(novel_id):
    """Add a new chapter to a novel (author only)"""
    try:
        # Get user ID from JWT
        user_id = get_jwt_identity()
        
        # Get author record
        author = Author.query.filter_by(user_id=user_id).first()
        if not author:
            return error_response('Author not found', 404)
        
        # Get request data
        data = request.get_json()
        
        # Required fields validation
        required_fields = ['title', 'content']
        if not all(key in data for key in required_fields):
            return error_response(f'Missing required fields: {", ".join(required_fields)}', 400)
        
        # Use service to add chapter
        result = NovelService.add_chapter(
            author_id=author.id,
            novel_id=novel_id,
            title=data.get('title'),
            content=data.get('content'),
            chapter_number=data.get('chapter_number')
        )
        
        # Handle error response
        if not result['success']:
            error_msg = result['error']
            status_code = 404 if 'not found' in error_msg.lower() else 400
            return error_response(error_msg, status_code)
        
        # Return success response with format matching the documentation
        return success_response({
            'success': True,
            'message': 'Chapter added successfully',
            'chapter_id': result['chapter']['id']
        }, 201)
    except Exception as e:
        return error_response(str(e), 500)

@novel_bp.route('/<int:novel_id>', methods=['PUT'])
@jwt_required()
def update_novel(novel_id):
    """Update novel information (author only)"""
    try:
        # Get user ID from JWT
        user_id = get_jwt_identity()
        
        # Get request data
        data = request.get_json()
        
        # Use service to update novel
        result = NovelService.update_novel(
            novel_id=novel_id,
            user_id=user_id,
            title=data.get('title'),
            category=data.get('category'),
            intro=data.get('intro'),
            cover=data.get('cover'),
            status=data.get('status'),
            tags=data.get('tags')
        )
        
        # Handle error response
        if not result['success']:
            error_msg = result['error']
            if 'permission' in error_msg.lower():
                status_code = 403
            elif 'not found' in error_msg.lower():
                status_code = 404
            else:
                status_code = 400
            return error_response(error_msg, status_code)
        
        # Return success response
        return success_response({'message': 'Novel updated successfully'})
    except Exception as e:
        return error_response(str(e), 500)

@novel_bp.route('/<int:novel_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_novel(novel_id):
    """Delete a novel (author or admin only)"""
    try:
        # Get user ID from JWT
        user_id = get_jwt_identity()
        
        # Use service to delete novel
        result = NovelService.delete_novel(user_id, novel_id)
        
        # Handle error response
        if not result['success']:
            error_msg = result['error']
            if 'permission' in error_msg.lower():
                status_code = 403
            elif 'not found' in error_msg.lower():
                status_code = 404
            else:
                status_code = 400
            return error_response(error_msg, status_code)
        
        # Return success response
        return success_response({'message': 'Novel deleted successfully'})
    except Exception as e:
        return error_response(str(e), 500)

@novel_bp.route('/chapters/<int:chapter_id>', methods=['DELETE'])
@jwt_required()
def delete_chapter(chapter_id):
    try:
        user_id = get_jwt_identity()
        
        # Use service to delete chapter with user_id
        result = NovelService.delete_chapter(user_id=user_id, chapter_id=chapter_id)
        
        if not result['success']:
            error_msg = result['error']
            if 'permission' in error_msg.lower():
                return error_response(error_msg, 403)
            elif 'not found' in error_msg.lower():
                return error_response(error_msg, 404)
            else:
                return error_response(error_msg, 400)
        
        return success_response({'message': 'Chapter deleted successfully'})
    except Exception as e:
        return error_response(str(e))

@novel_bp.route('/refresh-cache', methods=['POST'])
@jwt_required()
def refresh_cache():
    user_id = get_jwt_identity()
    
    # Use service to refresh cache
    result = NovelService.refresh_cache(user_id)
    
    if not result['success']:
        # 判断错误类型并返回适当的状态码
        error_msg = result['error']
        if 'permission denied' in error_msg.lower():
            return error_response(error_msg, 403)
        else:
            return error_response(error_msg)
    
    return success_response({'message': result['message']})

@novel_bp.route('/chapters/<int:chapter_id>', methods=['PUT'])
@jwt_required()
def update_chapter(chapter_id):
    """更新章节内容（作者或管理员）"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # 使用服务更新章节 - 直接传递user_id
        result = NovelService.update_chapter(user_id=user_id, chapter_id=chapter_id, data=data)
        
        if not result['success']:
            error_msg = result['error']
            if 'permission' in error_msg.lower():
                return error_response(error_msg, 403)
            elif 'not found' in error_msg.lower():
                return error_response(error_msg, 404)
            else:
                return error_response(error_msg, 400)
        
        return success_response({
            'message': 'Chapter updated successfully',
            'chapter': result.get('chapter')
        })
    except Exception as e:
        return error_response(str(e))

@novel_bp.route('/author/pending', methods=['GET'])
@jwt_required()
@author_required()
def get_author_pending_content():
    """Get author's pending/rejected content"""
    try:
        # Get author ID from user ID
        user_id = get_jwt_identity()
        author = Author.query.filter_by(user_id=user_id).first()
        
        if not author:
            return error_response('Author not found', 404)
        
        # Get pending content for author
        result = NovelDAO.get_author_pending_content(author.id)
        
        return success_response({
            'pending_novels': result['novels'],
            'pending_chapters': result['chapters']
        })
    except Exception as e:
        return error_response(str(e), 500) 