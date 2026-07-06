"""
Synthetic data generator for the search system.
"""

import json
import random
from typing import List, Dict, Any
from datetime import datetime, timedelta
from faker import Faker
from tqdm import tqdm
from models.schemas import Document
from config.settings import config

class SyntheticDataGenerator:
    """Generates synthetic social media and news data."""
    
    def __init__(self, seed: int = None):
        """Initialize the generator with a seed for reproducibility."""
        self.faker = Faker()
        if seed:
            Faker.seed(seed)
            random.seed(seed)
        
        # Pre-defined topics and content templates
        self.topics = [
            "technology", "science", "politics", "sports", "entertainment",
            "business", "health", "education", "environment", "travel",
            "food", "fashion", "art", "music", "gaming"
        ]
        
        self.sentiments = ["positive", "neutral", "negative"]
        self.platforms = ["twitter", "facebook", "reddit", "news", "linkedin"]
        
    def generate_document(self) -> Document:
        """Generate a single document with synthetic content."""
        
        # Choose topic and platform
        topic = random.choice(self.topics)
        platform = random.choice(self.platforms)
        sentiment = random.choice(self.sentiments)
        
        # Generate content based on topic
        content = self._generate_content(topic, sentiment)
        
        # Create metadata
        metadata = {
            "topic": topic,
            "platform": platform,
            "sentiment": sentiment,
            "author": self.faker.name(),
            "location": self.faker.city(),
            "hashtags": self._generate_hashtags(topic),
            "engagement": {
                "likes": random.randint(0, 1000),
                "shares": random.randint(0, 500),
                "comments": random.randint(0, 200)
            }
        }
        
        return Document(
            id=self.faker.uuid4(),
            content=content,
            metadata=metadata,
            created_at=self.faker.date_time_between(
                start_date="-30d", 
                end_date="now"
            )
        )
    
    def _generate_content(self, topic: str, sentiment: str) -> str:
        """Generate content based on topic and sentiment."""
        
        templates = {
            "technology": [
                "Just discovered an amazing new AI tool that will revolutionize {field}! {sentiment}",
                "The latest {field} innovations are mind-blowing. Can't wait to see what's next!",
                "Having issues with the new {field} update. Anyone else experiencing this?",
                "Excited to announce our new {field} platform launching next week!",
                "The future of {field} is here and it's incredible!"
            ],
            "science": [
                "New breakthrough in {field} research could change everything we know!",
                "Fascinating study on {field} published today. Results are promising.",
                "Scientists discover unexpected phenomenon in {field} experiment.",
                "The {field} community is buzzing about this latest finding.",
                "Can anyone explain this {field} concept? I'm confused."
            ],
            "politics": [
                "Major policy changes in {field} announced today. What do you think?",
                "Controversial debate on {field} continues to divide opinions.",
                "Exciting developments in {field} legislation! Progress at last!",
                "The {field} situation is getting worse every day. We need action.",
                "Understanding the {field} implications of this new law."
            ],
            "sports": [
                "Incredible match today! The {field} team dominated from start to finish!",
                "Devastating loss for the {field} team. Better luck next time.",
                "Record-breaking performance in {field} competition!",
                "The {field} rivalry continues - who will come out on top?",
                "Training for {field} competition. Wish me luck!"
            ]
        }
        
        # Get template for topic or use generic
        topic_templates = templates.get(topic, [
            "Interesting development in {field}: {sentiment}",
            "Sharing my thoughts on {field} - what's yours?",
            "Just had an amazing experience with {field}!",
            "The {field} landscape is changing rapidly.",
            "Can we talk about {field} for a moment?"
        ])
        
        template = random.choice(topic_templates)
        
        # Sentiment modifiers
        sentiment_modifiers = {
            "positive": ["amazing", "incredible", "fantastic", "great", "exciting"],
            "neutral": ["interesting", "noteworthy", "curious", "standard"],
            "negative": ["concerning", "troubling", "problematic", "disappointing"]
        }
        
        # Fill in template
        content = template.format(
            field=topic,
            sentiment=random.choice(sentiment_modifiers[sentiment])
        )
        
        # Add some randomness
        if random.random() < 0.3:
            content += f" #{self._generate_hashtag(topic)}"
        
        return content
    
    def _generate_hashtags(self, topic: str) -> List[str]:
        """Generate relevant hashtags for a topic."""
        num_hashtags = random.randint(1, 3)
        hashtags = []
        
        base_tags = {
            "technology": ["#tech", "#innovation", "#AI", "#coding", "#future"],
            "science": ["#science", "#research", "#discovery", "#STEM"],
            "politics": ["#politics", "#government", "#election", "#policy"],
            "sports": ["#sports", "#game", "#winning", "#team"],
            "entertainment": ["#entertainment", "#movies", "#music", "#hollywood"]
        }
        
        tags = base_tags.get(topic, ["#trending", "#viral"])
        
        for _ in range(num_hashtags):
            if tags:
                hashtag = random.choice(tags)
                if hashtag not in hashtags:
                    hashtags.append(hashtag)
        
        return hashtags
    
    def _generate_hashtag(self, topic: str) -> str:
        """Generate a single hashtag."""
        return random.choice([
            f"#{topic}",
            f"#{topic}news",
            f"#{topic}life",
            f"#{topic}world",
            f"#{topic}updates"
        ])
    
    def generate_dataset(self, num_samples: int = None) -> List[Document]:
        """Generate a dataset of documents."""
        if num_samples is None:
            num_samples = config.num_samples
        
        print(f"Generating {num_samples} synthetic documents...")
        documents = []
        
        for _ in tqdm(range(num_samples)):
            documents.append(self.generate_document())
        
        return documents
    
    def save_dataset(self, documents: List[Document], filename: str = "synthetic_data.json"):
        """Save dataset to file."""
        filepath = f"{config.data_dir}/{filename}"
        
        data = []
        for doc in documents:
            data.append({
                "id": doc.id,
                "content": doc.content,
                "metadata": doc.metadata,
                "created_at": doc.created_at.isoformat()
            })
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Dataset saved to {filepath}")
        return filepath
    
    def load_dataset(self, filename: str = "synthetic_data.json") -> List[Document]:
        """Load dataset from file."""
        filepath = f"{config.data_dir}/{filename}"
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        documents = []
        for item in data:
            doc = Document(
                id=item["id"],
                content=item["content"],
                metadata=item["metadata"],
                created_at=datetime.fromisoformat(item["created_at"])
            )
            documents.append(doc)
        
        print(f"Loaded {len(documents)} documents from {filepath}")
        return documents