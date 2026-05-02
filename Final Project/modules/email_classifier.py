"""
Email Classifier module: Uses the OpenAI API to triage emails and draft replies.

Exposes:
  - validate_api_key()    : Quick health-check for the OpenAI key.
  - classify_email(...)   : Returns one of URGENT / NEEDS_REPLY / FYI / CAN_IGNORE.
  - generate_reply_draft(...) : Returns a short draft reply for NEEDS_REPLY emails.
"""

from openai import OpenAI, AuthenticationError, OpenAIError
from config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


VALID_CATEGORIES = ["URGENT", "NEEDS_REPLY", "FYI", "CAN_IGNORE"]


CLASSIFICATION_SYSTEM_PROMPT = """You are an email triage assistant. Your job is to classify emails into one of four categories:
1. URGENT - Requires immediate action or is time-sensitive
2. NEEDS_REPLY - Requires a response from the user
3. FYI - Informational, no action needed
4. CAN_IGNORE - Spam, newsletters, notifications that don't need attention

For each email, respond with ONLY the classification category, nothing else.
Example: "URGENT" or "NEEDS_REPLY" or "FYI" or "CAN_IGNORE"
"""


REPLY_SYSTEM_PROMPT = (
    "You are drafting a professional, concise email reply. "
    "Be friendly and to the point. Keep it brief (2-3 sentences max)."
)


def validate_api_key():
    """
    Cheap health-check: hit the models endpoint with the configured key.

    Returns:
        (ok: bool, message: str): ok=True if the key is valid, otherwise
        ok=False with a human-readable error message.
    """
    if not OPENAI_API_KEY:
        return False, "OPENAI_API_KEY is missing from .env."

    try:
        client.models.list()
        return True, "OpenAI API key is valid."
    except AuthenticationError:
        return False, (
            "OpenAI rejected the API key (401 Unauthorized). "
            "Verify OPENAI_API_KEY in .env is current and the account has credits."
        )
    except OpenAIError as e:
        return False, f"OpenAI request failed: {e}"
    except Exception as e:
        return False, f"Unexpected error validating OpenAI key: {e}"


def classify_email(subject, from_addr, snippet):
    """
    Classify a single email into one of four triage categories.

    Returns:
        str: One of URGENT / NEEDS_REPLY / FYI / CAN_IGNORE.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=10,
            messages=[
                {"role": "system", "content": CLASSIFICATION_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"Classify this email:\n"
                        f"From: {from_addr}\n"
                        f"Subject: {subject}\n"
                        f"Content: {snippet}"
                    ),
                },
            ],
        )

        classification = response.choices[0].message.content.strip().upper()
        return classification if classification in VALID_CATEGORIES else "FYI"

    except Exception as e:
        print(f"  Error classifying email: {e}")
        return "FYI"


def generate_reply_draft(subject, from_addr, snippet):
    """
    Generate a short, professional draft reply for a single email.

    Returns:
        str: Draft reply body (no salutation/signature).
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=250,
            messages=[
                {"role": "system", "content": REPLY_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"Draft a reply to this email:\n"
                        f"From: {from_addr}\n"
                        f"Subject: {subject}\n"
                        f"Content: {snippet}\n\n"
                        f"Respond with only the body of the email "
                        f"(no salutation or signature needed). Keep it professional and brief."
                    ),
                },
            ],
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"  Error generating reply: {e}")
        return "I'll get back to you on this."


if __name__ == "__main__":
    ok, msg = validate_api_key()
    print(f"API key check: {msg}")

    if ok:
        test_email = {
            "subject": "Meeting tomorrow at 2 PM",
            "from": "boss@company.com",
            "snippet": "Hi, just confirming our meeting tomorrow at 2 PM in conference room B.",
        }
        classification = classify_email(
            test_email["subject"], test_email["from"], test_email["snippet"]
        )
        print(f"Classification: {classification}")
        if classification == "NEEDS_REPLY":
            draft = generate_reply_draft(
                test_email["subject"], test_email["from"], test_email["snippet"]
            )
            print(f"Draft Reply:\n{draft}")
