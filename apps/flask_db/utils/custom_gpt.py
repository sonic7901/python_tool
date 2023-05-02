import openai


def read_ask(input_string):
    # 設定 API 金鑰
    openai.api_key = "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"

    # 定義問題
    question = input_string

    # 設定 GPT-3 模型的引擎 ID
    model_engine = "text-davinci-002"

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


def read_cvss(input_issue_name):
    # init
    temp_result = 0
    try:
        temp_str = f"如果網站上發現\"{input_issue_name}\"可能會有什麼資安問題, 從這些問題來評估CVSSv3.1的分數可能落在哪個數字範圍?"
        temp_result = read_ask(temp_str)[0]
    except Exception as ex:
        print('Exception:' + str(ex))
    return temp_result


def read_owasp(input_issue_name):
    # init
    temp_result = ""
    temp_str = f"依序列出2017年 OWASP TOP 10的項目名稱與編號, {input_issue_name}問題屬於哪一種,編號是多少?"
    temp_answer = read_ask(temp_str)
    temp_str = temp_answer[-1]
    if "A1" in temp_str:
        temp_result = "A03"
    elif "A2" in temp_str:
        temp_result = "A07"
    elif "A3" in temp_str:
        temp_result = "A02"
    elif "A4" in temp_str:
        temp_result = "A05"
    elif "A5" in temp_str:
        temp_result = "A01"
    elif "A6" in temp_str:
        temp_result = "A05"
    elif "A7" in temp_str:
        temp_result = "A03"
    elif "A8" in temp_str:
        temp_result = "A08"
    elif "A9" in temp_str:
        temp_result = "A06"
    elif "A10" in temp_str:
        temp_result = "A09"
    return temp_result


if __name__ == '__main__':
    test_issue_name = "CSP 未設定"
    print(test_issue_name)
    print("CVSSv3: " + read_cvss(test_issue_name))
    print("OWASP Top 10(2021): " + read_owasp(test_issue_name))
