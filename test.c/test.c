#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

string word = get_string("Player 1: ");
int ascii = word[0] - 1;
printf("This is %i", ascii);