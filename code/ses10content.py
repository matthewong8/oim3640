for renee in range(4):
    print(renee)

for letter in 'Saad Abdullah':
    print(letter)

count = 0
for letter in "Babson College":
    count += 1
    print(count)

count = 0
for c in "Babson College":
    count += 1
    print(count)

count = 0
for c in "100 years!":
    count += 1  # means count = count + 1
    print(count)

n = 5
while n > 0:
    print(n)
    n -= 2

print('after while loop, n is', n)

n = 5
while True:
    if n <= 0:
        break
    print(n)
    n -= 2

def uses_any(word, letters):
    for letter in word:
        if letter in letters:
            return True
        else:
            return False

print (uses_any('hello', 'xyz'))
print (uses_any('hello', 'aeiou'))
print (uses_any('orange', 'aeiou'))

def version_a(word):
    for letter in word:
        if letter in 'aeiou':
            print(letter)
    print('Done')

def version_b(word):
    for letter in word:
        if letter in 'aeiou':
            return letter
    return 'None found'

# version_a('hello')
# print('---')
# print(version_b('hello'))

version_a('nbc')
print('---')
print(version_b('nbc'))

import random

roll = 0
while roll != 6:
    roll = random.randint(1, 6)
    print("Rolled:", roll)
    if roll > 3:
        print("That's a high roll!")
    else:
        print("That's a low roll!")

print("Got a 6, stopping.")

name = 'chloe'
name[0]
name[1]
name[2]
name[4]


name = 'chloe'
name_backup = name
id(name)