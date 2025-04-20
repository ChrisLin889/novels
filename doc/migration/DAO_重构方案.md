# DAO层重构执行计划

## 背景

当前项目中存在架构不一致问题：部分DAO（数据访问对象）类定义在services目录，另一部分定义在dao目录。
本方案旨在将所有DAO类统一迁移到dao目录，提高架构一致性和代码可维护性。

## 当前状况

**services目录中的DAO类:**
- NovelDAO (novel_service.py) ✅ 已完成迁移
- InteractionDAO (interaction_service.py) ✅ 已完成迁移
- UserDAO (user_service.py) ✅ 已完成迁移
- SearchDAO (search_service.py)

**dao目录中的DAO类:**
- AdminDAO (admin_dao.py)
- SearchDAO (search_dao.py) - 注意：与services中的SearchDAO同名

## 迁移执行顺序

按以下顺序执行迁移工作：

1. NovelDAO (低风险) ✅ 已完成
2. InteractionDAO (中等风险) ✅ 已完成
3. UserDAO (中等风险) ✅ 已完成
4. SearchDAO (高风险，存在冲突)

## 详细迁移步骤

### 1. NovelDAO 迁移

- [x] **准备工作**
  - [x] 分析 novel_service.py 中 NovelDAO 的依赖和引用情况
  - [x] 确认 NovelDAO 依赖的模型类：Novel, Chapter, novel_tag

- [x] **代码迁移**
  - [x] 创建新文件：`backend/app/dao/novel_dao.py`
  - [x] 将 NovelDAO 类完整复制到新文件
  - [x] 添加所有必要的导入语句

- [x] **更新引用**
  - [x] 在 novel_service.py 中更新导入路径
  - [x] 检查并更新其他可能引用 NovelDAO 的文件

- [x] **测试验证**
  - [x] 运行单元测试（如有）
  - [x] 手动验证关键功能
  - [x] 确认数据操作正常

### 2. InteractionDAO 迁移

- [x] **准备工作**
  - [x] 分析 interaction_service.py 中 InteractionDAO 的依赖和引用情况
  - [x] 确认依赖的模型类：UserCollection, UserHistory, Comment, UserFollowing, PrivateMessage, UserTip
  - [x] 检查 novel_service.py 中对 InteractionDAO 的引用（update_reading_history方法）

- [x] **代码迁移**
  - [x] 创建新文件：`backend/app/dao/interaction_dao.py`
  - [x] 将 InteractionDAO 类完整复制到新文件
  - [x] 添加所有必要的导入语句

- [x] **更新引用**
  - [x] 在 interaction_service.py 中更新导入路径
  - [x] 在 novel_service.py 中更新导入路径
  - [x] 检查并更新其他可能引用 InteractionDAO 的文件

- [x] **测试验证**
  - [x] 确认所有方法都正确迁移，无遗漏
  - [x] 确认所有调用点都已正确更新导入路径
  - [x] 确认无循环导入问题

### 3. UserDAO 迁移

- [x] **准备工作**
  - [x] 分析 user_service.py 中 UserDAO 的依赖和引用情况
  - [x] 确认 UserDAO 依赖的模型类：User 及其他工具类
  - [x] 检查是否有其他服务直接引用 UserDAO

- [x] **代码迁移**
  - [x] 创建新文件：`backend/app/dao/user_dao.py`
  - [x] 将 UserDAO 类完整复制到新文件
  - [x] 添加所有必要的导入语句

- [x] **更新引用**
  - [x] 在 user_service.py 中更新导入路径
  - [x] 检查并更新其他可能引用 UserDAO 的文件

- [x] **测试验证**
  - [x] 运行单元测试（如有）
  - [x] 手动验证用户相关功能（登录、注册等）
  - [x] 确认数据操作正常

### 4. SearchDAO 冲突处理

- [ ] **准备工作**
  - [ ] 详细比较 dao/search_dao.py 和 services/search_service.py 中的 SearchDAO 类
  - [ ] 分析两个类的功能是否重叠或互补
  - [ ] 制定合并策略

- [ ] **解决方案选择**
  - 根据分析结果，选择以下方案之一：
  - [ ] **方案1**: 功能重叠时，合并为一个完整实现
  - [x] **方案2**: 功能互补时，合并两个类的方法到一个完整实现
  - [ ] **方案3**: 功能完全不同时，重命名其中一个类（如 NovelSearchDAO 和 GeneralSearchDAO）

- [ ] **整合具体方案**
  - 将所有功能整合到services/search_service.py中
  - 整合原则：
    - 保留services/search_service.py的DAO-Service分层架构
    - 将dao/search_dao.py中的方法转换为查询创建函数
    - 删除功能重复部分，选择更合理的实现
    - 保持函数签名一致性，确保向后兼容
  - 具体修改内容：
    - 保留SearchDAO现有方法：search_novels_query, search_by_tag_query, get_similar_novels_query
    - 添加dao/search_dao.py中的独有方法：get_category_novels_query, log_search_query
    - 扩展search_novels_query方法以支持更多过滤条件
    - 在SearchService类中添加对应的服务方法，如get_category_novels
    - 添加tags字段处理的兼容代码，同时支持关联表和文本字段查询
  - 代码结构图：
    ```
    SearchDAO:
    - search_novels_query()     // 增强版，支持更多过滤条件
    - search_by_tag_query()     // 兼容两种tags实现
    - get_similar_novels_query()
    - get_category_novels_query() // 新增
    - log_search_query()        // 新增
    
    SearchService:
    - search_novels()
    - search_by_tag()
    - suggest_similar_novels()
    - get_category_novels()     // 新增
    - record_search_keyword()   // 保留现有
    - track_search_keyword()    // 保留现有
    - get_trending_keywords()   // 保留现有
    ```
  - 可能的风险：
    - 数据模型差异：两个实现对tags字段处理方式不同
    - 接口变化：函数参数和返回值变化可能影响现有调用
    - 性能风险：合并后可能包含更多过滤条件
    - 循环依赖风险：确保DAO不依赖Service
    - 迁移过程风险：临时功能不可用

- [ ] **代码迁移**
  - [ ] 根据选定方案，修改 dao/search_dao.py
  - [ ] 确保所有功能得到保留或适当合并
  - [ ] 添加所有必要的导入语句

- [ ] **更新引用**
  - [ ] 在 search_service.py 中更新导入路径
  - [ ] 检查并更新其他可能引用 SearchDAO 的文件
  - [ ] 如果重命名了类，确保所有引用点都使用新名称

- [ ] **测试验证**
  - [ ] 运行单元测试（如有）
  - [ ] 手动验证所有搜索相关功能
  - [ ] 确认所有搜索功能正常工作

## 特别注意事项

- [ ] **检查循环依赖**
  - [ ] 确保不会在DAO和Service之间创建循环导入
  - [ ] DAO只依赖模型和低级工具类，不依赖Service类

- [ ] **确保事务处理一致**
  - [ ] 移动代码后事务处理逻辑保持不变
  - [ ] 检查db.session.commit()的位置和上下文

- [ ] **保持异常处理**
  - [ ] 保持原有的异常处理逻辑
  - [ ] 确保错误信息传递机制不变

## 风险缓解措施

- [ ] 每次迁移前创建代码分支或提交当前状态
- [ ] 每完成一个DAO迁移后进行全面测试
- [ ] 保留回滚计划，以便在出现问题时恢复
- [ ] 逐步实施，不要同时迁移多个DAO

## 完成后验证

- [ ] 确保所有DAO类都位于dao目录下
- [ ] 确保所有service类正确引用对应的DAO
- [ ] 运行完整的项目测试套件
- [ ] 验证所有功能正常工作
- [ ] 更新项目文档以反映新架构 

## 附录：SearchDAO整合详细代码实现

以下是SearchDAO整合方案的具体代码实现，可作为参考：

```python
# services/search_service.py (整合后)
from typing import List, Dict, Optional
from sqlalchemy import or_, and_, func, desc
from app import db
from app.models.novel import Novel
from datetime import datetime, timedelta
import logging
import os

logger = logging.getLogger(__name__)

class SearchDAO:
    """
    Data Access Object for search-related operations
    Only handles direct database queries with no business logic
    """
    
    @staticmethod
    def search_novels_query(
        q: Optional[str] = None,
        category: Optional[str] = None,
        min_words: Optional[int] = None,
        max_words: Optional[int] = None,
        status: Optional[str] = None,
        updated_after: Optional[datetime] = None
    ):
        """
        Create query for searching novels with multiple filters
        
        Args:
            q: Search keyword for title, author, or intro
            category: Novel category
            min_words: Minimum word count
            max_words: Maximum word count
            status: Novel status (ongoing, completed)
            updated_after: Last updated after this date
            
        Returns:
            SQLAlchemy query object
        """
        query = Novel.query
        
        # Apply keyword search
        if q:
            query = query.filter(or_(
                Novel.title.ilike(f'%{q}%'),
                Novel.author.ilike(f'%{q}%'),
                Novel.intro.ilike(f'%{q}%')
            ))
            
        # Apply additional filters
        if category:
            query = query.filter(Novel.category == category)
            
        if status:
            query = query.filter(Novel.status == status)
        
        if min_words:
            query = query.filter(Novel.total_words >= min_words)
            
        if max_words:
            query = query.filter(Novel.total_words <= max_words)
            
        if updated_after:
            query = query.filter(Novel.updated_at >= updated_after)
            
        return query
    
    @staticmethod
    def search_by_tag_query(tag: str):
        """
        Create query for searching novels by tag
        
        Args:
            tag: Tag to search for
            
        Returns:
            SQLAlchemy query object
        """
        # 使用any方法处理关联表形式的tags
        try:
            # 首先尝试使用关联表方式
            return Novel.query.filter(Novel.tags.any(name=tag))
        except Exception:
            # 如果出错，使用文本字段方式 (兼容性处理)
            return Novel.query.filter(Novel.tags.ilike(f'%{tag}%'))
    
    @staticmethod
    def get_similar_novels_query(novel: Novel, limit: int = 5):
        """
        Create query for finding similar novels
        
        Args:
            novel: Novel to find similar ones for
            limit: Maximum number of similar novels
            
        Returns:
            SQLAlchemy query object
        """
        # Find novels with same category
        query = Novel.query.filter(
            and_(
                Novel.category == novel.category,
                Novel.id != novel.id
            )
        ).order_by(
            Novel.view_count.desc()  # Sort by popularity
        ).limit(limit)
        
        return query
        
    @staticmethod
    def get_category_novels_query(category: str):
        """
        Create query for getting novels by category
        
        Args:
            category: Novel category
            
        Returns:
            SQLAlchemy query object
        """
        return Novel.query.filter(Novel.category == category)
    
    @staticmethod
    def log_search_query(user_id: Optional[int], keyword: str) -> None:
        """
        Log a search query for analytics
        
        Args:
            user_id: ID of user making the search (None for anonymous)
            keyword: Search keyword
        """
        # 这里可以实现实际的搜索日志记录功能
        # 如果有SearchHistory模型，可以记录到数据库
        # 如果使用其他方式如日志文件，也可以在这里实现
        pass

class SearchService:
    """
    Service for handling search operations
    Handles business logic, error handling, and response formatting
    """
    
    @staticmethod
    def search_novels(
        q: Optional[str] = None,
        category: Optional[str] = None,
        min_words: Optional[int] = None,
        max_words: Optional[int] = None,
        status: Optional[str] = None,
        updated_after: Optional[datetime] = None,
        page: int = 1, 
        per_page: int = 20
    ) -> Dict:
        """
        Search novels by multiple criteria
        
        Args:
            q: Search keyword
            category: Novel category
            min_words: Minimum word count
            max_words: Maximum word count
            status: Novel status
            updated_after: Updated after date
            page: Page number
            per_page: Items per page
            
        Returns:
            Dict with search results and pagination info
        """
        try:
            # Build the query with all filters
            query = SearchDAO.search_novels_query(
                q=q, 
                category=category,
                min_words=min_words,
                max_words=max_words,
                status=status,
                updated_after=updated_after
            )
            
            # Get total count for pagination
            total = query.count()
            
            # Apply pagination
            results = query.order_by(Novel.updated_at.desc()) \
                          .offset((page - 1) * per_page) \
                          .limit(per_page) \
                          .all()
                          
            # Log search query if keyword provided
            if q:
                # 可以接收user_id参数，这里简化为None
                SearchDAO.log_search_query(None, q)
                
            # Prepare response
            return {
                'success': True,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page,
                'results': [novel.to_dict() for novel in results]
            }
        except Exception as e:
            logger.error(f"Error in search_novels: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def search_by_tag(tag: str, page: int = 1, per_page: int = 20) -> Dict:
        """
        Search novels by tag
        
        Args:
            tag: Tag to search for
            page: Page number
            per_page: Items per page
            
        Returns:
            Dict with search results and pagination info
        """
        try:
            # Get query for tag search
            query = SearchDAO.search_by_tag_query(tag)
            
            # Get total count for pagination
            total = query.count()
            
            # Apply pagination
            results = query.order_by(Novel.updated_at.desc()) \
                          .offset((page - 1) * per_page) \
                          .limit(per_page) \
                          .all()
                          
            # Prepare response
            return {
                'success': True,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page,
                'results': [novel.to_dict() for novel in results]
            }
        except Exception as e:
            logger.error(f"Error in search_by_tag: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
        
    @staticmethod
    def suggest_similar_novels(novel_id: int, limit: int = 5) -> Dict:
        """
        Suggest similar novels based on category and tags
        
        Args:
            novel_id: ID of the novel to find similar ones for
            limit: Number of suggestions to return
            
        Returns:
            Dict with similar novels
        """
        try:
            novel = Novel.query.get(novel_id)
            if not novel:
                return {
                    'success': False,
                    'error': 'Novel not found'
                }
                
            # Get query for similar novels
            query = SearchDAO.get_similar_novels_query(novel, limit)
            similar_novels = query.all()
            
            return {
                'success': True,
                'results': [n.to_dict() for n in similar_novels]
            }
        except Exception as e:
            logger.error(f"Error in suggest_similar_novels: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
            
    @staticmethod
    def get_category_novels(category: str, page: int = 1, per_page: int = 20) -> Dict:
        """
        Get novels by category
        
        Args:
            category: Novel category
            page: Page number
            per_page: Items per page
            
        Returns:
            Dict with novels and pagination info
        """
        try:
            # Get query for category search
            query = SearchDAO.get_category_novels_query(category)
            
            # Get total count for pagination
            total = query.count()
            
            # Apply pagination
            results = query.order_by(Novel.updated_at.desc()) \
                          .offset((page - 1) * per_page) \
                          .limit(per_page) \
                          .all()
                          
            # Prepare response
            return {
                'success': True,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page,
                'results': [novel.to_dict() for novel in results]
            }
        except Exception as e:
            logger.error(f"Error in get_category_novels: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def record_search_keyword(keyword: str) -> None:
        """
        Record search keyword for trending analysis
        This method is kept for compatibility but no longer stores data in Redis
        
        Args:
            keyword: The search keyword
        """
        # No longer tracking search keywords after Redis removal
        pass
    
    @staticmethod
    def track_search_keyword(keyword):
        """
        Track search keywords for trending
        This method is kept for compatibility but no longer stores data in Redis
        
        Args:
            keyword: Keyword to track
        """
        # No longer tracking search keywords after Redis removal
        pass
    
    @staticmethod
    def get_trending_keywords(limit=10):
        """
        Get trending search keywords
        Now returns empty list since Redis tracking is removed
        
        Args:
            limit: Number of keywords to return
            
        Returns:
            Empty list (Redis functionality removed)
        """
        # No longer have trending keywords after Redis removal
        return [] 