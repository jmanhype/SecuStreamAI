from src.celery_app import app
from src.scripts.nightly_finetune import finetune_model

@app.task
def nightly_finetune():
    finetune_model()