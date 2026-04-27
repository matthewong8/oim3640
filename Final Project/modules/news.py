"""
News module: Fetches top news headlines from RSS feeds
"""

import sys
import warnings
# Suppress cgi module warning on Python 3.13+
if sys.version_info >= (3, 13):
    warnings.filterwarnings('ignore', category=DeprecationWarning)

import feedparser
from config import RSS_FEEDS, MAX_NEWS_ARTICLES


def get_news_briefing():
    """
    Fetch top news articles from configured RSS feeds.
    
    Returns:
        str: Formatted news briefing with top headlines
    """
    articles = []
    
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            
            # Extract top articles from this feed
            for entry in feed.entries[:3]:  # 3 articles per feed
                articles.append({
                    "title": entry.get("title", "No title"),
                    "link": entry.get("link", "No link"),
                    "source": feed.feed.get("title", "Unknown Source")
                })
        
        except Exception as e:
            print(f"Error fetching feed {feed_url}: {str(e)}")
    
    # Format for briefing
    if not articles:
        return "TOP NEWS\nNo articles available"
    
    briefing = "TOP NEWS TODAY\n" + "=" * 40 + "\n"
    
    for i, article in enumerate(articles[:MAX_NEWS_ARTICLES], 1):
        briefing += f"\n{i}. {article['title']}\n   Source: {article['source']}\n"
    
    return briefing


if __name__ == "__main__":
    # Test news module
    print(get_news_briefing())
