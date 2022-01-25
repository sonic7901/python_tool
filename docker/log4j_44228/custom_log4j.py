import os
import subprocess
import json
import difflib
from bs4 import BeautifulSoup

import custom_request
import custom_log

bypass_split_list = ['New Relic']
bypass_issue_list = ['Microsoft 365',
                     'Microsoft PowerPoint',
                     'Microsoft SharePoint',
                     'Microsoft Excel',
                     'Microsoft Word',
                     ]
pass_issue_list = ['Azure', 'Azure AD B2C', 'Azure CDN']
high_name_list = ['Apache Tomcat']
high_dict = {'Apache Tomcat': {'max': 90099, 'min': 90000}}


def read_wappalyzer(input_url):
    # 0.init
    result_list = []
    # 1. wappalyzer
    try:
        # 1.1 not in docker
        env = os.environ.get('ENV', 'test')
        if env == 'test':
            cmd = ['docker',
                   'run',
                   '--rm',
                   'test_1',
                   'node',
                   'src/drivers/npm/cli.js',
                   input_url]
        # 1.2 in docker
        else:
            cmd = ['node',
                   'src/drivers/npm/cli.js',
                   input_url]
        cmd_result = subprocess.run(cmd, stdout=subprocess.PIPE, timeout=60)
        cmd_output = cmd_result.stdout.decode('utf-8')
        temp_list = cmd_output.split('\n')
        for str_output in temp_list:
            if 'urls' in str_output:
                cmd_output = str_output
        cmd_json = json.loads(cmd_output)
        for temp_technologies in cmd_json['technologies']:
            if temp_technologies['name']:
                if temp_technologies['version']:
                    result_list.append({"name": temp_technologies['name'], "version": temp_technologies['version']})
                    # print('name: ' + temp_technologies['name'])
                    # print('version: ' + temp_technologies['version'])
                else:
                    result_list.append({"name": temp_technologies['name'], "version": "0"})
                    # print('name: ' + temp_technologies['name'])
                    # print('version: 0')

    except Exception as ex:
        custom_log.error(ex)
    # print(result_list)
    return result_list


def read_app_list():
    count = 0
    page_source = custom_request.read_get("https://github.com/cisagov/log4j-affected-db/blob/develop/SOFTWARE-LIST.md")
    utf_8_page = str(page_source).encode('utf-8')
    soup = BeautifulSoup(utf_8_page, 'html.parser')
    data = []
    result_list = []
    tables = soup.find_all('table')
    table_body = tables[1].find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        data.append([ele.text for ele in cols if ele])  # Get rid of empty values
    for d in data:
        # print(d[3])
        if d[4] == "Affected" or d[3] == "Fixed":
            count += 1
            result_list.append([d[0], d[1], d[4]])
    return result_list


def check_app(input_name, input_app_list):
    for temp_app in input_app_list:
        if len(input_name) < 4:
            break
        if input_name in temp_app[0] or input_name in temp_app[1]:
            diff_vendor = (difflib.SequenceMatcher(None, input_name, temp_app[0]).quick_ratio()) * 100
            diff_product = (difflib.SequenceMatcher(None, input_name, temp_app[1]).quick_ratio()) * 100
            if diff_vendor > 40 or diff_product > 40:
                print("input :" + input_name)
                print("vendor:" + temp_app[0])
                print("product:" + temp_app[1])
                print("diff_vendor:" + str(int(diff_vendor)) + "%")
                print("diff_product:" + str(int(diff_product)) + "%")
                return True
        if temp_app[0] in input_name or temp_app[1] in input_name:
            diff_vendor = (difflib.SequenceMatcher(None, input_name, temp_app[0]).quick_ratio()) * 100
            diff_product = (difflib.SequenceMatcher(None, input_name, temp_app[1]).quick_ratio()) * 100
            if diff_vendor > 40 or diff_product > 40:
                print("input :" + input_name)
                print("vendor:" + temp_app[0])
                print("product:" + temp_app[1])
                print("diff_vendor:" + str(int(diff_vendor)) + "%")
                print("diff_product:" + str(int(diff_product)) + "%")
                return True
    return False


def check_app_2(input_name, check_vendor_name, check_product_name):
    input_product_name = ""
    input_vendor_name = ""
    diff_product = 0
    diff_vendor = 0
    temp_result = 0
    if (input_name not in bypass_split_list) and (' ' in input_name):
        temp_list = input_name.split(' ', 1)
        input_vendor_name = temp_list[0]
        input_product_name = temp_list[1]
    else:
        input_product_name = input_name
        input_vendor_name = input_name
    if input_vendor_name in check_vendor_name:
        diff_vendor = (difflib.SequenceMatcher(None, input_vendor_name, check_vendor_name).quick_ratio()) * 100
    if input_product_name in check_product_name:
        diff_product = (difflib.SequenceMatcher(None, input_product_name, check_product_name).quick_ratio()) * 100
    if (diff_vendor > 75 and diff_product > 45) or (diff_vendor > 75 and check_product_name == 'All Products'):
        temp_result = 2
        print('Medium')
        print("input :" + input_name)
        print("input_vendor_name:" + input_vendor_name)
        print("input_product_name:" + input_product_name)
        print("check_vendor_name:" + check_vendor_name)
        print("check_product_name:" + check_product_name)
        print("diff_vendor:" + str(int(diff_vendor)) + "%")
        print("diff_product:" + str(int(diff_product)) + "%")
    elif diff_vendor > 75 and len(input_vendor_name) > 3:
        temp_result = 1
        print('Low:vendor')
        print("input :" + input_name)
        print("input_vendor_name:" + input_vendor_name)
        print("input_product_name:" + input_product_name)
        print("check_vendor_name:" + check_vendor_name)
        print("check_product_name:" + check_product_name)
        print("diff_vendor:" + str(int(diff_vendor)) + "%")
        print("diff_product:" + str(int(diff_product)) + "%")
    elif diff_product > 85 and len(input_product_name) > 5:
        temp_result = 1
        print('Low:product')
        print("input :" + input_name)
        print("input_vendor_name:" + input_vendor_name)
        print("input_product_name:" + input_product_name)
        print("check_vendor_name:" + check_vendor_name)
        print("check_product_name:" + check_product_name)
        print("diff_vendor:" + str(int(diff_vendor)) + "%")
        print("diff_product:" + str(int(diff_product)) + "%")

    return temp_result


def scan(input_url):
    try:
        temp_additional = ""
        temp_app_list = read_app_list()
        temp_result_list = read_wappalyzer(input_url)
        for temp_result in temp_result_list:
            if check_app(temp_result['name'], temp_app_list):
                temp_additional = temp_result['name'] + ', ' + temp_additional
        # print(temp_additional)

    except Exception as ex:
        print(ex)


def read_wappalyzer_list():
    result_list = []
    count = 0
    from urllib.request import urlopen
    import json
    for x in range(ord('a'), ord('z')+1):
        url = "https://raw.githubusercontent.com/AliasIO/wappalyzer/master/src/technologies/" + chr(x) + ".json"
        response = urlopen(url)
        data_json = json.loads(response.read())
        for dict_data in data_json:
            result_list.append([str(dict_data), data_json[dict_data]['website']])
            count += 1
            # print(str(count) + '. ' + str(dict_data))
    return result_list


def test_main():
    log4j_list = read_app_list()
    wappalyzer_list = read_wappalyzer_list()
    main_count = 0
    result_dict = {}
    for temp_software in wappalyzer_list:
        if temp_software[0] in bypass_issue_list:
            continue
        if temp_software[0] in pass_issue_list:
            result_dict[temp_software[0]] = 2
        for log4j in log4j_list:
            issue_level = check_app_2(temp_software[0], log4j[0], log4j[1])
            if issue_level > 0:
                main_count += 1
                print(temp_software[1])
                if temp_software[0] in result_dict:
                    if issue_level > result_dict[temp_software[0]]:
                        result_dict[temp_software[0]] = issue_level
                else:
                    result_dict[temp_software[0]] = issue_level
                print("== " + str(main_count) + " =============================================")

    for i in result_dict:
        print(str(i) + ' : ' + str(result_dict[i]))


def docker_scan():
    pass


if __name__ == '__main__':
    test_main()
    # read_wappalyzer_list()
    """
    try:
        scan("https://www.evergreen-marine.com/")
    except Exception as unit_ex:
        print(unit_ex)
    """
