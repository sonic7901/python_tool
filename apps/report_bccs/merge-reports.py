#!/usr/bin/env python3

import logging
import argparse
import sys
import json
import os
import glob

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')


def init_main_report(report):
    data = {}
    with open(report, 'r', encoding="utf-8") as file:
        data = json.load(file)
    file.close()
    return data


def merge_report(main_report, file):
    cout_list = ["A1", "A2", "A3", "A4", "A5",
                 "A6", "A7", "A8", "A9", "A10", "others"]
    with open(file, 'r', encoding="utf-8") as report:
        data = json.load(report)
        url = data["urlList"][0]
        main_report["urlList"].append(url)
        main_report["summaryList"].append(data["summaryList"][0])
        main_report["issues"][url] = data["issues"][url]
        for name in cout_list:
            main_report["owaspSummary"][name] = main_report["owaspSummary"][name] + \
                data["owaspSummary"][name]
        return main_report


def add_issueid(report_json):
    issue_id = 1

    urls = report_json["urlList"]
    for url in urls:
        issues = len(report_json["issues"][url])
        for i in range(issues):
            report_json["issues"][url][i]["issueId"] = issue_id
            issue_id += 1
    return report_json


def main(dir, output_name):
    reports = []
    if dir is None:
        reports = glob.glob('/data/*.json')
    else:
        reports = glob.glob(f'{dir}/**/result.json', recursive=True)

    reports = ['./report_1/result.json',
               './report_2/result.json']

    print(reports)

    # check file exists
    for r in reports:
        if os.path.exists(r) == False:
            logger.error("file %s is not exists" % r)
            return False

    all_report = ' '.join(map(str, reports))
    logger.info("report to merge: " + all_report)

    # use first as main report
    logger.info("use %s as main report" % reports[0])
    result = init_main_report(reports[0])

    # merge others
    for item in reports[1:]:
        result = merge_report(result, item)

    result = add_issueid(result)

    with open(output_name, 'w', encoding='utf8') as f:
        json.dump(result, f, ensure_ascii=False)
        f.close()

    logger.info("write file to "+output_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir',
                        help='<Required> report path', required=False)
    parser.add_argument('-o', '--output', default='result_merged.json',
                        help='output file name', required=False)
    args = parser.parse_args()
    sys.exit(
        main(
            dir=args.dir, output_name=args.output
        )
    )
