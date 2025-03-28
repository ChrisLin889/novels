import unittest
from app import create_app, db
from app.models.user import User
from app.models.admin import SensitiveWord, ContentAudit, UserAction, CrawledNovel, CrawledChapter
from app.services.admin_service import AdminService
from datetime import datetime

class TestAdminService(unittest.TestCase):
    
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
    
    def _create_test_data(self):
        # Create admin user
        admin = User(
            username="admin",
            email="admin@example.com",
            role="admin",
            status="active"
        )
        admin.set_password("admin_password")
        db.session.add(admin)
        
        # Create regular users
        for i in range(1, 5):
            user = User(
                username=f"user{i}",
                email=f"user{i}@example.com",
                role="user",
                status="active"
            )
            user.set_password("password")
            db.session.add(user)
        
        # Create sensitive words
        sensitive_words = [
            {"word": "badword1", "level": 2, "category": "profanity"},
            {"word": "badword2", "level": 3, "category": "profanity"},
            {"word": "political1", "level": 2, "category": "political"}
        ]
        
        for word_data in sensitive_words:
            word = SensitiveWord(
                word=word_data["word"],
                level=word_data["level"],
                category=word_data["category"],
                added_by=1  # Admin user ID
            )
            db.session.add(word)
        
        # Create crawled novel
        novel = CrawledNovel(
            title="Test Crawled Novel",
            author="Test Author",
            category="fantasy",
            intro="Test introduction",
            status="pending",
            source_site="test_site"
        )
        db.session.add(novel)
        
        # Create chapters for the crawled novel
        for i in range(1, 4):
            chapter = CrawledChapter(
                novel_id=1,
                chapter_number=i,
                title=f"Chapter {i}",
                content=f"Content for chapter {i}",
                source_url=f"http://example.com/chapter{i}"
            )
            db.session.add(chapter)
        
        db.session.commit()
    
    def test_get_users(self):
        """Test getting users list"""
        with self.app.app_context():
            # Get all users
            result = AdminService.get_users()
            self.assertEqual(result['total'], 5)  # 4 regular + 1 admin
            
            # Filter by role
            admin_result = AdminService.get_users(role="admin")
            self.assertEqual(admin_result['total'], 1)
            self.assertEqual(admin_result['users'][0]['role'], "admin")
            
            user_result = AdminService.get_users(role="user")
            self.assertEqual(user_result['total'], 4)
    
    def test_ban_and_unban_user(self):
        """Test banning and unbanning users"""
        with self.app.app_context():
            # Ban a user
            result = AdminService.manage_user(
                admin_id=1,
                user_id=2,
                action="ban",
                reason="Test ban",
                duration=7
            )
            self.assertTrue(result['success'])
            
            # Verify user is banned
            banned_user = User.query.get(2)
            self.assertEqual(banned_user.status, "banned")
            self.assertIsNotNone(banned_user.ban_until)
            
            # Unban the user
            result = AdminService.manage_user(
                admin_id=1,
                user_id=2,
                action="unban",
                reason="Test unban"
            )
            self.assertTrue(result['success'])
            
            # Verify user is unbanned
            unbanned_user = User.query.get(2)
            self.assertEqual(unbanned_user.status, "active")
            self.assertIsNone(unbanned_user.ban_until)
    
    def test_user_actions(self):
        """Test getting user action history"""
        with self.app.app_context():
            # Ban a user to create an action
            AdminService.manage_user(
                admin_id=1,
                user_id=2,
                action="ban",
                reason="Test ban",
                duration=7
            )
            
            # Get all actions
            result = AdminService.get_user_actions()
            self.assertEqual(result['total'], 1)
            
            # Filter by user ID
            result = AdminService.get_user_actions(user_id=2)
            self.assertEqual(result['total'], 1)
            self.assertEqual(result['actions'][0]['target_user_id'], 2)
            
            # Filter by non-existent user
            result = AdminService.get_user_actions(user_id=999)
            self.assertEqual(result['total'], 0)
    
    def test_sensitive_word_filtering(self):
        """Test filtering sensitive content"""
        with self.app.app_context():
            # Test text with no sensitive words
            text = "This is a normal text with no bad words."
            has_sensitive, matches, filtered = AdminService.filter_sensitive_content(text)
            self.assertFalse(has_sensitive)
            self.assertEqual(len(matches), 0)
            self.assertEqual(filtered, text)
            
            # Test text with sensitive words
            text = "This text contains badword1 and political1 which are bad."
            has_sensitive, matches, filtered = AdminService.filter_sensitive_content(text)
            self.assertTrue(has_sensitive)
            self.assertEqual(len(matches), 2)
            self.assertNotEqual(filtered, text)  # Should be filtered
            self.assertIn("********", filtered)  # badword1 replaced
    
    def test_sensitive_word_management(self):
        """Test managing sensitive words"""
        with self.app.app_context():
            # Get sensitive words
            result = AdminService.get_sensitive_words()
            self.assertEqual(result['total'], 3)
            
            # Filter by category
            result = AdminService.get_sensitive_words(category="profanity")
            self.assertEqual(result['total'], 2)
            
            # Add a new sensitive word
            result = AdminService.manage_sensitive_word(
                word="newbadword",
                level=2,
                category="profanity",
                admin_id=1,
                action="add"
            )
            self.assertTrue(result['success'])
            
            # Verify word was added
            result = AdminService.get_sensitive_words()
            self.assertEqual(result['total'], 4)
            
            # Delete a word
            word_id = result['words'][0]['id']
            result = AdminService.manage_sensitive_word(
                word="",
                level=0,
                category="",
                admin_id=1,
                action="delete",
                word_id=word_id
            )
            self.assertTrue(result['success'])
            
            # Verify word was deleted
            result = AdminService.get_sensitive_words()
            self.assertEqual(result['total'], 3)
    
    def test_crawled_novels(self):
        """Test crawled novel management"""
        with self.app.app_context():
            # Get crawled novels
            result = AdminService.get_crawled_novels()
            self.assertEqual(result['total'], 1)
            self.assertEqual(result['novels'][0]['status'], "pending")
            
            # Get chapters
            result = AdminService.get_crawled_chapters(1)
            self.assertEqual(result['total'], 3)
            
            # Approve the novel
            result = AdminService.manage_crawled_novel(
                novel_id=1,
                action="approve"
            )
            self.assertTrue(result['success'])
            
            # Verify novel was approved
            novel = CrawledNovel.query.get(1)
            self.assertEqual(novel.status, "approved")


if __name__ == '__main__':
    unittest.main() 