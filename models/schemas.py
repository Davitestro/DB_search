"""
Data models for the search system.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Document(BaseModel):
    """Represents a single document in the search system."""
    
    id: str = Field(..., description="Unique document identifier")
    content: str = Field(..., description="Document text content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SearchQuery(BaseModel):
    """Represents a search query."""
    
    text: str = Field(..., description="Search query text")
    top_k: int = Field(10, description="Number of results to return")
    use_semantic: bool = Field(True, description="Use semantic search")
    use_bm25: bool = Field(True, description="Use BM25 search")
    filters: Optional[Dict[str, Any]] = Field(None, description="Metadata filters")


class SearchResult(BaseModel):
    """Represents a single search result."""
    
    document: Document
    score: float = Field(..., description="Relevance score (higher is better)")
    rank: int = Field(..., description="Result rank")


class SearchResponse(BaseModel):
    """Represents the search response."""
    
    query: str
    results: List[SearchResult]
    total_results: int
    processing_time_ms: float