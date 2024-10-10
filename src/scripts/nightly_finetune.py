import dspy
from dspy.teleprompt.finetune import BootstrapFinetune
from src.pipeline.model_inference import SecurityEventAnalyzer, EnhancedEventAnalyzer
from src.db.database import SessionLocal
from src.models.db_models import Event
from src.core.config import settings
import yaml
import torch
from src.ml_models.pytorch_model import SecurityEventModel
from src.utils.data_preparation import prepare_data
from src.utils.model_training import train_model
from dspy import BootstrapFinetune
import dspy
from src.config.event_config import event_types, risk_levels

def load_dspy_config():
    with open('src/config/dspy_config.yaml', 'r') as file:
        return yaml.safe_load(file)

def get_training_data():
    db = SessionLocal()
    events = db.query(Event).all()
    training_data = [
        {
            "context": f"Event type: {event.event_type}, Severity: {event.severity}",
            "event_description": event.description,
            "risk_level": event.risk_level,
            "action": event.action,
            "analysis": event.analysis
        }
        for event in events
    ]
    db.close()
    return training_data

def finetune_model():
    # DSPy model fine-tuning
    config = load_dspy_config()
    training_data = get_training_data()

    openai_lm = dspy.OpenAI(
        model=config['language_model']['name'],
        api_key=settings.OPENAI_API_KEY
    )

    finetuner = BootstrapFinetune(
        metric=lambda gold, pred, trace: gold.risk_level == pred.risk_level
    )

    analyzer = EnhancedEventAnalyzer()
    finetuned_model = finetuner.compile(
        analyzer,
        trainset=training_data,
        target=config['language_model']['name'],
        bsize=8,
        epochs=1,
        lr=5e-5
    )

    # Save the fine-tuned DSPy model
    finetuned_model.save('src/models/finetuned_model')

    # PyTorch model training
    pytorch_model = SecurityEventModel(num_event_types=len(event_types), num_risk_levels=len(risk_levels))
    train_data = prepare_data(get_training_data())
    train_model(pytorch_model, train_data, num_epochs=10, learning_rate=1e-4)
    torch.save(pytorch_model.state_dict(), 'src/models/pytorch_model.pth')

if __name__ == "__main__":
    finetune_model()