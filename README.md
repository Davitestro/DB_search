# Smart Search System

A hybrid search system combining BM25, semantic search, and reranking for social media and news data.

## Features

- **Hybrid Search**: Combines BM25 (keyword) and semantic search for better results
- **Semantic Understanding**: Uses Sentence Transformers to understand meaning, not just keywords
- **Reranking**: Cross-encoder model for refining search results
- **Synthetic Data Generation**: Generate realistic social media and news data for testing
- **FAISS Integration**: Fast vector similarity search
- **Production Ready**: Structured code, type hints, and proper error handling

## Installation

Install the dependencies directly from the repository:

```bash
pip install -r requirements.txt
```

Or install the project as a package:

```bash
pip install -e .
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions, coding guidelines, and the pull request checklist.

## Usage
Quick Start

```python
from main import SmartSearchSystem

# Initialize system
system = SmartSearchSystem()

# Generate and index data
documents = system.generate_data(1000)
system.index_data(documents)

# Search
results = system.search("AI technology innovation", top_k=5)
```

## Interactive Mode
```bash
python main.py
```

## Architecture

### Synthetic Data Generator: Creates realistic social media posts and news articles

### Embedding Generator: Converts text to vectors using sentence-transformers

### Search Index: Manages BM25 and FAISS indexes

### Searcher: Performs hybrid search combining multiple approaches

### Reranker: Uses cross-encoder to refine results

## Customization

Modify config/settings.py to adjust:

## Embedding model

Search weights (BM25 vs semantic)

Number of results

Data generation parameters