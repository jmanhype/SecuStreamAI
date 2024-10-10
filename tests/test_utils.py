import pytest
from src.utils.time_utils import timestamp_to_datetime, datetime_to_timestamp
from src.utils.ip_utils import is_valid_ip, get_ip_geolocation
from datetime import datetime

def test_timestamp_to_datetime():
    timestamp = 1633036800
    dt = timestamp_to_datetime(timestamp)
    assert isinstance(dt, datetime)
    assert dt.year == 2021
    assert dt.month == 10
    assert dt.day == 1

def test_datetime_to_timestamp():
    dt = datetime(2021, 10, 1, 12, 0, 0)
    timestamp = datetime_to_timestamp(dt)
    assert timestamp == 1633089600

@pytest.mark.parametrize("ip,expected", [
    ("192.168.1.1", True),
    ("256.0.0.1", False),
    ("10.0.0.0", True),
    ("invalid_ip", False),
])
def test_is_valid_ip(ip, expected):
    assert is_valid_ip(ip) == expected

def test_get_ip_geolocation():
    ip = "8.8.8.8"  # Google's public DNS
    geolocation = get_ip_geolocation(ip)
    assert "country" in geolocation
    assert "city" in geolocation
    assert "latitude" in geolocation
    assert "longitude" in geolocation