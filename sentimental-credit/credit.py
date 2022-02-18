from cs50 import get_string

# Get the number to the variable and pass it to an unique function that checks and print it
def main():
    card_number = get_string("Card Number: ")
    print_card_flag(card_number)

# Check the functions that fits in and then print it flag
def print_card_flag(card_number):
    if (check_sum(card_number)) == False:
        print("INVALID")
    elif (check_amex(card_number)) == True:
        print("AMEX")
    elif (check_mastercard(card_number)) == True:
        print("MASTERCARD")
    elif (check_visa(card_number)) == True:
        print("VISA")

def check_sum(card_number):
    # initialise variables
    sum = 0
    length = len(card_number)

    # sum_of_double(i) = sum of digits in 2i. defined for i in range(10)
    sum_of_double = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]

    # loop through card_number and add the digits contribution to checksum
    for i in range(length):
        ith_digit_from_right = int(card_number[length-1-i])

        # if i is even, then we are in odd position from right, so just add ith digit
        if i % 2 == 0:
            sum += ith_digit_from_right

        # if i is odd, we are at even position from right, so add double of ith digit
        else:
            sum += sum_of_double[ith_digit_from_right]

    # if final digit in sum is 0, then passes checksum test
    if sum % 10 == 0:
        return True
    else:
        return False

def check_amex(card_number):
    # if card_number satisfies amex conditions, return True otherwise false
    if len(card_number) == 15 and int(card_number[:2]) in [34,37]:
        return True
    else:
        return False

def check_mastercard(card_number):
        # if card_number satisfies amex conditions, return True otherwise false
    if len(card_number) == 16 and int(card_number[:2]) in [51, 51, 53, 54, 55]:
        return True
    else:
        return False

def check_visa(card_number):
        # if card_number satisfies amex conditions, return True otherwise false
    if len(card_number) in [13,16] and int(card_number[0]) == 4:
        return True
    else:
        return False

# Run the programming
main()