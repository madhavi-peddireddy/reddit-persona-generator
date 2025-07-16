"""
Utility functions for the Reddit User Persona Generator.
"""

import logging
import os
import re
from typing import List, Dict, Any

from typing import Optional


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('persona_generator.log')
        ]
    )
    
    return logging.getLogger(__name__)


def validate_reddit_url(url: str) -> bool:
    """Validate Reddit user URL format."""
    pattern = r'^https://www\.reddit\.com/user/[^/]+/?'
    return bool(re.match(pattern, url))


def create_output_directories(base_dir: str) -> None:
    """Create necessary output directories."""
    directories = [
        base_dir,
        os.path.join(base_dir, 'scraped_data'),
        'data',
        'data/scraped_data'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def extract_username_from_url(url: str) -> Optional[str]:
    """Extract username from Reddit URL."""
    match = re.search(r'/user/([^/]+)', url)
    return match.group(1) if match else None


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system usage."""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limit length
    return filename[:100]


def format_timestamp(timestamp: float) -> str:
    """Format Unix timestamp to readable string."""
    from datetime import datetime
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def chunk_text(text: str, max_length: int = 4000) -> List[str]:
    """Chunk text into smaller pieces for API calls."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 > max_length:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate basic text similarity."""
    # Simple implementation using word overlap
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0


def clean_text(text: str) -> str:
    """Clean text for analysis."""
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove markdown formatting
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text