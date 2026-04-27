# Final Project Proposal — Daily Assistant Agent

## What Are You Building?

An agentic AI-powered Python application that runs automatically every morning and delivers a single, personalized daily briefing email. The agent fetches the day's weather, top news headlines, and reads the user's Gmail inbox — using the Claude API to classify emails by urgency, draft replies for messages that need a response, and compile everything into one clean, actionable summary sent straight to the user's inbox before their day begins.

## Why?

Every morning, getting ready for the day involves opening four or five different apps — checking the weather, scrolling through news, triaging emails, figuring out what actually needs attention. It's fragmented and time-consuming, and most of the "decisions" involved (is this email urgent? what should I reply to this?) are repetitive enough that an AI can handle them.

This project solves that by collapsing everything into a single automated email that arrives without any manual effort. It's a real tool I would use daily, and it demonstrates a complete agentic workflow: the agent doesn't just fetch data — it reasons about it, makes decisions, takes actions (writing drafts, classifying emails), and delivers a structured output autonomously.

Beyond personal utility, this also has a practical angle: a version of this tool could be packaged as a service for small business owners or freelancers who are overwhelmed by their inboxes. Building it for myself is the first step.

## MVP vs. Stretch Goals

### Minimum Viable Product

The MVP is a fully working agent that, when triggered, completes the following pipeline end-to-end:

- **Weather module** — Fetches current conditions and the day's forecast for a configured city using the OpenWeatherMap API
- **News module** — Pulls today's top headlines from RSS feeds using feedparser (no API key required)
- **Gmail reader module** — Authenticates with the Gmail API, reads new/unread emails, and sends them to the Claude API for classification into four categories: Urgent, Needs Reply, FYI, and Can Ignore
- **Draft writer module** — For every email classified as "Needs Reply," uses the Claude API to generate a context-aware draft reply saved directly to the Gmail Drafts folder
- **Email builder + sender** — Assembles all of the above into a structured plain-text briefing and sends it to the user's own inbox via Gmail SMTP
- **Config + environment setup** — User preferences (name, city, email address) stored in config.py; all API keys stored in .env and excluded from the repo via .gitignore

### Stretch Goals (if time allows)

- **Google Calendar integration** — Pull the day's events from Google Calendar and include a schedule section in the briefing
- **HTML email template** — Replace plain-text output with a beautifully formatted HTML email using a briefing.html template
- **Automatic daily scheduling** — Use the schedule library so the agent runs at 8:00 AM every day without manual execution
- **Briefing history log** — Store each day's briefing locally in a SQLite database or JSON file for reference
- **Web dashboard** — A minimal Flask page that displays the last 7 days of briefings in the browser

## What Don't You Know Yet?

- **Gmail API authentication flow** — I understand OAuth2 conceptually but have not implemented it in Python before. I'll need to learn how to generate and store credentials using google-auth-oauthlib and handle token refresh properly.

- **Saving drafts via Gmail API** — I know how to send email via SMTP, but programmatically creating a draft inside Gmail's UI (not just sending) requires using the Gmail REST API's drafts.create endpoint, which I haven't used yet.

- **Prompt engineering for email classification** — Getting Claude to reliably classify and triage emails across many different tones and topics will require careful prompt design. I may need to iterate on the system prompt significantly.

- **Rate limits and API costs** — The Claude API charges per token. Processing a full inbox of emails every morning could add up. I'll need to implement a cap (e.g., only process the first 20 unread emails) to keep costs predictable and build in error handling for rate limit responses.

- **Running the scheduler reliably** — Using schedule in a long-running Python process works locally, but keeping it running in the background every day on a personal laptop (vs. a server) requires either a cron job setup or running on a cloud instance. I'll need to figure out the most practical local solution first.
