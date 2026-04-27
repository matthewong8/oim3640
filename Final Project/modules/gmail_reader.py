"""
Gmail Reader module: Authenticates with Gmail API and reads emails
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64


SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def authenticate_gmail():
    """
    Authenticate with Gmail API using OAuth2.
    Handles token refresh and initial setup.
    
    Returns:
        service: Gmail API service object
    """
    creds = None
    
    # Load existing token if available
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    
    # Refresh or create new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # First-time setup: need credentials.json from Google Cloud Console
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save token for next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    
    return build("gmail", "v1", credentials=creds)


def get_unread_emails(service, max_results=20):
    """
    Fetch unread emails from Gmail inbox.
    
    Args:
        service: Gmail API service object
        max_results: Maximum number of emails to fetch
    
    Returns:
        list: List of email dictionaries with subject, from, snippet
    """
    try:
        # Query for unread emails
        results = service.users().messages().list(
            userId="me",
            q="is:unread",
            maxResults=max_results
        ).execute()
        
        messages = results.get("messages", [])
        
        if not messages:
            return []
        
        # Get full details for each message
        emails = []
        for msg in messages:
            msg_data = service.users().messages().get(
                userId="me",
                id=msg["id"],
                format="full"
            ).execute()
            
            headers = msg_data["payload"]["headers"]
            
            email_info = {
                "id": msg["id"],
                "subject": next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject"),
                "from": next((h["value"] for h in headers if h["name"] == "From"), "Unknown"),
                "snippet": msg_data["snippet"]
            }
            
            emails.append(email_info)
        
        return emails
    
    except Exception as e:
        print(f"Error fetching emails: {str(e)}")
        return []


if __name__ == "__main__":
    # Test Gmail reader
    service = authenticate_gmail()
    emails = get_unread_emails(service, max_results=5)
    for email in emails:
        print(f"From: {email['from']}")
        print(f"Subject: {email['subject']}")
        print(f"Preview: {email['snippet']}\n")
