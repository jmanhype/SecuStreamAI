import json
import redis
import yaml
from typing import Any, Optional, Dict
from core.config import settings
import logging

logger = logging.getLogger(__name__)

# Load Redis configuration
def load_redis_config(path: str = 'src/config/redis_config.yaml') -> Dict:
    with open(path, 'r') as file:
        return yaml.safe_load(file)

redis_config = load_redis_config()

class RedisClient:
    """
    A centralized Redis client for handling various Redis operations.
    """
    def __init__(self):
        try:
            self.redis = redis.Redis(
                host=redis_config['host'],
                port=redis_config['port'],
                db=redis_config['db'],
                decode_responses=True,
                max_connections=redis_config.get('max_connections', 10),
                socket_timeout=redis_config.get('socket_timeout', 5),
                socket_connect_timeout=redis_config.get('socket_connect_timeout', 5),
                retry_on_timeout=redis_config.get('retry_on_timeout', True)
            )
            # Test the connection
            self.redis.ping()
            logger.info("Connected to Redis successfully.")
        except redis.RedisError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise e

    def set(self, key: str, value: Any, expiration: Optional[int] = None) -> bool:
        """
        Set a key-value pair in Redis.

        Args:
            key (str): The key to set.
            value (Any): The value to set (will be JSON serialized if not a string).
            expiration (Optional[int]): Time in seconds for the key to expire.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if isinstance(value, str):
                return self.redis.set(key, value, ex=expiration)
            else:
                serialized = json.dumps(value)
                return self.redis.set(key, serialized, ex=expiration)
        except redis.RedisError as e:
            logger.error(f"Redis SET error for key {key}: {e}")
            return False

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from Redis by key.

        Args:
            key (str): The key to retrieve.

        Returns:
            Optional[Any]: The retrieved value or None if not found.
        """
        try:
            value = self.redis.get(key)
            if value is None:
                return None
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        except redis.RedisError as e:
            logger.error(f"Redis GET error for key {key}: {e}")
            return None

    def delete(self, key: str) -> bool:
        """
        Delete a key from Redis.

        Args:
            key (str): The key to delete.

        Returns:
            bool: True if the key was deleted, False otherwise.
        """
        try:
            return bool(self.redis.delete(key))
        except redis.RedisError as e:
            logger.error(f"Redis DELETE error for key {key}: {e}")
            return False

    def increment(self, key: str) -> Optional[int]:
        """
        Increment the integer value of a key by one.

        Args:
            key (str): The key to increment.

        Returns:
            Optional[int]: The new value after incrementing, or None if failed.
        """
        try:
            return self.redis.incr(key)
        except redis.RedisError as e:
            logger.error(f"Redis INCR error for key {key}: {e}")
            return None

    def add_to_set(self, set_name: str, value: Any) -> bool:
        """
        Add a value to a Redis set.

        Args:
            set_name (str): The name of the set.
            value (Any): The value to add.

        Returns:
            bool: True if the item was added, False otherwise.
        """
        try:
            if not isinstance(value, str):
                value = json.dumps(value)
            return self.redis.sadd(set_name, value) == 1
        except redis.RedisError as e:
            logger.error(f"Redis SADD error for set {set_name}: {e}")
            return False

    def get_set_members(self, set_name: str) -> set:
        """
        Retrieve all members of a Redis set.

        Args:
            set_name (str): The name of the set.

        Returns:
            set: The set members.
        """
        try:
            return self.redis.smembers(set_name)
        except redis.RedisError as e:
            logger.error(f"Redis SMEMBERS error for set {set_name}: {e}")
            return set()

    def get_set_count(self, set_name: str) -> int:
        """
        Get the number of members in a Redis set.

        Args:
            set_name (str): The name of the set.

        Returns:
            int: The count of set members.
        """
        try:
            return self.redis.scard(set_name)
        except redis.RedisError as e:
            logger.error(f"Redis SCARD error for set {set_name}: {e}")
            return 0

    def append_to_list(self, list_name: str, value: Any) -> bool:
        """
        Append a value to a Redis list.

        Args:
            list_name (str): The name of the list.
            value (Any): The value to append.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if not isinstance(value, str):
                value = json.dumps(value)
            self.redis.rpush(list_name, value)
            return True
        except redis.RedisError as e:
            logger.error(f"Redis RPUSH error for list {list_name}: {e}")
            return False

    def get_list_items(self, list_name: str, start: int = 0, end: int = -1) -> list:
        """
        Retrieve items from a Redis list.

        Args:
            list_name (str): The name of the list.
            start (int, optional): Start index. Defaults to 0.
            end (int, optional): End index. Defaults to -1 (all).

        Returns:
            list: The list items.
        """
        try:
            items = self.redis.lrange(list_name, start, end)
            processed_items = []
            for item in items:
                try:
                    processed_items.append(json.loads(item))
                except json.JSONDecodeError:
                    processed_items.append(item)
            return processed_items
        except redis.RedisError as e:
            logger.error(f"Redis LRANGE error for list {list_name}: {e}")
            return []

    def flush_db(self) -> bool:
        """
        Flush the entire Redis database.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.redis.flushdb()
            logger.info("Redis database flushed successfully.")
            return True
        except redis.RedisError as e:
            logger.error(f"Redis FLUSHDB error: {e}")
            return False

# Create a global instance of the RedisClient
redis_client = RedisClient()
