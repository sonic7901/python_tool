import src.utils.custom_shell


def run(temp_input, temp_filename):
    temp_result_list = src.utils.custom_shell.run_shell(temp_input)
    with open(temp_filename, "a") as temp_file:
        for temp_result in temp_result_list:
            temp_file.write(temp_result + '\n')
    return

