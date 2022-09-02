import sqlite3
import os

import sys


def init(db_file):
    try:
        if os.path.isfile(db_file):
            print('database ' + str(db_file) + ' already exist')
            os.remove(db_file)
        create_table_user(db_file)
        create_table_issue(db_file)
        create_table_mission(db_file)
        add_user(db_file, 'cymetrics', 'aA@123456')
        # testcase

    except Exception as ex:
        print('Exception:' + str(ex))


def create_table_user(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE USER(
                    ID INTEGER PRIMARY KEY,
                    NAME           TEXT    NOT NULL,
                    PASS           TEXT    NOT NULL);''')
        print('table user created')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))


def create_table_mission(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE MISSION(
                    ID INTEGER PRIMARY KEY,
                    URL           TEXT    NOT NULL,
                    COMPANY       TEXT    NOT NULL,
                    TARGET        TEXT   ,
                    STATUS        TEXT    NOT NULL,
                    LINK          TEXT);''')
        print('table mission created')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))


# id, origin, bypass, score, weight, cost, name_en, name_zh, desc_en, desc_zh, advice_en, advice_zh
def create_table_issue(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE ISSUE(
                    ID INTEGER PRIMARY KEY,
                    ORIGIN         TEXT    NOT NULL,
                    BYPASS         TEXT    NOT NULL,
                    SCORE          INT     NOT NULL,
                    WEIGHT         INT     NOT NULL,
                    COST           INT     NOT NULL,
                    NAME_EN        TEXT    NOT NULL,
                    NAME_ZH        TEXT    NOT NULL,
                    DESCRIPTION_EN TEXT    NOT NULL,
                    DESCRIPTION_ZH TEXT    NOT NULL,
                    ADVICE_EN      TEXT    NOT NULL,
                    ADVICE_ZH      TEXT    NOT NULL);''')
        print('table issue created')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))

    try:
        import utils.custom_csv
        nmp = utils.custom_csv.read_file_to_dict("zap_report.csv")
        # df = pandas.read_excel("zap_report.xlsx")
        # nmp = df.values
        for n in nmp:
            print(n)
            temp_bypass = ''
            if not n['enabled']:
                temp_bypass = 'all'

            temp_score = 0
            if n['risk'] == 'High':
                temp_score = 75
            elif n['risk'] == 'Medium':
                temp_score = 50
            elif n['risk'] == 'Low':
                temp_score = 25

            temp_cost = 0
            if n['cost'] == 'High':
                temp_cost = 75
            elif n['cost'] == 'Medium':
                temp_cost = 50
            elif n['cost'] == 'Low':
                temp_cost = 25

            add_issue(db_file, n['origin'], temp_bypass, temp_score, '100', temp_cost,
                      n['name_en'], n['name_zh'], n['desc_en'], n['desc_zh'], n['advice_en'], n['advice_zh'])

    except Exception as ex:
        print('Exception:' + str(ex))


# id, issue_id, tag
def add_user(db_file, input_name, input_pass):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        sql_exec = f"INSERT INTO USER (NAME,PASS) VALUES (\"{input_name}\",\"{input_pass}\")"
        temp_cmd.execute(sql_exec)
        print('add_user ' + str(input_name))
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))


def add_issue(db_file,
              origin,
              bypass,
              score,
              weight,
              cost,
              name_en,
              name_zh,
              desc_en,
              desc_zh,
              advice_en,
              advice_zh):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        sql_exec = f"INSERT INTO ISSUE (ORIGIN,BYPASS,SCORE,WEIGHT,COST," \
                   f"NAME_EN,NAME_ZH,DESCRIPTION_EN,DESCRIPTION_ZH,ADVICE_EN,ADVICE_ZH) VALUES (" \
                   f"\"{origin}\"," \
                   f"\"{bypass}\"," \
                   f"\"{score}\"," \
                   f"\"{weight}\"," \
                   f"\"{cost}\"," \
                   f"\"{name_en}\"," \
                   f"\"{name_zh}\"," \
                   f"\"{desc_en}\"," \
                   f"\"{desc_zh}\"," \
                   f"\"{advice_en}\"," \
                   f"\"{advice_zh}\")"
        temp_cmd.execute(sql_exec)
        print('add_testcase ' + str(origin))
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))


def update_issue(db_file,
                 origin,
                 bypass,
                 score,
                 weight,
                 cost,
                 name_en,
                 name_zh,
                 desc_en,
                 desc_zh,
                 advice_en,
                 advice_zh):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        sql_exec = f"UPDATE ISSUE (ORIGIN,BYPASS,SCORE,WEIGHT,COST," \
                   f"NAME_EN,NAME_ZH,DESCRIPTION_EN,DESCRIPTION_ZH,ADVICE_EN,ADVICE_ZH) VALUES (" \
                   f"\"{origin}\"," \
                   f"\"{bypass}\"," \
                   f"\"{score}\"," \
                   f"\"{weight}\"," \
                   f"\"{cost}\"," \
                   f"\"{name_en}\"," \
                   f"\"{name_zh}\"," \
                   f"\"{desc_en}\"," \
                   f"\"{desc_zh}\"," \
                   f"\"{advice_en}\"," \
                   f"\"{advice_zh}\")"
        temp_cmd.execute(sql_exec)
        print('add_testcase ' + str(origin))
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))


def add_mission(db_file, input_url, input_company, input_target):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_status = "waiting"
        temp_link = ""
        sql_exec = f"INSERT INTO MISSION (URL,COMPANY,TARGET,STATUS,LINK) VALUES (" \
                   f"\"{input_url}\"," \
                   f"\"{input_company}\"," \
                   f"\"{input_target}\"," \
                   f"\"{temp_status}\"," \
                   f"\"{temp_link}\")"
        temp_cmd.execute(sql_exec)
        print('add_mission: ' + str(input_company))
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))


def update_status_by_id(db_file, input_id, input_status):
    try:
        if os.path.isfile(db_file):
            sql = f"UPDATE TESTCASE SET STATUS=\"{input_status}\" where ID={input_id};"
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            temp_cmd.execute(sql)
            temp_conn.commit()
            temp_conn.close()
        else:
            print('database ' + str(db_file) + ' not found')
    except Exception as ex:
        print('Exception:' + str(ex))


def update_mission_by_id(db_file, input_id, input_status, input_link):
    try:
        if os.path.isfile(db_file):
            sql = f"UPDATE MISSION SET STATUS=\"{input_status}\", LINK=\"{input_link}\" where ID={input_id};"
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            temp_cmd.execute(sql)
            temp_conn.commit()
            temp_conn.close()
        else:
            print('database ' + str(db_file) + ' not found')
    except Exception as ex:
        print('Exception:' + str(ex))


def read_fields(db_file, input_table):
    # sql = "select * from " + str(input_table)
    sql = f"PRAGMA table_info({input_table})"
    if os.path.isfile(db_file):
        print('database ' + str(db_file) + ' already exist')
    temp_conn = sqlite3.connect(db_file)
    temp_cmd = temp_conn.cursor()
    temp_cmd.execute(sql)
    temp_data = temp_cmd.fetchall()
    temp_field_name = [field[1] for field in temp_data]
    print(temp_field_name)
    return temp_field_name


def read_issue_by_id(db_file, input_id):
    temp_data = []
    try:
        if os.path.isfile(db_file):
            sql = f"select SCORE, WEIGHT, NAME_ZH, NAME_EN, DESCRIPTION_ZH, DESCRIPTION_EN, ADVICE_ZH, ADVICE_EN" \
                  f" from ISSUE where ID=" + str(input_id) + ";"
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            temp_cmd.execute(sql)
            temp_data = temp_cmd.fetchall()
        else:
            print('database ' + str(db_file) + ' not found')
    except Exception as ex:
        print('Exception:' + str(ex))
    return temp_data[0]


def read_verify_by_id(db_file, input_id):
    temp_result = ""
    try:
        if os.path.isfile(db_file):
            sql = f"select VERIFY from TESTCASE where ID=\"{input_id}\";"
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            temp_cmd.execute(sql)
            temp_data = temp_cmd.fetchall()
            print('sql data:' + str(temp_data))
            temp_result = str(temp_data[-1][0])
            print(temp_result)
        else:
            print('database ' + str(db_file) + ' not found')
    except Exception as ex:
        print('Exception:' + str(ex))
    return temp_result


def read_data(db_file, input_table):
    temp_data = ''
    if os.path.isfile(db_file):
        sql = "select * from " + str(input_table)
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute(sql)
        temp_data = temp_cmd.fetchall()
    else:
        print('database ' + str(db_file) + ' not found')
    return temp_data


def read_data_missions(db_file):
    temp_data = ''
    if os.path.isfile(db_file):
        sql = "select COMPANY,URL,STATUS,LINK from MISSION"
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute(sql)
        temp_data = temp_cmd.fetchall()
        print(temp_data)
    else:
        print('database ' + str(db_file) + ' not found')
    return temp_data


def read_data_issues(db_file):
    temp_data = ''
    if os.path.isfile(db_file):
        sql = "select ID,ORIGIN,NAME_ZH,NAME_EN from ISSUE"
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute(sql)
        temp_data = temp_cmd.fetchall()
        print(temp_data)
    else:
        print('database ' + str(db_file) + ' not found')
    return temp_data


def read_data_users(db_file):
    temp_data = ''
    if os.path.isfile(db_file):
        sql = "select NAME,PASS from USER"
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute(sql)
        temp_data = temp_cmd.fetchall()
        print(temp_data)
    else:
        print('database ' + str(db_file) + ' not found')
    return temp_data


if __name__ == "__main__":
    init('test.db')
    # add_user('test.db', 'u1', 'passwd')
    # add_testcase('test.db', 't1', 'test', 'test2.py', '1')
    # read_fields('test.db', 'TESTCASE')
    # read_testcase_id('test.db', 't1')
    # update_status_by_id('test.db', '1', 'test2')
    # read_data('test.db', 'ISSUE')
    # add_mission('test.db', "http://www.example.com", "Demo 公司 2", "入口網站")
    # read_data_mission('test.db')
    # read_issue_by_id('test.db', 5)
