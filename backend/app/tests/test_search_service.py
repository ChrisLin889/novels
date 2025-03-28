import unittest
from app import create_app, db
from app.models.novel import Novel, Chapter
from app.models.user import User
from app.services.search_service import SearchService
from datetime import datetime, timedelta

class TestSearchService(unittest.TestCase):
    
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
        # Create test novels with different categories and properties
        novels = [
            {
                'title': 'Fantasy Adventure',
                'author': 'Author One',
                'category': 'fantasy',
                'intro': 'An epic adventure in a magical world',
                'status': 'ongoing'
            },
            {
                'title': 'Sci-Fi Journey',
                'author': 'Author Two',
                'category': 'sci-fi',
                'intro': 'Space exploration in future centuries',
                'status': 'completed'
            },
            {
                'title': 'Modern Mystery',
                'author': 'Author Three',
                'category': 'mystery',
                'intro': 'Detective solves mysterious crimes',
                'status': 'ongoing'
            },
            {
                'title': 'Another Fantasy',
                'author': 'Author Four',
                'category': 'fantasy',
                'intro': 'Another magical adventure in fantasy realm',
                'status': 'ongoing'
            }
        ]
        
        for i, novel_data in enumerate(novels):
            novel = Novel(**novel_data)
            db.session.add(novel)
            
            # Add chapters for this novel
            for j in range(1, 4):
                chapter = Chapter(
                    novel_id=i+1,
                    title=f"Chapter {j}",
                    content=f"Content for chapter {j} of {novel_data['title']}",
                    chapter_number=j
                )
                db.session.add(chapter)
        
        db.session.commit()
    
    def test_basic_search(self):
        """Test basic keyword search"""
        with self.app.app_context():
            # Search for 'fantasy' - should return 2 results
            results = SearchService.search_novels('fantasy')
            self.assertEqual(results['total'], 2)
            self.assertEqual(len(results['results']), 2)
            
            # Search for 'mystery' - should return 1 result
            results = SearchService.search_novels('mystery')
            self.assertEqual(results['total'], 1)
            self.assertEqual(results['results'][0]['title'], 'Modern Mystery')
    
    def test_category_filter(self):
        """Test search with category filter"""
        with self.app.app_context():
            # Search for novels in fantasy category
            results = SearchService.search_novels('', category='fantasy')
            self.assertEqual(results['total'], 2)
            
            # Search for novels in sci-fi category
            results = SearchService.search_novels('', category='sci-fi')
            self.assertEqual(results['total'], 1)
            self.assertEqual(results['results'][0]['title'], 'Sci-Fi Journey')
    
    def test_status_filter(self):
        """Test search with status filter"""
        with self.app.app_context():
            # Search for ongoing novels
            results = SearchService.search_novels('', status='ongoing')
            self.assertEqual(results['total'], 3)
            
            # Search for completed novels
            results = SearchService.search_novels('', status='completed')
            self.assertEqual(results['total'], 1)
            self.assertEqual(results['results'][0]['title'], 'Sci-Fi Journey')
    
    def test_pagination(self):
        """Test search pagination"""
        with self.app.app_context():
            # Get first page with 2 items per page
            results = SearchService.search_novels('', page=1, per_page=2)
            self.assertEqual(len(results['results']), 2)
            self.assertEqual(results['total'], 4)
            self.assertEqual(results['total_pages'], 2)
            
            # Get second page
            results = SearchService.search_novels('', page=2, per_page=2)
            self.assertEqual(len(results['results']), 2)
    
    def test_combined_filters(self):
        """Test search with multiple filters"""
        with self.app.app_context():
            # Search for ongoing fantasy novels
            results = SearchService.search_novels(
                '',
                category='fantasy',
                status='ongoing'
            )
            self.assertEqual(results['total'], 2)
            
            # Should find no completed fantasy novels
            results = SearchService.search_novels(
                '',
                category='fantasy',
                status='completed'
            )
            self.assertEqual(results['total'], 0)
    
    def test_similar_novels(self):
        """Test similar novels suggestion"""
        with self.app.app_context():
            # Get similar novels for the first fantasy novel
            similar = SearchService.suggest_similar_novels(1)
            
            # Should return the other fantasy novel
            self.assertEqual(len(similar), 1)
            self.assertEqual(similar[0]['title'], 'Another Fantasy')
            
            # Get similar novels for the mystery novel
            similar = SearchService.suggest_similar_novels(3)
            
            # Should return no similar novels (no other mystery novels)
            self.assertEqual(len(similar), 0)


if __name__ == '__main__':
    unittest.main() 