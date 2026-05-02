# Daily Assistant Agent

An agentic AI-powered Python application that delivers a personalized HTML briefing email every morning — weather, general world news, business & finance headlines, and a fully triaged Gmail inbox — all sent to your inbox before you start your day.

## What it does

When you run `main.py`, the agent walks through six stages end-to-end:

1. **Weather** — fetches current conditions for your configured city from OpenWeatherMap.
2. **General news** — pulls top headlines from BBC and The Guardian world feeds via RSS.
3. **Business & finance news** — pulls headlines from BBC Business, CNBC, The Guardian Business, and MarketWatch (covers investing, M&A, company news, and markets).
4. **Gmail authentication** — connects to your Gmail account via OAuth2.
5. **Inbox triage** — reads your unread emails (default cap: 20) and uses the OpenAI API (`gpt-3.5-turbo`) to classify each one into **Urgent**, **Needs Reply**, **FYI**, or **Can Ignore**. For every email tagged *Needs Reply*, it generates a short draft response and saves it directly to your Gmail Drafts folder.
6. **Briefing email** — assembles all of the above into a clean HTML email (with a plain-text fallback) and sends it to your inbox.

A snapshot of every run is also saved as JSON in `history/YYYY-MM-DD.json` so you can build dashboards or weekly digests later.

## Tech stack

- **Python 3.13**
- **OpenAI API** — email classification and draft generation
- **Gmail API** (`google-api-python-client`) — read inbox, save drafts, send the briefing
- **OpenWeatherMap API** — weather
- **feedparser** — RSS headline aggregation (no API key required)
- **google-auth-oauthlib** — Gmail OAuth2 flow

## Project structure

```
Final Project/
├── main.py                          # Entry point + pipeline orchestrator
├── config.py                        # User settings + RSS feed lists
├── requirements.txt                 # Python dependencies
├── .env                             # API keys + email (not committed)
├── credentials.json                 # Gmail OAuth credentials (not committed)
├── token.pickle                     # Gmail OAuth token (not committed)
├── history/                         # Daily briefing snapshots (not committed)
├── modules/
│   ├── __init__.py
│   ├── weather.py                   # OpenWeatherMap integration
│   ├── news.py                      # RSS feed parser (general + business)
│   ├── gmail_reader.py              # Gmail OAuth2 + unread email fetcher
│   ├── email_classifier.py          # OpenAI classification + draft generation
│   ├── email_sender.py              # Sends HTML briefing + creates Gmail drafts
│   ├── briefing_html.py             # HTML email template renderer
│   └── history.py                   # Saves daily briefing as JSON
├── proposal.md                      # Original project proposal
├── AI_USAGE.md                      # Documentation of AI tool usage
└── README.md                        # This file
```

## Setup

### 1. Clone and install

```bash
git clone https://github.com/matthewong8/daily-assistant-agent.git
cd daily-assistant-agent
python -m venv venv
venv\Scripts\activate          # Windows
# or
source venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
```

### 2. Get the API keys

**OpenWeatherMap** — sign up at https://openweathermap.org/api and copy your free API key.

**OpenAI** — get a key from https://platform.openai.com/account/api-keys. The free tier is no longer offered, so the account must have a paid balance or active billing.

**Gmail** — go to https://console.cloud.google.com:
1. Create a new project
2. Enable the **Gmail API**
3. Configure the OAuth consent screen as **External**, and add your own Gmail address as a test user
4. Create an **OAuth 2.0 Client ID** of type **Desktop app**
5. Download the JSON, rename it to `credentials.json`, and place it in the project root

### 3. Configure environment variables

Create a `.env` file in the project root:

```
OPENWEATHER_API_KEY=your_openweather_key
OPENAI_API_KEY=your_openai_key
USER_EMAIL=your-email@gmail.com
GMAIL_USER_EMAIL=your-gmail@gmail.com
```

`.env` is gitignored — never commit it.

### 4. Personalize `config.py`

Edit `config.py` to set:

```python
USER_NAME = "Matthew"           # Your name (used in the briefing greeting)
CITY = "Boston"                 # Your city for weather
GMAIL_MAX_EMAILS = 20           # Max unread emails to process per run
MAX_NEWS_ARTICLES = 5
MAX_BUSINESS_ARTICLES = 7
```

The `RSS_FEEDS` and `BUSINESS_RSS_FEEDS` lists are also configurable if you want different sources.

## Running

```bash
python main.py
```

On the first run, a browser window opens asking you to authorize Gmail access. After that, a `token.pickle` file is saved and you won't need to re-authorize for ~7 days (Google's limit while the OAuth app is in "Testing" mode).

The console prints each stage as it runs:

```
==================================================
  DAILY ASSISTANT AGENT
  2026-05-01  08:00:00
==================================================

[ Pre-flight ] Validating OpenAI API key...
  OpenAI API key is valid.

[1/6] Fetching weather...
  Boston: 12.4°C, Light rain

[2/6] Fetching top general news headlines...
  5 general headline(s) fetched.
    1. ...

[3/6] Fetching business & finance news...
  7 business headline(s) fetched.
    1. ...

[4/6] Authenticating with Gmail...
  Authenticated.

[5/6] Reading and classifying emails (cap: 20)...
  20 unread email(s) found. Classifying...
    [URGENT     ] Project deadline reminder
    [NEEDS_REPLY] Re: Coffee chat next week
    ...

[6/6] Rendering HTML briefing and sending to your inbox...
  Briefing sent to your-email@gmail.com

==================================================
  BRIEFING SENT SUCCESSFULLY
  Drafts saved : 3
  Completed in : 14s
  History saved: .../history/2026-05-01.json
==================================================
```

## Automating the daily run

The proposal mentioned three approaches:

- **Windows Task Scheduler** — easiest local option. Create a task that runs `python main.py` every morning at 8:00 AM. Reliable as long as your laptop is on/awake.
- **Python `schedule` library** — works but requires the script to run 24/7.
- **GitHub Actions** — most reliable, runs in the cloud. Requires uploading `credentials.json` and `token.pickle` as encrypted secrets and refreshing the token weekly while the OAuth app is in Testing mode.

## Stretch goals from the original proposal

| Goal                                | Status                                                |
|-------------------------------------|-------------------------------------------------------|
| HTML email template                 | ✅ Implemented (`modules/briefing_html.py`)           |
| Business / finance news section     | ✅ Implemented (`BUSINESS_RSS_FEEDS` in `config.py`)  |
| Briefing history log                | ✅ Implemented (JSON in `history/`)                   |
| OpenAI key validation on startup    | ✅ Implemented (`validate_api_key()` pre-flight check)|
| Google Calendar integration         | ⏳ Not yet                                            |
| Automatic daily scheduling          | ⏳ Not yet (manual run for now)                       |
| Web dashboard (Flask)               | ⏳ Not yet                                            |

## Troubleshooting

**`ModuleNotFoundError: No module named 'dotenv'`**
You forgot to install dependencies into the venv. Run `pip install -r requirements.txt`.

**`FileNotFoundError: credentials.json`**
Download OAuth credentials from Google Cloud Console (Desktop app type) and save as `credentials.json` in the project root.

**`OpenAI rejected the API key (401 Unauthorized)`**
Verify `OPENAI_API_KEY` in `.env` is current and the OpenAI account has billing/credits set up. The pre-flight check will surface this before any emails get processed.

**Gmail asks me to re-authorize every week**
That's Google's limit on OAuth apps in "Testing" mode. Either accept the weekly re-auth, or publish your app via Google's verification process.

## License

MIT — feel free to fork and modify.
