# Week 9 (3/24/2026)

## What I learned this week
- tuples
  - like lists but cant be changed once made
  - still support indexing and slicing
- tuple unpacking
  - a, b = b, a (swap without a temp variable, pretty cool)
  - functions can return multiple things as a tuple
- can use tuples as dict keys
  - lists cant because theyre mutable, tuples can because theyre not
- zip() pairs up two lists
  - dict(zip(...)) makes a quick lookup
- sets
  - unordered, no duplicates
  - set(['AAPL', 'AAPL']) becomes {'AAPL'}
- set operations
  - & intersection (whats in both)
  - | union (everything from both)
  - - difference (in A but not B)
- sets WAY faster than lists for "in" checks (slides said 2800x)
- text analysis - using everything together
  - count words, find top 10, find words that only appear once (hapax legomena)

## Code I'm proud of (Optional)

## Challenges I feel
- knowing when to use tuple vs list, they look the same to me
- set operations feel like math i forgot

## AI Usage (If any)
- asked copilot to explain tuple unpacking

## Questions going forward
- when do I use dict vs set vs Counter for MP2?
- how do I prep for Quiz 2?
