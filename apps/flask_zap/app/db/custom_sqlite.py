import sqlite3
import os
import sys


def init(db_file):
    try:
        if os.path.isfile(db_file):
            print('database ' + str(db_file) + ' already exist')
            os.remove(db_file)
        create_table_user(db_file)
        create_table_testcase(db_file)
        add_user(db_file, 'admin', 'passwd')
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


def create_table_testcase(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE TESTCASE(
                    ID INTEGER PRIMARY KEY,
                    NAME           TEXT    NOT NULL,
                    DESCRIPTION    TEXT    ,
                    FILE           TEXT    NOT NULL,
                    VERIFY         TEXT    NOT NULL,
                    STATUS         TEXT    NOT NULL,
                    USER_ID        INT     NOT NULL);''')
        print('table testcase created')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))


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


def add_testcase(db_file, input_name, input_description, input_file, input_verify):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        sql_exec = f"INSERT INTO TESTCASE (NAME,DESCRIPTION,FILE,VERIFY,STATUS,USER_ID) VALUES (" \
                   f"\"{input_name}\"," \
                   f"\"{input_description}\"," \
                   f"\"{input_file}\"," \
                   f"\"{input_verify}\"," \
                   f"\"N/A\")"
        temp_cmd.execute(sql_exec)
        print('add_testcase ' + str(input_name))
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


def read_testcase_id(db_file, input_name):
    temp_result = 0
    try:
        if os.path.isfile(db_file):
            sql = f"select ID from TESTCASE where NAME=\"{input_name}\";"
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
    # read_data('test.db', 'TESTCASE')
    sys.exit(0)
