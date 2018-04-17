import sys
from collections import Counter


class BinaryTree:
    def __init__(self):
        self.left = None
        self.right = None
        self.char = ''
        self.freq = 0
        self.parent = None


def print_tree(node, i):
    print(i, 'Freq: ', node.freq)
    print(i, 'Char: ', node.char, '\n')
    if node.right: print_tree(node.right, i + ' ')
    if node.left: print_tree(node.left, i + ' ')


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


def rebuild_tree(bit_string):
    i = 0; j = 0; d_start = 0; new_char = ''; root_node = BinaryTree()
    node = root_node
    for bit in bit_string:
        j += 1
        if i > 0:
            new_char += bit
            i -= 1
            if i == 0:
                #print('j is ', j)
                #print('char is ',new_char)
                node.char = chr(int(new_char,2))
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


def parse_binary():
    data = file.read()
    bit_string = ''
    for byte in data[:-1]:
        bit_string += format(byte,'b').zfill(8)
    last_byte = ord(data[-1:])
    b_tuple = rebuild_tree(bit_string[1:])
    dict_tree = b_tuple[0]
    data_start = b_tuple[1]
    make_dict(dict_tree,'')
    return last_byte, bit_string, data_start


def get_child_node():
    node = BinaryTree()
    item = freq_list.most_common(len(freq_list))[-1]
    if item[0] in node_dict:
        node = node_dict[item[0]]
        del node_dict[item[0]]
    else:
        node.char = item[0]
        node.freq = item[1]
    del freq_list[item[0]]
    return node


def make_node(i):
    node = BinaryTree()
    node.left = get_child_node()
    node.right = get_child_node()
    node.char = 'node' + str(i)
    node.freq = node.right.freq + node.left.freq
    freq_list[node.char] = node.freq
    node_dict[node.char] = node


def header_helper(node, string_header):
    if node.char[0:4] != "node":
        string_header += '1'
        char_code = bin(int.from_bytes(node.char.encode(), 'big'))
        string_header += '0' + char_code[2:]
        return string_header
    else:
        string_header += '0'
        string_header = header_helper(node.left, string_header)
        string_header = header_helper(node.right, string_header)
        return string_header


def make_dict(node, code):
    if node.right:
        make_dict(node.right, code + '1')
    if node.left:
        make_dict(node.left, code + '0')
    if not node.left and not node.right:
        conv_dict[node.char] = code


def make_bin(new_filename, data, byte_array):
    bit_array = ''; byte = ''; i = 0
    with open(new_filename,'wb') as bin_file:
        string_header = ''
        bit_array += header_helper(node_dict['node' + str(node_id - 1)], string_header)
        for file_char in data:
            bit_array += conv_dict[file_char]
        for bit in bit_array:
            if i == 7:
                byte += bit
                byte_array.append(int(byte, base=2))
                i = 0; byte = ''
            else:
                byte += bit
                i += 1
        if i > 0:
            last_byte = i
            while i < 8:
                i += 1
                byte += '0'
            byte_array.append(int(byte, base=2))
            byte_array.append(last_byte)
        bin_file.write(bytes(byte_array))


def make_decompressed(output_filename, output_data):
    if output_filename[:-3] != 'txt':
        with open(output_filename,'wb') as output_file:
            bin_output_data = str.encode(output_data)
            output_file.write(bin_output_data)
    else:
        with open(output_filename,'w') as output_file:
            output_file.write(output_data)


#filename = str(sys.argv[1])
#output_name = str(sys.argv[2])
filename = 'output.bin'
output_name = 'decompressed.txt'
if filename[-3:] != 'bin':
    with open(filename, 'r') as file:
        file_data = file.read()
        freq_list = Counter(file_data.strip())
        node_dict = dict()
        conv_dict = dict()
        node_id = 0
        while len(freq_list) > 1:
            make_node(node_id)
            node_id += 1
        make_dict(node_dict['node'+str(node_id-1)],'')
        make_bin(output_name, file_data, [])
elif filename[-3:] == 'bin':
    with open(filename, 'rb') as file:
        conv_dict = dict(); inv_dict = dict(); output_data = ''; code = ''
        a_tuple = parse_binary()
        last_byte = a_tuple[0]
        bit_string = a_tuple[1]
        data_start = a_tuple[2]
        for char in conv_dict:
            inv_dict[str(conv_dict[char])] = char
        for bit in bit_string[39:-(8-last_byte)]:
            code += bit
            if code in inv_dict:
                output_data += inv_dict[code]
                code = ''
        make_decompressed(output_name,output_data)
else:
    print('Error: Invalid Filename')
