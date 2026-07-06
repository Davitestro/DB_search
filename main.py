"""
Main entry point for the smart search system.
"""

import sys
import time
from typing import List
from models.schemas import Document, SearchQuery, SearchResponse
from data.generator import SyntheticDataGenerator
from search.indexer import SearchIndex
from search.searcher import Searcher
from search.embeddings import EmbeddingGenerator
from config.settings import config

class SmartSearchSystem:
    """Main search system orchestrator."""
    
    def __init__(self):
        """Initialize the search system."""
        self.generator = SyntheticDataGenerator(seed=config.random_seed)
        self.embedding_generator = EmbeddingGenerator()
        self.index = SearchIndex(self.embedding_generator)
        self.searcher = Searcher(self.index, self.embedding_generator)
        self.documents: List[Document] = []
    
    def generate_data(self, num_samples: int = None) -> List[Document]:
        """Generate synthetic dataset."""
        if num_samples is None:
            num_samples = config.num_samples
        
        print(f"Generating {num_samples} synthetic documents...")
        self.documents = self.generator.generate_dataset(num_samples)
        return self.documents
    
    def index_data(self, documents: List[Document] = None):
        """Index the documents."""
        if documents is None:
            documents = self.documents
        
        if not documents:
            print("No documents to index.")
            return
        
        self.index.add_documents(documents)
    
    def search(self, query_text: str, top_k: int = 10) -> SearchResponse:
        """Perform a search."""
        query = SearchQuery(
            text=query_text,
            top_k=top_k,
            use_semantic=True,
            use_bm25=True
        )
        
        return self.searcher.search(query)
    
    def save_index(self, path: str = None):
        """Save the index to disk."""
        self.index.save(path)
    
    def load_index(self, path: str = None):
        """Load the index from disk."""
        self.index.load(path)


def main():
    """Main function to demonstrate the search system."""
    
    print("=" * 60)
    print("SMART SEARCH SYSTEM - DEMO")
    print("=" * 60)
    
    # Initialize system
    system = SmartSearchSystem()
    
    # Generate data
    documents = system.generate_data(1000)
    print(f"Generated {len(documents)} documents")
    print("Example document:")
    print(f"  Content: {documents[0].content[:100]}...")
    print(f"  Metadata: {documents[0].metadata}")
    print()
    
    # Index data
    print("Building search index...")
    system.index_data(documents)
    print()
    
    # Test searches
    test_queries = [
        "AI technology innovation",
        "sports team wins championship",
        "new science discovery",
        "political debate controversy",
        "machine learning breakthrough"
    ]
    
    print("Performing test searches:")
    print("-" * 60)
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        
        # Search
        response = system.search(query, top_k=5)
        
        # Display results
        print(f"  Results: {response.total_results} found in {response.processing_time_ms:.2f}ms")
        for i, result in enumerate(response.results, 1):
            doc = result.document
            print(f"  {i}. Score: {result.score:.3f} - {doc.content[:80]}...")
            print(f"     Platform: {doc.metadata.get('platform', 'unknown')}")
            print(f"     Topic: {doc.metadata.get('topic', 'unknown')}")
            print()
    
    print("=" * 60)
    print("Search system ready for use!")
    print("=" * 60)
    
    # Interactive mode
    while True:
        print("\nEnter a search query (or 'quit' to exit):")
        user_query = input("> ").strip()
        
        if user_query.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not user_query:
            continue
        
        response = system.search(user_query, top_k=5)
        print(f"\nSearch results ({response.total_results} found):")
        for i, result in enumerate(response.results, 1):
            doc = result.document
            print(f"\n{i}. Score: {result.score:.3f}")
            print(f"   Content: {doc.content[:150]}...")
            print(f"   Platform: {doc.metadata.get('platform', 'unknown')}")
            print(f"   Topic: {doc.metadata.get('topic', 'unknown')}")
            print(f"   Date: {doc.created_at.strftime('%Y-%m-%d %H:%M')}")


if __name__ == "__main__":
    main()