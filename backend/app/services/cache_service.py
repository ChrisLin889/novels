import redis
import json
import os
from typing import Any, Dict, List, Optional, Union
from functools import wraps
import time

# Initialize Redis connection
redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

# Mock Redis implementation for when Redis is not available
class MockRedis:
    def __init__(self):
        self.data = {}
        self.expiry = {}
    
    def setex(self, key, ttl, value):
        self.data[key] = value
        self.expiry[key] = time.time() + ttl
        return True
    
    def get(self, key):
        if key in self.data:
            if key in self.expiry and time.time() > self.expiry[key]:
                del self.data[key]
                if key in self.expiry:
                    del self.expiry[key]
                return None
            return self.data[key]
        return None
    
    def delete(self, *keys):
        count = 0
        for key in keys:
            if key in self.data:
                del self.data[key]
                if key in self.expiry:
                    del self.expiry[key]
                count += 1
        return count
    
    def keys(self, pattern):
        import fnmatch
        matching_keys = [k for k in self.data.keys() if fnmatch.fnmatch(k, pattern)]
        return matching_keys
    
    def flushdb(self):
        self.data.clear()
        self.expiry.clear()
        return True
    
    def ping(self):
        return True

# Try to connect to Redis, fall back to mock if unavailable
try:
    redis_client = redis.from_url(redis_url)
    # Test connection
    redis_client.ping()
    print("Connected to Redis successfully")
except Exception as e:
    print(f"Redis connection failed: {str(e)}")
    print("Using in-memory mock Redis instead")
    redis_client = MockRedis()

# Default cache TTLs
DEFAULT_TTL = 3600  # 1 hour
LONG_TTL = 86400  # 24 hours
SHORT_TTL = 300  # 5 minutes

# Cache key prefixes
NOVEL_PREFIX = "novel:"
CHAPTER_PREFIX = "chapter:"
RANKING_PREFIX = "ranking:"
CATEGORY_PREFIX = "category:"
USER_PREFIX = "user:"
COLLECTION_PREFIX = "collection:"

class CacheService:
    """
    Service for handling caching operations
    """
    
    @staticmethod
    def set(key: str, value: Any, ttl: int = DEFAULT_TTL) -> bool:
        """
        Set a value in the cache
        
        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            ttl: Time to live in seconds
            
        Returns:
            bool: True if successful
        """
        try:
            json_value = json.dumps(value)
            redis_client.setex(key, ttl, json_value)
            return True
        except Exception as e:
            print(f"Cache set error: {str(e)}")
            return False
    
    @staticmethod
    def get(key: str) -> Optional[Any]:
        """
        Get a value from the cache
        
        Args:
            key: Cache key
            
        Returns:
            Any: The cached value, or None if not found
        """
        try:
            value = redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Cache get error: {str(e)}")
            return None
    
    @staticmethod
    def delete(key: str) -> bool:
        """
        Delete a value from the cache
        
        Args:
            key: Cache key
            
        Returns:
            bool: True if successful
        """
        try:
            redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error: {str(e)}")
            return False
    
    @staticmethod
    def delete_pattern(pattern: str) -> bool:
        """
        Delete all keys matching a pattern
        
        Args:
            pattern: Pattern to match (e.g. "user:*")
            
        Returns:
            bool: True if successful
        """
        try:
            keys = redis_client.keys(pattern)
            if keys:
                redis_client.delete(*keys)
            return True
        except Exception as e:
            print(f"Cache delete pattern error: {str(e)}")
            return False
    
    @staticmethod
    def refresh_novel_cache() -> bool:
        """
        Refresh all novel-related caches
        
        Returns:
            bool: True if successful
        """
        try:
            CacheService.delete_pattern(f"{NOVEL_PREFIX}*")
            CacheService.delete_pattern(f"{CHAPTER_PREFIX}*")
            CacheService.delete_pattern(f"{RANKING_PREFIX}*")
            CacheService.delete_pattern(f"{CATEGORY_PREFIX}*")
            return True
        except Exception as e:
            print(f"Refresh novel cache error: {str(e)}")
            return False
    
    @staticmethod
    def clear_all() -> bool:
        """
        Clear all cache
        
        Returns:
            bool: True if successful
        """
        try:
            redis_client.flushdb()
            return True
        except Exception as e:
            print(f"Clear cache error: {str(e)}")
            return False
    
    @staticmethod
    def cache_novel_rankings(ranking_type: str, data: List[Dict], ttl: int = DEFAULT_TTL) -> bool:
        """
        Cache novel rankings (hot, latest, etc)
        
        Args:
            ranking_type: Type of ranking ('hot', 'latest', 'popular', etc)
            data: List of novel data to cache
            ttl: Time to live in seconds
            
        Returns:
            bool: True if successful
        """
        key = f"{RANKING_PREFIX}{ranking_type}"
        return CacheService.set(key, data, ttl)
    
    @staticmethod
    def get_novel_rankings(ranking_type: str) -> Optional[List[Dict]]:
        """
        Get cached novel rankings
        
        Args:
            ranking_type: Type of ranking ('hot', 'latest', 'popular', etc)
            
        Returns:
            List or None: Cached rankings or None if not found
        """
        key = f"{RANKING_PREFIX}{ranking_type}"
        return CacheService.get(key)
        
    @staticmethod
    def cache_novel_categories(categories: List[Dict], ttl: int = LONG_TTL) -> bool:
        """
        Cache novel categories
        
        Args:
            categories: List of category data
            ttl: Time to live in seconds
            
        Returns:
            bool: True if successful
        """
        key = f"{CATEGORY_PREFIX}all"
        return CacheService.set(key, categories, ttl)
        
    @staticmethod
    def get_novel_categories() -> Optional[List[Dict]]:
        """
        Get cached novel categories
        
        Returns:
            List or None: Cached categories or None if not found
        """
        key = f"{CATEGORY_PREFIX}all"
        return CacheService.get(key)
        
    @staticmethod
    def cache_novel_detail(novel_id: int, novel_data: Dict, ttl: int = DEFAULT_TTL) -> bool:
        """
        Cache novel detail
        
        Args:
            novel_id: ID of the novel
            novel_data: Novel data to cache
            ttl: Time to live in seconds
            
        Returns:
            bool: True if successful
        """
        key = f"{NOVEL_PREFIX}{novel_id}"
        return CacheService.set(key, novel_data, ttl)
        
    @staticmethod
    def get_novel_detail(novel_id: int) -> Optional[Dict]:
        """
        Get cached novel detail
        
        Args:
            novel_id: ID of the novel
            
        Returns:
            Dict or None: Cached novel data or None if not found
        """
        key = f"{NOVEL_PREFIX}{novel_id}"
        return CacheService.get(key)
        
    @staticmethod
    def cache_chapter_content(novel_id: int, chapter_id: int, chapter_data: Dict, ttl: int = DEFAULT_TTL) -> bool:
        """
        Cache chapter content
        
        Args:
            novel_id: ID of the novel
            chapter_id: ID of the chapter
            chapter_data: Chapter data to cache
            ttl: Time to live in seconds
            
        Returns:
            bool: True if successful
        """
        key = f"{CHAPTER_PREFIX}{novel_id}:{chapter_id}"
        return CacheService.set(key, chapter_data, ttl)
        
    @staticmethod
    def get_chapter_content(novel_id: int, chapter_id: int) -> Optional[Dict]:
        """
        Get cached chapter content
        
        Args:
            novel_id: ID of the novel
            chapter_id: ID of the chapter
            
        Returns:
            Dict or None: Cached chapter data or None if not found
        """
        key = f"{CHAPTER_PREFIX}{novel_id}:{chapter_id}"
        return CacheService.get(key)
        
    @staticmethod
    def cache_user_collections(user_id: int, collections: List[Dict], ttl: int = SHORT_TTL) -> bool:
        """
        Cache user collections
        
        Args:
            user_id: ID of the user
            collections: List of collection data
            ttl: Time to live in seconds
            
        Returns:
            bool: True if successful
        """
        key = f"{USER_PREFIX}{user_id}:{COLLECTION_PREFIX}"
        return CacheService.set(key, collections, ttl)
        
    @staticmethod
    def get_user_collections(user_id: int) -> Optional[List[Dict]]:
        """
        Get cached user collections
        
        Args:
            user_id: ID of the user
            
        Returns:
            List or None: Cached collections or None if not found
        """
        key = f"{USER_PREFIX}{user_id}:{COLLECTION_PREFIX}"
        return CacheService.get(key)
        
    @staticmethod
    def invalidate_user_cache(user_id: int) -> bool:
        """
        Invalidate all cache for a user
        
        Args:
            user_id: ID of the user
            
        Returns:
            bool: True if successful
        """
        return CacheService.delete_pattern(f"{USER_PREFIX}{user_id}:*")


def cached(key_prefix: str, ttl: int = DEFAULT_TTL):
    """
    Decorator for caching function results
    
    Args:
        key_prefix: Prefix for cache key
        ttl: Time to live in seconds
        
    Example:
        @cached("user_profile", 300)
        def get_user_profile(user_id):
            # This result will be cached for 5 minutes
            # The cache key will be "user_profile:{user_id}"
            return db.query.get(user_id)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from prefix and arguments
            arg_str = ':'.join(str(arg) for arg in args if not callable(arg))
            kwarg_str = ':'.join(f"{k}={v}" for k, v in kwargs.items())
            key = f"{key_prefix}:{arg_str}:{kwarg_str}" if arg_str or kwarg_str else key_prefix
            
            # Try to get from cache
            cached_value = CacheService.get(key)
            if cached_value is not None:
                return cached_value
            
            # Call the function and cache the result
            result = func(*args, **kwargs)
            CacheService.set(key, result, ttl)
            return result
        return wrapper
    return decorator


def cache_with_version(cache_key: str, version_key: str = None, ttl: int = DEFAULT_TTL):
    """
    Decorator for caching function results with version control
    Useful for data that needs to be invalidated as a group
    
    Args:
        cache_key: Base cache key
        version_key: Key to store the version number
        ttl: Time to live in seconds
    """
    if version_key is None:
        version_key = f"{cache_key}:version"
        
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get current version
            version = CacheService.get(version_key)
            if version is None:
                version = int(time.time())
                CacheService.set(version_key, version, LONG_TTL)
                
            # Create versioned cache key
            full_key = f"{cache_key}:v{version}"
            
            # Try to get from cache
            cached_value = CacheService.get(full_key)
            if cached_value is not None:
                return cached_value
                
            # Call the function and cache the result
            result = func(*args, **kwargs)
            CacheService.set(full_key, result, ttl)
            return result
        return wrapper
    return decorator


def invalidate_cache_version(version_key: str):
    """
    Invalidate a cache version by updating its version number
    
    Args:
        version_key: Version key to invalidate
    """
    new_version = int(time.time())
    CacheService.set(version_key, new_version, LONG_TTL)
    return new_version 