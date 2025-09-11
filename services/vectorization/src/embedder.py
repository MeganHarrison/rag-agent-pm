"""
Simple embedder for creating document embeddings.
"""

import openai
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Embedder:
    """Simple embedding service using OpenAI."""
    
    def __init__(self):
        self.client = openai.AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        )
        self.model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    
    async def embed_text(self, text: str) -> List[float]:
        """Create embedding for a single text."""
        response = await self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding
    
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for multiple texts."""
        embeddings = []
        for text in texts:
            embedding = await self.embed_text(text)
            embeddings.append(embedding)
        return embeddings


def create_embedder() -> Embedder:
    """Factory function to create embedder."""
    return Embedder()
