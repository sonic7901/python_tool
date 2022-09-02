import os
import pathlib


def replace_string(input_file, old_str, new_str):
    with open(input_file) as old_file:
        with open(input_file + '.tmp', 'w') as new_file:
            lines = old_file.readlines()
            for line in lines:
                if old_str in line:
                    line = line.replace(old_str, new_str)
                new_file.write(line)
    os.remove(input_file)
    os.rename(input_file + '.tmp', input_file)


def add_lines(input_file, input_string_list, next_line):
    with open(input_file) as old_file:
        with open(input_file + '.tmp', 'w') as new_file:
            lines = old_file.readlines()
            if next_line == '':
                for line in lines:
                    new_file.write(line)
                for input_string in input_string_list:
                    new_file.write(input_string)
            else:
                for line in lines:
                    if next_line in line:
                        for input_string in input_string_list:
                            new_file.write(input_string)
                    new_file.write(line)
    os.remove(input_file)
    os.rename(input_file + '.tmp', input_file)


def read_name(input_str):
    return pathlib.Path(input_str).resolve().stem


def read_extension(input_str):
    temp_extension = ''
    temp_result = os.path.splitext(input_str)
    for temp_data in temp_result:
        if '.' == temp_data[0]:
            temp_extension = temp_data[1:]
    return temp_extension


if __name__ == "__main__":
    with open('test.txt', 'w') as test_file:
        test_file.write('123\n')
        test_file.write('456\n')
        test_file.write('789\n')
    replace_string('test.txt', '456', '000')
    add_lines('test.txt', ['111\n'], '000')
    print(read_name('/a/b/test.txt'))
    print(read_extension('test.txt'))

