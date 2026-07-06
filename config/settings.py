"""
Configuration settings for the search system.
"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class SearchConfig:
    """Configuration class for search system."""
    
    # Embedding model settings
    embedding_model_name: str = "all-MiniLM-L6-v2"
    embedding_dimension: int = 384
    
    # Search settings
    bm25_weight: float = 0.5
    semantic_weight: float = 0.5
    top_k_initial: int = 50
    top_k_final: int = 10
    
    # Data generation settings
    num_samples: int = 1000
    random_seed: int = 42
    
    # File paths
    data_dir: str = "data"
    index_dir: str = "data/indexes"
    
    def __post_init__(self):
        """Create directories if they don't exist."""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.index_dir, exist_ok=True)


# Singleton configuration instance
config = SearchConfig()