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
    """
    # nar_lab
    custom_report.set_company('資安暨智慧科技研發大樓')
    main_json_1 = {'target': '門禁系統', 'site': [{'@name': ''}], 'input': '60.249.236.100'}
    main_json_2 = {'target': 'CCTV-01', 'site': [{'@name': ''}], 'input': '60.249.236.101'}
    main_json_3 = {'target': 'CCTV-02', 'site': [{'@name': ''}], 'input': '60.249.236.102'}
    main_json_4 = {'target': 'CCTV-03', 'site': [{'@name': ''}], 'input': '60.249.236.103'}
    main_json_5 = {'target': 'CCTV-04', 'site': [{'@name': ''}], 'input': '60.249.236.104'}
    custom_report.transfer_report([main_json_1, main_json_2, main_json_3, main_json_4, main_json_5])
    # nar_lab end
    """
