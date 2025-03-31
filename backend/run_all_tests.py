import unittest
import sys
from app.tests.test_interaction_service import TestInteractionService
from app.tests.test_cache_service import TestCacheService
from app.tests.test_api_endpoints import TestAPIEndpoints
from app.tests.test_search_service import TestSearchService
from app.tests.test_admin_service import TestAdminService

def run_tests():
    """Run all backend unit tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestInteractionService))
    test_suite.addTest(unittest.makeSuite(TestCacheService))
    test_suite.addTest(unittest.makeSuite(TestAPIEndpoints))
    test_suite.addTest(unittest.makeSuite(TestSearchService))
    test_suite.addTest(unittest.makeSuite(TestAdminService))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    print("Running all backend unit tests...")
    sys.exit(run_tests()) 