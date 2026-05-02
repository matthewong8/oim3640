# Week 11 (4/9)

## What I learned this week
- MP3 due 4/21 (Web App with MBTA + Mapbox)
- wrote MP3 proposal in class
- more flask
  - turning python scripts into web apps
  - dynamic routes: <name> and <int:n> in the url
    - example: @app.route('/hello/<name>')
  - render_template() to use html files
- HTML forms
  - method="POST", action="..."
  - access form data with request.form['fieldname']
- template inheritance
  - base template with {% block %} blocks
  - child templates fill them in
- flask app structure
  - app.py, helper modules, templates/, static/
  - .env for API keys

## Code I'm proud of (Optional)

## Challenges I feel
- jinja2 syntax with {% %} and {{ }} is confusing
- still wrapping my head around template inheritance

## AI Usage (If any)
- copilot helped me with the MP3 proposal

## Questions going forward
- whats the difference between {% %} and {{ }} in templates?
