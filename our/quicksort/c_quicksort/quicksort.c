#include<stdio.h>


void swap(int* a, int* b)
{
    int t = *a;
    *a = *b;
    *b = t;
}

int partition (int arr[], int low, int high)
{
    int pivot = arr[high];
    int i = (low - 1);
 
    for (int j = low; j <= high- 1; j++)
    {
        if (arr[j] <= pivot)
        {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

void quickSort(int arr[], int low, int high)
{
    if (low < high)
    {
        int pi = partition(arr, low, high);
 
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

void printArray(int arr[], int size)
{
    int i;
    for (i=0; i < size; i++)
        printf("%d ", arr[i]);
    printf("n");
}

int main(int argc, char** argv)
{
    char *input = argv[1], *output = argv[2];
    int i = 0, j = 0;
    int inputArray[1000000];

    FILE *inputFile, *outputFile;
    inputFile = fopen(input, "r");

    for (i = 0; i < 1000000; i++)
    {
        fscanf(inputFile, "%d ", &inputArray[i]);
    }

    int n = sizeof(inputArray)/sizeof(inputArray[0]);
    quickSort(inputArray, 0, n-1);

    outputFile = fopen(output, "w");
    for(j = 0; j < 1000000; j++) {
        fprintf(outputFile, "%d\n", inputArray[j]);
    }

    //printf("Sorted array: n");
    //printArray(inputArray, n);
    return 0;
}

