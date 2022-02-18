import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # Define the max sequences of the person
    sequences = {}

    # Read database file into a variable
    with open(sys.argv[1]) as database:
        reader = csv.DictReader(database)
        strs_tested = reader.fieldnames[1:]

    # Read DNA sequence file into a variable
    sequence = open(sys.argv[2], 'r').read()

    # TODO: Find longest match of each STR in DNA sequence
    for str in strs_tested:
        str_max = longest_match(sequence, str)
        sequences[str] = str_max


    # Check database for matching profiles
    with open(sys.argv[1]) as database:
        reader = csv.DictReader(database)
        for person in reader:
            match = 0
            for str in sequences:
                if int(person[str]) == sequences[str]:
                    match += 1
            if match == len(sequences):
                print(person["name"])
                exit(0)
    return print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    sequence_length = len(sequence)
    subsequence_length = len(subsequence)


    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

            # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
