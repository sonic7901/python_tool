
import socket
import requests
import json

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


def read_ip(input_domain):
    try:
        ip_address = socket.gethostbyname(input_domain)
        return ip_address
    except socket.gaierror as e:
        return f"Error converting domain to IP: {e}"


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
        temp_json = {"asn": input_data, "date": "2024-02-01"}
        temp_request = requests.post(temp_url, headers=headers, json=temp_json)
        return {'code': temp_request.status_code, 'text': temp_request.text}
    except Exception as ex:
        print('Exception:' + str(ex))
        return {'code': 0, 'text': ''}


def read_org(input_ip):
    temp_url = f"https://ipinfo.io/{input_ip}?token=6251879f905493"
    temp_result = read_get(temp_url)
    # print(temp_result['text'])
    temp_dict = json.loads(temp_result['text'])
    # print(temp_dict)
    temp_org = ""
    if 'org' in temp_dict.keys():
        temp_org = temp_dict['org']
    return temp_org


def is_private_or_reserved(ip):
    try:
        # 私有IP范围
        private_ranges = [
            ("10.0.0.0", "10.255.255.255"),
            ("172.16.0.0", "172.31.255.255"),
            ("192.168.0.0", "192.168.255.255")
        ]

        # 保留IP范围
        reserved_ranges = [
            ("127.0.0.0", "127.255.255.255"),
            ("169.254.0.0", "169.254.255.255"),
            ("224.0.0.0", "239.255.255.255"),
            ("240.0.0.0", "255.255.255.254")
        ]

        ip_int = int.from_bytes(map(int, ip.split('.')), 'big')

        for start, end in private_ranges + reserved_ranges:
            start_int = int.from_bytes(map(int, start.split('.')), 'big')
            end_int = int.from_bytes(map(int, end.split('.')), 'big')
            if start_int <= ip_int <= end_int:
                return True
    except Exception as ex:
        print(ex)

    return False


def test():
    # 示例范围，这里我们仅仅检查一个非常小的范围
    for i in range(1, 256):
        ip = f"219.253.192.{i}"
        if not is_private_or_reserved(ip):
            print(ip + ':' + read_org(ip))


def read_check_ip(input_ip):
    if not is_private_or_reserved(input_ip):
        print(input_ip + ':' + read_org(input_ip))


def read_list_asn():
    print(read_post("https://bgpranking-ng.circl.lu/json/asn", "18302"))


def test_whois():
    from ipwhois import IPWhois

    def query_isp(ip_address):
        obj = IPWhois(ip_address)
        results = obj.lookup_rdap(depth=1)

        # 獲取ISP信息
        isp = results.get('network', {}).get('name')
        if isp:
            print(f"ISP for {ip_address}: {isp}")
        else:
            print(f"ISP information for {ip_address} not found.")

    # 例子：查詢IP地址8.8.8.8的ISP
    query_isp('8.8.8.8')


def query_isp(ip_address):
    response = requests.get(f'http://ip-api.com/json/{ip_address}')
    data = response.json()

    # 检查请求是否成功
    if data['status'] == 'success':
        isp = data.get('isp')
        print(f"ISP for {ip_address}: {isp}")
    else:
        print(f"Error: {data.get('message', 'Unknown error')}")


# testcase
if __name__ == '__main__':
    # read_org("47.241.205.129")
    # test()
    # read_list_asn()
    query_isp("8.8.8.8")
