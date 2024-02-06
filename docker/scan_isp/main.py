import socket
import re
import requests
import json
import ipaddress
import random
from bs4 import BeautifulSoup

list_org_white = [
    "Comcast Cable Communications, LLC",
    "AT&T Services, Inc.",
    "Verizon Communications Inc.",
    "China Telecom",
    "British Telecommunications PLC",
    "Google LLC",
    "Amazon Technologies Inc.",
    "Microsoft Corporation",
    "Cloudflare, Inc.",
    "Akamai Technologies, Inc.",
    "Apple Inc.",
    "Facebook, Inc.",
    "Deutsche Telekom AG",
    "NTT Communications Corporation",
    "Orange S.A.",
    "T-Mobile USA, Inc.",
    "Vodafone Group PLC",
    "SoftBank Corp.",
    "Level 3 Communications, Inc.",
    "Time Warner Cable Inc."
]

list_org_black = []


def is_domain_format(input_str):
    # 正則表達式匹配域名格式
    pattern = r'^(?=.{1,253}$)(([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,})$'
    if re.match(pattern, input_str):
        return True
    return False


def get_ip(input_str):
    if is_domain_format(input_str):
        # 輸入符合域名格式，嘗試解析域名
        try:
            return socket.gethostbyname(input_str)
        except socket.gaierror:
            return "Error: Unable to resolve domain to IP."
    else:
        # 檢查輸入是否為有效的IP地址
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
    }
    # 1. get
    try:
        temp_request = requests.get(temp_url, headers=headers)
        return {'code': temp_request.status_code, 'text': temp_request.text}
    except Exception as ex:
        print('Exception:' + str(ex))
        return {'code': 0, 'text': ''}


def read_post(temp_url, input_data):
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
        'Content-Type': 'application/json'
    }
    # 1. get
    try:
        temp_request = requests.post(temp_url, headers=headers, json=input_data)
        return {'code': temp_request.status_code, 'text': temp_request.text}
    except Exception as ex:
        print('Exception:' + str(ex))
        return {'code': 0, 'text': ''}


def read_org(input_ip):
    # 0. init
    temp_org = ""
    # 1. read ip info
    try:
        temp_url = f"https://ipinfo.io/{input_ip}?token=6251879f905493"
        temp_result = read_get(temp_url)
        temp_dict = json.loads(temp_result['text'])
        if 'org' in temp_dict.keys():
            temp_org = temp_dict['org']
    except Exception as ex:
        print("Exception: " + str(ex))
    return temp_org


def check_reserved(ip):
    try:
        private_reserved = [
            ("10.0.0.0", "10.255.255.255"),
            ("172.16.0.0", "172.31.255.255"),
            ("192.168.0.0", "192.168.255.255")
        ]
        system_reserved = [
            ("127.0.0.0", "127.255.255.255"),
            ("169.254.0.0", "169.254.255.255"),
            ("224.0.0.0", "239.255.255.255"),
            ("240.0.0.0", "255.255.255.254")
        ]
        ip_int = int.from_bytes(map(int, ip.split('.')), 'big')
        for start, end in private_reserved + system_reserved:
            start_int = int.from_bytes(map(int, start.split('.')), 'big')
            end_int = int.from_bytes(map(int, end.split('.')), 'big')
            if start_int <= ip_int <= end_int:
                return True
    except Exception as ex:
        print(ex)

    return False


def generate_random_ip():
    # 產生四個0到255之間的隨機整數
    ip_parts = [str(random.randint(0, 255)) for _ in range(4)]
    # 將整數部分用點分隔並合併成IP地址字串
    ip_address = '.'.join(ip_parts)
    return ip_address


def calculate_stats(numbers):
    # 計算排名在第33%和第66%位置的分數
    n = len(numbers)
    index33 = int(n * 0.33)
    index66 = int(n * 0.66)

    rank_33 = numbers[index33]
    rank_66 = numbers[index66]

    return numbers, rank_33, rank_66


def scan(input_data):
    # 0. init
    temp_status = True
    # 1. read data
    temp_ip = get_ip(input_data)
    if check_reserved(temp_ip):
        return 0
    temp_org = read_org(temp_ip)
    temp_list = temp_org.split(" ")
    temp_as_number = ""
    temp_as_name = ""
    temp_status = True
    for temp_data in temp_list:
        if temp_status:
            temp_as_number = temp_data
            temp_status = False
        else:
            temp_as_name = temp_as_name + temp_data
    temp_as_number = temp_as_number[2:]
    # print("ip: " + temp_ip)
    # print("ASN_Number:" + temp_as_number)
    # print("ASN_Name:" + temp_as_name)
    temp_dict = {"asn": temp_as_number, "period": 5}
    temp_response = read_post("https://bgpranking-ng.circl.lu/json/asn_history", temp_dict)
    temp_dict_2 = json.loads(temp_response['text'])
    asn_history = temp_dict_2["response"]["asn_history"]

    latest_score = None

    check_today = True

    for entry in reversed(asn_history):
        if check_today:
            check_today = False
            continue
        date, score = entry
        if score != 0:
            latest_score = int(score * 10000000)
            break

    if latest_score is None:
        # print("All scores are 0.")
        latest_score = 0

    # print("ASN_Rank:" + str(latest_score))
    # print("----------------------------------------------")
    return latest_score


def scan_2(input_data):
    temp_ip = get_ip(input_data)
    temp_org = read_org(temp_ip)
    temp_list = temp_org.split(" ")
    temp_as_number = ""
    temp_as_name = ""
    temp_status = True
    for temp_data in temp_list:
        if temp_status:
            temp_as_number = temp_data
            temp_status = False
        else:
            temp_as_name = temp_as_name + temp_data
    temp_as_number = temp_as_number[2:]
    temp_response = read_get(f"https://asrank.caida.org/asns?asn={temp_as_number}")
    soup = BeautifulSoup(temp_response['text'], 'html.parser')
    as_rank_row = soup.find('th', string='AS rank').find_parent('tr')
    as_rank = as_rank_row.find_all('td')[0].text
    return int(as_rank)


def analyze():
    temp_list_score = []
    for i in range(0, 100000):
        while True:
            temp_ip = generate_random_ip()
            temp_score = scan(temp_ip)
            if temp_score != 0:
                temp_list_score.append(temp_score)
                print(str(i) + ". " + str(temp_ip) + " : " + str(temp_score))
                break
    temp_list_score = sorted(temp_list_score)
    all_scores, rank_33, rank_66 = calculate_stats(temp_list_score)
    print("所有分數:" + str(temp_list_score))
    print("排名在第 33% 的分數:" + str(rank_33))
    print("排名在第 66% 的分數:" + str(rank_66))


def get_status_security(input_ip):
    print("ip: " + str(input_ip))
    temp_score = scan(input_ip)
    print("asn_score: " + str(temp_score))
    temp_rank = scan_2(input_ip)
    print("asn_rank: " + str(temp_rank))
    if temp_score < 126 or temp_rank > 7000:
        print("asn_scan: Fail")
        return False
    else:
        print("asn_scan: Pass")
        return True


# testcase
if __name__ == '__main__':
    unit_test_ip = "8.8.8.8"
    # scan(unit_test_ip)
    analyze()
    # scan_2(unit_test_ip)
    # get_status_security(unit_test_ip)
    '''
    if get_status_security(unit_test_ip):
        print("Pass")
    else:
        print("Fail")
    '''
