# scripts/generate_events.py

import json
import time
import random
from kafka import KafkaProducer
import redis
import argparse
import os

# Kafka producer setup
kafka_server = 'localhost:29092'  # Explicitly set the server address
kafka_topic = 'security-events'  # Explicitly set the topic name

def generate_event():
    """Generate a simulated security event."""
    event_types = [
        'login_attempt', 'firewall_alert', 'access_violation', 'system_anomaly',
        'malware_detection', 'data_exfiltration', 'privilege_escalation', 'ddos_attack'
    ]
    event = {
        'event_type': random.choice(event_types),
        'timestamp': int(time.time()),
        'source_ip': f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
        'destination_ip': f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
        'severity': random.choice(['low', 'medium', 'high', 'critical']),
        'description': "Simulated security event",
        'user_id': f"user_{random.randint(1000, 9999)}",
        'device_id': f"device_{random.randint(100, 999)}"
    }
    return event

def main(kafka_server, topic, redis_host, redis_port, events_per_second):
    """Produce security events to Kafka and Redis at a specified rate."""
    # Initialize Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=kafka_server,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    # Initialize Redis client
    redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)
    
    try:
        while True:
            event = generate_event()
            
            # Send to Kafka
            producer.send(topic, value=event)
            print(f"Sent event to Kafka: {event}")
            
            # Push to Redis list
            redis_client.lpush('event_queue', json.dumps(event))
            print(f"Sent event to Redis: {event}")

            time.sleep(1 / events_per_second)  # Control the event generation rate
    except KeyboardInterrupt:
        print("Event generation stopped.")
    finally:
        # Close Kafka producer and Redis connection
        producer.close()
        redis_client.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate simulated security events')
    parser.add_argument('--kafka-server', default='localhost:29092', help='Kafka server address')
    parser.add_argument('--topic', default='security-events', help='Kafka topic to publish events')
    parser.add_argument('--redis-host', default='localhost', help='Redis server host')
    parser.add_argument('--redis-port', type=int, default=6379, help='Redis server port')
    parser.add_argument('--rate', type=float, default=1.0, help='Events per second')
    args = parser.parse_args()
    
    main(args.kafka_server, args.topic, args.redis_host, args.redis_port, args.rate)
