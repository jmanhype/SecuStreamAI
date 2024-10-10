import pytest
import torch
from src.ml_models.pytorch_model import SecurityEventModel, prepare_data, train_model
from src.config.event_config import event_types, risk_levels
from src.ml_models.continuous_learning import fine_tune_model

@pytest.fixture
def security_event_model():
    return SecurityEventModel(num_event_types=len(event_types), num_risk_levels=len(risk_levels))

@pytest.fixture
def sample_model():
    return SecurityEventModel(num_event_types=5, num_risk_levels=3)

def test_security_event_model_initialization(security_event_model):
    assert security_event_model is not None
    assert hasattr(security_event_model, 'bert')
    assert hasattr(security_event_model, 'fc_event_type')
    assert hasattr(security_event_model, 'fc_risk_level')

def test_model_initialization(sample_model):
    assert isinstance(sample_model, SecurityEventModel)
    assert hasattr(sample_model, 'bert')
    assert hasattr(sample_model, 'fc_event_type')
    assert hasattr(sample_model, 'fc_risk_level')

def test_security_event_model_forward_pass(security_event_model):
    batch_size = 4
    seq_length = 128
    input_ids = torch.randint(0, 1000, (batch_size, seq_length))
    attention_mask = torch.ones((batch_size, seq_length))
    other_features = torch.rand((batch_size, 6))
    
    event_type_logits, risk_level_logits = security_event_model(input_ids, attention_mask, other_features)
    
    assert event_type_logits.shape == (batch_size, len(event_types))
    assert risk_level_logits.shape == (batch_size, len(risk_levels))

def test_model_forward_pass(sample_model):
    input_ids = torch.randint(0, 1000, (1, 512))
    attention_mask = torch.ones((1, 512))
    other_features = torch.rand((1, 6))
    
    event_type_logits, risk_level_logits = sample_model(input_ids, attention_mask, other_features)
    
    assert event_type_logits.shape == (1, 5)
    assert risk_level_logits.shape == (1, 3)

def test_security_event_model_output_range(security_event_model):
    batch_size = 4
    seq_length = 128
    input_ids = torch.randint(0, 1000, (batch_size, seq_length))
    attention_mask = torch.ones((batch_size, seq_length))
    other_features = torch.rand((batch_size, 6))
    
    event_type_logits, risk_level_logits = security_event_model(input_ids, attention_mask, other_features)
    
    assert torch.all(event_type_logits >= -1e6) and torch.all(event_type_logits <= 1e6)
    assert torch.all(risk_level_logits >= -1e6) and torch.all(risk_level_logits <= 1e6)

def test_prepare_data():
    events = [
        {"description": "Failed login attempt", "event_type": 0, "risk_level": 1},
        {"description": "Successful login", "event_type": 1, "risk_level": 0},
    ]
    input_ids, attention_masks, other_features, event_type_labels, risk_level_labels = prepare_data(events)
    
    assert input_ids.shape[0] == 2
    assert attention_masks.shape[0] == 2
    assert other_features.shape == (2, 6)
    assert event_type_labels.shape == (2,)
    assert risk_level_labels.shape == (2,)

@pytest.mark.asyncio
async def test_train_model():
    model = SecurityEventModel(num_event_types=5, num_risk_levels=3)
    events = [
        {"description": "Failed login attempt", "event_type": 0, "risk_level": 1},
        {"description": "Successful login", "event_type": 1, "risk_level": 0},
    ]
    
    initial_params = [param.clone() for param in model.parameters()]
    
    await train_model(model, events, num_epochs=1)
    
    # Check if parameters have been updated
    for initial, current in zip(initial_params, model.parameters()):
        assert not torch.allclose(initial, current)

def test_security_event_model_gradient_flow(security_event_model):
    batch_size = 4
    seq_length = 128
    input_ids = torch.randint(0, 1000, (batch_size, seq_length))
    attention_mask = torch.ones((batch_size, seq_length))
    other_features = torch.rand((batch_size, 6))
    
    event_type_logits, risk_level_logits = security_event_model(input_ids, attention_mask, other_features)
    loss = event_type_logits.sum() + risk_level_logits.sum()
    loss.backward()
    
    for name, param in security_event_model.named_parameters():
        assert param.grad is not None, f"No gradient for {name}"
        assert not torch.isnan(param.grad).any(), f"NaN gradient for {name}"

@pytest.mark.parametrize("batch_size,seq_length", [(1, 64), (8, 256), (16, 512)])
def test_model_with_different_input_sizes(security_model, batch_size, seq_length):
    input_ids = torch.randint(0, 1000, (batch_size, seq_length))
    attention_mask = torch.ones((batch_size, seq_length))
    other_features = torch.rand((batch_size, 6))
    
    event_type_logits, risk_level_logits = security_model(input_ids, attention_mask, other_features)
    
    assert event_type_logits.shape == (batch_size, 5)
    assert risk_level_logits.shape == (batch_size, 3)

from hypothesis import given, strategies as st
import torch
from src.ml_models.pytorch_model import SecurityEventModel

@given(
    batch_size=st.integers(min_value=1, max_value=32),
    seq_length=st.integers(min_value=16, max_value=512),
    num_features=st.integers(min_value=1, max_value=10)
)
def test_security_event_model_property(batch_size, seq_length, num_features):
    model = SecurityEventModel(num_event_types=5, num_risk_levels=3)
    input_ids = torch.randint(0, 1000, (batch_size, seq_length))
    attention_mask = torch.ones((batch_size, seq_length))
    other_features = torch.rand((batch_size, num_features))
    
    event_type_logits, risk_level_logits = model(input_ids, attention_mask, other_features)
    
    assert event_type_logits.shape == (batch_size, 5)
    assert risk_level_logits.shape == (batch_size, 3)
    assert torch.all(torch.isfinite(event_type_logits))
    assert torch.all(torch.isfinite(risk_level_logits))

@given(
    descriptions=st.lists(st.text(), min_size=1, max_size=10),
    event_types=st.lists(st.integers(min_value=0, max_value=4), min_size=1, max_size=10),
    risk_levels=st.lists(st.integers(min_value=0, max_value=2), min_size=1, max_size=10)
)
def test_prepare_data_property(descriptions, event_types, risk_levels):
    events = [
        {"description": desc, "event_type": et, "risk_level": rl}
        for desc, et, rl in zip(descriptions, event_types, risk_levels)
    ]
    input_ids, attention_masks, other_features, event_type_labels, risk_level_labels = prepare_data(events)
    
    assert input_ids.shape[0] == len(events)
    assert attention_masks.shape[0] == len(events)
    assert other_features.shape == (len(events), 6)
    assert event_type_labels.shape == (len(events),)
    assert risk_level_labels.shape == (len(events),)

@pytest.mark.asyncio
async def test_continuous_learning():
    model = SecurityEventModel(num_event_types=5, num_risk_levels=3)
    initial_params = [param.clone() for param in model.parameters()]

    new_events = [
        {"description": "New type of attack", "event_type": 2, "risk_level": 2},
        {"description": "Previously unseen behavior", "event_type": 3, "risk_level": 1},
    ]

    await fine_tune_model(model, new_events)

    # Check if parameters have been updated
    for initial, current in zip(initial_params, model.parameters()):
        assert not torch.allclose(initial, current)

    # Test model performance on new data
    test_event = {"description": "Similar to new attack", "event_type": 2, "risk_level": 2}
    input_ids, attention_mask, other_features, _, _ = prepare_data([test_event])
    event_type_logits, risk_level_logits = model(input_ids, attention_mask, other_features)

    predicted_event_type = torch.argmax(event_type_logits, dim=1).item()
    predicted_risk_level = torch.argmax(risk_level_logits, dim=1).item()

    assert predicted_event_type == 2
    assert predicted_risk_level == 2