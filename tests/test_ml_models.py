import pytest
import torch
from src.ml_models.pytorch_model import SecurityEventModel

@pytest.fixture
def security_model():
    return SecurityEventModel(num_event_types=5, num_risk_levels=3)

def test_model_initialization(security_model):
    assert isinstance(security_model, SecurityEventModel)
    assert hasattr(security_model, 'bert')
    assert hasattr(security_model, 'fc_event_type')
    assert hasattr(security_model, 'fc_risk_level')

def test_model_forward_pass(security_model):
    batch_size = 4
    seq_length = 128
    input_ids = torch.randint(0, 1000, (batch_size, seq_length))
    attention_mask = torch.ones((batch_size, seq_length))
    other_features = torch.rand((batch_size, 6))
    
    event_type_logits, risk_level_logits = security_model(input_ids, attention_mask, other_features)
    
    assert event_type_logits.shape == (batch_size, 5)
    assert risk_level_logits.shape == (batch_size, 3)

def test_model_output_range(security_model):
    batch_size = 4
    seq_length = 128
    input_ids = torch.randint(0, 1000, (batch_size, seq_length))
    attention_mask = torch.ones((batch_size, seq_length))
    other_features = torch.rand((batch_size, 6))
    
    event_type_logits, risk_level_logits = security_model(input_ids, attention_mask, other_features)
    
    assert torch.all(event_type_logits >= -1e6) and torch.all(event_type_logits <= 1e6)
    assert torch.all(risk_level_logits >= -1e6) and torch.all(risk_level_logits <= 1e6)

def test_model_training_step(security_model):
    optimizer = torch.optim.Adam(security_model.parameters())
    
    batch_size = 4
    seq_length = 128
    input_ids = torch.randint(0, 1000, (batch_size, seq_length))
    attention_mask = torch.ones((batch_size, seq_length))
    other_features = torch.rand((batch_size, 6))
    event_type_labels = torch.randint(0, 5, (batch_size,))
    risk_level_labels = torch.randint(0, 3, (batch_size,))
    
    event_type_logits, risk_level_logits = security_model(input_ids, attention_mask, other_features)
    loss = torch.nn.functional.cross_entropy(event_type_logits, event_type_labels) + \
           torch.nn.functional.cross_entropy(risk_level_logits, risk_level_labels)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    assert not torch.isnan(loss)
    assert loss > 0