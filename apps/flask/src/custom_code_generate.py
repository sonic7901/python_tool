import os


def run(old_path, new_path):
    if os.path.isfile(old_path):
        print('exist')
        with open(old_path, 'r') as old_file:
            with open(new_path, 'w') as new_file:
                old_lines = old_file.readlines()
                for temp_line in old_lines:
                    new_file.write(temp_line)
                    print(temp_line)
    else:
        print(old_path + ' not found')


if __name__ == "__main__":
    run('./upload/test_sql11.py', './upload/custom_new.py')
