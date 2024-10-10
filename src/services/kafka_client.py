import json
import logging
from kafka import KafkaProducer
from typing import Dict
from core.config import settings

logger = logging.getLogger(__name__)

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

async def produce_event(topic: str, event: Dict):
    """
    Produce a security event to the specified Kafka topic.

    Args:
        topic (str): The Kafka topic to publish to.
        event (Dict): The security event data.
    """
    try:
        producer.send(topic, value=event)
        producer.flush()
        logger.info(f"Produced event to Kafka topic '{topic}': {event}")
    except Exception as e:
        logger.error(f"Failed to produce event to Kafka topic '{topic}': {str(e)}")
        raise e