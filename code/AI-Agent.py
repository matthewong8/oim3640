"""
AI Email Agent - Automatically generates professional email replies using OpenAI
Requires user review before sending to ensure quality and appropriateness
"""

import os
import pickle
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.api_core import retry
from googleapiclient.discovery import build
import openai
from email.mime.text import MIMEText

# Gmail API configuration
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
GMAIL_API_VERSION = 'v1'

# OpenAI configuration
openai.api_key = os.getenv('OPENAI_API_KEY')  # Set your OpenAI API key as environment variable

# Spam keywords to filter out
SPAM_KEYWORDS = ['unsubscribe', 'click here', 'limited time', 'act now', 'promotional', 'offer', 'deal']

class EmailAgent:
    def __init__(self):
        """Initialize the email agent with Gmail and OpenAI connections"""
        self.service = self.authenticate_gmail()
        self.processed_emails = []
        
    def authenticate_gmail(self):
        """Authenticate with Gmail API using OAuth"""
        creds = None
        
        # Load existing credentials
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        return build(GMAIL_API_VERSION, 'gmail', credentials=creds)
    
    def is_spam(self, subject, body):
        """Check if email is likely spam based on keywords"""
        content = (subject + ' ' + body).lower()
        for keyword in SPAM_KEYWORDS:
            if keyword in content:
                return True
        return False
    
    def get_unread_emails(self, max_results=5):
        """Fetch unread emails from inbox"""
        try:
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread -is:spam',
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            return messages
        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []
    
    def get_email_details(self, message_id):
        """Get full email details including subject, from, and body"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            subject = next(h['value'] for h in headers if h['name'] == 'Subject')
            sender = next(h['value'] for h in headers if h['name'] == 'From')
            
            # Extract body
            if 'parts' in message['payload']:
                body = message['payload']['parts'][0]['body'].get('data', '')
            else:
                body = message['payload']['body'].get('data', '')
            
            if body:
                body = base64.urlsafe_b64decode(body).decode('utf-8')
            
            return {
                'id': message_id,
                'subject': subject,
                'sender': sender,
                'body': body[:500]  # Limit to first 500 chars for clarity
            }
        except Exception as e:
            print(f"Error getting email details: {e}")
            return None
    
    def generate_reply(self, email_subject, email_body, sender):
        """Use OpenAI to generate a professional reply"""
        try:
            prompt = f"""You are a professional email assistant. Generate a concise, professional, and friendly email reply.

Original Email:
From: {sender}
Subject: {email_subject}
Body: {email_body}

Requirements:
- Keep it under 150 words
- Professional tone
- Friendly and helpful
- If the email is unclear or seems like a request you can't fulfill, mention it at the end with: "[Note: This email seems unclear - please review]"

Generate only the reply body (no greeting/signature):"""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message['content'].strip()
        except Exception as e:
            print(f"Error generating reply with OpenAI: {e}")
            return None
    
    def send_email(self, to, subject, body):
        """Send email reply"""
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = f"Re: {subject}"
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def mark_as_read(self, message_id):
        """Mark email as read"""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
        except Exception as e:
            print(f"Error marking email as read: {e}")
    
    def process_emails(self):
        """Main workflow: fetch, filter, generate replies, and get user approval"""
        print("\n" + "="*60)
        print("AI EMAIL AGENT - Professional Reply Generator")
        print("="*60)
        
        emails = self.get_unread_emails()
        
        if not emails:
            print("No unread emails found.")
            return
        
        print(f"\nFound {len(emails)} unread email(s). Processing...\n")
        
        for i, message in enumerate(emails, 1):
            email = self.get_email_details(message['id'])
            
            if not email:
                continue
            
            # Check for spam
            if self.is_spam(email['subject'], email['body']):
                print(f"[{i}] SKIPPED - Likely spam email from: {email['sender']}")
                self.mark_as_read(message['id'])
                continue
            
            print(f"\n{'─'*60}")
            print(f"[Email {i}]")
            print(f"From: {email['sender']}")
            print(f"Subject: {email['subject']}")
            print(f"Preview: {email['body'][:200]}...")
            print(f"{'─'*60}")
            
            # Generate reply
            print("\nGenerating professional reply...")
            reply = self.generate_reply(email['subject'], email['body'], email['sender'])
            
            if not reply:
                print("Failed to generate reply.")
                continue
            
            # Check for unclear email flag
            if "[Note: This email seems unclear" in reply:
                print("\n⚠️  FLAG: This email seems unclear - review recommended")
            
            print("\n📧 GENERATED REPLY:")
            print("─" * 60)
            print(reply)
            print("─" * 60)
            
            # Get user approval
            while True:
                user_input = input("\nAction (send/skip/edit): ").strip().lower()
                
                if user_input == 'send':
                    if self.send_email(email['sender'], email['subject'], reply):
                        print("✓ Email sent successfully!")
                        self.mark_as_read(message['id'])
                        self.processed_emails.append({
                            'from': email['sender'],
                            'subject': email['subject'],
                            'status': 'sent'
                        })
                    else:
                        print("✗ Failed to send email.")
                    break
                
                elif user_input == 'skip':
                    print("Skipped.")
                    break
                
                elif user_input == 'edit':
                    print("Edit mode: Enter new reply (type 'DONE' on new line when finished):")
                    lines = []
                    while True:
                        line = input()
                        if line.upper() == 'DONE':
                            break
                        lines.append(line)
                    reply = '\n'.join(lines)
                    print("Updated reply. Send? (yes/no):")
                    if input().strip().lower() == 'yes':
                        if self.send_email(email['sender'], email['subject'], reply):
                            print("✓ Email sent successfully!")
                            self.mark_as_read(message['id'])
                        else:
                            print("✗ Failed to send email.")
                    break
                
                else:
                    print("Invalid action. Try again (send/skip/edit):")
        
        print("\n" + "="*60)
        print("PROCESSING COMPLETE")
        print(f"Emails processed: {len(self.processed_emails)}")
        print("="*60 + "\n")


def main():
    """Main entry point"""
    try:
        agent = EmailAgent()
        agent.process_emails()
    except Exception as e:
        print(f"Fatal error: {e}")


if __name__ == '__main__':
    main()
