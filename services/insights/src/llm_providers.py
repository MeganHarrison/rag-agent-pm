"""
LLM Manager for Insights Service

Simple wrapper around OpenAI client for generating insights.
"""

import os
import openai
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class LLMManager:
    """Simple LLM client wrapper."""
    
    def __init__(self):
        self.client = openai.AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        )
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    
    async def generate(self, prompt: str, temperature: float = 0.1) -> str:
        """Generate text using the LLM."""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=2000
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"LLM generation failed: {e}")


# Global instance
llm_manager = LLMManager()
