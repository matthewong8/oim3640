"""
Email Classifier module: Uses OpenAI API to classify and analyze emails
"""

from openai import OpenAI
from config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


CLASSIFICATION_SYSTEM_PROMPT = """You are an email triage assistant. Your job is to classify emails into one of four categories:
1. URGENT - Requires immediate action or is time-sensitive
2. NEEDS_REPLY - Requires a response from the user
3. FYI - Informational, no action needed
4. CAN_IGNORE - Spam, newsletters, notifications that don't need attention

For each email, respond with ONLY the classification category, nothing else.
Example: "URGENT" or "NEEDS_REPLY" or "FYI" or "CAN_IGNORE"
"""


def classify_email(subject, from_addr, snippet):
    """
    Classify an email using OpenAI API.
    
    Args:
        subject: Email subject line
        from_addr: Sender email address
        snippet: Email preview/snippet
    
    Returns:
        str: Classification category (URGENT, NEEDS_REPLY, FYI, CAN_IGNORE)
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=10,
            messages=[
                {"role": "system", "content": CLASSIFICATION_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"""Classify this email:
From: {from_addr}
Subject: {subject}
Content: {snippet}"""
                }
            ]
        )
        
        classification = response.choices[0].message.content.strip().upper()
        
        # Validate classification
        valid_categories = ["URGENT", "NEEDS_REPLY", "FYI", "CAN_IGNORE"]
        if classification in valid_categories:
            return classification
        else:
            return "FYI"  # Default to FYI if uncertain
    
    except Exception as e:
        print(f"Error classifying email: {str(e)}")
        return "FYI"


def generate_reply_draft(subject, from_addr, snippet):
    """
    Generate a context-aware draft reply for an email.
    
    Args:
        subject: Email subject line
        from_addr: Sender email address
        snippet: Email preview/snippet
    
    Returns:
        str: Draft reply text
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=250,
            messages=[
                {"role": "system", "content": "You are drafting a professional, concise email reply. Be friendly and to the point. Keep it brief (2-3 sentences max)."},
                {
                    "role": "user",
                    "content": f"""Draft a reply to this email:
From: {from_addr}
Subject: {subject}
Content: {snippet}

Respond with only the body of the email (no salutation or signature needed). Keep it professional and brief."""
                }
            ]
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error generating reply: {str(e)}")
        return "I'll get back to you on this."


if __name__ == "__main__":
    # Test classification
    test_email = {
        "subject": "Meeting tomorrow at 2 PM",
        "from": "boss@company.com",
        "snippet": "Hi, just confirming our meeting tomorrow at 2 PM in conference room B."
    }
    
    classification = classify_email(test_email["subject"], test_email["from"], test_email["snippet"])
    print(f"Classification: {classification}")
    
    if classification == "NEEDS_REPLY":
        draft = generate_reply_draft(test_email["subject"], test_email["from"], test_email["snippet"])
        print(f"Draft Reply:\n{draft}")
