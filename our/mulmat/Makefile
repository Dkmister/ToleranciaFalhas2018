# C compiler
CC = gcc -g
CC_FLAGS = -fopenmp

destDir = /tmp/mulmat

all: gen_bin gen_data mv_bin

gen_bin: mulmat.c
	$(CC) $(CC_FLAGS) mulmat.c -o mulmat

gen_data: gen_bin
	./mulmat matrix1.txt matrix2.txt result

mv_bin: gen_data
	mkdir -p $(destDir)
	mv mulmat result $(destDir)
	@echo "All Done, executables should be in the $(destDir)"


