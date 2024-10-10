import asyncio
import pytest
from src.pipeline.model_inference import perform_inference, decide_inference_method
from unittest.mock import patch

def test_decide_inference_method():
    assert decide_inference_method({"context": "login", "event_description": "Successful login"}) == 'rule_based'
    assert decide_inference_method({"context": "network", "event_description": "Unusual traffic pattern detected"}) == 'dspy'
    assert decide_inference_method({"context": "system", "event_description": "New process created"}) == 'pytorch'

def test_decide_inference_method_edge_cases():
    assert decide_inference_method({"context": "login", "event_description": "Unusual login pattern", "severity": "high"}) == 'pytorch'
    assert decide_inference_method({"context": "unknown", "event_description": "Complex scenario"}) == 'dspy'
    assert decide_inference_method({"context": "network", "event_description": "Normal traffic", "severity": "low"}) == 'rule_based'
    assert decide_inference_method({"context": "system", "event_description": "Critical error", "severity": "critical"}) == 'dspy'

@pytest.mark.parametrize("event", [
    {"context": "unknown", "event_description": "Ambiguous event"},
    {"context": "login", "event_description": "Complex login scenario", "severity": "critical"},
    {"context": "network", "event_description": "Simple network event", "severity": "low"}
])
def test_decide_inference_method_edge_cases(event):
    method = decide_inference_method(event)
    assert method in ['rule_based', 'pytorch', 'dspy']

@pytest.mark.asyncio
async def test_perform_inference_rule_based():
    event = {"context": "login", "event_description": "Failed login attempt"}
    result = await perform_inference({"inputs": event})
    assert "risk_level" in result
    assert "action" in result
    assert "analysis" in result

@pytest.mark.asyncio
async def test_perform_inference_pytorch():
    event = {"context": "system", "event_description": "Unexpected system shutdown"}
    result = await perform_inference({"inputs": event})
    assert "risk_level" in result
    assert "action" in result
    assert "analysis" in result

@pytest.mark.asyncio
async def test_perform_inference_dspy():
    event = {"context": "network", "event_description": "Large data transfer to unknown IP"}
    result = await perform_inference({"inputs": event})
    assert "risk_level" in result
    assert "action" in result
    assert "analysis" in result

@pytest.mark.asyncio
async def test_perform_inference_error_handling():
    invalid_event = {"invalid_key": "invalid_value"}
    with pytest.raises(ValueError):
        await perform_inference({"inputs": invalid_event})

@pytest.mark.asyncio
async def test_perform_inference_logging(caplog):
    event = {"context": "login", "event_description": "Successful login"}
    await perform_inference({"inputs": event})
    assert "Performing inference" in caplog.text

@pytest.mark.asyncio
async def test_perform_inference_with_mocks():
    with patch('src.pipeline.model_inference.rule_based_inference') as mock_rule_based, \
         patch('src.pipeline.model_inference.pytorch_inference') as mock_pytorch, \
         patch('src.pipeline.model_inference.dspy_inference') as mock_dspy:
        
        mock_rule_based.return_value = {"risk_level": "low", "action": "monitor", "analysis": "Normal activity"}
        mock_pytorch.return_value = {"risk_level": "medium", "action": "investigate", "analysis": "Unusual pattern detected"}
        mock_dspy.return_value = {"risk_level": "high", "action": "alert", "analysis": "Potential security threat"}

        events = [
            {"context": "login", "event_description": "Successful login"},
            {"context": "system", "event_description": "Unexpected process started"},
            {"context": "network", "event_description": "Large data transfer to unknown IP"}
        ]

        for event in events:
            result = await perform_inference({"inputs": event})
            assert "risk_level" in result
            assert "action" in result
            assert "analysis" in result

        mock_rule_based.assert_called_once()
        mock_pytorch.assert_called_once()
        mock_dspy.assert_called_once()

@pytest.mark.asyncio
async def test_perform_inference_with_empty_event():
    with pytest.raises(ValueError):
        await perform_inference({"inputs": {}})

@pytest.mark.asyncio
async def test_perform_inference_with_unsupported_method():
    with patch('src.pipeline.model_inference.decide_inference_method', return_value='unsupported_method'):
        with pytest.raises(ValueError):
            await perform_inference({"inputs": {"context": "test", "event_description": "test"}})

@pytest.mark.asyncio
async def test_perform_inference_rule_based():
    event = {"context": "login", "event_description": "Failed login attempt", "severity": "medium"}
    with patch('src.pipeline.model_inference.rule_based_inference') as mock_rule_based:
        mock_rule_based.return_value = {"risk_level": "medium", "action": "investigate", "analysis": "Potential unauthorized access attempt"}
        result = await perform_inference({"inputs": event})
        assert result["risk_level"] == "medium"
        assert result["action"] == "investigate"
        assert "unauthorized access" in result["analysis"].lower()

@pytest.mark.asyncio
async def test_perform_inference_pytorch():
    event = {"context": "system", "event_description": "Unexpected system shutdown", "severity": "high"}
    with patch('src.pipeline.model_inference.pytorch_inference') as mock_pytorch:
        mock_pytorch.return_value = {"risk_level": "high", "action": "alert", "analysis": "Potential system compromise"}
        result = await perform_inference({"inputs": event})
        assert result["risk_level"] == "high"
        assert result["action"] == "alert"
        assert "system compromise" in result["analysis"].lower()

@pytest.mark.asyncio
async def test_perform_inference_dspy():
    event = {"context": "network", "event_description": "Large data transfer to unknown IP", "severity": "critical"}
    with patch('src.pipeline.model_inference.dspy_inference') as mock_dspy:
        mock_dspy.return_value = {"risk_level": "critical", "action": "block", "analysis": "Potential data exfiltration"}
        result = await perform_inference({"inputs": event})
        assert result["risk_level"] == "critical"
        assert result["action"] == "block"
        assert "data exfiltration" in result["analysis"].lower()

@pytest.mark.parametrize("event,expected_method", [
    ({"context": "login", "event_description": "Normal login", "severity": "low"}, "rule_based"),
    ({"context": "system", "event_description": "Complex system behavior", "severity": "medium"}, "pytorch"),
    ({"context": "network", "event_description": "Unusual traffic pattern", "severity": "high"}, "dspy"),
    ({"context": "unknown", "event_description": "Ambiguous event", "severity": "low"}, "rule_based"),
])
def test_decide_inference_method_comprehensive(event, expected_method):
    assert decide_inference_method(event) == expected_method

@pytest.mark.asyncio
async def test_perform_inference_with_external_service_failure():
    event = {"context": "network", "event_description": "Unusual traffic pattern", "severity": "high"}
    with patch('src.pipeline.model_inference.dspy_inference', side_effect=Exception("External service failure")):
        with pytest.raises(Exception) as exc_info:
            await perform_inference({"inputs": event})
        assert "External service failure" in str(exc_info.value)

@pytest.mark.asyncio
async def test_perform_inference_with_invalid_method():
    event = {"context": "unknown", "event_description": "Test event"}
    with patch('src.pipeline.model_inference.decide_inference_method', return_value='invalid_method'):
        with pytest.raises(ValueError, match="Invalid inference method"):
            await perform_inference({"inputs": event})

@pytest.mark.asyncio
async def test_perform_inference_with_timeout():
    event = {"context": "network", "event_description": "Slow processing event"}
    with patch('src.pipeline.model_inference.dspy_inference', side_effect=asyncio.TimeoutError):
        result = await perform_inference({"inputs": event})
        assert result["risk_level"] == "high"
        assert "timeout occurred" in result["analysis"].lower()

@pytest.mark.parametrize("event,expected_method", [
    ({"context": "login", "event_description": "", "severity": "low"}, "rule_based"),
    ({"context": "", "event_description": "Unusual activity", "severity": "high"}, "dspy"),
    ({"context": "system", "event_description": None, "severity": "critical"}, "pytorch"),
])
def test_decide_inference_method_edge_cases(event, expected_method):
    assert decide_inference_method(event) == expected_method
