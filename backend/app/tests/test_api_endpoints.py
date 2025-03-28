import unittest
import json
import base64
from app import create_app, db
from app.models.user import User
from app.models.novel import Novel, Chapter
from app.models.interaction import UserCollection, UserHistory, Comment, UserFollowing, PrivateMessage, UserTip
from flask_jwt_extended import create_access_token

class TestAPIEndpoints(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Create test data
            self._create_test_data()
            # Create access tokens for testing
            self.user_token = create_access_token(identity=1)
            self.author_token = create_access_token(identity=2)
            self.admin_token = create_access_token(identity=3)
    
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
    
    # Helper methods
    def _auth_headers(self, token):
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    
    # Interaction API Tests
    def test_collection_api(self):
        """Test collection API endpoints"""
        # Test toggle collection
        response = self.client.post(
            '/api/interaction/collection',
            headers=self._auth_headers(self.user_token),
            data=json.dumps({'novel_id': 1})
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['is_collected'])
        
        # Test get collection status
        response = self.client.get(
            '/api/interaction/collection/status/1',
            headers=self._auth_headers(self.user_token)
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['is_collected'])
        
        # Test get user collections
        response = self.client.get(
            '/api/interaction/collection',
            headers=self._auth_headers(self.user_token)
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total'], 1)
    
    def test_comment_api(self):
        """Test comment API endpoints"""
        # Test add comment
        response = self.client.post(
            '/api/interaction/comment',
            headers=self._auth_headers(self.user_token),
            data=json.dumps({
                'novel_id': 1,
                'content': 'Test API comment'
            })
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        comment_id = data['comment']['id']
        
        # Test get novel comments
        response = self.client.get(
            '/api/interaction/comments/1',
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['comments']), 1)
        
        # Test delete comment
        response = self.client.delete(
            f'/api/interaction/comment/{comment_id}',
            headers=self._auth_headers(self.user_token)
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Comment deleted successfully')
    
    def test_follow_api(self):
        """Test follow API endpoints"""
        # Test toggle follow
        response = self.client.post(
            '/api/interaction/follow',
            headers=self._auth_headers(self.user_token),
            data=json.dumps({'user_id': 2})
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['is_following'])
        
        # Test get follow status
        response = self.client.get(
            '/api/interaction/follow/status/2',
            headers=self._auth_headers(self.user_token)
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['is_following'])
        
        # Test get followers
        response = self.client.get('/api/interaction/followers/2')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total'], 1)
        
        # Test get following
        response = self.client.get('/api/interaction/following/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total'], 1)
    
    def test_message_api(self):
        """Test messaging API endpoints"""
        # Setup: Make user2 (author) follow user1 to enable messaging
        with self.app.app_context():
            following = UserFollowing(
                follower_id=2,
                followed_id=1
            )
            db.session.add(following)
            db.session.commit()
        
        # Test send message
        response = self.client.post(
            '/api/interaction/message',
            headers=self._auth_headers(self.user_token),
            data=json.dumps({
                'recipient_id': 2,
                'content': 'Test API message'
            })
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        message_id = data['data']['id']
        
        # Test get conversation
        response = self.client.get(
            '/api/interaction/conversation/2',
            headers=self._auth_headers(self.user_token)
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['messages']), 1)
        
        # Test get inbox
        response = self.client.get(
            '/api/interaction/inbox',
            headers=self._auth_headers(self.author_token)
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['unread_count'], 1)
        
        # Test mark message as read
        response = self.client.post(
            f'/api/interaction/message/{message_id}/read',
            headers=self._auth_headers(self.author_token)
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Message marked as read')
    
    def test_tip_api(self):
        """Test tipping API endpoints"""
        # Test send tip
        response = self.client.post(
            '/api/interaction/tip',
            headers=self._auth_headers(self.user_token),
            data=json.dumps({
                'author_id': 2,
                'novel_id': 1,
                'amount': 500,
                'message': 'Test API tip'
            })
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        
        # Test get tips received
        response = self.client.get(
            '/api/interaction/tips/received',
            headers=self._auth_headers(self.author_token)
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['tips']), 1)
        self.assertEqual(data['total_amount'], 500)
        
        # Test get tips sent
        response = self.client.get(
            '/api/interaction/tips/sent',
            headers=self._auth_headers(self.user_token)
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['tips']), 1)
        self.assertEqual(data['total_amount'], 500)
    
    # Cache API Tests
    def test_cache_api(self):
        """Test cache API endpoints"""
        # Test refresh cache (admin only)
        response = self.client.post(
            '/api/cache/refresh',
            headers=self._auth_headers(self.admin_token)
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Cache refreshed successfully')
        
        # Test non-admin cannot refresh cache
        response = self.client.post(
            '/api/cache/refresh',
            headers=self._auth_headers(self.user_token)
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        
        # Test clear novel cache (author can clear their own novel)
        response = self.client.delete(
            '/api/cache/novel/1',
            headers=self._auth_headers(self.author_token)
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Novel cache cleared successfully')
        
        # Test clear user cache
        response = self.client.delete(
            '/api/cache/user/1',
            headers=self._auth_headers(self.user_token)
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'User cache cleared successfully')
        
        # Test admin can clear ranking cache
        response = self.client.delete(
            '/api/cache/rankings/hot',
            headers=self._auth_headers(self.admin_token)
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('cache cleared successfully' in data['message'])


if __name__ == '__main__':
    unittest.main() 