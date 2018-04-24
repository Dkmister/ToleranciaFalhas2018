
#include<stdio.h>

#include<stdlib.h>
/*

This program does Matrix Multiplication on 2 matrices
that are present in files in the current directory
The output is printed onto STDOUT

Author: Sidharth N. Kashyap
*/

//Change this if you need to modify the size of the matrix
#define MATRIX_SIZE 3
/*
This function reads the matrix into a 2D array and returns the pointer
*/

int** readMatrix(char* fileName)
{
  FILE *fp;
  int** matrix;
/*Allocate the matrix dynamically and read the file
you need to give sizeof(int*) as this
holds the pointer to array to be allocated in the next step*/
  matrix =malloc(sizeof(int*)*MATRIX_SIZE);
  int i=0;
int j=0;
for(i=0;i<MATRIX_SIZE;i++)
  { //Allocate actual integer pointers
       matrix[i]=malloc(sizeof(int)*MATRIX_SIZE);
       if(matrix[i] == NULL)
       {
          fprintf(stderr, "out of memory\n");
          exit(0);
       }
  }

/*
The allocation of memory is now complete,
read the file and store into memory allocated
*/
   fp = fopen(fileName,"r");
   for(int k=0;k<MATRIX_SIZE;k++)
   {

       for(j=0;j<MATRIX_SIZE;j++)
       {
              int test;
              fscanf(fp,"%d",&test);
              matrix[k][j] = test;
       }
    }
    fclose(fp);
return matrix;
}

/*
This function does the matrix multiplication,
you need 3 loops as you need to traverse 2 arrays
and perform addition

The result of multiplication is added to the sum

The value of sum is then stored to result array
*/
int** matrixMultiply(int** matrix1, int** matrix2)
{
  int** result;
   result = malloc(sizeof(int*)*MATRIX_SIZE);
   for(int i=0;i<MATRIX_SIZE;i++)
   {
        result[i] = malloc(sizeof(int)*MATRIX_SIZE);
   }
   for (int i=0;i<MATRIX_SIZE;i++)
   {
       for(int j=0;j<MATRIX_SIZE;j++)
       {
           int sum = 0;
           for(int k=0;k<MATRIX_SIZE;k++)
           {
              int item1 = matrix1[i][k];
              int item2 = matrix2[k][j];
              int mul = item1*item2;
              sum = sum + mul;
          }
          result[i][j] = sum;
      }
  }
return result;
}

int main()
{

//change these file names if you need
   char* fileName1 = "matrix1.txt";
   char* fileName2 = "matrix2.txt";
//pointers
    int** matrix1;
    int** matrix2;
    int** result;
    matrix1 = readMatrix(fileName1);
    matrix2 = readMatrix(fileName2);
    result = matrixMultiply(matrix1, matrix2);

//print the matrix, comment out if you dont need this
    for(int k=0;k<MATRIX_SIZE;k++)
    {
        printf("\n");
        for(int j=0;j<MATRIX_SIZE;j++)
        {
            printf("%d\t",result[k][j]);
        }
    }
free(matrix1);
free(matrix2);
free(result);


return 0;
}
