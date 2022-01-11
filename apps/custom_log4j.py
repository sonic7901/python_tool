import utils.custom_markdown
import utils.custom_request as temp_request
from bs4 import BeautifulSoup
import pandas as pd
from collections import OrderedDict
from pprint import pprint
import json
import difflib


def read_app_list():
    count = 0
    page_source = temp_request.read_get("https://github.com/cisagov/log4j-affected-db/blob/develop/SOFTWARE-LIST.md")
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


def scan(input_name, input_app_list):
    for temp_app in input_app_list:
        if input_name in temp_app[0] or input_name in temp_app[1]:
            diff_vendor = (difflib.SequenceMatcher(None, input_name, temp_app[0]).quick_ratio()) * 100
            diff_product = (difflib.SequenceMatcher(None, input_name, temp_app[1]).quick_ratio()) * 100
            if diff_vendor > 40 or diff_product > 40:
                print("input:" + input_name)
                print("vendor:" + temp_app[0])
                print("product:" + temp_app[1])
                print("diff_vendor:" + str(int(diff_vendor)) + "%")
                print("diff_product:" + str(int(diff_product)) + "%")
                print("==============================")
                break


def read_json():
    temp_app_list = read_app_list()
    with open('s.json') as json_file:
        data = json.load(json_file)
        for single_data in data:
            # print(single_data)
            scan(single_data, temp_app_list)
    pass


read_json()
