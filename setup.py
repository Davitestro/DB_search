from pathlib import Path
from setuptools import find_packages, setup

README = Path(__file__).parent / "README.md"

setup(
    name="db-search",
    version="0.1.0",
    description="A hybrid search system combining BM25, semantic search, and reranking",
    long_description=README.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="DB Search Contributors",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy>=1.24.0,<2.0.0",
        "pandas>=2.0.0,<3.0.0",
        "scikit-learn>=1.3.0,<2.0.0",
        "sentence-transformers>=2.2.0,<3.0.0",
        "torch>=2.0.0,<3.0.0",
        "faiss-cpu>=1.7.0,<2.0.0",
        "rank-bm25>=0.2.0,<1.0.0",
        "python-dotenv>=1.0.0,<2.0.0",
        "pydantic>=2.0.0,<3.0.0",
        "tqdm>=4.66.0,<5.0.0",
        "faker>=19.0.0,<20.0.0",
        "transformers>=4.30.0,<5.0.0",
        "tokenizers>=0.13.0,<1.0.0",
    ],
    python_requires=">=3.9",
)
