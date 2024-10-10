import json
from kafka import KafkaConsumer

consumer = KafkaConsumer('events', bootstrap_servers=['localhost:9092'], 
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

def consume_events():
    for message in consumer:
        try:
            yield message.value
        except json.JSONDecodeError:
            print(f"Failed to parse message: {message.value}")