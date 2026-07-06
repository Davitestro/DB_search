"""
Indexing system for documents.
"""

import numpy as np
import faiss
import pickle
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from rank_bm25 import BM25Okapi
from models.schemas import Document
from search.embeddings import EmbeddingGenerator
from config.settings import config

class SearchIndex:
    """Manages both BM25 and FAISS indexes."""
    
    def __init__(self, embedding_generator: EmbeddingGenerator = None):
        """Initialize the search index."""
        self.documents: List[Document] = []
        self.bm25_index: Optional[BM25Okapi] = None
        self.faiss_index: Optional[faiss.Index] = None
        self.embeddings: Optional[np.ndarray] = None
        
        if embedding_generator is None:
            self.embedding_generator = EmbeddingGenerator()
        else:
            self.embedding_generator = embedding_generator
        
        # Tokenized corpus for BM25
        self.tokenized_corpus: List[List[str]] = []
    
    def add_documents(self, documents: List[Document]):
        """Add documents to the index."""
        print(f"Adding {len(documents)} documents to index...")
        
        # Store documents
        self.documents.extend(documents)
        
        # Prepare for BM25
        self.tokenized_corpus.extend([
            doc.content.lower().split() 
            for doc in documents
        ])
        
        # Build BM25 index
        self._build_bm25_index()
        
        # Generate embeddings and build FAISS index
        self._build_faiss_index()
        
        print(f"Index built with {len(self.documents)} documents")
    
    def _build_bm25_index(self):
        """Build the BM25 index."""
        if self.tokenized_corpus:
            self.bm25_index = BM25Okapi(self.tokenized_corpus)
            print(f"BM25 index built with {len(self.tokenized_corpus)} documents")
    
    def _build_faiss_index(self):
        """Build the FAISS index for semantic search."""
        if not self.documents:
            return
        
        # Generate embeddings
        texts = [doc.content for doc in self.documents]
        self.embeddings = self.embedding_generator.encode_documents(texts)
        
        # Create FAISS index
        dimension = self.embeddings.shape[1]
        self.faiss_index = faiss.IndexFlatIP(dimension)  # Inner product for similarity
        self.faiss_index.add(self.embeddings)
        
        print(f"FAISS index built with {self.faiss_index.ntotal} vectors")
    
    def save(self, index_path: str = None):
        """Save the index to disk."""
        if index_path is None:
            index_path = f"{config.index_dir}/search_index"
        
        Path(index_path).mkdir(parents=True, exist_ok=True)
        
        # Save documents
        with open(f"{index_path}/documents.pkl", 'wb') as f:
            pickle.dump(self.documents, f)
        
        # Save BM25
        with open(f"{index_path}/bm25_index.pkl", 'wb') as f:
            pickle.dump(self.bm25_index, f)
        
        # Save tokenized corpus
        with open(f"{index_path}/tokenized_corpus.pkl", 'wb') as f:
            pickle.dump(self.tokenized_corpus, f)
        
        # Save FAISS index
        faiss.write_index(self.faiss_index, f"{index_path}/faiss_index.bin")
        
        # Save embeddings
        with open(f"{index_path}/embeddings.npy", 'wb') as f:
            np.save(f, self.embeddings)
        
        print(f"Index saved to {index_path}")
    
    def load(self, index_path: str = None):
        """Load the index from disk."""
        if index_path is None:
            index_path = f"{config.index_dir}/search_index"
        
        # Load documents
        with open(f"{index_path}/documents.pkl", 'rb') as f:
            self.documents = pickle.load(f)
        
        # Load BM25
        with open(f"{index_path}/bm25_index.pkl", 'rb') as f:
            self.bm25_index = pickle.load(f)
        
        # Load tokenized corpus
        with open(f"{index_path}/tokenized_corpus.pkl", 'rb') as f:
            self.tokenized_corpus = pickle.load(f)
        
        # Load FAISS index
        self.faiss_index = faiss.read_index(f"{index_path}/faiss_index.bin")
        
        # Load embeddings
        with open(f"{index_path}/embeddings.npy", 'rb') as f:
            self.embeddings = np.load(f)
        
        print(f"Index loaded from {index_path}")