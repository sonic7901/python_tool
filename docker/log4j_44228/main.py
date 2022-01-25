import custom_log4j
import sys


def main_log4j(input_url):
    try:
        temp_result = custom_log4j.docker_scan(input_url)
        if len(temp_result) > 0:
            custom_log4j.write_report(temp_result)
        return True
    except Exception as ex:
        print(ex)
        return False


if __name__ == '__main__':
    temp_url = sys.argv[1]
    if not main_log4j(temp_url):
        sys.exit(2)
