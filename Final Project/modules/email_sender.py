"""
Email Sender module: Sends briefing email and creates draft replies
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import GMAIL_USER_EMAIL, USER_EMAIL
from googleapiclient.errors import HttpError
import base64


def send_briefing_email(service, briefing_text):
    """
    Send the compiled briefing email to the user's inbox via Gmail API.
    
    Args:
        service: Gmail API service object
        briefing_text: The compiled briefing content
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        message = MIMEText(briefing_text)
        message["to"] = GMAIL_USER_EMAIL
        message["subject"] = "☀️ Your Daily Briefing"
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = {"raw": raw_message}
        
        service.users().messages().send(
            userId="me",
            body=send_message
        ).execute()
        
        print(f"✓ Briefing sent to {GMAIL_USER_EMAIL}")
        return True
    
    except HttpError as e:
        print(f"✗ Failed to send briefing: {str(e)}")
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
