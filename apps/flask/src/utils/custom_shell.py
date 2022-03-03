import subprocess
import locale

# setting
console_length = 200


def run_shell(input_str):
    try:
        result_list = []
        result = subprocess.check_output(input_str, shell=True)
        result_string = result.decode(locale.getdefaultlocale()[1])
        result_spilt = result_string.split('\r\n')
        for temp_str in result_spilt:
            tempt_len = len(temp_str)
            if len(temp_str) > console_length:
                for i in range(0, int(tempt_len / console_length) + 1):
                    temp_spilt_str = temp_str[i * console_length:(i + 1) * console_length]
                    result_list.append(temp_spilt_str)
                    print(temp_spilt_str)
            else:
                result_list.append(temp_str)
                print(temp_str)

        return result_list
    except Exception as ex:
        print('Exception:' + str(ex))
        return []
