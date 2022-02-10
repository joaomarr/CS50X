// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

typedef uint8_t BYTE;
typedef int16_t SAMPLE_AUDIO;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // Copying the header
    BYTE headerBuffer[HEADER_SIZE]; // Creating an empty array of bytes, a buffer

    fread(headerBuffer, sizeof(BYTE), HEADER_SIZE, input); // Reading and copying the input header to headerBuffer
    fwrite(headerBuffer, sizeof(BYTE), HEADER_SIZE, output); // Passing the arguments of headerBuffer to the new output file

    // Updating the output file to the factor of volume

    SAMPLE_AUDIO buffer;

    while (fread(&buffer, sizeof(SAMPLE_AUDIO), 1, input) == 1) // Looping through input SAMPLE_AUDIO
    {
        buffer = buffer * factor;
        fwrite(&buffer, sizeof(SAMPLE_AUDIO), 1, output);
    }

    // Close files
    fclose(input);
    fclose(output);
}
