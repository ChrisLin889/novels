import unittest
import json
import time
from app import create_app, db
from app.services.cache_service import CacheService, cached, cache_with_version, invalidate_cache_version
from app.models.novel import Novel, Chapter
from app.models.user import User

class TestCacheService(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Create test data
            self._create_test_data()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            CacheService.clear_all()
    
    def _create_test_data(self):
        # Create test user
        user = User(
            username="testauthor",
            email="test@example.com",
            role="author"
        )
        user.set_password("password")
        db.session.add(user)
        
        # Create test novel
        novel = Novel(
            title="Test Novel",
            author="testauthor",
            category="fantasy",
            intro="Test description",
            status="ongoing"
        )
        db.session.add(novel)
        
        # Create test chapters
        for i in range(1, 4):
            chapter = Chapter(
                novel_id=1,
                title=f"Chapter {i}",
                content=f"Content for chapter {i}",
                chapter_number=i
            )
            db.session.add(chapter)
        
        db.session.commit()
    
    def test_basic_cache_operations(self):
        """Test basic cache operations (set, get, delete)"""
        with self.app.app_context():
            # Test set and get
            CacheService.set("test_key", "test_value")
            value = CacheService.get("test_key")
            self.assertEqual(value, "test_value")
            
            # Test delete
            CacheService.delete("test_key")
            value = CacheService.get("test_key")
            self.assertIsNone(value)
            
            # Test non-existent key
            value = CacheService.get("non_existent_key")
            self.assertIsNone(value)
    
    def test_json_serialization(self):
        """Test JSON serialization of complex data"""
        with self.app.app_context():
            test_data = {
                "string": "value",
                "number": 123,
                "list": [1, 2, 3],
                "dict": {"key": "value"}
            }
            
            CacheService.set("test_json", test_data)
            value = CacheService.get("test_json")
            
            self.assertEqual(value, test_data)
    
    def test_novel_caching(self):
        """Test novel-specific caching methods"""
        with self.app.app_context():
            novel = Novel.query.get(1)
            novel_dict = novel.to_dict()
            
            # Test novel detail caching
            CacheService.cache_novel_detail(novel.id, novel_dict)
            cached_novel = CacheService.get_novel_detail(novel.id)
            
            self.assertEqual(cached_novel['title'], novel.title)
            self.assertEqual(cached_novel['id'], novel.id)
    
    def test_chapter_caching(self):
        """Test chapter content caching"""
        with self.app.app_context():
            chapter = Chapter.query.get(1)
            chapter_dict = chapter.to_dict(include_content=True)
            
            # Test chapter caching
            CacheService.cache_chapter_content(chapter.novel_id, chapter.id, chapter_dict)
            cached_chapter = CacheService.get_chapter_content(chapter.novel_id, chapter.id)
            
            self.assertEqual(cached_chapter['title'], chapter.title)
            self.assertEqual(cached_chapter['content'], chapter.content)
    
    def test_rankings_caching(self):
        """Test rankings caching methods"""
        with self.app.app_context():
            # Create sample ranking data
            ranking_data = [
                {"id": 1, "title": "Novel 1", "views": 1000},
                {"id": 2, "title": "Novel 2", "views": 500}
            ]
            
            # Test ranking caching
            CacheService.cache_novel_rankings("hot", ranking_data)
            cached_ranking = CacheService.get_novel_rankings("hot")
            
            self.assertEqual(len(cached_ranking), 2)
            self.assertEqual(cached_ranking[0]["views"], 1000)
    
    def test_cache_decorator(self):
        """Test the @cached decorator"""
        call_count = 0
        
        @cached("test_func")
        def test_function():
            nonlocal call_count
            call_count += 1
            return "result"
        
        with self.app.app_context():
            # First call should execute the function
            result1 = test_function()
            self.assertEqual(result1, "result")
            self.assertEqual(call_count, 1)
            
            # Second call should use cached result
            result2 = test_function()
            self.assertEqual(result2, "result")
            self.assertEqual(call_count, 1)  # Count should still be 1
            
            # Force the function to run again by mocking cache miss
            CacheService.clear_all()
            result3 = test_function()
            self.assertEqual(result3, "result")
            self.assertEqual(call_count, 2)
    
    def test_versioned_cache(self):
        """Test the @cache_with_version decorator"""
        call_count = 0
        
        @cache_with_version("versioned_func")
        def versioned_function():
            nonlocal call_count
            call_count += 1
            return "versioned_result"
        
        with self.app.app_context():
            # First call should execute the function
            result1 = versioned_function()
            self.assertEqual(result1, "versioned_result")
            self.assertEqual(call_count, 1)
            
            # Second call should use cached result
            result2 = versioned_function()
            self.assertEqual(result2, "versioned_result")
            self.assertEqual(call_count, 1)
            
            # Force the function to run again by mocking cache miss
            CacheService.clear_all()
            
            result3 = versioned_function()
            self.assertEqual(result3, "versioned_result")
            self.assertEqual(call_count, 2)


if __name__ == '__main__':
    unittest.main()