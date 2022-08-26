import time
import sys
import json
import pprint
import difflib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType


def read_get_page(input_url, input_cookie=None, headless_mode=False):
    # 0. init
    chrome_options = Options()
    # 1. set headless
    chrome_options.add_argument("--incognito")
    if headless_mode:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

    # 2. set user-agent
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) " \
         "AppleWebKit/537.36 (KHTML, like Gecko) " \
         "Chrome/92.0.4515.159 Safari/537.36"
    chrome_options.add_argument('user-agent={}'.format(ua))
    # chrome_options.add_argument('--ignore-ssl-errors=yes')
    # chrome_options.add_argument('--ignore-certificate-errors')
    # 3. open browser
    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=chrome_options)
    # 4. set cookie
    if input_cookie:
        driver.get(input_url)
        driver.add_cookie(input_cookie)
    # 5. send request
    driver.implicitly_wait(10)
    driver.get(input_url)
    # print messages
    for entry in driver.get_log('browser'):
        print(entry)
    temp_result = driver.page_source
    # 6. close browser
    driver.quit()
    return temp_result


"""
test_json_list = [
{'type': 'write', 'xpath': '//*[@id="account"]', 'text': 'account'},
{'type': 'write', 'xpath': '//*[@id="password"]', 'text': 'password'},
{'type': 'click', 'xpath': '/html/body/div/div/div/form/button', 'text': ''}]
x_dict = read_login_header(input_url="https://member.ithome.com.tw/login",input_action_list=test_json_list)
"""


def read_login_auto(input_url, input_username, input_password, headless_mode=False):
    # 0. init
    chrome_options = Options()
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    # 1. set headless
    chrome_options.add_argument("--incognito")
    if headless_mode:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
    # 2. set user-agent
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) " \
         "AppleWebKit/537.36 (KHTML, like Gecko) " \
         "Chrome/92.0.4515.159 Safari/537.36"
    chrome_options.add_argument('user-agent={}'.format(ua))
    # 3. open browser
    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
                              options=chrome_options,
                              desired_capabilities=capabilities)
    # 5. error login
    try:
        driver.implicitly_wait(10)
        driver.get(input_url)
        time.sleep(2)
        input_list = driver.find_elements(By.XPATH, "//input")
        link_list = driver.find_elements(By.XPATH, "//a[@href]")
        status_login = False
        for i_link in range(0, len(link_list)):
            if status_login:
                break
            for i_input in range(1, len(input_list)):
                if status_login:
                    break
                driver.get(input_url)
                driver.refresh()
                time.sleep(3)
                temp_link_list = driver.find_elements(By.XPATH, "//a")
                temp_input_list = driver.find_elements(By.XPATH, "//input")
                print(str(i_link) + "-" + str(i_input))
                try:
                    temp_input_list[i_input - 1].send_keys(input_username)
                    temp_input_list[i_input].send_keys(input_password + "1")
                    temp_link_list[i_link].click()
                    time.sleep(3)
                    error_login_source = driver.page_source
                    driver.get(input_url)
                    driver.refresh()
                    temp_link_list = driver.find_elements(By.XPATH, "//a")
                    temp_input_list = driver.find_elements(By.XPATH, "//input")
                    temp_input_list[i_input - 1].send_keys(input_username)
                    temp_input_list[i_input].send_keys(input_password)
                    temp_link_list[i_link].click()
                    time.sleep(3)
                    valid_login_source = driver.page_source
                    diff = 1 - (difflib.SequenceMatcher(None, error_login_source, valid_login_source).quick_ratio())
                    diff_present = diff * 100
                    print('diff: ' + str(diff_present) + '%')
                    if 0.1 < diff_present:
                        temp_logs = driver.get_log("performance")
                        temp_header = read_extra(input_url, temp_logs)
                        status_login = True
                        print("header:" + str(temp_header))
                        print('login success')
                    else:
                        print('login fail')
                except Exception as ex:
                    pass
        driver.get(input_url)
        time.sleep(1)
        button_list = driver.find_elements(By.XPATH, "//button")
        input_list = driver.find_elements(By.XPATH, "//input")
        for i_button in range(0, len(button_list)):
            if status_login:
                break
            for i_input in range(1, len(input_list)):
                if status_login:
                    break
                driver.get(input_url)
                driver.refresh()
                temp_button_list = driver.find_elements(By.XPATH, "//button")
                temp_input_list = driver.find_elements(By.XPATH, "//input")
                print(str(i_button) + "-" + str(i_input))
                try:
                    temp_input_list[i_input - 1].send_keys(input_username)
                    temp_input_list[i_input].send_keys(input_password + "1")
                    temp_button_list[i_button].click()
                    time.sleep(1)
                    error_login_source = driver.page_source
                    driver.refresh()
                    temp_button_list = driver.find_elements(By.XPATH, "//button")
                    temp_input_list = driver.find_elements(By.XPATH, "//input")
                    temp_input_list[i_input - 1].send_keys(input_username)
                    temp_input_list[i_input].send_keys(input_password)
                    temp_button_list[i_button].click()
                    time.sleep(1)
                    valid_login_source = driver.page_source
                    diff = (difflib.SequenceMatcher(None, error_login_source, valid_login_source).quick_ratio())
                    print('diff: ' + str(100 - (diff * 100)) + '%')
                    if diff > 0:
                        status_login = True
                        temp_logs = driver.get_log("performance")
                        temp_header = read_extra(input_url, temp_logs)
                        print("header:" + temp_header)
                        print('login success')
                    else:
                        print('login fail')
                except Exception as ex:
                    pass
    except Exception as ex:
        print('Exception:' + str(ex))
    finally:
        driver.quit()
        return status_login


def read_login_header(input_url, input_action_list, input_cookie=None, headless_mode=False):
    # 0. init
    chrome_options = Options()
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    before_login_source = None
    error_login_source = None
    valid_login_source = None
    second_write = False
    # 1. set headless
    chrome_options.add_argument("--incognito")
    if headless_mode:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
    # 2. set user-agent
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) " \
         "AppleWebKit/537.36 (KHTML, like Gecko) " \
         "Chrome/92.0.4515.159 Safari/537.36"
    chrome_options.add_argument('user-agent={}'.format(ua))
    # 3. open browser
    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
                              options=chrome_options,
                              desired_capabilities=capabilities)
    driver.set_window_size(1024, 768)
    # 4. set cookie
    if input_cookie:
        driver.get(input_url)
        driver.add_cookie(input_cookie)
    # 5. error login
    try:
        driver.implicitly_wait(10)
        driver.get(input_url)
        before_login_source = driver.page_source
        for temp_action in input_action_list:
            if temp_action['type'] == 'click':
                driver.find_element(By.XPATH, temp_action['xpath']).click()
            if temp_action['type'] == 'write':
                if second_write:
                    driver.find_element(By.XPATH, temp_action['xpath']).send_keys(temp_action['text'] + '1')
                else:
                    driver.find_element(By.XPATH, temp_action['xpath']).send_keys(temp_action['text'])
                    second_write = True
        time.sleep(3)
        error_login_source = driver.page_source
        # driver.refresh()
        driver.get(input_url)
        error_auth_logs = driver.get_log("performance")
        error_header = read_extra(input_url, error_auth_logs)
        print(error_header)
        print("header length:" + str(len(str(error_header))))
    except Exception as ex:
        print('Exception:' + str(ex))
    finally:
        driver.quit()

    # 6. try login
    driver_2 = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
                                options=chrome_options,
                                desired_capabilities=capabilities)
    driver_2.set_window_size(1024, 768)
    driver_2.get(input_url)
    for temp_action in input_action_list:
        if temp_action['type'] == 'click':
            driver_2.find_element(By.XPATH, temp_action['xpath']).click()
        if temp_action['type'] == 'write':
            driver_2.find_element(By.XPATH, temp_action['xpath']).send_keys(temp_action['text'])
    time.sleep(3)
    valid_login_source = driver_2.page_source
    # driver_2.refresh()
    driver_2.get(input_url)
    temp_logs = driver_2.get_log("performance")
    temp_header = read_extra(input_url, temp_logs)
    print(temp_header)
    print("header length:" + str(len(str(temp_header))))
    # 7. close browser and return result
    driver_2.quit()
    diff_error = difflib.SequenceMatcher(None, before_login_source, error_login_source).quick_ratio()
    diff_valid = difflib.SequenceMatcher(None, before_login_source, valid_login_source).quick_ratio()
    diff = int(abs(diff_error - diff_valid) * 100)
    print('diff: ' + str(diff) + '%')
    if diff < 10:
        print('login fail')
    else:
        print('login success')
    """
    if len(str(error_header)) == len(str(temp_header)):
        print('login fail')
    else:
        print('login success')
    """
    return temp_header


def read_extra(input_url, input_logs):
    extra_info = False
    for entry in input_logs:
        temp_log = json.loads(entry["message"])["message"]
        try:
            if temp_log['params']['request']['url'] == input_url:
                if "Network.requestWillBeSent" == temp_log["method"]:
                    extra_info = True
        except Exception:
            pass
        if extra_info:
            if "Network.requestWillBeSentExtraInfo" == temp_log["method"]:
                extra_header = temp_log['params']['headers']
                extra_info = False
    return extra_header


def read_bing_search(input_query, input_cookie=None, headless_mode=False):
    # 0. init setting
    retry_count = 5
    max_page = 5
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    result_list = []
    url_list = []
    title_list = []
    # 1. set headless
    if headless_mode:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
    # 2.1 set default header
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) " \
         "AppleWebKit/537.36 (KHTML, like Gecko) " \
         "Chrome/92.0.4515.159 Safari/537.36"
    chrome_options.add_argument('user-agent={}'.format(ua))
    # 3. open browser
    basic_url = "https://www.bing.com/search?q="
    temp_url = basic_url + input_query
    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
                              chrome_options=chrome_options)
    # 4. set cookie
    if input_cookie:
        driver.get(temp_url)
        driver.add_cookie(input_cookie)
    # 5. send request
    driver.implicitly_wait(10)
    driver.get(temp_url)
    # 6. Crawler
    for _page in range(max_page):
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        h2_list = soup.find_all('h2')
        for h2 in h2_list:
            try:
                temp_dict = h2.contents[0].attrs
                if len(temp_dict) > 1:
                    temp_url = temp_dict['href']
                    temp_title = h2.text
                    if 'http' in temp_dict['href']:
                        if temp_url not in url_list:
                            url_list.append(temp_url)
                            title_list.append(temp_title)
                            result_list.append({'title': temp_title, 'link': temp_url})
            except Exception as ex:
                print(str(ex))
                pass

        # 6.1 Turn to the next page
        try:
            driver.find_element(By.XPATH, "//a[@class='sb_pagN sb_pagN_bp b_widePag sb_bp ']").click()
            time.sleep(1)
        except Exception as ex:
            print('Search Early Stopping.')
            print(ex)
            retry_count = retry_count - 1
            if retry_count == 0:
                break

    # 7. close browser
    driver.quit()

    return result_list


def read_google_search(input_query,
                       input_cookie=None,
                       headless_mode=False):
    # 0. init setting
    retry_count = 5
    max_page = 5
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    title_list = []
    # 1. set headless
    if headless_mode:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

    # 2 set default header
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) " \
         "AppleWebKit/537.36 (KHTML, like Gecko) " \
         "Chrome/92.0.4515.159 Safari/537.36"
    chrome_options.add_argument('user-agent={}'.format(ua))

    # 3. open browser
    basic_url = "https://www.google.com/search?q="
    temp_url = basic_url + input_query
    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
                              chrome_options=chrome_options)
    # 4. set cookie
    if input_cookie:
        driver.get(temp_url)
        driver.add_cookie(input_cookie)
    # 5. send request
    driver.implicitly_wait(10)
    driver.get(temp_url)
    # 6. Crawler
    for _page in range(max_page):
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        titles = soup.find_all('h3')
        for title in titles:
            try:
                temp_url = title.parent['href']
                if title not in title_list:
                    title_list.append({"name": title.text, "url": temp_url})
            except Exception as ex:
                print('Exception:' + str(ex))
        # 6.1. Turn to the next page
        try:
            driver.find_element(By.LINK_TEXT, '下一頁').click()
            time.sleep(1)
        except Exception as ex:
            print('Search Early Stopping.')
            print(ex)
            retry_count = retry_count - 1
            if retry_count == 0:
                break

    # 6. close browser
    driver.quit()

    return title_list


def read_json(input_file):
    temp_file = open(input_file)
    temp_json = json.load(temp_file)
    return temp_json


def read_get_page_screenshot(input_url, input_path, input_filename, input_cookie=None, headless_mode=False):
    # 0. init
    chrome_options = Options()
    # 1. set headless
    chrome_options.add_argument("--incognito")
    if headless_mode:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

    # 2. set user-agent
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) " \
         "AppleWebKit/537.36 (KHTML, like Gecko) " \
         "Chrome/92.0.4515.159 Safari/537.36"
    chrome_options.add_argument('user-agent={}'.format(ua))
    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=chrome_options)
    # 4. set cookie
    if input_cookie:
        driver.get(input_url)
        driver.add_cookie(input_cookie)
    # 5. send request
    driver.implicitly_wait(10)
    driver.set_window_size(1200, 600)
    driver.get(input_url)
    # 6. close browser
    driver.get_screenshot_as_file(input_path + input_filename)
    driver.quit()
    return


# testcase
if __name__ == '__main__':
    # print(read_get(input_url="https://www.example.com"))
    # print(read_bing_search('Cymetrics'))
    # print(read_google_search('Cymetrics'))
    """
    # auto login ithome
    read_login_form(input_url="https://member.ithome.com.tw/login",
                    input_username="saicx016",
                    input_password="a12345678",
                    headless_mode=True)
    
    read_login_auto(input_url="http://bioid.tw/login.php",
                    input_username="phe23967@boofx.com",
                    input_password="a12345678",
                    headless_mode=False)
    
    # manual login ithome
    test_json_list = [{'type': 'write', 'xpath': '//*[@id="account"]', 'text': 'saicx016'},
                      {'type': 'write', 'xpath': '//*[@id="password"]', 'text': 'a12345678'},
                      {'type': 'click', 'xpath': '/html/body/div/div/div/form/button', 'text': ''}]
    x_dict = read_login_header(input_url="https://member.ithome.com.tw/login",
                               input_action_list=test_json_list)
    """
    main_result = read_get_page(input_url="https://www.example.com")
    if "Example Domain" in main_result:
        print("unit test (custom_chrome) : pass")
        sys.exit(0)
    else:
        print("unit test (custom_chrome) : fail")
        sys.exit(1)


