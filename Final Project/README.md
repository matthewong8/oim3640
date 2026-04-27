# Daily Assistant Agent

An agentic AI-powered Python application that delivers a personalized daily briefing email every morning—weather, top news, and email triage—all sent to your inbox before you start your day.

## Features

### MVP (Core Functionality)
- ✅ **Weather briefing** — Current conditions and forecast via OpenWeatherMap API
- ✅ **Top news headlines** — RSS feed aggregation from BBC and The Guardian
- ✅ **Email reader** — OAuth2 authentication with Gmail API
- ✅ **AI email classification** — Claude API classifies emails into: Urgent, Needs Reply, FYI, Can Ignore
- ✅ **Draft reply generator** — Auto-generates context-aware email drafts
- ✅ **Briefing delivery** — Sends compiled briefing to your inbox
- ✅ **Secure setup** — .env for secrets, .gitignore to prevent commits

### Stretch Goals (If Time Allows)
- 🔄 **Google Calendar integration** — Include your day's schedule
- 📄 **HTML email template** — Rich formatting instead of plain text
- ⏰ **Automatic daily scheduling** — Runs at 8:00 AM automatically
- 📚 **Briefing history** — SQLite database of past briefings
- 🖥️ **Web dashboard** — Flask app to view last 7 days of briefings

## Technology Stack

- **Python 3.x** — Core language
- **Claude API (Anthropic)** — Email classification and reply generation
- **Gmail API v1** — Email reading and draft creation
- **OpenWeatherMap API** — Weather data
- **feedparser** — RSS feed parsing (no API key needed)
- **google-auth-oauthlib** — Gmail OAuth2 authentication

## Project Structure

```
daily-assistant-agent/
├── main.py                          # Entry point - orchestrates the pipeline
├── config.py                        # User settings and preferences
├── requirements.txt                 # Python dependencies
├── .env                            # API keys (DO NOT COMMIT)
├── .gitignore                      # Excludes secrets and __pycache__
├── token.pickle                    # Gmail OAuth token (DO NOT COMMIT)
├── credentials.json                # Gmail OAuth credentials (DO NOT COMMIT)
├── modules/
│   ├── __init__.py
│   ├── weather.py                  # OpenWeatherMap integration
│   ├── news.py                     # RSS feed parser
│   ├── gmail_reader.py             # Gmail API authentication and reading
│   ├── claude_classifier.py        # Email classification and reply generation
│   └── email_sender.py             # Gmail draft and briefing email sending
├── README.md                        # This file
├── AI_USAGE.md                     # AI tool usage documentation
└── proposal.md                     # Project proposal
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/daily-assistant-agent.git
cd daily-assistant-agent
```

### 2. Create and Activate Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get API Keys

#### OpenWeatherMap API
1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Generate an API key
4. Copy the key

#### Claude API (Anthropic)
1. Go to [Anthropic Console](https://console.anthropic.com)
2. Sign up or log in
3. Create an API key
4. Copy the key

#### Gmail API
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable the **Gmail API**
4. Create an **OAuth 2.0 Desktop Application** credential
5. Download the credentials as `credentials.json`
6. Save it in the project root directory (it will be auto-excluded by .gitignore)

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
OPENWEATHER_API_KEY=your_api_key_here
CLAUDE_API_KEY=your_api_key_here
USER_EMAIL=your-email@gmail.com
GMAIL_USER_EMAIL=your-gmail@gmail.com
```

**Do NOT commit `.env` to GitHub** — it's already in `.gitignore`.

### 6. Configure User Settings

Edit `config.py` with your preferences:

```python
USER_NAME = "Your Name"
CITY = "Boston"  # For weather
GMAIL_MAX_EMAILS = 20  # Keep costs down
MAX_NEWS_ARTICLES = 5
```

## Running the Agent

### Manual Run (Test)

```bash
python main.py
```

This will:
1. Fetch weather and news
2. Read your 20 most recent unread emails
3. Classify each email using Claude
4. Generate drafts for emails that need replies
5. Compile and send the briefing to your inbox

### Automatic Daily Execution (Stretch Goal)

To run automatically at 8:00 AM every day, use the schedule library (already in requirements.txt):

```python
import schedule
import time
from main import run_daily_briefing

schedule.every().day.at("08:00").do(run_daily_briefing)

while True:
    schedule.run_pending()
    time.sleep(60)
```

Or use a cron job (macOS/Linux) or Task Scheduler (Windows).

## Usage Example

```bash
$ python main.py

==================================================
🤖 DAILY ASSISTANT AGENT
⏰ 2026-04-27 08:00:00
==================================================

[1/5] Fetching weather...
✓ Weather fetched

[2/5] Fetching news headlines...
✓ News fetched

[3/5] Authenticating with Gmail...
✓ Gmail authenticated

[4/5] Fetching and classifying emails (max 20)...
✓ Found 8 unread emails

[URGENT] Deadline: Project proposal due today
  From: boss@company.com

[NEEDS_REPLY] Team meeting reschedule
  From: colleague@company.com
  → Generating draft reply for: Team meeting reschedule

[5/5] Compiling briefing and sending...
✓ Briefing sent to your-gmail@gmail.com

==================================================
✓ BRIEFING COMPLETE AND SENT
==================================================
```

## Troubleshooting

### Gmail API Authentication Issues

**Problem**: `Error: credentials.json not found`
- **Solution**: Download OAuth credentials from Google Cloud Console and save as `credentials.json` in project root

**Problem**: `Error: token.pickle is invalid`
- **Solution**: Delete `token.pickle` and re-authenticate. You'll be prompted to grant permissions again.

### API Key Issues

**Problem**: `Invalid API key` or `401 Unauthorized`
- **Solution**: 
  - Verify your keys in `.env` are correct
  - Restart the app after updating `.env`
  - Check that you haven't exceeded API rate limits

**Problem**: `Rate limit exceeded`
- **Solution**: 
  - Reduce `GMAIL_MAX_EMAILS` in `config.py`
  - Wait a few hours before running again
  - Consider upgrading to a paid API tier

### Email Sending Issues

**Problem**: `Failed to send briefing: 400 Bad Request`
- **Solution**: 
  - Verify `GMAIL_USER_EMAIL` in `.env` matches your Gmail account
  - Ensure you have "Allow less secure apps" enabled (or use App Passwords for 2FA accounts)

## Future Enhancements

1. **Google Calendar integration** — Add your day's schedule to briefing
2. **HTML email template** — Rich formatting with CSS styling
3. **Persistent scheduling** — Use APScheduler for robust background task
4. **Briefing history dashboard** — Flask web app showing past 7 days
5. **Customizable themes** — User-defined email classification categories
6. **Multiple news sources** — Expand beyond BBC and The Guardian
7. **Weather alerts** — Flag severe weather conditions
8. **Email filtering rules** — Skip certain senders or domains

## Learning Outcomes

- ✅ OAuth2 authentication with Gmail API
- ✅ Building agentic workflows with AI
- ✅ Multi-API integration (Anthropic, Google, OpenWeatherMap)
- ✅ Email handling in Python (SMTP and REST APIs)
- ✅ Environment configuration and secrets management
- ✅ Error handling and API rate limiting
- ✅ RSS feed parsing and data aggregation

## License

MIT License — Feel free to modify and redistribute.

## Questions?

See `AI_USAGE.md` for documentation on how AI was used to build this project.
