#include <stdio.h>
#include <cs50.h>

void print_credit_card_brand(long long ccn);
bool checksum(long long ccn);
int find_length(long long n);
bool check_validity(long long credit_card_number);

int main(void)
{
    long long credit_card_number;
    do
    {
        credit_card_number = get_long_long("Number: ");
    }
    while (credit_card_number < 0);

    if(check_validity(credit_card_number))
        print_credit_card_brand(credit_card_number);
    else
        printf("INVALID\n");
}

bool check_validity(long long credit_card_number)
{
    int len = find_length(credit_card_number);
    return (len == 13 || len == 15 || len == 16) && checksum(credit_card_number);
}

int find_length(long long n)
{
    int len;
    for (len = 0;n != 0; n /= 10, len++);
    return len;
}

bool checksum(long long ccn)
{
    int sum = 0;
    for(int i = 0; ccn != 0; ccn /= 10, i++)
    {
        if (i % 2 == 0)
        {
            sum += ccn % 10;
        }
        else
        {
            int digit = 2 * (ccn % 10);
            sum += digit / 10 + digit % 10;
        }
    }
    return (sum % 10) == 0;
}

void print_credit_card_brand(long long ccn)
{
    if ((ccn >= 34e13 && ccn < 35e13) || (ccn >= 37e13 && ccn < 38e13))
        printf("AMEX\n");
    else if (ccn >= 51e14 && ccn < 56e14)
        printf("MASTERCARD\n");
    else if ((ccn >= 4e12 && ccn < 5e12) || (ccn >= 4e15 && ccn < 5e15))
        printf("VISA\n");
    else
        printf("INVALID\n");
}