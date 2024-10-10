import pytest
from src.services.cache_service import cache_service
from src.services.prometheus_client import increment_event_count, increment_analysis_errors, EVENT_COUNT, ANALYSIS_ERRORS

def test_cache_service():
    key = "test_key"
    value = "test_value"
    
    cache_service.set(key, value)
    assert cache_service.get(key) == value
    
    cache_service.delete(key)
    assert cache_service.get(key) is None

def test_cache_service_expiration():
    key = "expiring_key"
    value = "expiring_value"
    
    cache_service.set(key, value, expire=1)  # expire after 1 second
    assert cache_service.get(key) == value
    
    import time
    time.sleep(1.1)  # wait for slightly more than 1 second
    
    assert cache_service.get(key) is None

def test_prometheus_metrics():
    initial_count = EVENT_COUNT._value.get()
    increment_event_count()
    assert EVENT_COUNT._value.get() == initial_count + 1
    
    initial_errors = ANALYSIS_ERRORS._value.get()
    increment_analysis_errors()
    assert ANALYSIS_ERRORS._value.get() == initial_errors + 1

def test_prometheus_metrics_multiple_increments():
    initial_count = EVENT_COUNT._value.get()
    for _ in range(5):
        increment_event_count()
    assert EVENT_COUNT._value.get() == initial_count + 5

def test_prometheus_metrics_concurrent_increments():
    import threading
    
    initial_count = EVENT_COUNT._value.get()
    num_threads = 10
    
    def increment():
        for _ in range(100):
            increment_event_count()
    
    threads = [threading.Thread(target=increment) for _ in range(num_threads)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    assert EVENT_COUNT._value.get() == initial_count + (num_threads * 100)
