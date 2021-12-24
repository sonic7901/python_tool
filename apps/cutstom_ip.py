import utils.custom_chrome


def get_domain(input_ip):
    print('get_domain start')
    # 0. init
    result = ""
    temp_url_80 = "http://" + input_ip
    temp_url_8080 = "http://" + input_ip + ":8080"
    temp_url_443 = "https://" + input_ip
    temp_url_8443 = "https://" + input_ip + ":8443"
    print(utils.custom_chrome.read_get_page(temp_url_443))
    print('get_domain end')
    return result


if __name__ == '__main__':
    get_domain("117.56.220.20")