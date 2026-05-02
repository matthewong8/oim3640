# Configuration for Daily Assistant Agent
# Update these with your personal information

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the project root regardless of current working directory
_PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(_PROJECT_ROOT / ".env")

# User Information
USER_NAME = "Matthew"  # Your name for personalization
USER_EMAIL = os.getenv("USER_EMAIL", "matthewnathanielong@gmail.com")
CITY = "Boston"  # Your city for weather

# API Keys (loaded from .env)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GMAIL_USER_EMAIL = os.getenv("GMAIL_USER_EMAIL")  # Gmail account to send from

# Gmail settings
GMAIL_MAX_EMAILS = 20  # Max unread emails to process per run (keep costs down)

# News settings — General world news
RSS_FEEDS = [
    "https://feeds.bbc.co.uk/news/rss.xml",
    "https://feeds.theguardian.com/theguardian/world/rss",
]
MAX_NEWS_ARTICLES = 5  # Number of top general headlines to include

# News settings — Business / Finance / Markets / M&A
BUSINESS_RSS_FEEDS = [
    "https://feeds.bbc.co.uk/news/business/rss.xml",                  # BBC Business
    "https://www.cnbc.com/id/10001147/device/rss/rss.html",           # CNBC Business News
    "https://www.theguardian.com/uk/business/rss",                    # Guardian Business
    "https://feeds.marketwatch.com/marketwatch/topstories/",          # MarketWatch top stories
]
MAX_BUSINESS_ARTICLES = 7  # Number of business headlines to include

# Email settings
BRIEFING_TIME = "08:00"  # Time to send briefing (24-hour format)
INCLUDE_CALENDAR = False  # Set to True when Google Calendar is integrated
