"""
Intelligent document chunking for optimal RAG performance.
"""

from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import re


class ChunkType(Enum):
    """Types of chunks that can be created."""
    STANDARD = "standard"
    HIERARCHICAL = "hierarchical"
    SEMANTIC = "semantic"


@dataclass
class Chunk:
    """Represents a document chunk with metadata."""
    content: str
    chunk_type: ChunkType
    parent_id: str = None
    depth_level: int = 0
    metadata: Dict[str, Any] = None


class IntelligentChunker:
    """Intelligent document chunking with multiple strategies."""
    
    def __init__(
        self,
        base_chunk_size: int = 1000,
        chunk_overlap: int = 200,
        enable_hierarchical: bool = True,
        enable_semantic: bool = True
    ):
        self.base_chunk_size = base_chunk_size
        self.chunk_overlap = chunk_overlap
        self.enable_hierarchical = enable_hierarchical
        self.enable_semantic = enable_semantic
    
    async def chunk_document(
        self,
        content: str,
        document_id: str,
        metadata: Dict[str, Any] = None
    ) -> Tuple[List[Chunk], Dict[str, Any]]:
        """
        Chunk a document using intelligent strategies.
        
        Returns:
            Tuple of (chunks, chunk_metadata)
        """
        
        chunks = []
        chunk_metadata = {}
        
        # Simple chunking for now
        # Split by paragraphs first
        paragraphs = content.split('\n\n')
        
        current_chunk = ""
        chunk_index = 0
        
        for paragraph in paragraphs:
            # If adding this paragraph would exceed chunk size, save current chunk
            if len(current_chunk) + len(paragraph) > self.base_chunk_size and current_chunk:
                chunks.append(Chunk(
                    content=current_chunk.strip(),
                    chunk_type=ChunkType.STANDARD,
                    parent_id=document_id,
                    metadata={
                        'chunk_index': chunk_index,
                        'document_type': metadata.get('document_type', 'unknown') if metadata else 'unknown'
                    }
                ))
                
                # Start new chunk with overlap
                overlap_text = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else current_chunk
                current_chunk = overlap_text + " " + paragraph
                chunk_index += 1
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
        
        # Add final chunk if any content remains
        if current_chunk.strip():
            chunks.append(Chunk(
                content=current_chunk.strip(),
                chunk_type=ChunkType.STANDARD,
                parent_id=document_id,
                metadata={
                    'chunk_index': chunk_index,
                    'document_type': metadata.get('document_type', 'unknown') if metadata else 'unknown'
                }
            ))
        
        # Metadata about the chunking process
        chunk_metadata = {
            'total_chunks': len(chunks),
            'chunking_strategy': 'paragraph_based',
            'average_chunk_size': sum(len(c.content) for c in chunks) / len(chunks) if chunks else 0
        }
        
        return chunks, chunk_metadata
