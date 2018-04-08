# Codigo referente a multiplicacao entre duas matrizes
# Feito por Vilmar Neto
x = [[2,4],
     [4,8]]


y = [[1,0],
     [0,1]]

result = [[sum(a*b for a,b in zip(x_row,y_col)) for y_col in zip(*y)] for x_row in x]

for r in result:
	print(r)
