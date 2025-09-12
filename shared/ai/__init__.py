"""Shared AI module for RAG Agent."""

from .prompts import ENHANCED_PM_SYSTEM_PROMPT, ENHANCED_CONVERSATIONAL_PM_SYSTEM_PROMPT, get_dynamic_prompt
from .providers import get_llm_model

__all__ = [
    'ENHANCED_PM_SYSTEM_PROMPT',
    'ENHANCED_CONVERSATIONAL_PM_SYSTEM_PROMPT',
    'get_dynamic_prompt', 
    'get_llm_model'
]