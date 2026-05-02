# Week 12 (4/16)

## What I learned this week
- final project proposal due tomorrow (4/17)
- MP3 due 4/21
- final project timeline:
  - Proposal: 4/17
  - Gallery Walk: 4/28
  - Peer Review: 4/30
  - Final Submission: 5/1
- API key protection
  - locally: .env file + python-dotenv, ALWAYS add .env to .gitignore
  - production: Render's environment variables dashboard
- Flask deployment
  - need requirements.txt
  - gunicorn = production server (not the flask dev server)
  - 2 platforms covered: Render and PythonAnywhere
- Render deployment
  - connect github repo
  - set root directory if app isnt at top level
  - start command: "gunicorn app:app"
- PythonAnywhere
  - beginner account, bash console, clone repo, configure web tab
- common gotchas:
  - dont leave debug=True in production
  - missing packages in requirements.txt
  - file path issues
  - cold start delays
- frontend / backend / fullstack - different parts of web apps

## Code I'm proud of (Optional)

## Challenges I feel
- so many deadlines stacking up
- not sure if Render or PythonAnywhere is better

## AI Usage (If any)
- copilot helped me write my final project proposal

## Questions going forward
- what does "gunicorn app:app" actually mean?
- how do I avoid the cold start issue?
