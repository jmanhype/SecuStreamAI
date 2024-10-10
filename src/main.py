# src/main.py

import sys
import subprocess

# Ensure we're running in the correct Conda environment
if not sys.prefix.endswith('secustreamai'):
    print("Activating secustreamai Conda environment...")
    subprocess.call(['conda', 'run', '-n', 'secustreamai', 'python'] + sys.argv)
    sys.exit(0)

import asyncio
import json
import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
import uvicorn
from kafka import KafkaConsumer
import redis  # Consider removing if not directly used
import dspy
from pipeline.model_inference import perform_inference
from api.v1.router import api_router
from core.config import settings
from services.cache_service import cache_service  # Existing import for caching
from services.analytics_service import update_risk_counters  # Existing import
from services.prometheus_client import (
    start_metrics_server,
    increment_event_count,
    increment_analysis_errors,
    observe_event_processing_time
)
from services.redis_client import redis_client  # New import
from services.spark_processing import start_spark_processing  # New import
from src.api.dependencies.rate_limiter import rate_limit
from prometheus_fastapi_instrumentator import Instrumentator

# Load environment variables and set up logging
load_dotenv()

import yaml
import logging.config

with open('src/config/logging_config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

# Configure DSPy with OpenAI model
openai_lm = dspy.OpenAI(
    model='gpt-3.5-turbo',
    api_key=settings.OPENAI_API_KEY  # Use settings
)
dspy.settings.configure(lm=openai_lm)

# Remove direct Redis client initialization if not needed
# redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# Initialize Prometheus Instrumentation
instrumentator = Instrumentator()

# Integrate Prometheus middleware
instrumentator.instrument(app).expose(app)

# Include API router with global rate limiting
app.include_router(
    api_router,
    prefix=settings.API_V1_STR,
    dependencies=[Depends(rate_limit(times=100, seconds=3600))]  # 100 requests per hour per IP
)

# Define the REQUEST_TIME metric (Consider removing if using PrometheusClient)
# If kept, move to prometheus_client.py

@dspy.settings.configure(lm=openai_lm)
def process_event(event):
    """Process a single event."""
    try:
        # Start timing the event processing
        import time
        start_time = time.time()
        
        # Prepare the input for the model
        model_input = {
            'inputs': {
                'context': f"Event type: {event['event_type']}, Severity: {event['severity']}",
                'event_description': event['description']
            }
        }

        # Perform analysis using the hybrid approach
        inference_result = perform_inference(model_input)

        # Store analysis result in Redis using cache_service
        event_key = f"event:{event['timestamp']}_{event['event_type']}"
        cache_service.set(event_key, inference_result)  # Updated to use cache_service

        # Update analytics counters
        update_risk_counters(inference_result['risk_level'])

        # Log successful processing
        logger.info(f"Processed event: {event['event_type']} with severity: {event['severity']}")
        logger.info(f"Risk Level: {inference_result['risk_level']}")
        logger.info(f"Analysis: {inference_result['analysis']}")
        logger.info(f"Recommended Action: {inference_result['action']}")

        # Increment Prometheus event counter
        increment_event_count()

        # Record processing time
        duration = time.time() - start_time
        observe_event_processing_time(duration)

    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")
        logger.error(f"Event data: {event}")
        increment_analysis_errors()  # Increment Prometheus error counter

async def kafka_consumer_task():
    """Kafka consumer task to listen for security events and process them."""
    # Kafka consumer configuration
    kafka_server = settings.KAFKA_SERVER
    kafka_topic = settings.KAFKA_TOPIC

    logger.info(f"KAFKA_SERVER is set to: {kafka_server}")
    logger.info(f"KAFKA_TOPIC is set to: {kafka_topic}")

    # Set up Kafka consumer
    consumer = KafkaConsumer(
        kafka_topic,
        bootstrap_servers=[kafka_server],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='security_event_processor',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    logger.info(f"Listening for events on Kafka topic '{kafka_topic}'...")

    # Process messages
    for message in consumer:
        event = message.value
        process_event(event)

@app.on_event("startup")
async def startup_event():
    """
    Startup event to initialize Prometheus metrics and start Kafka consumer.
    """
    # Start Prometheus metrics server
    start_metrics_server()
    logger.info(f"Prometheus metrics available at http://localhost:{settings.PROMETHEUS_PORT}")

    # Start Kafka consumer as a background task
    asyncio.create_task(kafka_consumer_task())

    # Start Spark processing service
    asyncio.create_task(start_spark_processing())
    logger.info("Spark processing service started")

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)