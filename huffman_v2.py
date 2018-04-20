# Huffman.py Desc:
#   Taking three arguments:
#   setting := argv[1] --- sets if it will compress or decompress (compress or decompress)
#   input_filename := argv[2] --- sets the input file name (with extension)
#   output_filename := argv[3] --- sets the output file name (with extension, has to be bin if set to compress)
#       Script call example: python huffman.py compress text.txt output.bin
# ---------------------------------------------------------------------------------------------------------------------
#   if set to compress (mode c) it:
#       parses the bytes, counts their frequencies and places them in a Counter()
#       then builds a tree based on that collection of frequencies using:
#           def build_tree()
#
#       builds a dict for the bytes and their shorthands, based on the tree, using:
#           def build_dict()
#
#       builds a header describing the tree using:
#           def build_header()
#
#       translates the file's bytes into the encoding and writes to output file using:
#           def build_file()
#
#   returns a compressed file of the .bin format (Note: manage so that non-bin extensions return an error)
# ---------------------------------------------------------------------------------------------------------------------
#   if set to decompress (mode d) it:
#       1. translates the header into a new translation tree using::
#           def rebuild_tree()
#
#       2. rebuilds a new conversion dict based on said tree using:
#           def build_dict() -- same as in the previous method
#
#       3. translates the file's bytes into the decoded version and saves them, using:
#           def build_file() -- note: method must be format agnostic
#
#   returns a decompressed file of the specificed format
import sys
from collections import Counter


class BinaryTree:
    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None
        self.index = None
        self.freq = 0


# print_tree desc:
#   Auxiliary method used for testing
#   Prints a tree's structure, depth first
def print_tree(node, i):
    print(i,'Value: ', node.index, ' Freq: ', node.freq,  '\n')
    if node.right: print_tree(node.right, i + '\t')
    if node.left: print_tree(node.left, i + '\t')


# get_new_node() desc:
#   Auxiliary method used by build tree
#   Returns a Tree Node equivalent to the least common element of the frequency collection
def get_new_node(parent):
    node = BinaryTree()
    least_common_pair = freq_counter.most_common(len(freq_counter))[-1]
    # selects least common node
    if least_common_pair[0] in node_list:
        node = node_list[least_common_pair[0]]
        del node_list[least_common_pair[0]]
    else:
        node.index = least_common_pair[0]
        node.freq = freq_counter[node.index]
        node.parent = parent
    del freq_counter[node.index]
    return node


# build_tree() desc:
#   Uses a collection of frequencies and a list of existing nodes
#   Returns a binary tree based on Huffman's Algorithm
def build_tree():
    node_number = 0
    node = BinaryTree()
    while len(freq_counter) > 1:
        node = BinaryTree()
        node.left = get_new_node(node)
        node.right = get_new_node(node)
        node.index = 'node' + str(node_number)
        node.freq =  node.right.freq + node.left.freq
        freq_counter[node.index] = node.freq
        node_list[node.index] = node
        # List of existing nodes - avoids recreating nodes
        node_number += 1
    return node


# build_dict() desc:
#   Using a Huffman encoding tree
#   Returns a dictionary that stores the translation from regular data to its compressed representation
def build_dict(node, code):
    if node.right:
        build_dict(node.right, code + '1')
    if node.left:
        build_dict(node.left, code + '0')
    if not node.left and not node.right:
        conversion_dictionary[node.index] = code
    return 0


# build_header() desc:
#   Builds a header that describes the tree used to encode the file
#   Returns said header in string format.
def build_header(node, header):
    #print(header)
    #print('index is ', node.index)
    if type(node.index) is int:
        header += '1'
        char_code = bin(node.index)
        #print('node is ', str(char_code[2:]).zfill(8))
        header += str(char_code[2:]).zfill(8)
        return header
    else:
        header += '0'
        header = build_header(node.left, header)
        header = build_header(node.right, header)
        return header


# build_file() desc:
#   Receives a string of bits
#   creates and writes said data selected output file
def build_file():
    with open(output_filename, 'wb') as output_file:
        i = 0
        byte = ''
        l_byte = 64
        byte_array = []
        for bit in output_data:
            if i == 7:
                byte += bit
                byte_array.append(int(byte, base=2))
                i = 0
                byte = ''
            else:
                byte += bit
                i += 1
        if i > 0:
            l_byte += i
            while i < 8:
                i += 1
                byte += '0'
            byte_array.append(int(byte, base=2))
        byte_array.append(l_byte)
        output_file.write(bytes(byte_array))
    return 0


# make_new() desc:
#   Searches for a free position for a new node in the existing structure
#   Returns a link to the created node
def make_new(node):
    if not node:
        node = BinaryTree()
        return node
    elif not node.left:
        node.left = BinaryTree()
        node.left.parent = node
        return node.left
    elif not node.right:
        node.right = BinaryTree()
        node.right.parent = node
        return node.right
    elif not node.parent:
        return -1
    else:
        return make_new(node.parent)


# rebuild_tree() desc:
#   Receives a compressed file. Analyzes the header and rebuilds the huffman tree.
#   Returns the huffman tree and the data start point (that is, post-header)
def rebuild_tree(bit_string):
    i = 0; j = 1; d_start = 0; new_char = ''; root_node = BinaryTree()
    node = root_node
    for bit in bit_string[1:]:
        j += 1
        if i > 0:
            new_char += bit
            i -= 1
            if i == 0:
                node.index = int(new_char,2)
                node = node.parent
                new_char = ''
        elif i == 0 and bit == '0':
            node = make_new(node)
            if node == -1:
                d_start = j
                i = -1
        elif i == 0 and bit == '1':
            node = make_new(node)
            i = 8
            if node == -1:
                d_start = j
                i = -1
    return root_node, d_start


# translate_file()
#   Converts the file data to a binary string according to the dictionary
#   Returns said compressed data string
def translate_file_c():
    output_str = ''
    for byte in file_data:
        output_str += conversion_dictionary[byte]
    return output_str


def translate_file_d(bit_string):
    output = []
    code = ''
    for bit in bit_string[data_start-1:-(8 - last_byte)]:
        code += bit
        if code in inverted_dictionary:
            output.append(inverted_dictionary[code])
            code = ''
    return output

def rebuild_file():
    with open(output_filename, 'wb') as output_file:
        output_file.write(bytes(output_data))
    return 0


# Main:
setting = str(sys.argv[1])
input_filename = str(sys.argv[2])
output_filename = str(sys.argv[3])
with open(input_filename, 'rb') as file:
    file_data = file.read()
    conversion_dictionary = dict()
    inverted_dictionary = dict()
    node_list = dict()
    file_header = ''
    if setting == 'compress' and output_filename[-3:] == 'bin':
        freq_counter = Counter(file_data.strip())
        huffman_tree = build_tree()
        build_dict(huffman_tree,'')
        output_data = build_header(huffman_tree,'') + translate_file_c()
        build_file()
    elif setting == 'decompress':
        bits = ''
        for byte_r in file_data[:-1]:     # ignore warning: possible & useful duck-typing cat-
            bits += format(byte_r, 'b').zfill(8)
        last_byte = ord(file_data[-1:]) - 64
        b_tuple = rebuild_tree(bits)
        huffman_tree = b_tuple[0]
        data_start = b_tuple[1]
        build_dict(huffman_tree,'')
        for index in conversion_dictionary:
            inverted_dictionary[str(conversion_dictionary[index])] = index
        output_data = translate_file_d(bits)
        rebuild_file()
    else:
        print('Error: Invalid Parameters')

