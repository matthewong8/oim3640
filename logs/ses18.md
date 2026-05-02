# Week 10 (3/31)

## What I learned this week
- error handling
  - common errors: NameError, TypeError, IndexError, KeyError, FileNotFoundError
  - try/except blocks so the program doesnt crash
  - can catch specific exceptions: except ValueError:
- APIs and JSON
  - requests library to talk to APIs
  - requests.get() vs requests.post()
  - JSON basically converts straight to a python dict
  - GET = ask for data, POST = send data
- API keys go in a .env file (NEVER commit to github)
  - python-dotenv loads them
- saw OpenAI API code
- public APIs that need no key (Open Notify, CoinDesk)

## Code I'm proud of (Optional)

## Challenges I feel
- nested JSON is confusing
- forgot to add .env to .gitignore at first

## AI Usage (If any)
- copilot helped me write try/except blocks

## Questions going forward
- how deep can JSON nesting go before I should give up
- when do you actually use POST vs GET in real apps?
