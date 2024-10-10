import pytest
import asyncio
from src.pipeline.model_inference import perform_inference

@pytest.mark.asyncio
async def test_concurrent_inference():
    events = [
        {"context": "login", "event_description": "Failed login attempt", "severity": "medium"},
        {"context": "network", "event_description": "Unusual traffic pattern", "severity": "high"},
        {"context": "system", "event_description": "Unexpected shutdown", "severity": "critical"}
    ]
    
    tasks = [perform_inference({"inputs": event}) for event in events]
    results = await asyncio.gather(*tasks)
    
    assert len(results) == 3
    for result in results:
        assert "risk_level" in result
        assert "action" in result
        assert "analysis" in result

@pytest.mark.asyncio
async def test_inference_timeout():
    slow_event = {"context": "slow", "event_description": "This event takes too long to process"}
    
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(perform_inference({"inputs": slow_event}), timeout=0.1)