import socket
import urllib.parse
import time
import secrets

import utils.custom_csv
import utils.custom_domain
import utils.custom_request
import utils.custom_log as logging


def run_delay(input_time, input_range):
    try:
        time.sleep(secrets.choice(range(input_time - input_range, input_time + input_range)))
    except Exception as ex:
        logging.error('Exception:' + str(ex))
    return


def read_domain_from_url(temp_domain):
    result_domain = ""
    try:
        if 'http' in temp_domain:
            temp_domain = urllib.parse.urlparse(temp_domain).netloc
        result_domain = socket.gethostbyname(temp_domain)
    except Exception as ex:
        logging.error('Exception:' + str(ex))
    return result_domain


def read_info_json(temp_ip):
    retry_count = 0
    status_code = 0
    result_json = {}
    try:
        while status_code != 200 and retry_count != 5:
            temp_response = utils.custom_request.read_get_json("http://ip-api.com/json/" + temp_ip)
            status_code = temp_response['code']
            result_json = temp_response['json']
            run_delay(3, 1)
            retry_count += 1
    except Exception as ex:
        logging.error('Exception:' + str(ex))

    return result_json


def test_gov():
    temp_dict = utils.custom_csv.read_file_to_dict('TopSites.csv')
    with open('ip_info_result.csv', 'w') as csv_file:
        csv_file.write('url,country,isp,org,asp\n')
    for temp in temp_dict:
        try:
            temp_url = temp['\ufeffWebsiteUrl']
            print(temp_url)
            temp_ip = read_domain_from_url(temp_url)
            print(temp_ip)
            if temp_ip:
                temp_info = read_info_json(temp_ip)
                print('country:' + temp_info['country'])
                print('isp    :' + temp_info['isp'])
                print('org    :' + temp_info['org'])
                print('asp    :' + temp_info['as'])
                with open('ip_info_result.csv', 'a') as csv_file:
                    csv_file.write(temp_url + ','
                                   + temp_info['country'] + ','
                                   + temp_info['isp'] + ','
                                   + temp_info['org'] + ','
                                   + temp_info['as'] + '\n')

            print("==========================")
        except Exception as ex:
            logging.error('Exception:' + str(ex))
    print('end')


def test_single(input_data):
    temp_domain = read_domain_from_url(input_data)
    temp_result = read_info_json(temp_domain)
    print('ip: ' + temp_result['query'])
    print('location: ' + temp_result['country'])
    print('isp: ' + temp_result['isp'])
    print('org: ' + temp_result['org'])
    return


if __name__ == '__main__':
    # test_gov()
    test_single("https://www.onedegree.hk/zh-hk")