import custom_report

if __name__ == '__main__':
    main_json_1 = custom_report.read_json('example.json')
    main_json_1["target"] = "Device_1"
    custom_report.transfer_report([main_json_1])
    # main_json_2 = custom_report.read_report('2022-07-04-ZAP-Report-172.16.100.227.json')
    # main_json_2["target"] = "Device_5"
    # transfer_report_en([main_json_1, main_json_2])
    # custom_report.transfer_report([main_json_1, main_json_2])
    # transfer_report([main_json_1])
    # read_screenshot('https://tw.yahoo.com/')
