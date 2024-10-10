import json
import logging
from typing import Dict
from src.pipeline.model_inference import perform_inference
from src.services.kafka_client import produce_event
from src.services.cache_service import cache_service  # New import

logger = logging.getLogger(__name__)

async def process_event(event: Dict) -> Dict:
    """
    Process a single security event.

    Args:
        event (Dict): The security event data.

    Returns:
        Dict: The result of the event processing.
    """
    try:
        # Perform inference on the event
        inference_result = perform_inference({'inputs': event})

        # Store the analysis result in Redis using cache_service
        event_key = f"event:{event['timestamp']}_{event['event_type']}"
        cache_service.set(event_key, inference_result)  # Updated to use cache_service

        logger.info(f"Processed event: {event['event_type']} with severity: {event['severity']}")
        logger.info(f"Risk Level: {inference_result['risk_level']}")
        logger.info(f"Analysis: {inference_result['analysis']}")
        logger.info(f"Recommended Action: {inference_result['action']}")

        # Produce the processed event to Kafka (optional, if needed)
        await produce_event('processed_events', inference_result)

        return inference_result

    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")
        logger.error(f"Event data: {event}")
        raise e