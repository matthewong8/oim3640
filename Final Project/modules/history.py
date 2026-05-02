"""
Briefing history module: Persists each daily briefing as a JSON file.

Each run writes to history/YYYY-MM-DD.json with a snapshot of what was
fetched and classified. This unlocks future features like a weekly digest,
trend graphs, or a Flask dashboard, and is useful for debugging.

Note: email content is intentionally NOT stored — only subject, sender,
classification, and whether a draft was created — to limit how much
personal data lives on disk.
"""

import datetime
import json
import os


# Resolve the history folder relative to the project root, regardless of CWD
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_DIR = os.path.join(_PROJECT_ROOT, "history")


def _ensure_history_dir():
    os.makedirs(HISTORY_DIR, exist_ok=True)


def save_briefing_history(
    weather,
    general_news,
    business_news,
    email_items,
    duration_seconds,
    success,
):
    """
    Save a snapshot of today's briefing to history/YYYY-MM-DD.json.

    Args:
        weather (dict | None): Weather payload from weather.get_weather_data().
        general_news (list[dict]): Articles from news.get_general_news().
        business_news (list[dict]): Articles from news.get_business_news().
        email_items (list[dict]): Classified emails from main.process_emails().
        duration_seconds (int): How long the briefing took to run.
        success (bool): Whether the briefing email was sent successfully.

    Returns:
        str | None: Absolute path to the saved file, or None on failure.
    """
    try:
        _ensure_history_dir()

        today = datetime.date.today()
        now = datetime.datetime.now()

        # Tally email categories without storing any email body content
        category_counts = {"URGENT": 0, "NEEDS_REPLY": 0, "FYI": 0, "CAN_IGNORE": 0}
        sanitized_emails = []
        for item in email_items:
            cat = item.get("classification", "FYI")
            if cat in category_counts:
                category_counts[cat] += 1
            sanitized_emails.append({
                "classification": cat,
                "subject": item.get("subject", ""),
                "from": item.get("from", ""),
                "draft_saved": item.get("draft_saved", False),
            })

        drafts_created = sum(1 for item in email_items if item.get("draft_saved"))

        snapshot = {
            "date": today.isoformat(),
            "timestamp": now.isoformat(timespec="seconds"),
            "duration_seconds": duration_seconds,
            "success": success,
            "weather": weather,
            "general_news": {
                "count": len(general_news),
                "articles": general_news,
            },
            "business_news": {
                "count": len(business_news),
                "articles": business_news,
            },
            "emails": {
                "total": len(email_items),
                "by_category": category_counts,
                "drafts_created": drafts_created,
                "items": sanitized_emails,
            },
        }

        path = os.path.join(HISTORY_DIR, f"{today.isoformat()}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)

        return path

    except Exception as e:
        print(f"  Could not save briefing history: {e}")
        return None
