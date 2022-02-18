# Import the get_string function
from cs50 import get_string

def main():
    # Get the text from the user
    text = get_string("Text: ")

    # Count all Letters, sentences and words
    numLetters = getNumLetters(text)
    numWords = getNumWords(text)
    numSentences = getNumSentences(text)

    # Get the grade level number given by the function
    gradeLevel = getGradeLevel(numLetters, numSentences, numWords)

    # Print the grade level
    printGradeLevel(gradeLevel)

def getNumLetters(text):
    letters = 0
    for i in text:
        if i.isalpha():
            letters += 1
    return letters

def getNumWords(text):
    words = 0
    for i in text:
        if i == " ":
            words += 1
    words += 1
    return words

def getNumSentences(text):
    sentences = 0
    for i in text:
        if i == "?" or i == "!" or i == ".":
            sentences += 1
    return sentences

def getGradeLevel(letters, sentences, words):
    s = sentences / words * 100
    l = letters / words * 100

    return round(0.0588 * l - 0.296 * s - 15.8);

def printGradeLevel(level):
    if level <= 1:
        print("Before Grade 1")
    elif level >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {level}")

main()