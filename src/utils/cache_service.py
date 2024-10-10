import json
import redis
from typing import Any, Optional
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True
        )

    def set(self, key: str, value: Any, expiration: int = 3600) -> bool:
        """
        Set a key-value pair in the cache.
        
        :param key: The key to set
        :param value: The value to set (will be JSON encoded)
        :param expiration: Time in seconds for the key to expire (default 1 hour)
        :return: True if successful, False otherwise
        """
        try:
            return self.redis_client.set(key, json.dumps(value), ex=expiration)
        except Exception as e:
            logger.error(f"Error setting cache for key {key}: {e}")
            return False

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.
        
        :param key: The key to retrieve
        :return: The value if found, None otherwise
        """
        try:
            value = self.redis_client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            logger.error(f"Error getting cache for key {key}: {e}")
            return None

    def delete(self, key: str) -> bool:
        """
        Delete a key from the cache.
        
        :param key: The key to delete
        :return: True if successful, False otherwise
        """
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            logger.error(f"Error deleting cache for key {key}: {e}")
            return False

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in the cache.
        
        :param key: The key to check
        :return: True if the key exists, False otherwise
        """
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.error(f"Error checking existence for key {key}: {e}")
            return False

    def flush(self) -> bool:
        """
        Flush the entire cache.
        
        :return: True if successful, False otherwise
        """
        try:
            return self.redis_client.flushdb()
        except Exception as e:
            logger.error(f"Error flushing cache: {e}")
            return False

# Create a global instance of the CacheService
cache_service = CacheService()
