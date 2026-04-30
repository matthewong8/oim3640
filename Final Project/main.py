"""
Daily Assistant Agent — Main Entry Point

Pipeline (matches proposal MVP):
  1. Fetch weather from OpenWeatherMap
  2. Fetch top general news headlines from RSS feeds
  3. Fetch business / finance / M&A news from RSS feeds
  4. Authenticate with Gmail via OAuth2
  5. Read unread emails, classify each one with AI, and draft replies
     for any email classified as NEEDS_REPLY
  6. Render a beautiful HTML briefing and send it to the user's inbox
"""

import datetime

from modules.weather import get_weather_data
from modules.news import get_general_news, get_business_news
from modules.gmail_reader import authenticate_gmail, get_unread_emails
from modules.claude_classifier import classify_email, generate_reply_draft
from modules.email_sender import send_briefing_email, create_draft_reply
from modules.briefing_html import render_briefing_html
from config import USER_NAME, GMAIL_MAX_EMAILS


# ---------------------------------------------------------------------------
# Console-side fetchers — each returns structured data for the renderer,
# while also printing a concise summary so the user can watch progress.
# A failure in one section never kills the whole run.
# ---------------------------------------------------------------------------

def fetch_weather():
    """Return weather dict (or None) and print a one-line console summary."""
    weather = get_weather_data()
    if weather:
        print(f"  {weather['city']}: {weather['temp']}°C, {weather['description']}")
    else:
        print("  Weather unavailable.")
    return weather


def fetch_general_news():
    articles = get_general_news()
    print(f"  {len(articles)} general headline(s) fetched.")
    for i, a in enumerate(articles, 1):
        print(f"    {i}. {a['title'][:80]}  [{a['source']}]")
    return articles


def fetch_business_news():
    articles = get_business_news()
    print(f"  {len(articles)} business headline(s) fetched.")
    for i, a in enumerate(articles, 1):
        print(f"    {i}. {a['title'][:80]}  [{a['source']}]")
    return articles


def process_emails(service):
    """
    Read unread emails, classify each one, and draft replies for NEEDS_REPLY.

    Returns:
        list[dict]: One dict per email with keys
            classification, subject, from, draft_saved, draft_text.
    """
    emails = get_unread_emails(service, max_results=GMAIL_MAX_EMAILS)

    if not emails:
        print("  Inbox is clear — no unread emails.")
        return []

    print(f"  {len(emails)} unread email(s) found. Classifying...")

    results = []
    valid_categories = {"URGENT", "NEEDS_REPLY", "FYI", "CAN_IGNORE"}

    for email in emails:
        classification = classify_email(
            email["subject"],
            email["from"],
            email["snippet"],
        )
        if classification not in valid_categories:
            classification = "FYI"

        item = {
            "classification": classification,
            "subject": email["subject"],
            "from": email["from"],
            "draft_saved": False,
            "draft_text": None,
        }

        print(f"    [{classification:<11}] {email['subject'][:65]}")

        if classification == "NEEDS_REPLY":
            draft = generate_reply_draft(
                email["subject"],
                email["from"],
                email["snippet"],
            )
            saved = create_draft_reply(service, email["id"], draft)
            item["draft_saved"] = bool(saved)
            item["draft_text"] = draft

        results.append(item)

    return results


# ---------------------------------------------------------------------------
# Plain-text fallback for email clients that won't render HTML
# ---------------------------------------------------------------------------

def build_plain_fallback(weather, general_news, business_news, email_items):
    """A minimal text version for email clients that can't show HTML."""
    today = datetime.date.today().strftime("%A, %B %d, %Y")
    lines = [
        f"GOOD MORNING, {USER_NAME.upper()}",
        f"Your Daily Briefing — {today}",
        "=" * 50,
        "",
        "WEATHER",
    ]

    if weather:
        lines.append(
            f"  {weather['city']}: {weather['temp']}°C "
            f"({weather['description']}), feels like {weather['feels_like']}°C, "
            f"humidity {weather['humidity']}%, wind {weather['wind_speed']} m/s"
        )
    else:
        lines.append("  Weather unavailable.")

    def add_news(label, articles):
        lines.append("")
        lines.append(label.upper())
        if not articles:
            lines.append("  No articles available.")
            return
        for i, a in enumerate(articles, 1):
            lines.append(f"  {i}. {a['title']}  ({a['source']})")
            if a["link"]:
                lines.append(f"     {a['link']}")

    add_news("Top News", general_news)
    add_news("Business & Finance", business_news)

    lines.append("")
    lines.append("INBOX TRIAGE")
    if not email_items:
        lines.append("  No unread emails.")
    else:
        for item in email_items:
            lines.append(f"  [{item['classification']}] {item['subject']}")
            lines.append(f"      From: {item['from']}")
            if item["draft_saved"]:
                lines.append("      → Draft reply saved to Gmail Drafts.")

    lines.append("")
    lines.append("Sent by Daily Assistant Agent")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------

def run_daily_briefing():
    """Run the full daily briefing pipeline end-to-end."""
    start_time = datetime.datetime.now()

    print()
    print("=" * 50)
    print("  DAILY ASSISTANT AGENT")
    print(f"  {start_time.strftime('%Y-%m-%d  %H:%M:%S')}")
    print("=" * 50)
    print()

    # 1 — Weather
    print("[1/6] Fetching weather...")
    try:
        weather = fetch_weather()
    except Exception as e:
        print(f"  Weather step failed: {e}")
        weather = None

    # 2 — General news
    print("\n[2/6] Fetching top general news headlines...")
    try:
        general_news = fetch_general_news()
    except Exception as e:
        print(f"  General news step failed: {e}")
        general_news = []

    # 3 — Business news
    print("\n[3/6] Fetching business & finance news...")
    try:
        business_news = fetch_business_news()
    except Exception as e:
        print(f"  Business news step failed: {e}")
        business_news = []

    # 4 — Gmail authentication (required to read emails AND send the briefing)
    print("\n[4/6] Authenticating with Gmail...")
    try:
        service = authenticate_gmail()
        print("  Authenticated.")
    except Exception as e:
        print(f"  Gmail authentication failed: {e}")
        print("  Cannot continue without Gmail access. Exiting.")
        return

    # 5 — Email triage + draft generation
    print(f"\n[5/6] Reading and classifying emails (cap: {GMAIL_MAX_EMAILS})...")
    try:
        email_items = process_emails(service)
    except Exception as e:
        print(f"  Email processing failed: {e}")
        email_items = []

    drafts_saved = sum(1 for item in email_items if item["draft_saved"])

    # 6 — Render HTML and send the briefing
    print("\n[6/6] Rendering HTML briefing and sending to your inbox...")
    html_body = render_briefing_html(
        name=USER_NAME,
        weather=weather,
        general_news=general_news,
        business_news=business_news,
        email_items=email_items,
    )
    plain_fallback = build_plain_fallback(
        weather, general_news, business_news, email_items
    )
    success = send_briefing_email(service, html_body, plain_fallback=plain_fallback)

    elapsed = (datetime.datetime.now() - start_time).seconds

    print()
    print("=" * 50)
    if success:
        print("  BRIEFING SENT SUCCESSFULLY")
    else:
        print("  FAILED TO SEND BRIEFING")
    print(f"  Drafts saved : {drafts_saved}")
    print(f"  Completed in : {elapsed}s")
    print("=" * 50)
    print()


if __name__ == "__main__":
    run_daily_briefing()
