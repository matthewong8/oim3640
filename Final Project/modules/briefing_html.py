"""
HTML email renderer for the Daily Assistant Agent briefing.

Uses inline CSS and table-based layout so the email renders correctly
across Gmail, Apple Mail, Outlook, and mobile clients.
"""

import datetime


# ---------------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------------

COLORS = {
    "page_bg":       "#f1f3f6",
    "card_bg":       "#ffffff",
    "header_start":  "#1a365d",
    "header_end":    "#2b6cb0",
    "text":          "#1a202c",
    "text_soft":     "#4a5568",
    "muted":         "#718096",
    "border":        "#e2e8f0",
    "border_soft":   "#edf2f7",
    "accent":        "#2b6cb0",
}

CATEGORY_STYLE = {
    "URGENT":      {"label": "Urgent",      "color": "#c53030", "bg": "#fff5f5"},
    "NEEDS_REPLY": {"label": "Needs Reply", "color": "#c05621", "bg": "#fffaf0"},
    "FYI":         {"label": "FYI",         "color": "#2b6cb0", "bg": "#ebf8ff"},
    "CAN_IGNORE":  {"label": "Can Ignore",  "color": "#718096", "bg": "#f7fafc"},
}


def _esc(value):
    """Escape HTML special characters so user content can't break the layout."""
    if value is None:
        return ""
    return (str(value)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


# ---------------------------------------------------------------------------
# Section renderers
# ---------------------------------------------------------------------------

def _section_header(label):
    """Small uppercase label that sits above each section."""
    return (
        f'<p style="margin: 0 0 14px 0; font-size: 11px; letter-spacing: 1.5px; '
        f'text-transform: uppercase; color: {COLORS["muted"]}; font-weight: 700;">'
        f'{_esc(label)}</p>'
    )


def _render_header(name, today):
    """Top hero header: greeting + date."""
    weekday = today.strftime("%A")
    full_date = today.strftime("%B %d, %Y")
    return f"""
      <tr>
        <td style="background: linear-gradient(135deg, {COLORS['header_start']} 0%, {COLORS['header_end']} 100%); padding: 36px 32px;">
          <p style="margin: 0; font-size: 12px; letter-spacing: 2px; text-transform: uppercase; color: rgba(255,255,255,0.75); font-weight: 600;">
            {_esc(weekday)} &middot; {_esc(full_date)}
          </p>
          <h1 style="margin: 10px 0 0 0; font-size: 30px; line-height: 1.2; font-weight: 700; color: #ffffff; letter-spacing: -0.5px;">
            Good morning, {_esc(name)}
          </h1>
          <p style="margin: 8px 0 0 0; font-size: 15px; color: rgba(255,255,255,0.85);">
            Here's everything you need to start your day.
          </p>
        </td>
      </tr>
    """


def _render_weather(weather):
    if weather is None:
        return f"""
          <tr>
            <td style="padding: 28px 32px; border-bottom: 1px solid {COLORS['border']};">
              {_section_header("Weather")}
              <p style="margin: 0; color: {COLORS['muted']}; font-size: 14px;">
                Couldn't fetch weather right now.
              </p>
            </td>
          </tr>
        """

    return f"""
      <tr>
        <td style="padding: 28px 32px; border-bottom: 1px solid {COLORS['border']};">
          {_section_header("Weather  ·  " + _esc(weather['city']))}
          <table width="100%" cellpadding="0" cellspacing="0" border="0">
            <tr>
              <td style="vertical-align: top;">
                <div style="font-size: 48px; font-weight: 700; color: {COLORS['text']}; line-height: 1; letter-spacing: -1.5px;">
                  {_esc(weather['temp'])}&deg;C
                </div>
                <div style="font-size: 16px; color: {COLORS['text_soft']}; margin-top: 8px; font-weight: 500;">
                  {_esc(weather['description'])}
                </div>
              </td>
            </tr>
          </table>

          <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top: 22px; padding-top: 18px; border-top: 1px solid {COLORS['border_soft']};">
            <tr>
              <td width="33%" style="font-size: 11px; color: {COLORS['muted']}; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; padding-right: 8px;">
                Feels like
                <div style="margin-top: 4px; color: {COLORS['text']}; font-size: 16px; font-weight: 600; text-transform: none; letter-spacing: 0;">
                  {_esc(weather['feels_like'])}&deg;C
                </div>
              </td>
              <td width="33%" style="font-size: 11px; color: {COLORS['muted']}; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; padding-right: 8px;">
                Humidity
                <div style="margin-top: 4px; color: {COLORS['text']}; font-size: 16px; font-weight: 600; text-transform: none; letter-spacing: 0;">
                  {_esc(weather['humidity'])}%
                </div>
              </td>
              <td width="33%" style="font-size: 11px; color: {COLORS['muted']}; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600;">
                Wind
                <div style="margin-top: 4px; color: {COLORS['text']}; font-size: 16px; font-weight: 600; text-transform: none; letter-spacing: 0;">
                  {_esc(weather['wind_speed'])} m/s
                </div>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    """


def _render_article_list(articles):
    """Render a numbered list of articles with title, source pill, and link."""
    if not articles:
        return (
            f'<p style="margin: 0; color: {COLORS["muted"]}; font-size: 14px;">'
            f'No articles available right now.</p>'
        )

    rows = []
    for i, article in enumerate(articles, 1):
        title = _esc(article["title"])
        source = _esc(article["source"])
        link = _esc(article["link"])

        # Make the title clickable if a link exists
        if link:
            title_html = (
                f'<a href="{link}" style="color: {COLORS["text"]}; text-decoration: none; '
                f'font-weight: 600;">{title}</a>'
            )
            read_link = (
                f'<a href="{link}" style="color: {COLORS["accent"]}; text-decoration: none; '
                f'font-size: 13px; font-weight: 600;">Read &rarr;</a>'
            )
        else:
            title_html = (
                f'<span style="color: {COLORS["text"]}; font-weight: 600;">{title}</span>'
            )
            read_link = ""

        rows.append(f"""
          <tr>
            <td style="padding: 16px 0; border-bottom: 1px solid {COLORS['border_soft']};">
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td width="28" style="vertical-align: top; font-size: 13px; color: {COLORS['muted']}; font-weight: 700; padding-top: 2px;">
                    {i:02d}
                  </td>
                  <td style="vertical-align: top;">
                    <div style="font-size: 15px; line-height: 1.45;">{title_html}</div>
                    <div style="margin-top: 8px;">
                      <span style="display: inline-block; padding: 3px 10px; background: {COLORS['border_soft']}; color: {COLORS['text_soft']}; font-size: 11px; font-weight: 600; border-radius: 12px; letter-spacing: 0.3px;">
                        {source}
                      </span>
                      {f'<span style="margin-left: 12px;">{read_link}</span>' if read_link else ''}
                    </div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        """)

    return (
        '<table width="100%" cellpadding="0" cellspacing="0" border="0">'
        + "".join(rows)
        + "</table>"
    )


def _render_news_section(label, articles):
    return f"""
      <tr>
        <td style="padding: 28px 32px; border-bottom: 1px solid {COLORS['border']};">
          {_section_header(label)}
          {_render_article_list(articles)}
        </td>
      </tr>
    """


def _render_email_pill(category, count):
    """A counter pill for the email summary at the top of the inbox section."""
    style = CATEGORY_STYLE.get(category, CATEGORY_STYLE["FYI"])
    return f"""
      <td style="padding: 0 6px 0 0;">
        <table cellpadding="0" cellspacing="0" border="0">
          <tr>
            <td style="background: {style['bg']}; padding: 10px 14px; border-radius: 8px; border: 1px solid {COLORS['border_soft']};">
              <div style="font-size: 10px; color: {style['color']}; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px;">
                {_esc(style['label'])}
              </div>
              <div style="font-size: 22px; color: {COLORS['text']}; font-weight: 700; margin-top: 2px;">
                {count}
              </div>
            </td>
          </tr>
        </table>
      </td>
    """


def _render_email_card(item):
    """Render a single email entry."""
    style = CATEGORY_STYLE.get(item["classification"], CATEGORY_STYLE["FYI"])
    badge = (
        f'<span style="display: inline-block; padding: 4px 10px; '
        f'background: {style["bg"]}; color: {style["color"]}; '
        f'font-size: 10px; font-weight: 700; border-radius: 10px; '
        f'letter-spacing: 0.6px; text-transform: uppercase;">'
        f'{_esc(style["label"])}</span>'
    )

    draft_block = ""
    if item.get("draft_saved") and item.get("draft_text"):
        draft_block = f"""
          <div style="margin-top: 12px; padding: 14px 16px; background: #fffaf0; border-left: 3px solid {CATEGORY_STYLE['NEEDS_REPLY']['color']}; border-radius: 4px;">
            <div style="font-size: 11px; color: {CATEGORY_STYLE['NEEDS_REPLY']['color']}; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 6px;">
              Draft saved to Gmail Drafts
            </div>
            <div style="font-size: 13px; color: {COLORS['text_soft']}; line-height: 1.55; font-style: italic;">
              "{_esc(item['draft_text'])}"
            </div>
          </div>
        """

    return f"""
      <tr>
        <td style="padding: 16px 0; border-bottom: 1px solid {COLORS['border_soft']};">
          <div>{badge}</div>
          <div style="margin-top: 8px; font-size: 15px; font-weight: 600; color: {COLORS['text']}; line-height: 1.4;">
            {_esc(item['subject'])}
          </div>
          <div style="margin-top: 4px; font-size: 13px; color: {COLORS['muted']};">
            From: {_esc(item['from'])}
          </div>
          {draft_block}
        </td>
      </tr>
    """


def _render_email_section(email_items):
    counts = {key: 0 for key in CATEGORY_STYLE}
    for item in email_items:
        cat = item["classification"]
        if cat in counts:
            counts[cat] += 1

    if not email_items:
        return f"""
          <tr>
            <td style="padding: 28px 32px; border-bottom: 1px solid {COLORS['border']};">
              {_section_header("Inbox Triage")}
              <p style="margin: 0; color: {COLORS['muted']}; font-size: 14px;">
                Inbox is clear — no unread emails.
              </p>
            </td>
          </tr>
        """

    pills = "".join(_render_email_pill(cat, counts[cat]) for cat in CATEGORY_STYLE)

    cards = "".join(_render_email_card(item) for item in email_items)

    return f"""
      <tr>
        <td style="padding: 28px 32px; border-bottom: 1px solid {COLORS['border']};">
          {_section_header(f"Inbox Triage  ·  {len(email_items)} unread")}
          <table cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 20px;">
            <tr>{pills}</tr>
          </table>
          <table width="100%" cellpadding="0" cellspacing="0" border="0">
            {cards}
          </table>
        </td>
      </tr>
    """


def _render_footer():
    return f"""
      <tr>
        <td style="padding: 22px 32px; text-align: center;">
          <p style="margin: 0; font-size: 12px; color: {COLORS['muted']}; line-height: 1.5;">
            Sent automatically by your Daily Assistant Agent
            <br>
            <span style="color: {COLORS['border']};">&middot; &middot; &middot;</span>
          </p>
        </td>
      </tr>
    """


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def render_briefing_html(name, weather, general_news, business_news, email_items):
    """
    Build the complete HTML email body.

    Args:
        name (str): Recipient first name.
        weather (dict | None): Output of weather.get_weather_data().
        general_news (list[dict]): Output of news.get_general_news().
        business_news (list[dict]): Output of news.get_business_news().
        email_items (list[dict]): Each item must have keys
            'classification', 'subject', 'from', and optionally
            'draft_saved' (bool) and 'draft_text' (str).

    Returns:
        str: Complete HTML document ready to send as the email body.
    """
    today = datetime.date.today()

    body = (
        _render_header(name, today)
        + _render_weather(weather)
        + _render_news_section("Top News", general_news)
        + _render_news_section("Business & Finance", business_news)
        + _render_email_section(email_items)
        + _render_footer()
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your Daily Briefing</title>
</head>
<body style="margin: 0; padding: 0; background-color: {COLORS['page_bg']}; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; color: {COLORS['text']}; -webkit-font-smoothing: antialiased;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: {COLORS['page_bg']}; padding: 24px 12px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; width: 100%; background-color: {COLORS['card_bg']}; border-radius: 14px; overflow: hidden; box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06);">
          {body}
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""
