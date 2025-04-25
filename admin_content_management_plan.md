# 小说平台管理员内容管理系统开发文档

## 1. 功能概述

本功能模块旨在为管理员提供一个全面的内容管理系统，用于管理平台上的所有小说、章节和评论。主要功能包括：

- 查看平台所有小说列表，支持分页和按标题筛选
- 查看特定小说的所有章节和评论
- 查看平台上所有章节，支持按小说筛选
- 查看平台上所有评论，支持按小说或章节筛选
- 独立删除单条评论
- 独立删除单个章节（同时删除该章节下的所有评论）
- 删除整本小说（同时级联删除所有相关章节和评论）

## 2. 技术架构

### 2.1 API设计

#### 2.1.1 获取小说列表

```
GET /admin/novels
请求参数：
- page: 页码（默认1）
- per_page: 每页数量（默认20）
- title: 标题筛选（可选）

响应：
{
  "novels": [...],  // 小说列表
  "total": 100,     // 总数量
  "page": 1,        // 当前页码
  "per_page": 20,   // 每页数量
  "total_pages": 5  // 总页数
}
```

#### 2.1.2 获取章节列表

```
GET /admin/chapters
请求参数：
- novel_id: 小说ID（可选，用于筛选）
- page: 页码（默认1）
- per_page: 每页数量（默认20）

响应：
{
  "chapters": [...],  // 章节列表（包含小说标题信息）
  "total": 100,       // 总数量
  "page": 1,          // 当前页码
  "per_page": 20,     // 每页数量
  "total_pages": 5    // 总页数
}
```

#### 2.1.3 获取评论列表

```
GET /admin/comments
请求参数：
- novel_id: 小说ID（可选，用于筛选）
- chapter_id: 章节ID（可选，用于筛选）
- page: 页码（默认1）
- per_page: 每页数量（默认20）

响应：
{
  "comments": [...],  // 评论列表（包含用户、小说、章节信息）
  "total": 100,       // 总数量
  "page": 1,          // 当前页码
  "per_page": 20,     // 每页数量
  "total_pages": 5    // 总页数
}
```

#### 2.1.4 删除小说

```
DELETE /admin/novels/{novel_id}

响应：
{
  "success": true,
  "message": "小说已成功删除"
}
```

#### 2.1.5 删除章节

```
DELETE /admin/chapters/{chapter_id}

响应：
{
  "success": true,
  "message": "章节已成功删除"
}
```

#### 2.1.6 删除评论

```
DELETE /admin/comments/{comment_id}

响应：
{
  "success": true,
  "message": "评论已成功删除"
}
```

### 2.2 数据流

1. 小说删除时，通过数据库外键级联关系自动删除章节，同时手动删除相关评论
2. 章节删除时，需手动删除关联的评论
3. 评论删除为独立操作，不影响关联的小说和章节

## 3. 后端实现

### 3.1 DAO层

需要在 `app/dao/admin_dao.py` 中添加以下方法：

```python
@staticmethod
def get_all_novels(page: int = 1, per_page: int = 20, title_filter: str = None) -> Tuple[List[Novel], int]:
    """获取所有小说，支持分页和标题筛选"""
    query = Novel.query
    
    if title_filter:
        query = query.filter(Novel.title.ilike(f'%{title_filter}%'))
    
    total = query.count()
    novels = query.order_by(desc(Novel.updated_at)).paginate(page=page, per_page=per_page).items
    
    return novels, total

@staticmethod
def get_all_chapters(novel_id: Optional[int] = None, page: int = 1, per_page: int = 20) -> Tuple[List[Chapter], int]:
    """获取所有章节，支持按小说ID筛选"""
    query = Chapter.query
    
    if novel_id:
        query = query.filter_by(novel_id=novel_id)
    
    total = query.count()
    chapters = query.order_by(Chapter.novel_id, Chapter.chapter_number).paginate(page=page, per_page=per_page).items
    
    return chapters, total

@staticmethod
def get_all_comments(novel_id: Optional[int] = None, chapter_id: Optional[int] = None, 
                    page: int = 1, per_page: int = 20) -> Tuple[List[Comment], int]:
    """获取所有评论，支持按小说ID或章节ID筛选"""
    query = Comment.query
    
    if novel_id:
        query = query.filter_by(novel_id=novel_id)
    
    if chapter_id:
        query = query.filter_by(chapter_id=chapter_id)
    
    total = query.count()
    comments = query.order_by(desc(Comment.created_at)).paginate(page=page, per_page=per_page).items
    
    return comments, total

@staticmethod
def delete_novel_cascade(novel_id: int) -> bool:
    """删除小说及其所有章节和评论（级联删除）"""
    novel = Novel.query.get(novel_id)
    if not novel:
        return False
    
    try:
        # 删除该小说下的所有评论
        Comment.query.filter_by(novel_id=novel_id).delete()
        
        # 删除小说（会通过外键约束级联删除章节）
        db.session.delete(novel)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"删除小说时出错: {str(e)}")
        return False

@staticmethod
def soft_delete_novel(novel_id: int) -> bool:
    """软删除小说（移至回收站）"""
    novel = Novel.query.get(novel_id)
    if not novel:
        return False
    
    try:
        # 软删除小说
        novel.is_deleted = True
        novel.deleted_at = datetime.now()
        
        # 同时软删除相关章节
        Chapter.query.filter_by(novel_id=novel_id).update({
            'is_deleted': True,
            'deleted_at': datetime.now()
        })
        
        # 同时软删除相关评论
        Comment.query.filter_by(novel_id=novel_id).update({
            'is_deleted': True,
            'deleted_at': datetime.now()
        })
        
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"软删除小说时出错: {str(e)}")
        return False

@staticmethod
def soft_delete_chapter(chapter_id: int) -> bool:
    """软删除章节（移至回收站）"""
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return False
    
    try:
        # 软删除章节
        chapter.is_deleted = True
        chapter.deleted_at = datetime.now()
        
        # 同时软删除相关评论
        Comment.query.filter_by(chapter_id=chapter_id).update({
            'is_deleted': True,
            'deleted_at': datetime.now()
        })
        
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"软删除章节时出错: {str(e)}")
        return False

@staticmethod
def soft_delete_comment(comment_id: int) -> bool:
    """软删除评论（移至回收站）"""
    comment = Comment.query.get(comment_id)
    if not comment:
        return False
    
    try:
        comment.is_deleted = True
        comment.deleted_at = datetime.now()
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"软删除评论时出错: {str(e)}")
        return False

@staticmethod
def get_deleted_novels(page: int = 1, per_page: int = 20, title_filter: str = None) -> Tuple[List[Novel], int]:
    """获取回收站中的所有小说"""
    query = Novel.query.filter_by(is_deleted=True)
    
    if title_filter:
        query = query.filter(Novel.title.ilike(f'%{title_filter}%'))
    
    total = query.count()
    novels = query.order_by(desc(Novel.deleted_at)).paginate(page=page, per_page=per_page).items
    
    return novels, total

@staticmethod
def get_deleted_chapters(novel_id: Optional[int] = None, page: int = 1, per_page: int = 20) -> Tuple[List[Chapter], int]:
    """获取回收站中的所有章节"""
    query = Chapter.query.filter_by(is_deleted=True)
    
    if novel_id:
        query = query.filter_by(novel_id=novel_id)
    
    total = query.count()
    chapters = query.order_by(desc(Chapter.deleted_at)).paginate(page=page, per_page=per_page).items
    
    return chapters, total

@staticmethod
def get_deleted_comments(novel_id: Optional[int] = None, chapter_id: Optional[int] = None, 
                         page: int = 1, per_page: int = 20) -> Tuple[List[Comment], int]:
    """获取回收站中的所有评论"""
    query = Comment.query.filter_by(is_deleted=True)
    
    if novel_id:
        query = query.filter_by(novel_id=novel_id)
    
    if chapter_id:
        query = query.filter_by(chapter_id=chapter_id)
    
    total = query.count()
    comments = query.order_by(desc(Comment.deleted_at)).paginate(page=page, per_page=per_page).items
    
    return comments, total

@staticmethod
def restore_novel(novel_id: int) -> bool:
    """从回收站还原小说及其关联内容"""
    novel = Novel.query.get(novel_id)
    if not novel or not novel.is_deleted:
        return False
    
    try:
        # 还原小说
        novel.is_deleted = False
        novel.deleted_at = None
        
        # 还原相关章节
        Chapter.query.filter_by(novel_id=novel_id, is_deleted=True).update({
            'is_deleted': False,
            'deleted_at': None
        })
        
        # 还原相关评论
        Comment.query.filter_by(novel_id=novel_id, is_deleted=True).update({
            'is_deleted': False,
            'deleted_at': None
        })
        
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"还原小说时出错: {str(e)}")
        return False

@staticmethod
def restore_chapter(chapter_id: int) -> bool:
    """从回收站还原章节及其关联评论"""
    chapter = Chapter.query.get(chapter_id)
    if not chapter or not chapter.is_deleted:
        return False
    
    try:
        # 还原章节
        chapter.is_deleted = False
        chapter.deleted_at = None
        
        # 同时还原相关评论
        Comment.query.filter_by(chapter_id=chapter_id, is_deleted=True).update({
            'is_deleted': False,
            'deleted_at': None
        })
        
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"还原章节时出错: {str(e)}")
        return False

@staticmethod
def restore_comment(comment_id: int) -> bool:
    """从回收站还原评论"""
    comment = Comment.query.get(comment_id)
    if not comment or not comment.is_deleted:
        return False
    
    try:
        comment.is_deleted = False
        comment.deleted_at = None
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"还原评论时出错: {str(e)}")
        return False

@staticmethod
def permanently_delete_novel(novel_id: int) -> bool:
    """永久删除回收站中的小说（同时级联删除章节和评论）"""
    return AdminDAO.delete_novel_cascade(novel_id)

@staticmethod
def permanently_delete_chapter(chapter_id: int) -> bool:
    """永久删除回收站中的章节（同时删除关联评论）"""
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return False
    
    try:
        # 删除该章节下的所有评论
        Comment.query.filter_by(chapter_id=chapter_id).delete()
        
        # 删除章节
        db.session.delete(chapter)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"永久删除章节时出错: {str(e)}")
        return False

@staticmethod
def permanently_delete_comment(comment_id: int) -> bool:
    """永久删除回收站中的评论"""
    comment = Comment.query.get(comment_id)
    if not comment:
        return False
    
    try:
        db.session.delete(comment)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"永久删除评论时出错: {str(e)}")
        return False
```

### 3.2 Service层

需要在 `app/services/admin_service.py` 中添加以下方法：

```python
@staticmethod
def get_all_novels(page: int = 1, per_page: int = 20, title_filter: str = None) -> Dict:
    """获取所有小说，支持分页和标题筛选"""
    novels, total = AdminDAO.get_all_novels(page, per_page, title_filter)
    
    return {
        'novels': [novel.to_dict() for novel in novels],
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    }

@staticmethod
def get_all_chapters(novel_id: Optional[int] = None, page: int = 1, per_page: int = 20) -> Dict:
    """获取所有章节，支持按小说ID筛选"""
    chapters, total = AdminDAO.get_all_chapters(novel_id, page, per_page)
    
    chapters_with_novel = []
    for chapter in chapters:
        chapter_dict = chapter.to_dict()
        novel = Novel.query.get(chapter.novel_id)
        if novel:
            chapter_dict['novel_title'] = novel.title
        chapters_with_novel.append(chapter_dict)
    
    return {
        'chapters': chapters_with_novel,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    }

@staticmethod
def get_all_comments(novel_id: Optional[int] = None, chapter_id: Optional[int] = None, 
                     page: int = 1, per_page: int = 20) -> Dict:
    """获取所有评论，支持按小说ID或章节ID筛选"""
    comments, total = AdminDAO.get_all_comments(novel_id, chapter_id, page, per_page)
    
    comments_with_details = []
    for comment in comments:
        comment_dict = comment.to_dict()
        
        # 添加用户信息
        user = User.query.get(comment.user_id)
        if user:
            comment_dict['user'] = {
                'id': user.id,
                'username': user.username,
                'avatar': user.avatar
            }
        
        # 添加小说标题
        if comment.novel_id:
            novel = Novel.query.get(comment.novel_id)
            if novel:
                comment_dict['novel_title'] = novel.title
        
        # 添加章节标题
        if comment.chapter_id:
            chapter = Chapter.query.get(comment.chapter_id)
            if chapter:
                comment_dict['chapter_title'] = chapter.title
        
        comments_with_details.append(comment_dict)
    
    return {
        'comments': comments_with_details,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    }

@staticmethod
def delete_novel(admin_id: int, novel_id: int) -> Dict:
    """删除小说及其所有章节和评论"""
    # 验证管理员权限
    if not PermissionService.has_role(admin_id, 'admin'):
        return {
            'success': False,
            'message': '需要管理员权限'
        }
    
    # 检查小说是否存在
    novel = Novel.query.get(novel_id)
    if not novel:
        return {
            'success': False,
            'message': f'ID为{novel_id}的小说不存在'
        }
    
    # 获取小说标题用于响应消息
    novel_title = novel.title
    
    # 删除小说（级联删除章节和评论）
    result = AdminDAO.delete_novel_cascade(novel_id)
    
    if result:
        return {
            'success': True,
            'message': f'小说"{novel_title}"（ID: {novel_id}）及其所有章节和评论已成功删除'
        }
    else:
        return {
            'success': False,
            'message': f'删除ID为{novel_id}的小说失败'
        }

@staticmethod
def delete_chapter(admin_id: int, chapter_id: int) -> Dict:
    """删除章节及其评论"""
    # 验证管理员权限
    if not PermissionService.has_role(admin_id, 'admin'):
        return {
            'success': False,
            'message': '需要管理员权限'
        }
    
    # 检查章节是否存在
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return {
            'success': False,
            'message': f'ID为{chapter_id}的章节不存在'
        }
    
    # 获取章节详情用于响应消息
    chapter_title = chapter.title
    novel_id = chapter.novel_id
    
    # 删除章节
    try:
        # 删除与此章节关联的评论
        Comment.query.filter_by(chapter_id=chapter_id).delete()
        
        # 删除章节
        result = NovelDAO.delete_chapter(chapter_id)
        
        if result:
            return {
                'success': True,
                'message': f'章节"{chapter_title}"（ID: {chapter_id}）及其评论已成功删除'
            }
        else:
            return {
                'success': False,
                'message': f'删除ID为{chapter_id}的章节失败'
            }
    except Exception as e:
        db.session.rollback()
        return {
            'success': False,
            'message': f'删除章节时出错: {str(e)}'
        }

@staticmethod
def delete_comment(admin_id: int, comment_id: int) -> Dict:
    """删除评论"""
    # 验证管理员权限
    if not PermissionService.has_role(admin_id, 'admin'):
        return {
            'success': False,
            'message': '需要管理员权限'
        }
    
    # 检查评论是否存在
    comment = Comment.query.get(comment_id)
    if not comment:
        return {
            'success': False,
            'message': f'ID为{comment_id}的评论不存在'
        }
    
    # 删除评论
    result = InteractionDAO.delete_comment(comment_id)
    
    if result:
        return {
            'success': True,
            'message': f'ID为{comment_id}的评论已成功删除'
        }
    else:
        return {
            'success': False,
            'message': f'删除ID为{comment_id}的评论失败'
        }
```

### 3.3 API层

需要在 `app/api/admin.py` 中添加以下路由：

```python
# ====== 小说、章节、评论管理 ======

@admin_bp.route('/novels', methods=['GET'])
@admin_required
def get_all_novels():
    """
    获取所有小说（分页）
    
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
    
    result = AdminService.get_all_novels(page=page, per_page=per_page, title_filter=title_filter)
    
    return jsonify(result)

@admin_bp.route('/chapters', methods=['GET'])
@admin_required
def get_all_chapters():
    """
    获取所有章节（分页）
    
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
    
    result = AdminService.get_all_chapters(novel_id=novel_id, page=page, per_page=per_page)
    
    return jsonify(result)

@admin_bp.route('/comments', methods=['GET'])
@admin_required
def get_all_comments():
    """
    获取所有评论（分页）
    
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
    
    result = AdminService.get_all_comments(
        novel_id=novel_id, 
        chapter_id=chapter_id, 
        page=page, 
        per_page=per_page
    )
    
    return jsonify(result)

@admin_bp.route('/novels/<int:novel_id>', methods=['DELETE'])
@admin_required
def delete_novel(novel_id):
    """
    删除小说及其所有章节和评论
    """
    # 从认证中获取管理员用户ID
    admin_id = g.user.id
    
    result = AdminService.delete_novel(admin_id, novel_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

@admin_bp.route('/chapters/<int:chapter_id>', methods=['DELETE'])
@admin_required
def delete_chapter(chapter_id):
    """
    删除章节及其评论
    """
    # 从认证中获取管理员用户ID
    admin_id = g.user.id
    
    result = AdminService.delete_chapter(admin_id, chapter_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

@admin_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@admin_required
def delete_comment(comment_id):
    """
    删除评论
    """
    # 从认证中获取管理员用户ID
    admin_id = g.user.id
    
    result = AdminService.delete_comment(admin_id, comment_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

# ====== 回收站功能 ======

@admin_bp.route('/recycle-bin/novels', methods=['GET'])
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
@admin_required
def restore_novel(novel_id):
    """
    从回收站还原小说及其关联内容
    """
    # 从认证中获取管理员用户ID
    admin_id = g.user.id
    
    result = AdminService.restore_novel(admin_id, novel_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

@admin_bp.route('/recycle-bin/chapters/<int:chapter_id>/restore', methods=['POST'])
@admin_required
def restore_chapter(chapter_id):
    """
    从回收站还原章节及其关联评论
    """
    # 从认证中获取管理员用户ID
    admin_id = g.user.id
    
    result = AdminService.restore_chapter(admin_id, chapter_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

@admin_bp.route('/recycle-bin/comments/<int:comment_id>/restore', methods=['POST'])
@admin_required
def restore_comment(comment_id):
    """
    从回收站还原评论
    """
    # 从认证中获取管理员用户ID
    admin_id = g.user.id
    
    result = AdminService.restore_comment(admin_id, comment_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

@admin_bp.route('/recycle-bin/novels/<int:novel_id>/permanent', methods=['DELETE'])
@admin_required
def permanently_delete_novel(novel_id):
    """
    永久删除回收站中的小说
    """
    # 从认证中获取管理员用户ID
    admin_id = g.user.id
    
    result = AdminService.permanently_delete_novel(admin_id, novel_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

@admin_bp.route('/recycle-bin/chapters/<int:chapter_id>/permanent', methods=['DELETE'])
@admin_required
def permanently_delete_chapter(chapter_id):
    """
    永久删除回收站中的章节
    """
    # 从认证中获取管理员用户ID
    admin_id = g.user.id
    
    result = AdminService.permanently_delete_chapter(admin_id, chapter_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)

@admin_bp.route('/recycle-bin/comments/<int:comment_id>/permanent', methods=['DELETE'])
@admin_required
def permanently_delete_comment(comment_id):
    """
    永久删除回收站中的评论
    """
    # 从认证中获取管理员用户ID
    admin_id = g.user.id
    
    result = AdminService.permanently_delete_comment(admin_id, comment_id)
    
    if not result['success']:
        return jsonify({
            'error': result['message']
        }), 400
    
    return jsonify(result)
```

## 4. 前端实现

### 4.1 API服务

在前端添加以下API服务函数（`src/api/admin.js`）：

```javascript
// 获取所有小说
export function getAllNovels(params) {
  return request({
    url: '/admin/novels',
    method: 'get',
    params
  });
}

// 获取所有章节
export function getAllChapters(params) {
  return request({
    url: '/admin/chapters',
    method: 'get',
    params
  });
}

// 获取所有评论
export function getAllComments(params) {
  return request({
    url: '/admin/comments',
    method: 'get',
    params
  });
}

// 删除小说
export function deleteNovel(novelId) {
  return request({
    url: `/admin/novels/${novelId}`,
    method: 'delete'
  });
}

// 删除章节
export function deleteChapter(chapterId) {
  return request({
    url: `/admin/chapters/${chapterId}`,
    method: 'delete'
  });
}

// 删除评论
export function deleteComment(commentId) {
  return request({
    url: `/admin/comments/${commentId}`,
    method: 'delete'
  });
}
```

### 4.2 前端页面

#### 4.2.1 小说管理页面

创建 `src/views/admin/NovelManagement.vue` 页面，功能包括：

- 小说列表展示
- 分页功能
- 按标题筛选
- 删除小说功能
- 查看小说详情、章节和评论的跳转链接

#### 4.2.2 章节管理页面

创建 `src/views/admin/ChapterManagement.vue` 页面，功能包括：

- 章节列表展示
- 分页功能
- 按小说筛选
- 删除章节功能
- 查看所属小说的链接

#### 4.2.3 评论管理页面

创建 `src/views/admin/CommentManagement.vue` 页面，功能包括：

- 评论列表展示
- 分页功能
- 按小说和章节筛选
- 删除评论功能
- 查看所属小说和章节的链接

#### 4.2.4 小说详情页面

扩展 `src/views/admin/NovelDetail.vue` 页面，功能包括：

- 小说基本信息展示
- 章节列表标签页
- 评论列表标签页
- 对章节和评论的删除功能

## 5. 数据库修改

本功能依赖于现有的数据库结构，需确保以下外键关系正确设置：

1. 小说表（novel）的主键 id 作为章节表（chapter）的外键 novel_id
2. 小说表（novel）的主键 id 作为评论表（comments）的外键 novel_id
3. 章节表（chapter）的主键 id 作为评论表（comments）的外键 chapter_id

为保证级联删除，应修改外键约束如下：

```sql
-- 修改chapter表的外键约束
ALTER TABLE `chapter` DROP FOREIGN KEY `chapter_ibfk_1`;
ALTER TABLE `chapter` ADD CONSTRAINT `chapter_ibfk_1` 
FOREIGN KEY (`novel_id`) REFERENCES `novel` (`id`) ON DELETE CASCADE;

-- 修改comments表的外键约束
ALTER TABLE `comments` DROP FOREIGN KEY `comments_ibfk_2`;
ALTER TABLE `comments` ADD CONSTRAINT `comments_ibfk_2` 
FOREIGN KEY (`novel_id`) REFERENCES `novel` (`id`) ON DELETE CASCADE;

ALTER TABLE `comments` DROP FOREIGN KEY `comments_ibfk_3`;
ALTER TABLE `comments` ADD CONSTRAINT `comments_ibfk_3` 
FOREIGN KEY (`chapter_id`) REFERENCES `chapter` (`id`) ON DELETE CASCADE;
```

## 6. 测试计划

### 6.1 单元测试

1. DAO层方法测试
   - 测试获取小说、章节、评论的分页和筛选功能
   - 测试删除操作和级联删除

2. Service层方法测试
   - 测试权限验证逻辑
   - 测试数据转换和格式化

3. API层路由测试
   - 测试API响应格式
   - 测试参数验证

### 6.2 集成测试

1. 测试小说删除后，相关章节和评论都被正确删除
2. 测试章节删除后，相关评论都被正确删除
3. 测试删除评论不影响相关小说和章节

### 6.3 前端测试

1. 列表页面的分页和筛选功能
2. 删除操作确认和反馈
3. 不同设备上的响应式布局测试

## 7. 部署注意事项

1. 数据库迁移：执行上述SQL语句修改外键约束
2. 权限配置：确保admin_required装饰器正确实现
3. 前端路由：在前端路由配置中添加新页面

## 8. 后续优化计划

1. 添加批量删除功能
2. 添加内容审核和自动过滤功能
3. 添加操作日志，记录管理员的删除行为
4. 添加内容恢复（从回收站还原）功能

## 9. 内容恢复（回收站）功能实现

### 9.1 功能概述

回收站功能将改变当前的删除机制，使被删除的内容（小说、章节、评论）先移至回收站，而不是直接永久删除。管理员可以查看回收站中的内容，并选择还原或永久删除。主要功能包括：

- 查看回收站中的所有小说、章节和评论
- 支持筛选和分页功能
- 还原被删除的小说（同时还原其关联的章节和评论）
- 还原被删除的章节（同时还原其关联的评论）
- 还原单条被删除的评论
- 永久删除回收站中的内容

### 9.2 数据库修改

为实现回收站功能，需要对现有数据表进行以下修改：

1. 在现有的 `novel`、`chapter` 和 `comments` 表中添加 `is_deleted` 和 `deleted_at` 字段：

```sql
-- 修改novel表
ALTER TABLE `novel` ADD COLUMN `is_deleted` TINYINT(1) NOT NULL DEFAULT 0;
ALTER TABLE `novel` ADD COLUMN `deleted_at` DATETIME NULL;

-- 修改chapter表
ALTER TABLE `chapter` ADD COLUMN `is_deleted` TINYINT(1) NOT NULL DEFAULT 0;
ALTER TABLE `chapter` ADD COLUMN `deleted_at` DATETIME NULL;

-- 修改comments表
ALTER TABLE `comments` ADD COLUMN `is_deleted` TINYINT(1) NOT NULL DEFAULT 0;
ALTER TABLE `comments` ADD COLUMN `deleted_at` DATETIME NULL;
```

### 9.3 后端实现计划

#### 9.3.1 DAO层修改

修改现有的删除方法，使其变为"软删除"；添加新的方法用于回收站管理和内容恢复。

#### 9.3.2 Service层修改

在 `app/services/admin_service.py` 中修改现有删除方法，并添加以下新方法：

```python
@staticmethod
def delete_novel(admin_id: int, novel_id: int) -> Dict:
    """软删除小说（移至回收站）"""
    # 验证管理员权限
    if not PermissionService.has_role(admin_id, 'admin'):
        return {
            'success': False,
            'message': '需要管理员权限'
        }
    
    # 检查小说是否存在
    novel = Novel.query.get(novel_id)
    if not novel:
        return {
            'success': False,
            'message': f'ID为{novel_id}的小说不存在'
        }
    
    # 获取小说标题用于响应消息
    novel_title = novel.title
    
    # 软删除小说（移至回收站）
    result = AdminDAO.soft_delete_novel(novel_id)
    
    if result:
        return {
            'success': True,
            'message': f'小说"{novel_title}"（ID: {novel_id}）已移至回收站'
        }
    else:
        return {
            'success': False,
            'message': f'移动ID为{novel_id}的小说至回收站失败'
        }

@staticmethod
def delete_chapter(admin_id: int, chapter_id: int) -> Dict:
    """软删除章节（移至回收站）"""
    # 验证管理员权限
    if not PermissionService.has_role(admin_id, 'admin'):
        return {
            'success': False,
            'message': '需要管理员权限'
        }
    
    # 检查章节是否存在
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return {
            'success': False,
            'message': f'ID为{chapter_id}的章节不存在'
        }
    
    # 获取章节详情用于响应消息
    chapter_title = chapter.title
    
    # 软删除章节（移至回收站）
    result = AdminDAO.soft_delete_chapter(chapter_id)
    
    if result:
        return {
            'success': True,
            'message': f'章节"{chapter_title}"（ID: {chapter_id}）已移至回收站'
        }
    else:
        return {
            'success': False,
            'message': f'移动ID为{chapter_id}的章节至回收站失败'
        }

@staticmethod
def delete_comment(admin_id: int, comment_id: int) -> Dict:
    """软删除评论（移至回收站）"""
    # 验证管理员权限
    if not PermissionService.has_role(admin_id, 'admin'):
        return {
            'success': False,
            'message': '需要管理员权限'
        }
    
    # 检查评论是否存在
    comment = Comment.query.get(comment_id)
    if not comment:
        return {
            'success': False,
            'message': f'ID为{comment_id}的评论不存在'
        }
    
    # 软删除评论（移至回收站）
    result = AdminDAO.soft_delete_comment(comment_id)
    
    if result:
        return {
            'success': True,
            'message': f'ID为{comment_id}的评论已移至回收站'
        }
    else:
        return {
            'success': False,
            'message': f'移动ID为{comment_id}的评论至回收站失败'
        }

@staticmethod
def get_recycled_novels(page: int = 1, per_page: int = 20, title_filter: str = None) -> Dict:
    """获取回收站中的小说"""
    novels, total = AdminDAO.get_deleted_novels(page, per_page, title_filter)
    
    return {
        'novels': [novel.to_dict() for novel in novels],
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    }

@staticmethod
def get_recycled_chapters(novel_id: Optional[int] = None, page: int = 1, per_page: int = 20) -> Dict:
    """获取回收站中的章节"""
    chapters, total = AdminDAO.get_deleted_chapters(novel_id, page, per_page)
    
    chapters_with_novel = []
    for chapter in chapters:
        chapter_dict = chapter.to_dict()
        novel = Novel.query.get(chapter.novel_id)
        if novel:
            chapter_dict['novel_title'] = novel.title
        chapters_with_novel.append(chapter_dict)
    
    return {
        'chapters': chapters_with_novel,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    }

@staticmethod
def get_recycled_comments(novel_id: Optional[int] = None, chapter_id: Optional[int] = None, 
                        page: int = 1, per_page: int = 20) -> Dict:
    """获取回收站中的评论"""
    comments, total = AdminDAO.get_deleted_comments(novel_id, chapter_id, page, per_page)
    
    comments_with_details = []
    for comment in comments:
        comment_dict = comment.to_dict()
        
        # 添加用户信息
        user = User.query.get(comment.user_id)
        if user:
            comment_dict['user'] = {
                'id': user.id,
                'username': user.username,
                'avatar': user.avatar
            }
        
        # 添加小说标题
        if comment.novel_id:
            novel = Novel.query.get(comment.novel_id)
            if novel:
                comment_dict['novel_title'] = novel.title
        
        # 添加章节标题
        if comment.chapter_id:
            chapter = Chapter.query.get(comment.chapter_id)
            if chapter:
                comment_dict['chapter_title'] = chapter.title
        
        comments_with_details.append(comment_dict)
    
    return {
        'comments': comments_with_details,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    }

@staticmethod
def restore_novel(admin_id: int, novel_id: int) -> Dict:
    """从回收站还原小说"""
    # 验证管理员权限
    if not PermissionService.has_role(admin_id, 'admin'):
        return {
            'success': False,
            'message': '需要管理员权限'
        }
    
    # 检查小说是否存在于回收站
    novel = Novel.query.get(novel_id)
    if not novel:
        return {
            'success': False,
            'message': f'ID为{novel_id}的小说不存在'
        }
    
    if not novel.is_deleted:
        return {
            'success': False,
            'message': f'ID为{novel_id}的小说不在回收站中'
        }
    
    # 获取小说标题用于响应消息
    novel_title = novel.title
    
    # 还原小说
    result = AdminDAO.restore_novel(novel_id)
    
    if result:
        return {
            'success': True,
            'message': f'小说"{novel_title}"（ID: {novel_id}）已从回收站还原'
        }
    else:
        return {
            'success': False,
            'message': f'还原ID为{novel_id}的小说失败'
        }

@staticmethod
def restore_chapter(admin_id: int, chapter_id: int) -> Dict:
    """从回收站还原章节"""
    # 验证管理员权限
    if not PermissionService.has_role(admin_id, 'admin'):
        return {
            'success': False,
            'message': '需要管理员权限'
        }
    
    # 检查章节是否存在于回收站
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return {
            'success': False,
            'message': f'ID为{chapter_id}的章节不存在'
        }
    
    if not chapter.is_deleted:
        return {
            'success': False,
            'message': f'ID为{chapter_id}的章节不在回收站中'
        }
    
    # 获取章节标题用于响应消息
    chapter_title = chapter.title
    
    # 还原章节
    result = AdminDAO.restore_chapter(chapter_id)
    
    if result:
        return {
            'success': True,
            'message': f'章节"{chapter_title}"（ID: {chapter_id}）已从回收站还原'
        }
    else:
        return {
            'success': False,
            'message': f'还原ID为{chapter_id}的章节失败'
        }

@staticmethod
def restore_comment(admin_id: int, comment_id: int) -> Dict:
    """从回收站还原评论"""
    # 验证管理员权限
    if not PermissionService.has_role(admin_id, 'admin'):
        return {
            'success': False,
            'message': '需要管理员权限'
        }
    
    # 检查评论是否存在于回收站
    comment = Comment.query.get(comment_id)
    if not comment:
        return {
            'success': False,
            'message': f'ID为{comment_id}的评论不存在'
        }
    
    if not comment.is_deleted:
        return {
            'success': False,
            'message': f'ID为{comment_id}的评论不在回收站中'
        }
    
    # 还原评论
    result = AdminDAO.restore_comment(comment_id)
    
    if result:
        return {
            'success': True,
            'message': f'ID为{comment_id}的评论已从回收站还原'
        }
    else:
        return {
            'success': False,
            'message': f'还原ID为{comment_id}的评论失败'
        }

@staticmethod
def permanently_delete_novel(admin_id: int, novel_id: int) -> Dict:
    """永久删除回收站中的小说"""
    # 验证管理员权限
    if not PermissionService.has_role(admin_id, 'admin'):
        return {
            'success': False,
            'message': '需要管理员权限'
        }
    
    # 检查小说是否存在于回收站
    novel = Novel.query.get(novel_id)
    if not novel:
        return {
            'success': False,
            'message': f'ID为{novel_id}的小说不存在'
        }
    
    if not novel.is_deleted:
        return {
            'success': False,
            'message': f'ID为{novel_id}的小说不在回收站中'
        }
    
    # 获取小说标题用于响应消息
    novel_title = novel.title
    
    # 永久删除小说
    result = AdminDAO.permanently_delete_novel(novel_id)
    
    if result:
        return {
            'success': True,
            'message': f'小说"{novel_title}"（ID: {novel_id}）已永久删除'
        }
    else:
        return {
            'success': False,
            'message': f'永久删除ID为{novel_id}的小说失败'
        }

@staticmethod
def permanently_delete_chapter(admin_id: int, chapter_id: int) -> Dict:
    """永久删除回收站中的章节"""
    # 验证管理员权限
    if not PermissionService.has_role(admin_id, 'admin'):
        return {
            'success': False,
            'message': '需要管理员权限'
        }
    
    # 检查章节是否存在于回收站
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return {
            'success': False,
            'message': f'ID为{chapter_id}的章节不存在'
        }
    
    if not chapter.is_deleted:
        return {
            'success': False,
            'message': f'ID为{chapter_id}的章节不在回收站中'
        }
    
    # 获取章节标题用于响应消息
    chapter_title = chapter.title
    
    # 永久删除章节
    result = AdminDAO.permanently_delete_chapter(chapter_id)
    
    if result:
        return {
            'success': True,
            'message': f'章节"{chapter_title}"（ID: {chapter_id}）已永久删除'
        }
    else:
        return {
            'success': False,
            'message': f'永久删除ID为{chapter_id}的章节失败'
        }

@staticmethod
def permanently_delete_comment(admin_id: int, comment_id: int) -> Dict:
    """永久删除回收站中的评论"""
    # 验证管理员权限
    if not PermissionService.has_role(admin_id, 'admin'):
        return {
            'success': False,
            'message': '需要管理员权限'
        }
    
    # 检查评论是否存在于回收站
    comment = Comment.query.get(comment_id)
    if not comment:
        return {
            'success': False,
            'message': f'ID为{comment_id}的评论不存在'
        }
    
    if not comment.is_deleted:
        return {
            'success': False,
            'message': f'ID为{comment_id}的评论不在回收站中'
        }
    
    # 永久删除评论
    result = AdminDAO.permanently_delete_comment(comment_id)
    
    if result:
        return {
            'success': True,
            'message': f'ID为{comment_id}的评论已永久删除'
        }
    else:
        return {
            'success': False,
            'message': f'永久删除ID为{comment_id}的评论失败'
        }
```

#### 9.3.3 API层修改

## 9.4 前端实现

### 9.4.1 API服务

在 `src/api/admin.js` 中添加以下API服务函数：

```javascript
// 获取回收站中的小说
export function getRecycledNovels(params) {
  return request({
    url: '/admin/recycle-bin/novels',
    method: 'get',
    params
  });
}

// 获取回收站中的章节
export function getRecycledChapters(params) {
  return request({
    url: '/admin/recycle-bin/chapters',
    method: 'get',
    params
  });
}

// 获取回收站中的评论
export function getRecycledComments(params) {
  return request({
    url: '/admin/recycle-bin/comments',
    method: 'get',
    params
  });
}

// 还原小说
export function restoreNovel(novelId) {
  return request({
    url: `/admin/recycle-bin/novels/${novelId}/restore`,
    method: 'post'
  });
}

// 还原章节
export function restoreChapter(chapterId) {
  return request({
    url: `/admin/recycle-bin/chapters/${chapterId}/restore`,
    method: 'post'
  });
}

// 还原评论
export function restoreComment(commentId) {
  return request({
    url: `/admin/recycle-bin/comments/${commentId}/restore`,
    method: 'post'
  });
}

// 永久删除回收站中的小说
export function permanentlyDeleteNovel(novelId) {
  return request({
    url: `/admin/recycle-bin/novels/${novelId}/permanent`,
    method: 'delete'
  });
}

// 永久删除回收站中的章节
export function permanentlyDeleteChapter(chapterId) {
  return request({
    url: `/admin/recycle-bin/chapters/${chapterId}/permanent`,
    method: 'delete'
  });
}

// 永久删除回收站中的评论
export function permanentlyDeleteComment(commentId) {
  return request({
    url: `/admin/recycle-bin/comments/${commentId}/permanent`,
    method: 'delete'
  });
}
```

### 9.4.2 回收站页面组件

#### 9.4.2.1 回收站主页面

创建 `src/views/admin/RecycleBin.vue` 页面：

```vue
<template>
  <div class="recycle-bin-container">
    <h1>内容回收站</h1>
    
    <el-tabs v-model="activeTab" @tab-click="handleTabClick">
      <el-tab-pane label="小说" name="novels">
        <novels-table v-if="activeTab === 'novels'" />
      </el-tab-pane>
      <el-tab-pane label="章节" name="chapters">
        <chapters-table v-if="activeTab === 'chapters'" />
      </el-tab-pane>
      <el-tab-pane label="评论" name="comments">
        <comments-table v-if="activeTab === 'comments'" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import NovelsTable from './recycle-bin/NovelsTable.vue';
import ChaptersTable from './recycle-bin/ChaptersTable.vue';
import CommentsTable from './recycle-bin/CommentsTable.vue';

export default {
  name: 'RecycleBin',
  components: {
    NovelsTable,
    ChaptersTable,
    CommentsTable
  },
  data() {
    return {
      activeTab: 'novels'
    };
  },
  methods: {
    handleTabClick() {
      // 在tab切换时重置分页等状态
    }
  }
};
</script>

<style scoped>
.recycle-bin-container {
  padding: 20px;
}
</style>
```

#### 9.4.2.2 回收站小说表格组件

创建 `src/views/admin/recycle-bin/NovelsTable.vue` 组件：

```vue
<template>
  <div class="novels-table">
    <div class="table-header">
      <el-input
        v-model="searchTitle"
        placeholder="搜索小说标题"
        style="width: 300px"
        clearable
        @keyup.enter.native="handleSearch"
        @clear="handleSearch"
      >
        <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
      </el-input>
    </div>
    
    <el-table
      v-loading="loading"
      :data="novels"
      border
      style="width: 100%"
    >
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="title" label="标题" min-width="200"></el-table-column>
      <el-table-column prop="author_name" label="作者" width="150"></el-table-column>
      <el-table-column prop="deleted_at" label="删除时间" width="180">
        <template slot-scope="scope">
          {{ formatDate(scope.row.deleted_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="success"
            @click="handleRestore(scope.row)"
          >还原</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="handlePermanentDelete(scope.row)"
          >永久删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <div class="pagination-container">
      <el-pagination
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page.sync="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      ></el-pagination>
    </div>
  </div>
</template>

<script>
import { getRecycledNovels, restoreNovel, permanentlyDeleteNovel } from '@/api/admin';
import { formatDate } from '@/utils/date';

export default {
  name: 'NovelsTable',
  data() {
    return {
      loading: false,
      novels: [],
      total: 0,
      currentPage: 1,
      pageSize: 20,
      searchTitle: ''
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    formatDate,
    fetchData() {
      this.loading = true;
      
      getRecycledNovels({
        page: this.currentPage,
        per_page: this.pageSize,
        title: this.searchTitle || undefined
      }).then(response => {
        this.novels = response.data.novels;
        this.total = response.data.total;
        this.loading = false;
      }).catch(error => {
        console.error('获取回收站小说失败:', error);
        this.$message.error('获取回收站小说失败');
        this.loading = false;
      });
    },
    handleSearch() {
      this.currentPage = 1;
      this.fetchData();
    },
    handleSizeChange(val) {
      this.pageSize = val;
      this.fetchData();
    },
    handleCurrentChange(val) {
      this.currentPage = val;
      this.fetchData();
    },
    handleRestore(row) {
      this.$confirm(`确定要还原小说"${row.title}"吗？此操作将同时还原该小说的所有章节和评论。`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        restoreNovel(row.id).then(response => {
          this.$message.success(response.data.message || '小说已成功还原');
          this.fetchData();
        }).catch(error => {
          console.error('还原小说失败:', error);
          this.$message.error(error.response?.data?.error || '还原小说失败');
        });
      }).catch(() => {
        // 取消操作
      });
    },
    handlePermanentDelete(row) {
      this.$confirm(`确定要永久删除小说"${row.title}"吗？此操作不可恢复。`, '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'danger'
      }).then(() => {
        permanentlyDeleteNovel(row.id).then(response => {
          this.$message.success(response.data.message || '小说已永久删除');
          this.fetchData();
        }).catch(error => {
          console.error('永久删除小说失败:', error);
          this.$message.error(error.response?.data?.error || '永久删除小说失败');
        });
      }).catch(() => {
        // 取消操作
      });
    }
  }
};
</script>

<style scoped>
.novels-table {
  margin-top: 20px;
}
.table-header {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
}
.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style>
```

#### 9.4.2.3 回收站章节表格组件

创建 `src/views/admin/recycle-bin/ChaptersTable.vue` 组件，类似于小说表格组件，但针对章节数据。

#### 9.4.2.4 回收站评论表格组件

创建 `src/views/admin/recycle-bin/CommentsTable.vue` 组件，类似于小说表格组件，但针对评论数据。

### 9.4.3 路由配置

在 `src/router/index.js` 中添加回收站页面路由：

```javascript
// 管理员路由
{
  path: '/admin',
  component: Layout,
  redirect: '/admin/dashboard',
  meta: { title: '管理后台', icon: 'dashboard', roles: ['admin'] },
  children: [
    // ... 现有路由 ...
    {
      path: 'recycle-bin',
      name: 'RecycleBin',
      component: () => import('@/views/admin/RecycleBin'),
      meta: { title: '内容回收站', icon: 'delete', roles: ['admin'] }
    }
  ]
}
```

### 9.4.4 修改现有页面

#### 9.4.4.1 修改现有删除操作的提示

在小说、章节和评论管理页面中，修改删除操作的确认文本，说明删除操作会将内容移至回收站而不是直接删除。例如：

```javascript
// 原来的删除确认提示
this.$confirm('确定要删除这部小说吗？此操作将同时删除相关联的章节和评论。', '警告', {...})

// 修改后的删除确认提示
this.$confirm('确定要将这部小说移至回收站吗？此操作将同时移除相关联的章节和评论。', '提示', {...})
```

## 9.5 测试计划

### 9.5.1 单元测试

1. DAO层测试
   - 测试软删除功能（验证is_deleted字段和deleted_at字段正确设置）
   - 测试获取已删除内容的方法
   - 测试还原功能
   - 测试永久删除功能

2. Service层测试
   - 测试权限验证逻辑
   - 测试软删除、还原和永久删除的业务逻辑
   - 测试获取回收站内容的数据格式

3. API层测试
   - 测试API的响应格式
   - 测试参数验证

### 9.5.2 集成测试

1. 测试小说软删除后，相关章节和评论是否也被正确标记为已删除
2. 测试小说还原后，相关章节和评论是否也被正确还原
3. 测试章节软删除后，相关评论是否也被正确标记为已删除
4. 测试章节还原后，相关评论是否也被正确还原
5. 测试永久删除小说、章节和评论的级联关系

### 9.5.3 前端测试

1. 回收站页面的分页和筛选功能
2. 还原和永久删除操作的确认和反馈
3. 不同设备上的响应式布局测试

## 9.6 部署注意事项

1. 数据库迁移：
   - 执行SQL语句添加is_deleted和deleted_at字段
   - 将现有的小说、章节和评论的is_deleted字段设置为false

2. 代码修改：
   - 修改现有的删除逻辑为软删除
   - 在查询列表数据时添加is_deleted=False条件，确保已删除内容不在正常列表中显示

3. 前端路由配置：
   - 在管理员菜单中添加回收站入口

## 9.7 实现总结

通过实现回收站功能，我们改进了平台的内容管理系统，提供了更安全的删除机制和内容恢复能力。这一功能的主要优势包括：

1. **数据安全性提升**：内容不会被直接永久删除，减少了误操作导致的数据丢失风险
2. **内容恢复能力**：允许管理员轻松还原被删除的内容，改善用户体验和平台管理能力
3. **更完善的管理流程**：提供了两步删除流程（软删除到回收站，然后永久删除），使内容管理更加可控
4. **级联恢复功能**：支持小说、章节及评论的级联恢复，保持数据完整性

## 9.8 实施路线图

为了确保回收站功能的顺利实施，我们将按照以下步骤进行开发：

### 阶段一：数据库准备（预计耗时：1天）

1. 创建数据库迁移脚本，为 novel、chapter 和 comments 表添加 is_deleted 和 deleted_at 字段
2. 执行迁移脚本，并确保现有数据的 is_deleted 字段默认值为 false

### 阶段二：后端功能开发（预计耗时：3天）

1. 实现 DAO 层方法：
   - 修改现有删除方法为软删除
   - 添加回收站查询和恢复方法
   - 实现永久删除方法

2. 实现 Service 层方法：
   - 封装软删除业务逻辑
   - 实现回收站数据查询和格式化
   - 封装恢复和永久删除业务逻辑

3. 实现 API 层接口：
   - 添加回收站相关路由
   - 实现相关接口的请求处理逻辑

### 阶段三：前端功能开发（预计耗时：3天）

1. 扩展 API 服务层，添加回收站相关方法
2. 开发回收站主页面和子组件：
   - 创建回收站主页面
   - 实现小说、章节和评论的回收站表格组件
3. 更新路由配置，添加回收站页面路由
4. 修改现有页面，更新删除操作的提示文本

### 阶段四：测试与部署（预计耗时：2天）

1. 单元测试：测试 DAO、Service 和 API 层方法
2. 集成测试：测试软删除、还原和永久删除的完整流程
3. 前端测试：测试页面功能和用户交互
4. 部署准备：
   - 编写部署文档
   - 准备数据库迁移脚本
   - 更新项目文档

### 总计预估时间：9天