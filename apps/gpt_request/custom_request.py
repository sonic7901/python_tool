import requests
import json
import openai


def read_issue(input_key):
    try:
        temp_url = "https://internal-api.dev.cymetrics.io/security/issue?key=" + input_key
        response = requests.get(temp_url)
        if response.status_code == 200:
            decoded_content = response.content.decode('utf-8')
            content_dict = json.loads(decoded_content)
            return content_dict
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return {}
    except Exception as ex:
        print(ex)
        return {}


def write_issue(input_data):
    # 0. init setting
    headers = {
        'Content-Type': 'application/json',
    }

    temp_data = {
        "id": input_data["id"],
        "key": "public_remote_ssh",
        "name": "公開的 SSH 服務",
        "nameEn": "Public SSH Service",
        "title": "公開的 SSH 服務",
        "weight": "1",
        "l0Weight": "2.73321683409505",
        "l1Weight": "8.88888888888889",
        "l2Weight": "25",
        "l1Category": "external_service",
        "l2Category": "remote_control",
        "riskLevel": "75",
        "complexityLevel": "25",
        "complianceIdList": [26, 22, 21, 20, 19, 10, 7],
        "weightList": [1, 1, 1, 1, 1, 1, 1],
        "referenceIdList": [],
        "descriptionId": "327",
        "recommendationId": "315"
    }

    response = requests.put("https://internal-api.dev.cymetrics.io/security/issue",
                            data=json.dumps(temp_data),
                            headers=headers)
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Failed to fetch data: {response.status_code}")


def read_ask_gpt4(input_string):
    # 設定 API 金鑰
    openai.api_key = "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"

    # 定義問題
    question = input_string

    # 設定 GPT-3 模型的引擎 ID
    model_engine = "gpt-3.5-turbo"

    # 呼叫 OpenAI API 並取得答案
    response = openai.Completion.create(
        engine=model_engine,
        prompt=question,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.1,
    )

    # 顯示答案
    answer = response.choices[0].text.strip()
    answer_list = answer.split("\n\n")
    return answer_list


def check_issue(input_issue_name):
    try:
        temp_str = f"\"{input_issue_name}\"是否會導致網站不安全?請用是或否回答"
        temp_result = read_ask_gpt4(temp_str)[0]
        if temp_result[0] == "是":
            return True
        else:
            return False
    except Exception as ex:
        print('Exception:' + str(ex))
        return False


def read_cvss(input_issue_name):
    # init
    temp_result = 0
    try:
        temp_str = f"多數情況下,\"{input_issue_name}\"的 CVSSv3 分數最可能是多少? 請回答我數字"
        temp_result = read_ask_gpt4(temp_str)[0]
    except Exception as ex:
        print('Exception:' + str(ex))
    return temp_result


if __name__ == '__main__':
    '''
    main_result = read_get_json("https://internal-api.dev.cymetrics.io/security/issue")
    if main_result['code'] == 200:
        print("unit test (custom_request) : pass")
        sys.exit(0)
    else:
        print("unit test (custom_request) : fail")
        sys.exit(1)
    '''
    # 使用函數
    url = "https://internal-api.dev.cymetrics.io/security/issue?key=public_remote_ssh"
    url_2 = "https://internal-api.dev.cymetrics.io/security/issue"
    read_data = read_issue("public_remote_ssh")
    write_issue(read_data)
