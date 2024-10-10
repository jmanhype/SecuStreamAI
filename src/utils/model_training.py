import torch
import torch.nn as nn

def train_model(model, train_data, num_epochs, learning_rate):
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0

        for i in range(0, len(train_data['input_ids']), 32):  # batch size of 32
            batch = {k: v[i:i+32] for k, v in train_data.items()}
            
            optimizer.zero_grad()
            
            event_type_logits, risk_level_logits = model(
                batch['input_ids'],
                batch['attention_masks'],
                batch['other_features']
            )
            
            loss = criterion(event_type_logits, batch['event_type_labels']) + \
                   criterion(risk_level_logits, batch['risk_level_labels'])
            
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()

        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {total_loss:.4f}")