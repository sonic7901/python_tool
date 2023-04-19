import custom_request
import custom_gpt


def test():
    temp_list = custom_request.read_get_json("https://internal-api.dev.cymetrics.io/security/issue")
    key_list = []
    for temp_dict in temp_list['json']:
        key_list.append(temp_dict['key'])
        print(temp_dict['name'])
        print("CVSSv3: " + custom_gpt.read_cvss(temp_dict['name']))
        print("OWASP Top 10(2021): " + custom_gpt.read_owasp(temp_dict['name']))


if __name__ == '__main__':
    test()
