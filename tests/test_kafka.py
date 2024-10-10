import pytest
from unittest.mock import patch, MagicMock
from src.message_brokers.kafka_producer import produce_event
from src.message_brokers.kafka_consumer import consume_events

@pytest.fixture
def mock_kafka_producer():
    with patch('kafka.KafkaProducer') as mock:
        producer = mock.return_value
        producer.send.return_value.get.return_value = MagicMock()
        yield producer

@pytest.fixture
def mock_kafka_consumer():
    with patch('kafka.KafkaConsumer') as mock:
        yield mock.return_value

def test_produce_event(mock_kafka_producer):
    event = {
        "event_type": "login_attempt",
        "timestamp": 1633036800,
        "description": "Failed login attempt"
    }
    produce_event(event)
    mock_kafka_producer.send.assert_called_once_with(
        'events',  # Assuming 'events' is the topic name
        value=b'{"event_type": "login_attempt", "timestamp": 1633036800, "description": "Failed login attempt"}'
    )
    mock_kafka_producer.send.return_value.get.assert_called_once()  # Ensure the future is awaited

def test_consume_events(mock_kafka_consumer):
    mock_messages = [
        MagicMock(value=b'{"event_type": "network_traffic", "timestamp": 1633036800}'),
        MagicMock(value=b'{"event_type": "login_success", "timestamp": 1633037000}')
    ]
    mock_kafka_consumer.__iter__.return_value = mock_messages

    events = list(consume_events())
    assert len(events) == 2
    assert events[0]['event_type'] == 'network_traffic'
    assert events[1]['event_type'] == 'login_success'

@pytest.mark.parametrize("invalid_event", [
    {},
    {"event_type": "invalid"},
    {"timestamp": 1633036800},
])
def test_produce_event_with_invalid_input(mock_kafka_producer, invalid_event):
    with pytest.raises(ValueError):
        produce_event(invalid_event)

def test_consume_events_with_invalid_message(mock_kafka_consumer):
    mock_messages = [
        MagicMock(value=b'{"event_type": "valid_event", "timestamp": 1633036800}'),
        MagicMock(value=b'invalid json'),
        MagicMock(value=b'{"incomplete": "json"'),
    ]
    mock_kafka_consumer.__iter__.return_value = mock_messages

    events = list(consume_events())
    assert len(events) == 1
    assert events[0]['event_type'] == 'valid_event'