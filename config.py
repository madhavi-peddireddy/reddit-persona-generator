import os
from dotenv import load_dotenv

load_dotenv()

# Reddit API Configuration
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'PersonaGenerator/1.0')

# Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Scraping Configuration
MAX_POSTS = 100
MAX_COMMENTS = 200
REQUEST_DELAY = 1  # seconds between requests