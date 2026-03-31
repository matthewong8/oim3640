freq = {'a': 3, 'b': 1, 'c': 2}
result = sorted(freq.items(), key = lambda x: x[1])
print(result)

import yfinance as yf
from pprint import pprint

tickers = ['AAPL', 'NVDA', 'MSFT', 'META', 'GOOG']
stocks = {}

for t in tickers:
    stocks[t] = yf.Ticker(t).info['currentPrice']
    # create a dictionary with the current price of each stock

print(stocks)

print('After sorting...')

def sort_by_price(t):
    return t[1] # helper function to sort by price in the tuple (the value in the k:v pair)

print(sorted(stocks.items(), key=sort_by_price))
print(sorted(stocks.items(), key=lambda t: t[1])) # same thing but using a lambda function instead of a helper function

a = [('c', 2), ('a', 3), ('b', 1), ('c', 1)]
sorted(a)


num = 100
try:
    a = float(input("Enter a number to divide by: "))
    print(num/a)
except ZeroDivisionError:
    print("Error: Division by zero is not allowed.")
except ValueError:
    print("Error: Please enter a valid number.")
finally:
    print('We still want to print this!')

# print("Let's move on to the next part of the code...")

names = ['Alice', 'Bob', 'Charlie']
uppercase_names = []

for name in names:
    try:
        print(name.upper())
        uppercase_names.append(name.upper())
    except AttributeError:
        print(f"Error: {name} is not a string.")

print("Uppercase names:", uppercase_names)

print("Let's move on to the next part of the code...")
