# Import the get_int from cs50
from cs50 import get_int

# ask for height and check if user provided a valif value
while True:
    height = get_int("Specify height of the pyramide: ")
    if height > 0 and height < 9:
        break

# print pyramide
for i in range(height):
    print(" " * (height - i - 1), end="")
    print("#" * (i + 1), end=" ")
    print(" " + "#" * (i + 1),)