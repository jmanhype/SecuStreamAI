from celery import Celery
from src.core.config import settings

app = Celery('secustreamai')
app.config_from_object(settings, namespace='CELERY')

# Load tasks modules
app.autodiscover_tasks(['src.tasks'])