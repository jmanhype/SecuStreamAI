import pytest
from scripts.generate_events import generate_random_event, generate_events

def test_generate_random_event():
    event = generate_random_event()
    assert "event_type" in event
    assert "timestamp" in event
    assert "source_ip" in event
    assert "destination_ip" in event
    assert "severity" in event
    assert "description" in event

def test_generate_events():
    num_events = 10
    events = generate_events(num_events)
    assert len(events) == num_events
    for event in events:
        assert "event_type" in event
        assert "timestamp" in event
        assert "source_ip" in event
        assert "destination_ip" in event
        assert "severity" in event
        assert "description" in event

@pytest.mark.parametrize("num_events", [0, 1, 100])
def test_generate_events_with_different_counts(num_events):
    events = generate_events(num_events)
    assert len(events) == num_events