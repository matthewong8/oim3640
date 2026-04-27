"""
Daily Assistant Agent - Main Entry Point
Orchestrates the full briefing pipeline
"""

from modules.weather import get_weather_briefing
from modules.news import get_news_briefing
from modules.gmail_reader import authenticate_gmail, get_unread_emails
from modules.claude_classifier import classify_email, generate_reply_draft
from modules.email_sender import send_briefing_email, create_draft_reply
from config import USER_NAME, GMAIL_MAX_EMAILS
import datetime


def run_daily_briefing():
    """
    Main function: Orchestrates the full daily briefing pipeline.
    1. Fetch weather and news
    2. Read unread emails
    3. Classify emails with Claude
    4. Generate drafts for emails that need replies
    5. Compile and send briefing
    """
    print("\n" + "="*50)
    print("🤖 DAILY ASSISTANT AGENT")
    print(f"⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50 + "\n")
    
    # Step 1: Fetch Weather and News
    print("[1/5] Fetching weather...")
    weather = get_weather_briefing()
    print("✓ Weather fetched\n")
    
    print("[2/5] Fetching news headlines...")
    news = get_news_briefing()
    print("✓ News fetched\n")
    
    # Step 2: Authenticate Gmail and fetch emails
    print("[3/5] Authenticating with Gmail...")
    try:
        service = authenticate_gmail()
        print("✓ Gmail authenticated\n")
    except Exception as e:
        print(f"✗ Gmail authentication failed: {str(e)}")
        return
    
    # Step 3: Get unread emails and classify them
    print(f"[4/5] Fetching and classifying emails (max {GMAIL_MAX_EMAILS})...")
    emails = get_unread_emails(service, max_results=GMAIL_MAX_EMAILS)
    
    if not emails:
        print("✓ No unread emails\n")
        email_summary = "No new emails."
    else:
        print(f"✓ Found {len(emails)} unread emails\n")
        
        # Classify each email and generate drafts if needed
        email_summary = f"UNREAD EMAILS ({len(emails)})\n" + "="*40 + "\n"
        
        for email in emails:
            classification = classify_email(
                email["subject"],
                email["from"],
                email["snippet"]
            )
            
            email_summary += f"\n[{classification}] {email['subject']}\n"
            email_summary += f"From: {email['from']}\n"
            
            # Generate draft reply if needed
            if classification == "NEEDS_REPLY":
                draft = generate_reply_draft(
                    email["subject"],
                    email["from"],
                    email["snippet"]
                )
                print(f"  → Generating draft reply for: {email['subject']}")
                create_draft_reply(service, email["id"], draft)
        
        email_summary += "\n✓ Drafts created for emails needing replies"
    
    # Step 4: Compile complete briefing
    print("\n[5/5] Compiling briefing and sending...")
    
    briefing = f"""
GOOD MORNING, {USER_NAME.upper()}!

Your personalized briefing for {datetime.date.today().strftime('%B %d, %Y')}

{weather}

{news}

{email_summary}

---
Sent by Daily Assistant Agent
"""
    
    # Send briefing
    success = send_briefing_email(service, briefing)
    
    if success:
        print("\n" + "="*50)
        print("✓ BRIEFING COMPLETE AND SENT")
        print("="*50 + "\n")
    else:
        print("\n" + "="*50)
        print("✗ BRIEFING FAILED")
        print("="*50 + "\n")


if __name__ == "__main__":
    run_daily_briefing()
