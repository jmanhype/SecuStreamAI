import torch
from transformers import BertTokenizer
from src.config.event_config import event_types, risk_levels

def prepare_data(events):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    input_ids = []
    attention_masks = []
    other_features = []
    event_type_labels = []
    risk_level_labels = []

    for event in events:
        encoded = tokenizer.encode_plus(
            event['description'],
            add_special_tokens=True,
            max_length=512,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt',
            truncation=True
        )
        
        input_ids.append(encoded['input_ids'])
        attention_masks.append(encoded['attention_mask'])
        
        other_features.append(torch.tensor([
            int(event['source_ip'].split('.')[-1]),
            int(event['destination_ip'].split('.')[-1]),
            ['low', 'medium', 'high'].index(event['severity'].lower()),
            hash(event['user_id']) % 100,
            hash(event['device_id']) % 100,
            event['timestamp']
        ], dtype=torch.float32))
        
        event_type_labels.append(event_types.index(event['event_type']))
        risk_level_labels.append(risk_levels.index(event['risk_level']))

    return {
        'input_ids': torch.cat(input_ids, dim=0),
        'attention_masks': torch.cat(attention_masks, dim=0),
        'other_features': torch.stack(other_features),
        'event_type_labels': torch.tensor(event_type_labels),
        'risk_level_labels': torch.tensor(risk_level_labels)
    }