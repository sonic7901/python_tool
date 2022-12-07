import requests
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


def read_linkedin_bing():
    # 0. init setting
    result_list = []
    basic_url = "https://www.zaproxy.org/docs/alerts/"
    # 1. first search for count number
    try:
        # alert: 0 ~ 100
        for i in range(0, 100):
            try:
                first_query = basic_url + str(i) + "/"
                first_response = read_get(first_query)
                if first_response['code'] == 200:
                    print('alert id: ' + str(i))
                    first_soup = BeautifulSoup(first_response['text'], 'html.parser')
                    temp_result_title = first_soup.find(class_='text--white')
                    temp_title = temp_result_title.text

                    temp_result_desc = first_soup.find('p')
                    print("summary: " + temp_result_desc.text)
                    temp_desc = temp_result_desc.text

                    temp_result_solution = first_soup.find(class_='mb-20')
                    temp_solution = temp_result_solution.contents[2]
                    temp_solution = temp_solution.strip()
                    print("solution: " + temp_solution)
                    result_list.append([temp_title, temp_desc, temp_solution])
            except Exception as ex:
                print('Exception:' + str(ex))
        # alert: 10000 ~ 10300
        for i in range(10000, 10300):
            try:
                first_query = basic_url + str(i) + "/"
                first_response = read_get(first_query)
                if first_response['code'] == 200:
                    print('alert id: ' + str(i))
                    first_soup = BeautifulSoup(first_response['text'], 'html.parser')
                    temp_result_title = first_soup.find(class_='text--white')
                    temp_title = temp_result_title.text

                    temp_result_desc = first_soup.find('p')
                    print("summary: " + temp_result_desc.text)
                    temp_desc = temp_result_desc.text

                    temp_result_solution = first_soup.find(class_='mb-20')
                    temp_solution = temp_result_solution.contents[2]
                    temp_solution = temp_solution.strip()
                    print("solution: " + temp_solution)
                    result_list.append([temp_title, temp_desc, temp_solution])
            except Exception as ex:
                print('Exception:' + str(ex))
        # alert: 20000 ~ 20100
        for i in range(20000, 20100):
            try:
                first_query = basic_url + str(i) + "/"
                first_response = read_get(first_query)
                if first_response['code'] == 200:
                    print('alert id: ' + str(i))
                    first_soup = BeautifulSoup(first_response['text'], 'html.parser')
                    temp_result_title = first_soup.find(class_='text--white')
                    temp_title = temp_result_title.text

                    temp_result_desc = first_soup.find('p')
                    print("summary: " + temp_result_desc.text)
                    temp_desc = temp_result_desc.text

                    temp_result_solution = first_soup.find(class_='mb-20')
                    temp_solution = temp_result_solution.contents[2]
                    temp_solution = temp_solution.strip()
                    print("solution: " + temp_solution)
                    result_list.append([temp_title, temp_desc, temp_solution])
            except Exception as ex:
                print('Exception:' + str(ex))

    except Exception as ex:
        print('Exception:' + str(ex))
    finally:
        return result_list


if __name__ == "__main__":
    read_linkedin_bing()
