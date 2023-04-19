import os
import json


def read_json(report_name):
    # 0. init
    dict_data = ""
    # 1. run
    try:
        if os.path.isfile(report_name):
            with open(report_name, 'r', encoding='utf-8') as read_file:
                dict_data = json.load(read_file)
    except Exception as ex:
        print('Exception:' + str(ex))
    return dict_data


def trans_report(input_json_list):
    # init
    result_json = []
    try:
        for report_data in input_json_list:
            print(str(report_data['site'][0]['@name']))
            for site in report_data['site']:
                for alert in site['alerts']:
                    print(alert['name'])
                    if 'evidence' in alert:
                        result_json.append({"issue_name": alert['name'], "more_info": alert['evidence']})
                    else:
                        result_json.append({"issue_name": alert['name'], "more_info": ""})
        print(result_json
              )
    except Exception as ex:
        print('Exception:' + str(ex))


if __name__ == '__main__':
    trans_report([read_json('example.json')])

