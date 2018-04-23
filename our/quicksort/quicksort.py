import sys

def a_swap(array = [], li = 0, ri = 0):
    aux = array[li]
    array[li] = array[ri]
    array[ri] = aux

def partition(array, begin, end):
    pivot = array[begin];
    left_index = begin + 1;
    right_index = end;
    done = False
    while not done:
        while left_index <= right_index and array[left_index] < pivot:
            left_index += 1
        while right_index >= left_index and array[right_index] >= pivot:
            right_index -= 1
        if left_index > right_index:
            done = True
        else:
            a_swap(array, left_index, right_index)
    a_swap(array, begin, right_index)
    return right_index

def quicksort(array = [], begin = 0, end = 0):
    if begin < end:
        split_at = partition(array, begin, end)
        quicksort(array, begin, split_at)
        quicksort(array, split_at + 1, end)


inputname = str(sys.argv[1])
outputname = str(sys.argv[2])
with open(inputname, 'r') as file:
    array = []
    output = ''
    substr = ' '
    line = file.readline()
    for i in line:
        if (i != ' '):
            substr += i
        else:
            array.append(int(substr)); substr = ' '
    array.append(int(substr));
    print('Initial Array:\t', array)
    quicksort(array, 0, len(array) - 1)
    print('Sorted Array:\t', array)
    with open(outputname, 'w') as file:
        for number in array[:-1]:
            output += str(number)
            output += ' '
        output += str(array[-1])
        file.write(output)
