import redis
import json
import os
from typing import Any, Dict, List, Optional, Union
from functools import wraps

# Initialize Redis connection
redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
redis_client = redis.from_url(redis_url)

# Default cache TTLs
DEFAULT_TTL = 3600  # 1 hour
LONG_TTL = 86400  # 24 hours
SHORT_TTL = 300  # 5 minutes

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
            CacheService.delete_pattern("novel_*")
            CacheService.delete_pattern("chapter:*")
            CacheService.delete_pattern("popular_novels:*")
            CacheService.delete_pattern("latest_novels:*")
            CacheService.delete_pattern("novel_categories")
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
            key = f"{key_prefix}:{arg_str}:{kwarg_str}"
            
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