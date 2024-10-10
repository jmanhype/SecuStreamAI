import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import BertModel, BertTokenizer
from src.config.event_config import event_types, risk_levels

class SecurityEventModel(nn.Module):
    def __init__(self, num_event_types, num_risk_levels):
        super(SecurityEventModel, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        
        self.fc_event_type = nn.Linear(self.bert.config.hidden_size, num_event_types)
        self.fc_risk_level = nn.Linear(self.bert.config.hidden_size, num_risk_levels)
        
        # Additional layers for other features
        self.fc_other = nn.Linear(6, 64)  # 6 for source_ip, destination_ip, severity, user_id, device_id, timestamp
        
        # Combine BERT output with other features
        self.fc_combined = nn.Linear(self.bert.config.hidden_size + 64, self.bert.config.hidden_size)

    def forward(self, input_ids, attention_mask, other_features):
        # Process text data through BERT
        bert_output = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = bert_output.pooler_output
        
        # Process other features
        other_output = F.relu(self.fc_other(other_features))
        
        # Combine BERT output with other features
        combined = torch.cat((pooled_output, other_output), dim=1)
        combined_output = F.relu(self.fc_combined(combined))
        
        # Event type classification
        event_type_logits = self.fc_event_type(combined_output)
        
        # Risk level assessment
        risk_level_logits = self.fc_risk_level(combined_output)
        
        return event_type_logits, risk_level_logits

    def predict(self, event):
        # Tokenize the description
        inputs = self.tokenizer(event['description'], return_tensors='pt', padding=True, truncation=True, max_length=512)
        
        # Prepare other features
        other_features = torch.tensor([
            int(event['source_ip'].split('.')[-1]),  # Use last octet of IP as a feature
            int(event['destination_ip'].split('.')[-1]),
            ['low', 'medium', 'high'].index(event['severity'].lower()),
            hash(event['user_id']) % 100,  # Simple hash to convert user_id to a number
            hash(event['device_id']) % 100,
            event['timestamp']
        ], dtype=torch.float32).unsqueeze(0)  # Add batch dimension
        
        # Forward pass
        with torch.no_grad():
            event_type_logits, risk_level_logits = self(inputs['input_ids'], inputs['attention_mask'], other_features)
        
        # Get predictions
        event_type_pred = torch.argmax(event_type_logits, dim=1).item()
        risk_level_pred = torch.argmax(risk_level_logits, dim=1).item()
        
        return event_type_pred, risk_level_pred

    @classmethod
    def load(cls, path):
        model = cls(num_event_types=len(event_types), num_risk_levels=len(risk_levels))
        model.load_state_dict(torch.load(path))
        model.eval()
        return model

# Function to prepare data for training
def prepare_data(events):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    
    input_ids = []
    attention_masks = []
    other_features = []
    event_type_labels = []
    risk_level_labels = []
    
    for event in events:
        # Tokenize the description
        encoded = tokenizer.encode_plus(
            event['description'],
            add_special_tokens=True,
            max_length=512,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        
        input_ids.append(encoded['input_ids'])
        attention_masks.append(encoded['attention_mask'])
        
        # Prepare other features
        other_features.append(torch.tensor([
            int(event['source_ip'].split('.')[-1]),
            int(event['destination_ip'].split('.')[-1]),
            ['low', 'medium', 'high'].index(event['severity'].lower()),
            hash(event['user_id']) % 100,
            hash(event['device_id']) % 100,
            event['timestamp']
        ], dtype=torch.float32))
        
        # Prepare labels
        event_type_labels.append(event['event_type'])
        risk_level_labels.append(event['risk_level'])
    
    return {
        'input_ids': torch.cat(input_ids, dim=0),
        'attention_mask': torch.cat(attention_masks, dim=0),
        'other_features': torch.stack(other_features),
        'event_type_labels': torch.tensor(event_type_labels),
        'risk_level_labels': torch.tensor(risk_level_labels)
    }

# Training function
def train_model(model, train_data, num_epochs, learning_rate):
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    event_type_criterion = nn.CrossEntropyLoss()
    risk_level_criterion = nn.CrossEntropyLoss()
    
    for epoch in range(num_epochs):
        model.train()
        optimizer.zero_grad()
        
        event_type_logits, risk_level_logits = model(
            train_data['input_ids'],
            train_data['attention_mask'],
            train_data['other_features']
        )
        
        event_type_loss = event_type_criterion(event_type_logits, train_data['event_type_labels'])
        risk_level_loss = risk_level_criterion(risk_level_logits, train_data['risk_level_labels'])
        
        total_loss = event_type_loss + risk_level_loss
        total_loss.backward()
        optimizer.step()
        
        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {total_loss.item()}")

# Example usage
if __name__ == "__main__":
    # Assuming we have predefined lists of event types and risk levels
    event_types = ["login", "logout", "file_access", "network_connection", "system_update"]
    risk_levels = ["low", "medium", "high"]
    
    model = SecurityEventModel(num_event_types=len(event_types), num_risk_levels=len(risk_levels))
    
    # Example event for prediction
    example_event = {
        "event_type": "login",
        "timestamp": 1633036800,
        "source_ip": "192.168.1.100",
        "destination_ip": "10.0.0.1",
        "severity": "medium",
        "description": "Failed login attempt from unusual location",
        "user_id": "user123",
        "device_id": "device456",
        "risk_level": "high"
    }
    
    event_type_pred, risk_level_pred = model.predict(example_event)
    print(f"Predicted Event Type: {event_types[event_type_pred]}")
    print(f"Predicted Risk Level: {risk_levels[risk_level_pred]}")
    
    # For training, you would prepare your data and call the train_model function
    # train_data = prepare_data(your_training_events)
    # train_model(model, train_data, num_epochs=10, learning_rate=1e-4)