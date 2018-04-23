# Codigo referente a multiplicacao entre duas matrizes
# Feito por Vilmar Neto

"""
function:
matrix result:= mat_mult (matrix a, matrix b)

Given 2 matrixes that can be multiplied, returns the result of the matrix multiplication.

It does the sum of the multiplication of each element in their place.

"""


def mat_mult(x,y):
	result = [[sum(a*b for a,b in zip(x_row,y_col)) for y_col in zip(*y)] for x_row in x]
	return result



x = [[2,4],
     [4,8]]


y = [[1,0],
     [0,1]]

result =  mat_mult(x,y)
for r in result:
	print(r)
