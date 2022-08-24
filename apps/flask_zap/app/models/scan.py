import time
import os
import app.db.custom_sqlite


def run_check():
    temp_data = app.db.custom_sqlite.read_data('../db/test.db', 'MISSION')
    for i in temp_data:
        if i[4] == 'waiting':
            print('-------------------')
            print('Company:' + i[2])
            print('URL:' + i[1])
            print('Target name:' + i[3])
            # run_docker(i[1])
            count_timeout_min = 3
            temp_status = ""
            while count_timeout_min != 0:
                print('scan time: ' + str(60 - count_timeout_min) + ' min')
                time.sleep(3)
                if not os.path.isfile('temp.json'):
                    print('found zap report')
                    break
                else:
                    print('scanning')
                    count_timeout_min -= 1
            if count_timeout_min == 0:
                print('time out')
            else:
                print('done')
            break


if __name__ == "__main__":
    run_check()
