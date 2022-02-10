#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <cs50.h>

int main(int argc, string argv[])
{
    // Errors handling
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    for (int k = 0; k < strlen(argv[1]); k++)
    {
        if (!isdigit(argv[1][k]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    // Defining variables
    string key = argv[1];
    string plaintext = get_string("plaintext: ");

    // Transform to integer
    int k = atoi(key);
    printf("ciphertext: ");

    // Print out according with the word
    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (isupper(plaintext[i]))
        {
            printf("%c", (((plaintext[i] - 65) + k) % 26) + 65);
        }
        else if (islower(plaintext[i]))
        {
            printf("%c", (((plaintext[i] - 97) + k) % 26) + 97);
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
}