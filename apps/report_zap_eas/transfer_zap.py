import os
import json
import csv
import sys

'''
Error codes:
0: no error
1: anything from python program exception (ex: import error, other uncaught error)
2: error reading zap report
3: error transforming report
'''


def read_report(report_name):
    dict_data = ""
    try:
        if os.path.isfile(report_name):
            with open(report_name, 'r', encoding='utf-8') as read_file:
                dict_data = json.load(read_file)
    except Exception as ex:
        print('Exception' + str(ex))
    return dict_data


def payloads2text(instances):
    all_info = ''
    for single in instances:
        url = single['uri']
        try:
            parameter = single['parameter']
        except Exception as ex:
            parameter = ''
        try:
            attack = single['attack']
        except Exception as ex:
            attack = ''
        try:
            evidence = single['evidence']
        except Exception as ex:
            evidence = ''
        if parameter != '' or attack != '' or evidence != '':
            more_info = url + \
                ' (' + parameter + attack + evidence + ')'
        else:
            more_info = url
        all_info = all_info + more_info + '\n'
    return all_info


def transfer_report(report_data):
    csv_issues = []
    scv_issue_tags = []
    csv_options = []
    checked_issues = []
    additional_info = {}

    # read issue list
    with open('transfer_zap.csv', newline='', encoding="utf-8") as csv_file:
        rows = csv.DictReader(csv_file)
        for row in rows:
            csv_issues.append(row['en'])
            scv_issue_tags.append(row['cn'])
            csv_options.append(row['options'])
    try:
        for site in report_data['site']:
            for alert in site['alerts']:
                if len(alert['instances']) == 0:
                    continue
                instances = alert['instances']
                options = []
                is_hit = False
                for issue in csv_issues:
                    if issue in alert['name']:
                        is_hit = True
                        issue_id = csv_issues.index(issue)
                        checked_issues.append(scv_issue_tags[issue_id])
                        op = csv_options[issue_id]
                        if len(op) != 0:
                            options.append(op)
                        all_info = payloads2text(instances)
                        tag = scv_issue_tags[issue_id]
                        # if already exists
                        if tag in additional_info:
                            additional_info[tag]["proof"] += all_info
                            additional_info[tag]["options"].extend(options)
                        else:
                            additional_info[tag] = {
                                "proof": all_info, "options": options}

                        additional_info[tag]["options"] = list(
                            set(additional_info[tag]["options"]))

                if is_hit != True:
                    print(f"bypass alert {alert['name']}")

        final_result = {
            "additionalInfo": additional_info,
            "checkedIssues": list(set(checked_issues))
        }

        print(json.dumps(final_result))
        return final_result

    except Exception as ex:
        print('Exception' + str(ex))
        return None


def write_report(tid, list_result):
    with open(tid + '.json', 'w') as outfile:
        json.dump(list_result, outfile)
    return True


if __name__ == '__main__':
    origin_report = read_report('2023-05-12-ZAP-Report-61.216.83.40.json')
    if origin_report == "":
        sys.exit(2)
    s_card_report = transfer_report(origin_report)
    if not s_card_report:
        sys.exit(3)
    write_report('data', s_card_report)
