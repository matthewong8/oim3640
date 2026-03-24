# Live Demo: Real Stock Data

import yfinance as yf

stock = yf.Ticker('AAPL')
info = stock.info
print(type(info))

# print(info.keys())
print(len(info))
print(info['shortName'])
print(info['longName'])
print(info['currentPrice'])

print(info['longBusinessSummary'])

print(info['longBusinessSummary'].split())
print('iPhone' in info ['longBusinessSummary'].split())
print('iPhone' in info ['longBusinessSummary'])
print(info['city'])
info['city'][0] = 'c'  # WRONG! Strings are immutable.
info['city'] = 'Wellesley'  # WRONG! info is a dictionary, but the value is a string, which is immutable.
print(info['city'])

info['founder'] = 'Robert'
print(info['founder'])

for k, v in info.items():
    print(k, v)

tickers = ['AAPL', 'NVDA', 'MSFT']
prices = {}
for t in tickers:
    prices[t] = yf.Ticker(t).info['currentPrice']
print(prices)

print(sorted(prices)) # create a new list of the keys in sorted order
print(sorted(prices.keys()))
print(sorted(prices.values(), reverse = True)) # create a new list of the values in sorted order, from largest to smallest

# how to sort stocks by values but still to show k: v?

print(tickers)
prices = {'AAPL': [252.53, 300], 'NVDA': [174.33, 209], 'MSFT': [372.845, 300]}
print(sum(v[0] for v in prices.values()))

total = 0
for price in prices.values():
    total += price[0]
print(total)

tickers.append('GOOG')
print(tickers)
# tickers = {}
for t in tickers:
    stock = yf.Ticker(t)
    prices[t] = stock.info['currentPrice']
print(prices)

tickers = ['AAPL', 'NVDA', 'MSFT']
stocks = {} # {'NVDA': [open, currentPrice, volume]}

for t in tickers:
    stocks[t] = yf.Ticker(t).info['open'], yf.Ticker(t).info['currentPrice'], yf.Ticker(t).info['volume'] # create a tuple of the three values and assign it to the key t in the stocks dictionary
    stocks[t] = [yf.Ticker(t).info['open'], yf.Ticker(t).info['currentPrice'], yf.Ticker(t).info['volume']] # create a list of the three values and assign it to the key t in the stocks dictionary
    info_list = {}
    for name in ['open', 'currentPrice', 'volume']:
        info_list[name] = yf.Ticker(t).info[name]
    stocks[t] = info_list

stocks['AAPL']['currentPrice'] = 260
print(stocks)


# Tuple unpacking and string splitting
tel = '124-567-8901'
a, b, c = tel.split('-')
c
*_, ext = tel.split('-')
ext
phonebook = ['124-567-8901', '987-654-3210']
for p in phonebook:
    *_, last four = p.split('-')
    print(last four)

# Tuples as dict keys

prices = {['AAPL', '2026-03-24']: 229} # WRONG! Lists are mutable, so they cannot be used as keys in a dictionary.
prices = {('AAPL', '2026-03-24'): 229} # RIGHT! Tuples are immutable, so they can be used as keys in a dictionary.

# Sets Unique Collections

watchlist = {'AAPL', 'NVDA', 'MSFT'}
print(watchlist) # Sets are unordered, so the order of the elements may not be the same as the order in which they were added.

tickers = ['AAPL', 'NVDA', 'MSFT', 'AAPL', 'NVDA'] # Lists can contain duplicates, so the same ticker can appear multiple times in the list.
unique = set(tickers) # Sets automatically remove duplicates, so the resulting set will only contain unique tickers.
len(set(tickers))

import timeit

words = open('words.txt').read().split()
word_set = set(words)

def search_list():
    return "zebra" in words

def search_set():
    return "zebra" in word_set

print('List:', timeit.timeit(search_list, number=1000))
print('Set:', timeit.timeit(search_set, number=1000))
#List: 0.8500s Set: 0.0003s