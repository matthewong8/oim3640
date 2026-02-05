for i in range(4):
    print("Iteration:", i)
    print("Square:", i*i)
    print()

def double(number):
    """Return double the input number."""
    return number * 2

print(double(5))
print(double("Hi"))
print(double([1, 2, 3]))

x = 10

def f():
    message = "Hello"
    x = 5
    return message + str(x)
print(f())
print(x)
print(message)

# Draw a square
"""
🟫🟫🟫🟫
🟫🟫🟫🟫
🟫🟫🟫🟫
🟫🟫🟫🟫
"""

def draw_square(size):
    for i in range(size):
        print("🟫" * size)
        for j in range(size):
            print("🟫", end="")
        print()

def draw_square(size):
    for i in range(size):
        print("🟫" * size)

draw_square(4)

"""
# create a function to draw a triangle
🟫              1 = 0 + 1
🟫🟫            2 = 1 + 1
🟫🟫🟫          3 = 2 + 1
🟫🟫🟫🟫        4 = 3 + 1


In row i, how many blocks are there? i + 1
"""
def draw_triangle(rows):
    for i in range(rows):
        print("🟫" * (i + 1))

draw_triangle(4)

"""
Draw a triangle like this (size = 5)

    #               4 spaces + 1 # = 5  5 - 0 - 1 = 4
   ##               3 spaces + 2 # = 5  5 - 1 - 1 = 3
  ###               2 spaces + 3 # = 5  5 - 2 - 1 = 2    
 ####               1 spaces + 4 # = 5  5 - 3 - 1 = 1
#####               0 spaces + 5 # = 5  5 - 4 - 1 = 0  

for i in range(size):
In row i, how many spaces are there? size - i - 1
how many #s are there? i + 1
"""

def draw_triangle(size):
    for i in range(size):
        print (" " * (size - i - 1) + "#" * (i + 1))

draw_triangle(5)

# create a function to draw a pyramid
"""
    #           4 spaces + 1 # = 5  5 - 0 - 1 = 4
   ###          3 spaces + 3 # = 6  6 - 1 - 2 = 3
  #####         2 spaces + 5 # = 7  7 - 2 - 3 = 2
 #######        1 spaces + 7 # = 8  8 - 3 - 4 = 1

for i in range(size):
In row i, how many spaces are there? size - i - 1
how many #s are there? i + 1
"""