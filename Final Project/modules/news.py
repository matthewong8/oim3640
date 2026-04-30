"""
News module: Fetches articles from RSS feeds and returns structured data.
"""

import sys
import warnings

# Suppress cgi module deprecation warning on Python 3.13+
if sys.version_info >= (3, 13):
    warnings.filterwarnings("ignore", category=DeprecationWarning)

import feedparser
from config import (
    RSS_FEEDS,
    MAX_NEWS_ARTICLES,
    BUSINESS_RSS_FEEDS,
    MAX_BUSINESS_ARTICLES,
)


def _fetch_articles(feeds, max_articles, articles_per_feed=3):
    """
    Pull articles from a list of RSS feeds.

    Returns:
        list[dict]: Each dict has keys 'title', 'link', 'source'.
    """
    articles = []

    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
            source = feed.feed.get("title", "Unknown Source")

            for entry in feed.entries[:articles_per_feed]:
                articles.append({
                    "title": entry.get("title", "No title"),
                    "link": entry.get("link", ""),
                    "source": source,
                })
        except Exception as e:
            print(f"  Error fetching feed {feed_url}: {e}")

    return articles[:max_articles]


def get_general_news():
    """Top general world-news headlines."""
    return _fetch_articles(RSS_FEEDS, MAX_NEWS_ARTICLES)


def get_business_news():
    """Top business / finance / M&A headlines."""
    return _fetch_articles(BUSINESS_RSS_FEEDS, MAX_BUSINESS_ARTICLES)


if __name__ == "__main__":
    from pprint import pprint
    print("--- GENERAL ---")
    pprint(get_general_news())
    print("--- BUSINESS ---")
    pprint(get_business_news())
