"""
Result reranking using cross-encoders.
"""

import numpy as np
from typing import List, Tuple
from sentence_transformers import CrossEncoder
from models.schemas import Document, SearchResult

class Reranker:
    """Reranks search results using a cross-encoder model."""
    
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        """Initialize the reranker."""
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the cross-encoder model."""
        print(f"Loading reranker model: {self.model_name}")
        self.model = CrossEncoder(self.model_name)
        print("Reranker model loaded")
    
    def rerank(
        self, 
        query: str, 
        candidates: List[Tuple[Document, float]], 
        top_k: int = 10
    ) -> List[SearchResult]:
        """Rerank candidates using cross-encoder."""
        if not candidates:
            return []
        
        # Prepare pairs for cross-encoder
        pairs = [[query, doc.content] for doc, _ in candidates]
        
        # Get scores
        scores = self.model.predict(pairs)
        
        # Create results
        results = []
        for i, (doc, original_score) in enumerate(candidates):
            cross_score = float(scores[i])
            
            # Combine original and cross-encoder scores
            final_score = 0.3 * original_score + 0.7 * cross_score
            
            result = SearchResult(
                document=doc,
                score=final_score,
                rank=0  # Will be set after sorting
            )
            results.append(result)
        
        # Sort by final score
        results.sort(key=lambda x: x.score, reverse=True)
        
        # Assign ranks
        for i, result in enumerate(results):
            result.rank = i + 1
        
        return results[:top_k]