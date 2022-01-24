import os
import subprocess
import json
import sys
import difflib
from bs4 import BeautifulSoup

import custom_request
import custom_log


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
                    custom_log.info('name: ' + temp_technologies['name'])
                    custom_log.info('version: ' + temp_technologies['version'])
                else:
                    result_list.append({"name": temp_technologies['name'], "version": "0"})
                    custom_log.info('name: ' + temp_technologies['name'])
                    custom_log.info('version: 0')

    except Exception as ex:
        custom_log.error(ex)
    print(result_list)
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
        if d[3] == "Affected" or d[3] == "Fixed":
            count += 1
            result_list.append([d[0], d[1], d[3]])
    return result_list


def check_app(input_name, input_app_list):
    for temp_app in input_app_list:
        if input_name in temp_app[0] or input_name in temp_app[1]:
            diff_vendor = (difflib.SequenceMatcher(None, input_name, temp_app[0]).quick_ratio()) * 100
            diff_product = (difflib.SequenceMatcher(None, input_name, temp_app[1]).quick_ratio()) * 100
            if diff_vendor > 40 or diff_product > 40:
                custom_log.info("input :" + input_name)
                custom_log.info("vendor:" + temp_app[0])
                custom_log.info("product:" + temp_app[1])
                custom_log.info("diff_vendor:" + str(int(diff_vendor)) + "%")
                custom_log.info("diff_product:" + str(int(diff_product)) + "%")
                return True
    return False


def scan(input_url):
    try:
        temp_additional = ""
        temp_app_list = read_app_list()
        temp_result_list = read_wappalyzer(input_url)
        for temp_result in temp_result_list:
            if check_app(temp_result['name'], temp_app_list):
                temp_additional = temp_result['name'] + ', ' + temp_additional
        print(temp_additional)

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    try:
        scan("https://www.evergreen-marine.com/")
    except Exception as unit_ex:
        print(unit_ex)
