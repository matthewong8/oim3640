"""
Email Sender module: Sends briefing email and creates draft replies
"""

import base64
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import GMAIL_USER_EMAIL
from googleapiclient.errors import HttpError


def send_briefing_email(service, html_body, plain_fallback=None):
    """
    Send the compiled briefing email (HTML) to the user's inbox via Gmail API.

    Args:
        service: Gmail API service object
        html_body (str): Full HTML document for the briefing.
        plain_fallback (str | None): Optional plain-text version for clients
            that can't render HTML.

    Returns:
        bool: True on success, False on failure.
    """
    try:
        # multipart/alternative lets the client choose HTML or plain text
        message = MIMEMultipart("alternative")
        message["to"] = GMAIL_USER_EMAIL
        message["subject"] = (
            f"Your Daily Briefing — "
            f"{datetime.date.today().strftime('%a, %b %d')}"
        )

        if plain_fallback:
            message.attach(MIMEText(plain_fallback, "plain", "utf-8"))
        message.attach(MIMEText(html_body, "html", "utf-8"))

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        service.users().messages().send(
            userId="me",
            body={"raw": raw_message},
        ).execute()

        print(f"  Briefing sent to {GMAIL_USER_EMAIL}")
        return True

    except HttpError as e:
        print(f"  Failed to send briefing: {e}")
        return False


def create_draft_reply(service, original_msg_id, reply_text):
    """
    Create a draft reply in Gmail's drafts folder.
    
    Args:
        service: Gmail API service object
        original_msg_id: ID of the original email
        reply_text: Draft reply content
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get original message to extract subject and recipient
        original = service.users().messages().get(
            userId="me",
            id=original_msg_id,
            format="full"
        ).execute()
        
        headers = original["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "Re: No Subject")
        from_addr = next((h["value"] for h in headers if h["name"] == "From"), "")
        
        # Ensure subject starts with "Re:"
        if not subject.startswith("Re:"):
            subject = f"Re: {subject}"
        
        # Create draft message
        message = MIMEText(reply_text)
        message["to"] = from_addr
        message["subject"] = subject
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        draft_message = {
            "message": {
                "raw": raw_message,
                "threadId": original.get("threadId")
            }
        }
        
        service.users().drafts().create(
            userId="me",
            body=draft_message
        ).execute()
        
        print(f"✓ Draft created as reply to: {subject}")
        return True
    
    except HttpError as e:
        print(f"✗ Failed to create draft: {str(e)}")
        return False
