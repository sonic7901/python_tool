import custom_report

if __name__ == '__main__':
    # example start
    # set company name
    custom_report.set_company('example')
    # normal example
    main_json_1 = custom_report.read_json('example.json')
    main_json_1["target"] = "Device_1"
    # none issue example
    main_json_2 = {'target': 'Device_2', 'site': [{'@name': ''}], 'input': '192.168.1.1'}
    # generator report
    # custom_report.transfer_report([main_json_1, main_json_2])
    custom_report.transfer_report_en([main_json_1, main_json_2])
    # example end

