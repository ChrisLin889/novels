import unittest
import json
from datetime import datetime
from app import create_app, db
from app.services.interaction_service import InteractionService, InteractionDAO
from app.models.user import User
from app.models.novel import Novel, Chapter
from app.models.interaction import UserCollection, UserHistory, Comment, UserFollowing, PrivateMessage, UserTip

class TestInteractionService(unittest.TestCase):
    
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
        # Create test users
        user1 = User(
            username="testuser1",
            email="user1@example.com",
            role="user"
        )
        user1.set_password("password")
        
        user2 = User(
            username="testauthor",
            email="author@example.com",
            role="author"
        )
        user2.set_password("password")
        
        user3 = User(
            username="testadmin",
            email="admin@example.com",
            role="admin"
        )
        user3.set_password("password")
        
        db.session.add_all([user1, user2, user3])
        
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
    
    def test_collection_operations(self):
        """Test novel collection operations"""
        with self.app.app_context():
            # Test adding to collection
            result = InteractionService.toggle_collection(user_id=1, novel_id=1)
            self.assertTrue(result['success'])
            self.assertTrue(result['is_collected'])
            
            # Check collection status
            result = InteractionService.get_collection_status(user_id=1, novel_id=1)
            self.assertTrue(result['is_collected'])
            
            # Test removing from collection
            result = InteractionService.toggle_collection(user_id=1, novel_id=1)
            self.assertTrue(result['success'])
            self.assertFalse(result['is_collected'])
            
            # Check collection status after removal
            result = InteractionService.get_collection_status(user_id=1, novel_id=1)
            self.assertFalse(result['is_collected'])
    
    def test_reading_history(self):
        """Test reading history operations"""
        with self.app.app_context():
            # Test updating reading history
            result = InteractionService.update_reading_history(user_id=1, novel_id=1, chapter_id=2)
            self.assertTrue(result['success'])
            
            # Test getting reading progress
            result = InteractionService.get_reading_progress(user_id=1, novel_id=1)
            self.assertTrue(result['success'])
            self.assertEqual(result['current_chapter_id'], 2)
            self.assertEqual(result['current_chapter_number'], 2)
    
    def test_comments(self):
        """Test comment operations"""
        with self.app.app_context():
            # Test adding a comment
            result = InteractionService.add_comment(user_id=1, novel_id=1, content="Test comment")
            self.assertTrue(result['success'])
            
            # Get the comment ID from the result
            comment_id = result['comment']['id']
            
            # Test getting comments
            result = InteractionService.get_comments(novel_id=1)
            self.assertTrue(result['success'])
            self.assertEqual(len(result['comments']), 1)
            
            # Test deleting comment
            result = InteractionService.delete_comment(user_id=1, comment_id=comment_id)
            self.assertTrue(result['success'])
            
            # Verify comment was deleted
            result = InteractionService.get_comments(novel_id=1)
            self.assertTrue(result['success'])
            self.assertEqual(len(result['comments']), 0)
    
    def test_follow_operations(self):
        """Test user following operations"""
        with self.app.app_context():
            # Test following a user
            result = InteractionService.toggle_follow(follower_id=1, followed_id=2)
            self.assertTrue(result['success'])
            self.assertTrue(result['is_following'])
            
            # Check follow status
            result = InteractionService.get_follow_status(follower_id=1, followed_id=2)
            self.assertTrue(result['success'])
            self.assertTrue(result['is_following'])
            
            # Test unfollowing
            result = InteractionService.toggle_follow(follower_id=1, followed_id=2)
            self.assertTrue(result['success'])
            self.assertFalse(result['is_following'])
            
            # Verify self-follow is prevented
            result = InteractionService.toggle_follow(follower_id=1, followed_id=1)
            self.assertFalse(result['success'])
    
    def test_followers_and_following(self):
        """Test getting followers and following lists"""
        with self.app.app_context():
            # Setup: User1 follows User2
            InteractionDAO.follow_user(follower_id=1, followed_id=2)
            
            # Test getting followers for User2
            result = InteractionService.get_followers(user_id=2)
            self.assertTrue(result['success'])
            self.assertEqual(result['total'], 1)
            self.assertEqual(result['followers'][0]['username'], 'testuser1')
            
            # Test getting following list for User1
            result = InteractionService.get_following(user_id=1)
            self.assertTrue(result['success'])
            self.assertEqual(result['total'], 1)
            self.assertEqual(result['following'][0]['username'], 'testauthor')
    
    def test_messaging(self):
        """Test private messaging operations"""
        with self.app.app_context():
            # Setup: User1 follows User2 (requirement for messaging)
            InteractionDAO.follow_user(follower_id=2, followed_id=1)
            
            # Test sending a message
            result = InteractionService.send_message(
                sender_id=1, 
                recipient_id=2, 
                content="Test message"
            )
            self.assertTrue(result['success'])
            
            # Get message ID for later use
            message_id = result['data']['id']
            
            # Test getting conversation
            result = InteractionService.get_conversation(user_id=1, other_user_id=2)
            self.assertTrue(result['success'])
            self.assertEqual(len(result['messages']), 1)
            
            # Test getting inbox
            result = InteractionService.get_inbox(user_id=2)
            self.assertTrue(result['success'])
            self.assertEqual(result['unread_count'], 1)
            
            # Test marking message as read
            result = InteractionService.mark_message_read(user_id=2, message_id=message_id)
            self.assertTrue(result['success'])
            
            # Verify message was marked as read
            result = InteractionService.get_inbox(user_id=2)
            self.assertTrue(result['success'])
            self.assertEqual(result['unread_count'], 0)
    
    def test_tipping(self):
        """Test tipping operations"""
        with self.app.app_context():
            # Test sending a tip
            result = InteractionService.send_tip(
                tipper_id=1,
                author_id=2,
                novel_id=1,
                amount=500,  # $5.00
                message="Great work!"
            )
            self.assertTrue(result['success'])
            
            # Test getting tips received
            result = InteractionService.get_tips_received(user_id=2)
            self.assertTrue(result['success'])
            self.assertEqual(len(result['tips']), 1)
            self.assertEqual(result['total_amount'], 500)
            
            # Test getting tips sent
            result = InteractionService.get_tips_sent(user_id=1)
            self.assertTrue(result['success'])
            self.assertEqual(len(result['tips']), 1)
            self.assertEqual(result['total_amount'], 500)


if __name__ == '__main__':
    unittest.main() 