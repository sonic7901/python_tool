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
    "Time Warner Cable Inc.",
    "Twitter Inc.",
    "Oath Holdings Inc.",
    "Akamai International B.V.",
    "PayPal, Inc.",
    "JPMorgan Chase & Co.",
    "U.S. BANCORP",
    "LINE Corporation",
    "General Motors LLC",
    "SQUIXA PTY LIMITED",
    "Telegram Messenger Inc",
    "Ford Motor Company"

]

list_org_black = []


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
        # temp_url = f"https://ipinfo.io/{input_ip}?token=6251879f905493"
        temp_url = f"https://ipinfo.io/{input_ip}?token=1af7be88ea4884"
        temp_result = read_get(temp_url)
        temp_dict = json.loads(temp_result['text'])
        if 'org' in temp_dict.keys():
            temp_org = temp_dict['org']
    except Exception as ex:
        print("Exception: " + str(ex))
    return temp_org


def read_asn(input_data):
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
            temp_as_name = temp_as_name + " " + temp_data
    temp_as_number = temp_as_number[2:]
    temp_as_name = temp_as_name[1:]
    return {"number": temp_as_number, "name": temp_as_name}


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


def scan_score(input_data):
    # 0. init
    temp_status = True
    # 1. read data
    temp_asn = read_asn(input_data)
    temp_asn_number = temp_asn['number']
    temp_asn_name = temp_asn['name']
    print("Input: " + input_data)
    print("ASN_Number: " + temp_asn_number)
    print("ASN_Name: " + temp_asn_name)
    if temp_asn_name in list_org_white:
        print("ASN_Score: 1000")
        return 1000
    temp_dict = {"asn": temp_asn_number, "period": 5}
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

    print("ASN_Score: " + str(latest_score))
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
    print("ASN_Rank: " + str(as_rank))
    return int(as_rank)


def analyze():
    temp_list_score = []
    for i in range(0, 100000):
        while True:
            temp_ip = generate_random_ip()
            temp_score = scan_score(temp_ip)
            if temp_score != 0:
                temp_list_score.append(temp_score)
                print(str(i) + ". " + str(temp_ip) + " : " + str(temp_score))
                break
    temp_list_score = sorted(temp_list_score)
    all_scores, rank_33, rank_66 = calculate_stats(temp_list_score)
    print("所有分數:" + str(temp_list_score))
    print("排名在第 33% 的分數:" + str(rank_33))
    print("排名在第 66% 的分數:" + str(rank_66))


def scan(input_ip):
    temp_score = scan_score(input_ip)
    temp_rank = scan_2(input_ip)
    if 0 < temp_score < 126:
        return False
    else:
        return True


def test():
    domains = [
        "google.com",
        "facebook.com",
        "youtube.com",
        "amazon.com",
        "twitter.com",
        "instagram.com",
        "linkedin.com",
        "wikipedia.org",
        "reddit.com",
        "netflix.com",
        "yahoo.com",
        "ebay.com",
        "bing.com",
        "microsoft.com",
        "apple.com",
        "pinterest.com",
        "paypal.com",
        "craigslist.org",
        "imdb.com",
        "cnn.com",
        "nytimes.com",
        "twitch.tv",
        "instagram.com",
        "dropbox.com",
        "spotify.com",
        "adobe.com",
        "github.com",
        "walmart.com",
        "target.com",
        "homedepot.com",
        "quora.com",
        "yelp.com",
        "tripadvisor.com",
        "zillow.com",
        "etsy.com",
        "chase.com",
        "bankofamerica.com",
        "wellsfargo.com",
        "usbank.com",
        "americanexpress.com",
        "booking.com",
        "expedia.com",
        "airbnb.com",
        "kayak.com",
        "pandora.com",
        "soundcloud.com",
        "vimeo.com",
        "dailymotion.com",
        "hulu.com",
        "medium.com",
        "linkedin.com",
        "tumblr.com",
        "flickr.com",
        "snapchat.com",
        "whatsapp.com",
        "wechat.com",
        "line.me",
        "telegram.org",
        "slack.com",
        "mail.ru",
        "yahoo.co.jp",
        "live.com",
        "office.com",
        "msn.com",
        "wordpress.org",
        "blogger.com",
        "medium.com",
        "weebly.com",
        "wix.com",
        "jimdo.com",
        "squarespace.com",
        "godaddy.com",
        "bluehost.com",
        "hostgator.com",
        "namecheap.com",
        "siteground.com",
        "aol.com",
        "weather.com",
        "mapquest.com",
        "britannica.com",
        "nationalgeographic.com",
        "smithsonianmag.com",
        "nature.com",
        "science.org",
        "cell.com",
        "sciencedirect.com",
        "nasa.gov",
        "space.com",
        "tesla.com",
        "ford.com",
        "chevrolet.com",
        "toyota.com",
        "honda.com"
    ]
    for temp_domain in domains:
        scan(temp_domain)


# testcase
if __name__ == '__main__':
    if scan('45.141.148.224'):
        print("Scan Result: Pass")
    else:
        print("Scan Result: Fail")
    # unit_test_ip = "facebook.com"
    # scan_score(unit_test_ip)
    # analyze()
    # scan_2(unit_test_ip)
    # test()

