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


def read_sb_count(temp_str):
    # 0. init setting
    result_str = ""
    result_int = 0

    # 1. read value from html element(sb_count)
    try:
        temp_list = temp_str.split(' ')
        temp_num_str = temp_list[-2]
        for s in temp_num_str:
            try:
                int(s)
                result_str = result_str + s
            except ValueError:
                pass
        try:
            result_int = int(result_str)
        except Exception as ex:
            print('Exception:' + str(ex))
        return result_int
    except Exception as ex:
        print('Exception:' + str(ex))
        return result_int


def read_linkedin_bing(temp_company):
    # 0. init setting
    search_status = True
    temp_record_str = ""
    search_count = 1
    repeat_count = 0
    result_count = 0
    repeat_limit = 20
    result_list = []
    basic_url = "https://www.bing.com/search?q="

    # 1. first search for count number
    try:
        first_query = "site%3Alinkedin.com+%26+intitle%3A" + temp_company
        first_response = read_get(basic_url + first_query)
        if first_response['code'] == 200:
            first_soup = BeautifulSoup(first_response['text'], 'html.parser')
            sb_count = first_soup.find(class_='sb_count')
            total_count = read_sb_count(sb_count.text)
        else:
            return result_list
    except Exception as ex:
        print('Exception:' + str(ex))
        return result_list

    # 2. parser all user form linkedin
    while search_status:
        try:
            test_query = "site%3Alinkedin.com+%26+intitle%3A" + temp_company + "&first=" + str(search_count)
            temp_response = read_get(basic_url + test_query)
            if temp_response['code'] == 200:
                temp_soup = BeautifulSoup(temp_response['text'], 'html.parser')
                new_record = temp_soup.find('h2')
                new_record_str = new_record.text
                if temp_record_str == new_record_str:
                    repeat_count += 1
                    # print('repeating times:', str(repeat_count))
                if total_count < search_count or repeat_count > repeat_limit:
                    search_status = False
                else:
                    temp_record_str = new_record_str
                    list_a = temp_soup.find_all('h2')
                    for temp_a in list_a:
                        temp_str = temp_a.text
                        temp_list = temp_str.split(' - ')
                        if len(temp_list) > 2:
                            if temp_company in temp_list[2]:
                                temp_name = temp_list[0] + '(' + temp_list[1] + ')'
                                if temp_name not in result_list:
                                    result_list.append(temp_name)
                                    result_count += 1
                                    repeat_count = 0
                                    print(str(result_count) + ':' + temp_name)
                    search_count += 10
            else:
                print(str(temp_response['code']))
        except Exception as ex:
            print('Exception:' + str(ex))
    return result_list


# testcase
if __name__ == '__main__':
    main_result = read_get("https://www.example.com")
    if main_result['code'] == 200:
        print("unit test (custom_request) : pass")
        sys.exit(0)
    else:
        print("unit test (custom_request) : fail")
        sys.exit(1)