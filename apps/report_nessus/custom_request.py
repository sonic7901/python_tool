import requests
import sys
from bs4 import BeautifulSoup


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


def read_nessus(input_plugin_id):
    pass
    # 0. init setting
    result_name = ''
    result_list = []
    basic_url = "https://zh-tw.tenable.com/plugins/nessus/"

    # 1. first search for count number
    try:
        first_query = basic_url + str(input_plugin_id)
        first_response = read_get(first_query)
        if first_response['code'] == 200:
            first_soup = BeautifulSoup(first_response['text'], 'html.parser')
            # name
            temp_result = first_soup.find(class_='h2')
            result_name = temp_result.text
            result_list.append(result_name)
            # detail
            temp_result_list = first_soup.find_all(class_='mb-3')
            result_detail = temp_result_list[3].text
            result_list.append(result_detail[2:])
            # solution
            result_solution = temp_result_list[4].text
            result_list.append(result_solution[4:])
            # Type
            temp_result_list = first_soup.find_all('a')
            result_type = ''
            for temp_result in temp_result_list:
                try:
                    if 'https://zh-tw.tenable.com/plugins/nessus/families/' in temp_result.attrs['href']:
                        result_type = temp_result.text
                        break
                except Exception as ex:
                    if not str(ex) == '\'href\'':
                        print('Exception:' + str(ex))
            result_list.append(result_type)
            return result_list
        else:
            return result_list
    except Exception as ex:
        print('Exception:' + str(ex))
        return result_list


# testcase
if __name__ == '__main__':
    read_nessus('170113')
