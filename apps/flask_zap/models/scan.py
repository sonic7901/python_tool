import time
import pathlib
import shutil
import os
import threading
import db.custom_sqlite
import utils.custom_report as zap_report


# file path
temp_path = str(pathlib.Path(__file__).parent.absolute()) + "\\"


def scan_thread():
    temp_thread = threading.Thread(target=run_check)
    temp_thread.start()


def run_check():
    time.sleep(3)
    while True:
        list_mission = db.custom_sqlite.read_data(temp_path + '../db/test.db', 'MISSION')
        for temp_mission in list_mission:
            scan_status = False
            # 0. debug
            print('-------------------')
            print('Company: ' + temp_mission[2])
            print('URL: ' + temp_mission[1])
            print('Target name: ' + temp_mission[3])
            print("status: " + temp_mission[4])
            if temp_mission[4] == 'waiting':
                # 1. scan
                db.custom_sqlite.update_mission_by_id(temp_path + '../db/test.db',
                                                      temp_mission[0],
                                                      'scanning',
                                                      '')
                run_docker(temp_mission[1])

                # 2. wait for scan result
                count_timeout_min = 60
                for i in range(0, count_timeout_min):
                    if os.path.isfile(temp_path + 'temp.json'):
                        print('status: scan end')
                        create_report(temp_mission[0], temp_mission[2], temp_mission[3])
                        print('status: report created')
                        scan_status = True
                        break
                    else:
                        print('status: scanning(' + str(i) + ' min)')
                        time.sleep(60)
                    if i == count_timeout_min - 1:
                        print('status: time out')

                # 3. update database
                if scan_status:
                    temp_file = '/report/' + str(temp_mission[0]) + "/VAS弱掃報告_" + temp_mission[2] + ".docx"
                    db.custom_sqlite.update_mission_by_id(temp_path + '../db/test.db',
                                                          temp_mission[0],
                                                          'success',
                                                          temp_file)
                    print('status: update success mission')
                else:
                    db.custom_sqlite.update_mission_by_id(temp_path + '../db/test.db',
                                                          temp_mission[0],
                                                          'fail',
                                                          '')
                    print('status: update fail mission')
            else:
                time.sleep(1)

        time.sleep(60)


def create_report(input_id, input_company, input_target):
    # 0. input check
    if input_company == "":
        temp_company = "Demo"
    else:
        temp_company = input_company
    temp_file = "VAS弱掃報告_" + temp_company + ".docx"

    if input_target == "":
        temp_target = "Device_1"
    else:
        temp_target = input_target

    # 1. report input
    zap_report.set_company(temp_company)
    main_json_1 = zap_report.read_json(temp_path + 'temp.json')
    main_json_1["target"] = temp_target

    # 2. generator report
    zap_report.transfer_report([main_json_1])
    if not os.path.isdir(temp_path + '..\\report\\' + str(input_id)):
        os.mkdir(temp_path + '..\\report\\' + str(input_id))
    shutil.copyfile(temp_file, temp_path + '..\\report\\' + str(input_id) + '\\' + temp_file)

    # 3. clear temp file
    os.remove(temp_path + 'temp.json')
    os.remove('VAS弱掃報告_' + input_company + '.docx')


def run_docker(temp_url):
    # debug
    print('zap scan: ' + temp_url)
    time.sleep(5)
    shutil.copyfile(temp_path + '/example.json', temp_path + '/temp.json')
    pass


if __name__ == "__main__":
    shutil.copyfile('example.json', 'temp.json')
    run_check()
