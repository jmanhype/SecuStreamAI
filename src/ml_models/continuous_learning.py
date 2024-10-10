import dspy
from dspy.teleprompt.finetune import BootstrapFinetune
from scripts.nightly_finetune import load_dspy_config
from src.pipeline.model_inference import EnhancedEventAnalyzer
from src.core.config import settings
import torch
from src.ml_models.pytorch_model import SecurityEventModel
from src.utils.data_preparation import prepare_data
from src.utils.model_training import train_model

async def fine_tune_model(model, new_events):
    # DSPy model fine-tuning
    config = load_dspy_config()
    
    openai_lm = dspy.OpenAI(
        model=config['language_model']['name'],
        api_key=settings.OPENAI_API_KEY
    )

    finetuner = BootstrapFinetune(
        metric=lambda gold, pred, trace: gold.risk_level == pred.risk_level
    )

    analyzer = EnhancedEventAnalyzer()
    finetuned_model = await finetuner.compile(
        analyzer,
        trainset=new_events,
        target=config['language_model']['name'],
        bsize=8,
        epochs=1,
        lr=5e-5
    )

    # Save the fine-tuned DSPy model
    finetuned_model.save('src/models/finetuned_model')

    # PyTorch model training
    if isinstance(model, SecurityEventModel):
        train_data = prepare_data(new_events)
        await train_model(model, train_data, num_epochs=5, learning_rate=1e-4)
        torch.save(model.state_dict(), 'src/models/pytorch_model.pth')

    return finetuned_model, model