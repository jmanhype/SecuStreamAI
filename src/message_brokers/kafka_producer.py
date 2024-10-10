import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

def produce_event(event):
    if not isinstance(event, dict) or 'event_type' not in event or 'timestamp' not in event:
        raise ValueError("Invalid event format")
    
    message = json.dumps(event).encode('utf-8')
    future = producer.send('events', value=message)
    future.get(timeout=10)  # Wait for the send to complete