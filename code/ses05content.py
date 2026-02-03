# a product would cost $100, how much tax do we pay?


product = 100  # in dollars
tax_rate = 0.0625
tax = product * tax_rate
print(f'The tax for the product which costs {product} is ${tax}.')  # f string

def calc_tax(price):
    """Calculate product tax based on given price"""
    tax_rate = 0.0625
    tax = price * tax_rate
    print(f'The tax for the product which costs {price} is ${tax}.')

#calc_tax(computer_price)
#calc_tax(iphone_price)

total_tax = calc_tax(computer_price) + calc_tax(iphone_price)
print(total_tax)