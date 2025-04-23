# 搜索模块API一致性修复方案

## 背景

我们对现有的搜索模块API文档与实际后端实现进行了对比分析，发现存在一些不一致的地方。本文档旨在详细说明这些差异并提供相应的修复建议，以确保API文档与实际实现保持一致。

## 发现的差异

### 1. 小说搜索 (`/api/search/novels`)

- **一致性状态**: 大部分一致
- **问题**: 无重大问题

### 2. 标签搜索

- **文档路径**: `/api/search/novels/tag/{tag}`
- **实际路径**: `/api/search/by-tag?tag={tag}`
- **差异描述**:
  - 路径不一致: 文档使用路径参数，实际实现使用查询参数
  - API路径名称不同

### 3. 相似小说推荐 (`/api/search/similar/{novel_id}`)

- **路径一致性**: 路径一致
- **参数一致性**: 参数一致
- **差异**:
  - 返回结构: 文档中返回 `{"similar_novels": [...]}`, 而实际实现返回 `{"results": [...]}`
  - 实现逻辑: 文档描述基于标签相似度推荐，实际实现仅基于相同类别

### 4. 获取热门标签 (`/api/search/tags/hot`)

- **状态**: 未实现
- **替代功能**: 系统中有 `/api/novel/tags` 接口可获取所有标签，但没有按热门程度排序

## 修复建议

### 1. 标签搜索接口修复

#### 方案1: 调整实现以符合文档（推荐）

```python
# 在 backend/app/api/search.py 中修改

# 将这个路由
@search_bp.route('/by-tag', methods=['GET'])
def search_by_tag():
    # 现有实现...

# 修改为
@search_bp.route('/novels/tag/<string:tag>', methods=['GET'])
def search_by_tag(tag):
    """
    Search novels by tag
    
    GET params:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    """
    try:
        # 不再从查询参数获取tag
        # tag = request.args.get('tag', '')
        if not tag:
            return error_response('Tag parameter is required', 400)
        
        # 其余代码不变...
        # Parse numeric parameters
        try:
            page = int(request.args.get('page', 1))
            per_page = min(int(request.args.get('per_page', 20)), 50)  # Limit max per_page
        except ValueError:
            return error_response('Invalid pagination parameters', 400)
        
        # Call service to search by tag
        result = SearchService.search_by_tag(
            tag=tag,
            page=page,
            per_page=per_page
        )
        
        # 其余代码不变...
    except Exception as e:
        return error_response(str(e), 500)
```

#### 方案2: 更新文档以匹配实现

如果选择不修改代码，应更新API文档，将路径从 `/api/search/novels/tag/{tag}` 更改为 `/api/search/by-tag?tag={tag}`。

### 2. 相似小说推荐修复

#### 返回结构修复

```python
# 在 backend/app/api/search.py 中修改

@search_bp.route('/similar/<int:novel_id>', methods=['GET'])
def get_similar_novels(novel_id):
    try:
        # 获取参数部分不变...
        
        # 修改返回结构，从 results 改为 similar_novels
        # 原来的代码:
        # return success_response({'results': result['results']})
        
        # 修改后:
        return success_response({'similar_novels': result['results']})
    except Exception as e:
        return error_response(str(e), 500)
```

#### 实现逻辑增强

```python
# 在 backend/app/services/search_service.py 中修改 SearchDAO.get_similar_novels_query 方法

@staticmethod
def get_similar_novels_query(novel: Novel, limit: int = 5):
    """
    创建查询以找到相似小说，基于标签相似度和分类
    
    Args:
        novel: 用于寻找相似小说的小说
        limit: 返回的最大相似小说数量
            
    Returns:
        SQLAlchemy查询对象
    """
    # 获取小说标签
    novel_tags = novel.tags.all()
    
    if novel_tags:
        # 如果小说有标签，找到具有相同标签的小说
        similar_novels = Novel.query.filter(
            Novel.id != novel.id,  # 排除当前小说
            Novel.tags.any(Tag.id.in_([tag.id for tag in novel_tags]))  # 具有至少一个相同标签
        ).order_by(
            func.count(novel_tag.c.tag_id).desc()  # 按共同标签数量排序
        ).limit(limit)
        
        # 如果找不到足够的相似小说，回退到相同类别
        if similar_novels.count() < limit:
            # 这里实现回退逻辑，先获取标签相似的，再补充同类别热门的
            pass
        
        return similar_novels
    else:
        # 小说没有标签，回退到相同类别热门小说
        return Novel.query.filter(
            and_(
                Novel.category == novel.category,
                Novel.id != novel.id
            )
        ).order_by(
            Novel.view_count.desc()  # 按流行度排序
        ).limit(limit)
```

### 3. 热门标签API实现

```python
# 在 backend/app/api/search.py 中添加新路由

@search_bp.route('/tags/hot', methods=['GET'])
def get_hot_tags():
    """
    获取热门标签
    
    GET params:
    - limit: 返回数量 (默认: 20)
    - category_id: 分类ID (可选，若提供则只返回该分类下的标签)
    """
    try:
        # 获取参数
        limit = min(int(request.args.get('limit', 20)), 100)  # 限制最大返回数量
        category_id = request.args.get('category_id')
        
        # 转换category_id为整数（如果提供）
        if category_id:
            try:
                category_id = int(category_id)
            except ValueError:
                return error_response('Invalid category_id parameter', 400)
        
        # 调用服务获取热门标签
        result = SearchService.get_hot_tags(limit=limit, category_id=category_id)
        
        # 处理错误响应
        if not result['success']:
            return error_response(result['error'], 400)
        
        # 返回成功响应
        return success_response({'tags': result['tags']})
    except Exception as e:
        return error_response(str(e), 500)
```

```python
# 在 backend/app/services/search_service.py 中添加新方法

@staticmethod
def get_hot_tags(limit: int = 20, category_id: Optional[int] = None) -> Dict[str, Any]:
    """
    获取热门标签（按使用频率排序）
    
    Args:
        limit: 返回标签数量
        category_id: 分类ID (可选)
        
    Returns:
        包含热门标签的结果字典
    """
    try:
        # 基础查询 - 使用SQL函数统计标签使用次数
        query = db.session.query(
            Tag,
            func.count(novel_tag.c.novel_id).label('novel_count')
        ).outerjoin(
            novel_tag,
            Tag.id == novel_tag.c.tag_id
        )
        
        # 如果提供了分类ID，则过滤特定分类的标签
        if category_id:
            query = query.filter(Tag.category_id == category_id)
        
        # 分组、排序并限制结果数量
        query = query.group_by(Tag.id).order_by(db.desc('novel_count')).limit(limit)
        
        # 执行查询
        result = query.all()
        
        # 格式化结果
        tags = []
        for tag, novel_count in result:
            tag_dict = tag.to_dict()
            tag_dict['novel_count'] = novel_count
            
            # 添加分类名称（如果有分类）
            if tag.category:
                tag_dict['category_name'] = tag.category.name
            else:
                tag_dict['category_name'] = None
                
            tags.append(tag_dict)
        
        return {
            'success': True,
            'tags': tags
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
```

## 实施建议

按照如下优先级实施修复：

1. **首要**: 热门标签API实现 - 目前完全缺失的功能
2. **次要**: 标签搜索接口修复 - 影响API使用一致性
3. **可选**: 相似小说推荐修复 - 功能基本可用，但可改进

## 测试计划

对于每项修改，建议进行以下测试：

1. 单元测试:
   - 为每个新增或修改的API端点编写单元测试
   - 测试边界条件和错误情况

2. 集成测试:
   - 测试前端应用是否能正确调用修改后的API
   - 验证返回数据格式是否符合预期

## 总结

通过实施上述建议，可以使搜索模块的API文档与实际实现保持一致，并完善现有功能。这将提高API的可用性和开发体验，同时确保系统功能的完整性。 