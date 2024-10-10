from prometheus_client import Counter, Histogram, start_http_server
from core.config import settings
import logging

logger = logging.getLogger(__name__)

# Define Prometheus metrics
EVENT_COUNT = Counter('processed_events_total', 'Total number of processed events')
ANALYSIS_ERRORS = Counter('analysis_errors_total', 'Total number of analysis errors')
EVENT_PROCESSING_TIME = Histogram('event_processing_seconds', 'Time spent processing events')

def start_metrics_server():
    """
    Start the Prometheus metrics server.
    """
    try:
        start_http_server(settings.PROMETHEUS_PORT)
        logger.info(f"Prometheus metrics server started on port {settings.PROMETHEUS_PORT}")
    except Exception as e:
        logger.error(f"Failed to start Prometheus metrics server: {e}")

def increment_event_count():
    """
    Increment the total number of processed events.
    """
    EVENT_COUNT.inc()

def increment_analysis_errors():
    """
    Increment the total number of analysis errors.
    """
    ANALYSIS_ERRORS.inc()

def observe_event_processing_time(duration: float):
    """
    Observe the time taken to process an event.

    Args:
        duration (float): Time in seconds spent processing the event.
    """
    EVENT_PROCESSING_TIME.observe(duration)
