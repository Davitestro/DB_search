"""
Embedding generation for semantic search.
"""

import numpy as np
from typing import List, Union
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from config.settings import config

class EmbeddingGenerator:
    """Generates embeddings for documents and queries."""
    
    def __init__(self, model_name: str = None):
        """Initialize the embedding model."""
        if model_name is None:
            model_name = config.embedding_model_name
        
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the SentenceTransformer model."""
        print(f"Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"Model loaded. Embedding dimension: {self.embedding_dim}")
    
    def encode(self, texts: Union[str, List[str]], batch_size: int = 32) -> np.ndarray:
        """Encode text(s) into embeddings."""
        if isinstance(texts, str):
            texts = [texts]
        
        print(f"Encoding {len(texts)} texts...")
        embeddings = []
        
        # Process in batches
        for i in tqdm(range(0, len(texts), batch_size)):
            batch = texts[i:i+batch_size]
            batch_embeddings = self.model.encode(
                batch, 
                convert_to_numpy=True,
                show_progress_bar=False
            )
            embeddings.append(batch_embeddings)
        
        return np.vstack(embeddings)
    
    def encode_documents(self, documents: List[str]) -> np.ndarray:
        """Encode a list of documents."""
        return self.encode(documents)
    
    def encode_query(self, query: str) -> np.ndarray:
        """Encode a single query."""
        return self.encode(query)[0]