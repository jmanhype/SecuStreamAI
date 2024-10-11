import dspy
import logging
import json
from typing import Dict
from src.services.cache_service import cache_service  # Updated import
import torch
from src.ml_models.pytorch_model import SecurityEventModel
from src.utils.cache_service import cache_service

logger = logging.getLogger(__name__)

class SecurityEventAnalyzer(dspy.Signature):
    """Signature for analyzing security events."""
    context = dspy.InputField()
    event_description = dspy.InputField()
    risk_level = dspy.OutputField()
    action = dspy.OutputField()
    analysis = dspy.OutputField()

class EnhancedEventAnalyzer(dspy.Module):
    """Uses the DSPy-configured LLM to perform detailed analysis and provide recommendations."""

    def __init__(self):
        super().__init__()
        self.analyzer = dspy.ChainOfThought(SecurityEventAnalyzer)

    def forward(self, context, event_description):
        """Generate a detailed analysis and recommendations based on the event description."""
        try:
            # Generate response from DSPy LLM
            response = self.analyzer(context=context, event_description=event_description)
            
            return {
                "risk_level": response.risk_level,
                "action": response.action,
                "analysis": response.analysis
            }
        except Exception as e:
            logger.error(f"Error in LLM analysis: {str(e)}")
            return {
                "risk_level": "error",
                "action": "N/A",
                "analysis": f"Could not analyze due to error: {str(e)}"
            }

class RuleBasedAnalyzer:
    def analyze(self, context, event_description):
        if "login" in context.lower():
            if "failed" in event_description.lower():
                return {
                    "risk_level": "medium",
                    "action": "Monitor and investigate",
                    "analysis": "Failed login attempt detected."
                }
            elif "successful" in event_description.lower():
                return {
                    "risk_level": "low",
                    "action": "Log and monitor",
                    "analysis": "Successful login event."
                }
        elif "file_access" in context.lower():
            if "sensitive" in event_description.lower():
                return {
                    "risk_level": "high",
                    "action": "Investigate immediately",
                    "analysis": "Sensitive file access detected."
                }
        # Add more rules as needed
        return None

def perform_inference(model_input: Dict, use_cache: bool = True) -> Dict:
    event = model_input['inputs']
    cache_key = f"{event['context']}::{event['event_description']}"
    
    if use_cache:
        cached_result = cache_service.get(cache_key)
        if cached_result:
            logger.info(f"Cache hit for key: {cache_key}")
            return cached_result

    # Decision-making mechanism
    method = decide_inference_method(event)
    
    if method == 'rule_based':
        rule_based = RuleBasedAnalyzer()
        result = rule_based.analyze(event['context'], event['event_description'])
        if result:
            logger.info("Rule-based analysis applied.")
            return result
    
    if method == 'pytorch':
        pytorch_model = SecurityEventModel.load('src/models/pytorch_model.pth')
        result = pytorch_model.predict(event)
        logger.info("PyTorch model inference applied.")
        return result
    
    # Default to DSPy-based LLM analysis
    dspy_analyzer = EnhancedEventAnalyzer()
    result = dspy_analyzer(context=event['context'], event_description=event['event_description'])
    logger.info("DSPy-based LLM analysis applied.")
    
    if use_cache:
        cache_service.set(cache_key, result)
    
    return result

def decide_inference_method(event: Dict) -> str:
    if is_common_event(event):
        return 'rule_based'
    elif requires_quick_classification(event):
        return 'pytorch'
    else:
        return 'dspy'

def is_common_event(event: Dict) -> bool:
    common_events = ['login', 'logout', 'file_access']
    return event.get('event_type') in common_events and event.get('severity', '').lower() in ['low', 'medium']

def requires_quick_classification(event: Dict) -> bool:
    return event.get('severity', '').lower() == 'high' or 'urgent' in event.get('description', '').lower()