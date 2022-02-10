#include "helpers.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int i, j;
    float floatr, floatg, floatb, avg;

    for (i = 0; i < height; i++)
    {
        for (j = 0; j < width; j++)
        {
            RGBTRIPLE pixel = image[i][j];
            floatr = pixel.rgbtRed;
            floatg = pixel.rgbtGreen;
            floatb = pixel.rgbtBlue;
            // Average of the amount of color in pixels
            avg = round((floatr + floatg + floatb) / 3.0);

            // Setting up the average color to the pixels colors
            image[i][j].rgbtRed = image[i][j].rgbtGreen = image[i][j].rgbtBlue = avg;
        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int i, j, sepiaRed, sepiaGreen, sepiaBlue, originalRed, originalGreen, originalBlue;
    float r, g, b;

    for (i = 0; i < height; i++)
    {
        for (j = 0; j < width; j++)
        {
            // Creating variables
            RGBTRIPLE pixel = image[i][j];
            originalRed = pixel.rgbtRed;
            originalGreen = pixel.rgbtGreen;
            originalBlue = pixel.rgbtBlue;

            // Setting up the sepia colors
            sepiaRed = round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);
            sepiaGreen = round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);
            sepiaBlue = round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);

            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            // Setting up the pixels colors to sepia colors
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int i, j;
    // Image buffer
    RGBTRIPLE bufferImg;

    // Iterate over every row of the image
    for (i = 0; i < height; i++)
    {
        // Iterate over every column that are less than width / 2
        for (j = 0; j < width / 2; j++)
        {
            // Storing the image in the buffer
            bufferImg = image[i][j];
            // Swap pixels on horizontally opposite sides
            image[i][j] = image[i][width - j - 1];
            // Setting back the other half of the image
            image[i][width - j - 1] = bufferImg;
        }
    }
    return;
}

int getBlur(int i, int j, int height, int width, RGBTRIPLE image[height][width] , int color_position)
{
    float counter = 0;
    int sum = 0;

    // Start from 1 row before it and end at 1 row after it- total of 3rows */
    for (int k = i - 1; k < (i + 2); k++)
    {
        // Start from 1 block before it and end at 1 block after it- total of 3blocks */
        for (int l = j - 1; l < (j + 2); l ++)
        {
            if (k < 0 || l < 0 || k >= height || l >= width)
            {
                continue;
            }
            if (color_position == 0)
            {
                sum += image[k][l].rgbtRed;
            }
            else if (color_position == 1)
            {
                sum += image[k][l].rgbtGreen;
            }
            else
            {
                sum += image[k][l].rgbtBlue;
            }
            counter++;

        }
    }
    return round(sum / counter);
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = getBlur(i, j, height, width, copy, 0);
            image[i][j].rgbtGreen = getBlur(i, j, height, width, copy, 1);
            image[i][j].rgbtBlue = getBlur(i, j, height, width, copy, 2);
        }
    }
    return;
}
