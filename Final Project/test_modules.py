#!/usr/bin/env python
"""
Quick test of all modules without Gmail
"""

print("Testing Daily Assistant Agent modules...\n")

# Test weather
print("[1/3] Testing Weather Module...")
from modules.weather import get_weather_briefing
weather = get_weather_briefing()
print(weather)
print("\n✓ Weather works!\n")

# Test news
print("[2/3] Testing News Module...")
from modules.news import get_news_briefing
news = get_news_briefing()
print(news[:300] + "...\n" if len(news) > 300 else news + "\n")
print("✓ News works!\n")

# Test OpenAI classifier
print("[3/3] Testing OpenAI Email Classifier...")
from modules.claude_classifier import classify_email, generate_reply_draft

test_email = {
    "subject": "Meeting at 2 PM tomorrow",
    "from": "boss@company.com",
    "snippet": "Hi, can we meet at 2 PM tomorrow to discuss the project?"
}

classification = classify_email(test_email["subject"], test_email["from"], test_email["snippet"])
print(f"Classification: {classification}")

if classification == "NEEDS_REPLY":
    draft = generate_reply_draft(test_email["subject"], test_email["from"], test_email["snippet"])
    print(f"Generated Reply:\n{draft}")

print("\n✓ OpenAI Classifier works!\n")
print("=" * 50)
print("✓✓✓ All core modules working! ✓✓✓")
print("=" * 50)
