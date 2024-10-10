import pytest
from unittest.mock import patch, MagicMock
from src.services.redis_client import RedisClient

@pytest.fixture
def mock_redis():
    with patch('redis.Redis') as mock:
        yield mock.return_value

def test_set_cache(mock_redis):
    redis_client = RedisClient()
    redis_client.set('test_key', 'test_value')
    mock_redis.set.assert_called_once_with('test_key', 'test_value')

def test_get_cache(mock_redis):
    mock_redis.get.return_value = b'test_value'
    redis_client = RedisClient()
    value = redis_client.get('test_key')
    assert value == 'test_value'
    mock_redis.get.assert_called_once_with('test_key')

def test_delete_cache(mock_redis):
    redis_client = RedisClient()
    redis_client.delete('test_key')
    mock_redis.delete.assert_called_once_with('test_key')