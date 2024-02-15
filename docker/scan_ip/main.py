import re
import socket
import ipaddress
import requests
import json


def is_domain_format(input_str):
    pattern = r'^(?=.{1,253}$)(([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,})$'
    if re.match(pattern, input_str):
        return True
    return False


def get_ip(input_str):
    if is_domain_format(input_str):
        try:
            return socket.gethostbyname(input_str)
        except socket.gaierror:
            return "Error: Unable to resolve domain to IP."
    else:
        try:
            ipaddress.ip_address(input_str)
            return input_str
        except ValueError:
            return "Error: Input is not a valid IP or domain format."


def read_get(temp_url):
    # 0. init setting
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.159 '
                      'Safari/537.36',
        'Accept-Language': 'zh-TW,zh;'
                           'q=0.9,en-US;'
                           'q=0.8,en;'
                           'q=0.7',
        'x-apikey': '4f71832da78c55abba8eb06b0c3316e6844a6702beac312a849872d8f676b673'
    }
    # 1. get
    try:
        temp_request = requests.get(temp_url, headers=headers)
        return {'code': temp_request.status_code, 'text': temp_request.text}
    except Exception as ex:
        print('Exception:' + str(ex))
        return {'code': 0, 'text': ''}


def scan(input_ip):
    print("Input: " + input_ip)
    temp_count = 0
    total_count = 0
    temp_result = read_get(f"https://www.virustotal.com/api/v3/ip_addresses/{input_ip}")
    temp_dict = json.loads(temp_result['text'])
    last_analysis_results = temp_dict['data']['attributes']['last_analysis_results']
    for temp_date in last_analysis_results.items():
        if temp_date[1]['result'] != 'clean' and temp_date[1]['result'] != 'unrated':
            print("Alert: " + temp_date[1]['engine_name'])
            temp_count += 1
        total_count += 1
    print("Alert Number: " + str(temp_count) + '/' + str(total_count))
    if temp_count > 1:
        return False
    else:
        return True


if __name__ == '__main__':
    if scan('45.141.148.224 '):
        print("Scan Result: Pass")
    else:
        print("Scan Result: Fail")
