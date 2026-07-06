"""
Search functionality using hybrid approach.
"""

import numpy as np
import time
from typing import List, Tuple, Optional
from models.schemas import Document, SearchQuery, SearchResult, SearchResponse
from search.indexer import SearchIndex
from search.embeddings import EmbeddingGenerator
from search.reranker import Reranker
from config.settings import config

class Searcher:
    """Hybrid search system combining BM25 and semantic search."""
    
    def __init__(
        self,
        index: SearchIndex = None,
        embedding_generator: EmbeddingGenerator = None,
        reranker: Reranker = None
    ):
        """Initialize the searcher."""
        if index is None:
            self.index = SearchIndex(embedding_generator)
        else:
            self.index = index
        
        if embedding_generator is None:
            self.embedding_generator = EmbeddingGenerator()
        else:
            self.embedding_generator = embedding_generator
        
        self.reranker = reranker or Reranker()
    
    def search(self, query: SearchQuery) -> SearchResponse:
        """Perform a hybrid search."""
        start_time = time.time()
        
        # Initial candidate retrieval
        candidates = self._get_candidates(query)
        
        # Rerank results
        reranked_results = self.reranker.rerank(
            query.text, 
            candidates, 
            top_k=query.top_k
        )
        
        # Create response
        response = SearchResponse(
            query=query.text,
            results=reranked_results,
            total_results=len(reranked_results),
            processing_time_ms=(time.time() - start_time) * 1000
        )
        
        return response
    
    def _get_candidates(self, query: SearchQuery) -> List[Tuple[Document, float]]:
        """Get initial candidates from BM25 and semantic search."""
        all_scores = {}
        
        # Get BM25 results
        if query.use_bm25 and self.index.bm25_index:
            bm25_scores = self._bm25_search(query.text, config.top_k_initial)
            for doc, score in bm25_scores:
                all_scores[doc.id] = {
                    'document': doc,
                    'bm25_score': score,
                    'semantic_score': 0.0,
                    'combined_score': 0.0
                }
        
        # Get semantic results
        if query.use_semantic and self.index.faiss_index:
            semantic_scores = self._semantic_search(query.text, config.top_k_initial)
            for doc, score in semantic_scores:
                if doc.id in all_scores:
                    all_scores[doc.id]['semantic_score'] = score
                else:
                    all_scores[doc.id] = {
                        'document': doc,
                        'bm25_score': 0.0,
                        'semantic_score': score,
                        'combined_score': 0.0
                    }
        
        # Normalize and combine scores
        results = []
        for doc_id, scores in all_scores.items():
            doc = scores['document']
            
            # Normalize scores
            bm25_score = self._normalize_score(scores['bm25_score'])
            semantic_score = self._normalize_score(scores['semantic_score'])
            
            # Combine scores
            combined = (config.bm25_weight * bm25_score + 
                       config.semantic_weight * semantic_score)
            
            results.append((doc, combined))
        
        # Sort by combined score
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:config.top_k_initial]
    
    def _bm25_search(self, query: str, top_k: int) -> List[Tuple[Document, float]]:
        """Perform BM25 search."""
        tokenized_query = query.lower().split()
        scores = self.index.bm25_index.get_scores(tokenized_query)
        
        # Get top-k indices
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if scores[idx] > 0:
                results.append((self.index.documents[idx], scores[idx]))
        
        return results
    
    def _semantic_search(self, query: str, top_k: int) -> List[Tuple[Document, float]]:
        """Perform semantic search using FAISS."""
        # Encode query
        query_embedding = self.embedding_generator.encode_query(query)
        
        # Search FAISS index
        query_embedding = query_embedding.reshape(1, -1)
        scores, indices = self.index.faiss_index.search(query_embedding, top_k)
        
        # Get documents
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.index.documents):
                results.append((self.index.documents[idx], float(score)))
        
        return results
    
    def _normalize_score(self, score: float) -> float:
        """Normalize a score to [0, 1] range."""
        if score <= 0:
            return 0.0
        # Simple sigmoid-like normalization
        return 1.0 / (1.0 + np.exp(-score))