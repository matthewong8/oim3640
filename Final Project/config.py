# Configuration for Daily Assistant Agent
# Update these with your personal information

import os
from dotenv import load_dotenv

load_dotenv()

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

# News settings
RSS_FEEDS = [
    "https://feeds.bbc.co.uk/news/rss.xml",
    "https://feeds.theguardian.com/theguardian/world/rss",
]
MAX_NEWS_ARTICLES = 5  # Number of top headlines to include

# Email settings
BRIEFING_TIME = "08:00"  # Time to send briefing (24-hour format)
INCLUDE_CALENDAR = False  # Set to True when Google Calendar is integrated
