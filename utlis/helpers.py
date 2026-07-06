"""
Utility helper functions.
"""

import json
import pickle
from typing import Any, Dict, List
from pathlib import Path
from datetime import datetime

def save_json(data: Any, filepath: str):
    """Save data as JSON."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def load_json(filepath: str) -> Any:
    """Load data from JSON."""
    with open(filepath, 'r') as f:
        return json.load(f)

def save_pickle(data: Any, filepath: str):
    """Save data as pickle."""
    with open(filepath, 'wb') as f:
        pickle.dump(data, f)

def load_pickle(filepath: str) -> Any:
    """Load data from pickle."""
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def ensure_directory(path: str):
    """Ensure a directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)

def format_time(seconds: float) -> str:
    """Format time in seconds to human-readable string."""
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining = seconds % 60
        return f"{int(minutes)}m {int(remaining)}s"
    else:
        hours = seconds // 3600
        remaining = seconds % 3600
        minutes = remaining // 60
        return f"{int(hours)}h {int(minutes)}m"