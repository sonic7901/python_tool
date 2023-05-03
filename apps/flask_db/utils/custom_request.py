import requests
import json
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


def read_get_json(temp_url):
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
        return {'code': temp_request.status_code, 'json': temp_request.json()}
    except Exception as ex:
        print('Exception:' + str(ex))
        return {'code': 0, 'json': ''}


def read_put(input_url, input_data):
    # 0. init setting
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.159 '
                      'Safari/537.36',
        'Content-Type': 'application/json'
    }
    json_payload = json.dumps(input_data)
    # 1. put
    try:
        temp_request = requests.put(input_url, headers=headers, data=json_payload)
        return {'code': temp_request.status_code}
    except Exception as ex:
        print('Exception:' + str(ex))
        return {'code': 0, 'json': ''}


def read_gpt(temp_question):
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
        'Authorization': 'Bearer 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',
        'Content-Type': 'application/json'

    }
    # 要傳送的參數
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": temp_question
            }
        ],
        "temperature": 0.01
    }
    # 將參數轉換為 JSON 格式
    json_payload = json.dumps(payload)
    # 1. post
    try:
        temp_request = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json_payload)
        temp_dict = temp_request.json()
        return {'code': temp_request.status_code, 'content': temp_dict['choices'][0]['message']['content']}
    except Exception as ex:
        print('Exception:' + str(ex))
        return {'code': 0, 'json': ''}


def read_alert():
    # 0. init setting
    result_list = []
    basic_url = "https://www.zaproxy.org/docs/alerts/"
    list_alert_id = []

    # 1. first search for count number
    try:
        # alert: 0 ~ 100
        for i in range(0, 45):
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

                    temp_result_risk = first_soup.find_all('td')
                    temp_risk = temp_result_risk[7].text
                    print("risk: " + temp_risk)
                    list_tags = []
                    temp_tags = temp_result_risk[15].text
                    if '\n' in temp_tags:
                        list_split = temp_tags.split('\n')
                        for temp_split in list_split:
                            if not temp_split == '':
                                list_tags.append(temp_split)
                    result_list.append([temp_title, temp_desc, temp_solution, temp_risk, list_tags])
            except Exception as ex:
                print('Exception:' + str(ex))
        # alert: 10000 ~ 10300
        for i in range(10000, 10205):
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

                    temp_result_risk = first_soup.find_all('td')
                    temp_risk = temp_result_risk[7].text
                    print("risk: " + temp_risk)
                    list_tags = []
                    temp_tags = temp_result_risk[15].text
                    if '\n' in temp_tags:
                        list_split = temp_tags.split('\n')
                        for temp_split in list_split:
                            if not temp_split == '':
                                list_tags.append(temp_split)
                    result_list.append([temp_title, temp_desc, temp_solution, temp_risk, list_tags])
            except Exception as ex:
                print('Exception:' + str(ex))
        # alert: 20000 ~ 20100
        for i in range(20000, 20020):
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

                    temp_result_risk = first_soup.find_all('td')
                    temp_risk = temp_result_risk[7].text
                    print("risk: " + temp_risk)
                    list_tags = []
                    temp_tags = temp_result_risk[15].text
                    if '\n' in temp_tags:
                        list_split = temp_tags.split('\n')
                        for temp_split in list_split:
                            if not temp_split == '':
                                list_tags.append(temp_split)
                    result_list.append([temp_title, temp_desc, temp_solution, temp_risk, list_tags])
            except Exception as ex:
                print('Exception:' + str(ex))

    except Exception as ex:
        print('Exception:' + str(ex))
    finally:
        return result_list


if __name__ == "__main__":
    # read_alert()
    main_data = read_gpt("如果網站上發現\"未設定 SPF\"會有哪些資安問題, 從這些資安問題來評估的CVSSv3.1分數可能落在哪個數字範圍?")
    print(main_data['content'])
    main_data_2 = read_gpt("這段文字中的CVSS分數煩為的中間數為多少? 只回答我中間數的數字\"" + main_data['content'] + "\"")
    print(main_data_2['content'])
