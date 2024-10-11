import random
import pytest
import asyncio
import time
from fastapi.testclient import TestClient
from src.main import app
from src.pipeline.model_inference import perform_inference

client = TestClient(app)

def generate_random_event():
    contexts = ["login", "network", "system"]
    descriptions = ["Successful login", "Failed login", "Large data transfer", "New process created", "System shutdown"]
    severities = ["low", "medium", "high"]
    
    return {
        "context": random.choice(contexts),
        "event_description": random.choice(descriptions),
        "severity": random.choice(severities)
    }

@pytest.mark.asyncio
async def test_inference_performance():
    start_time = time.time()
    events = [generate_random_event() for _ in range(100)]
    tasks = [perform_inference({"inputs": event}) for event in events]
    results = await asyncio.gather(*tasks)
    end_time = time.time()
    
    assert len(results) == 100
    processing_time = end_time - start_time
    assert processing_time < 5, f"Processing took {processing_time} seconds, which is more than the expected 5 seconds"
    
    print(f"Processed 100 events in {processing_time} seconds")

@pytest.mark.asyncio
async def test_concurrent_event_processing():
    num_events = 100
    concurrency = 10

    async def process_event(event_data):
        response = await client.post("/api/v1/events/", json=event_data)
        assert response.status_code == 201
        event_id = response.json()["id"]
        analysis_response = await client.post("/api/v1/analyze/", json={"event_id": event_id})
        assert analysis_response.status_code == 200

    start_time = time.time()
    events = [generate_random_event() for _ in range(num_events)]
    semaphore = asyncio.Semaphore(concurrency)

    async def bounded_process_event(event):
        async with semaphore:
            await process_event(event)

    await asyncio.gather(*[bounded_process_event(event) for event in events])
    end_time = time.time()

    total_time = end_time - start_time
    events_per_second = num_events / total_time

    print(f"Processed {num_events} events concurrently in {total_time:.2f} seconds")
    print(f"Events per second: {events_per_second:.2f}")

    assert events_per_second > 20  # Adjust this threshold based on your performance requirements

import pytest
import time
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_event_processing_performance():
    start_time = time.time()
    num_events = 100
    
    for _ in range(num_events):
        event_data = {
            "event_type": "network_traffic",
            "timestamp": int(time.time()),
            "source_ip": "192.168.1.100",
            "destination_ip": "10.0.0.1",
            "severity": "medium",
            "description": "Test event for performance",
        }
        response = client.post("/api/v1/events/", json=event_data)
        assert response.status_code == 201
    
    end_time = time.time()
    total_time = end_time - start_time
    events_per_second = num_events / total_time
    
    print(f"Processed {num_events} events in {total_time:.2f} seconds")
    print(f"Events per second: {events_per_second:.2f}")
    
    assert events_per_second > 10  # Adjust this threshold based on your performance requirements