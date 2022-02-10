#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // h = height, r = row, s = space, c = column
    int h;
    do
    {
    h = get_int("Height: ");
    }
    while (h < 1 || h > 8);

    {
        for(int r = 0; r < h; r++)
        {
            for(int s = 0; s < h - r - 1; s++)
            {
                printf(" ");
            }
            for(int c = 0; c <= r; c++)
            {
                printf("#");
            }
            printf("\n");
        }
    }
}
