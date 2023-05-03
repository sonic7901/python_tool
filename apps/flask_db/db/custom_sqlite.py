import sqlite3
import os
import utils.custom_csv
import utils.custom_request

# init
db_file = './test.db'


def init():
    try:
        if os.path.isfile(db_file):
            print('database ' + str(db_file) + ' already exist')
            os.remove(db_file)
        create_table_user()
        create_table_issue()
        create_table_language()
        create_table_issue_origin()
        create_table_issue_name()
        create_table_issue_description()
        create_table_advice()
        create_table_link_advice()
        create_table_reference()
        create_table_link_reference()
        create_table_type()
        create_table_link_type()
        add_user('cymetrics', 'aA@123456')
    except Exception as ex:
        print('Exception(init):' + str(ex))


def set_db(input_path):
    global db_file
    db_file = input_path
    return


def read_data(input_table):
    # init
    temp_list = []
    try:
        if os.path.isfile(db_file):
            sql_exec = "select * from " + str(input_table)
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            temp_cmd.execute(sql_exec)
            temp_data = temp_cmd.fetchall()
            for temp_tuple in temp_data:
                temp_list.append(list(temp_tuple))
        else:
            print('database ' + str(db_file) + ' not found')
    except Exception as ex:
        print('Exception(read_data):' + str(ex))
    finally:
        return temp_list


def read_gpt_update():
    # init
    temp_list = []
    try:
        if os.path.isfile(db_file):
            sql_exec = "select value from STATUS WHERE type=\"gpt_update\""
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            temp_cmd.execute(sql_exec)
            temp_data = temp_cmd.fetchall()
            for temp_tuple in temp_data:
                temp_list.append(list(temp_tuple))
        else:
            print('database ' + str(db_file) + ' not found')
    except Exception as ex:
        print('Exception(read_data):' + str(ex))
    finally:
        return temp_list[0]


def read_data_issue_name(input_id, input_language):
    # init
    temp_list = []
    try:
        if os.path.isfile(db_file):
            sql_exec = f"select DISPLAY from ISSUE_NAME where ISSUE_ID={input_id} and LANGUAGE_ID={input_language}"
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            temp_cmd.execute(sql_exec)
            temp_data = temp_cmd.fetchall()
            for temp_tuple in temp_data:
                temp_list.append(list(temp_tuple))
        else:
            print('database ' + str(db_file) + ' not found')
    except Exception as ex:
        print('Exception(read_data):' + str(ex))
    finally:
        return temp_list[0][0]


def read_data_issue_description(input_id, input_language):
    # init
    temp_list = []
    try:
        if os.path.isfile(db_file):
            sql_exec = f"select DISPLAY from ISSUE_DESCRIPTION " \
                       f"where ISSUE_ID={input_id} and LANGUAGE_ID={input_language}"
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            temp_cmd.execute(sql_exec)
            temp_data = temp_cmd.fetchall()
            for temp_tuple in temp_data:
                temp_list.append(list(temp_tuple))
        else:
            print('database ' + str(db_file) + ' not found')
    except Exception as ex:
        print('Exception(read_data):' + str(ex))
    finally:
        return temp_list[0][0]


def create_table_user():
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE USER(
                    ID INTEGER PRIMARY KEY,
                    USERNAME       TEXT     NOT NULL UNIQUE,
                    PASSWORD       TEXT     NOT NULL);''')
        print('create_table: user')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_user):' + str(ex))


def add_user(input_name, input_pass):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        sql_exec = f"INSERT INTO USER (USERNAME,PASSWORD) VALUES (\"{input_name}\",\"{input_pass}\")"
        temp_cmd.execute(sql_exec)
        temp_conn.commit()
        temp_conn.close()
        print('add_user: ' + str(input_name))
    except Exception as ex:
        print('Exception(add_user):' + str(ex))


def create_table_issue():
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE ISSUE(
                    ID INTEGER PRIMARY KEY,
                    CVSS           INT     NOT NULL,
                    WEIGHT         INT     NOT NULL,
                    COST           INT     NOT NULL);''')
        print('create_table: issue')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_issue):' + str(ex))


def add_issue(input_cvss, input_weight, input_cost):
    # init
    temp_id = 0
    check_status = True
    try:
        # input check
        input_cvss = int(input_cvss)
        if input_cvss < 0 or input_cvss > 100:
            check_status = False
        input_cost = int(input_cost)
        if input_cost < 0 or input_cost > 100:
            check_status = False
        input_weight = int(input_weight)
        if input_weight < 0 or input_weight > 1000:
            check_status = False
        # sql
        if check_status:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"INSERT INTO ISSUE (CVSS, COST, WEIGHT) " \
                       f"VALUES ({input_cvss},{input_cost},{input_weight})"
            temp_cmd.execute(sql_exec)
            temp_id = temp_cmd.lastrowid
            temp_conn.commit()
            temp_conn.close()
            print('add_issue(id): ' + str(temp_id))
        else:
            print('add_issue: input error')
    except Exception as ex:
        print('Exception(add_issue):' + str(ex))
    finally:
        return temp_id


def update_issue(input_id, input_cvss, input_weight, input_cost):
    # init
    temp_id = 0
    check_status = True
    try:
        # input check
        input_cvss = int(input_cvss)
        if input_cvss < 0 or input_cvss > 100:
            check_status = False
        input_cost = int(input_cost)
        if input_cost < 0 or input_cost > 100:
            check_status = False
        input_weight = int(input_weight)
        if input_weight < 0 or input_weight > 1000:
            check_status = False
        # sql
        if check_status:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"UPDATE ISSUE SET CVSS={input_cvss}, COST={input_cost}, " \
                       f"WEIGHT={input_weight} where ID={input_id}"
            temp_cmd.execute(sql_exec)
            temp_id = 1
            temp_conn.commit()
            temp_conn.close()
            print('update_issue(id): ' + str(input_id))
        else:
            print('update_issue: input error')
    except Exception as ex:
        print('Exception(update_issue):' + str(ex))
    finally:
        return temp_id


def delete_issue(input_id):
    # init
    temp_id = 0
    check_status = True
    try:
        # input check
        input_id = int(input_id)
        if input_id < 0:
            check_status = False
        # sql
        if check_status:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"DELETE FROM ISSUE where ID={input_id};"
            temp_cmd.execute(sql_exec)
            temp_id = 1
            temp_conn.commit()
            temp_conn.close()
            print('remove_issue(id): ' + str(input_id))
    except Exception as ex:
        print('Exception:' + str(ex))
    finally:
        return temp_id


def create_table_language():
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE LANGUAGE(
                    ID INTEGER PRIMARY KEY,
                    NAME TEXT  NOT NULL);''')
        temp_conn.commit()
        temp_conn.close()
        print('create_table: language')
    except Exception as ex:
        print('Exception(create_table_language):' + str(ex))


def add_language(input_language):
    # init
    temp_id = 0
    check_status = True
    try:
        # check length
        input_language = str(input_language)
        if len(input_language) > 64:
            check_status = False
        # sql
        if check_status:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"INSERT INTO LANGUAGE (NAME) " \
                       f"VALUES (\"{input_language}\")"
            temp_cmd.execute(sql_exec)
            temp_id = temp_cmd.lastrowid
            temp_conn.commit()
            temp_conn.close()
            print('add_language: ' + input_language)
        else:
            print('add_language: input error')
    except Exception as ex:
        print('Exception(add_language):' + str(ex))
    finally:
        return temp_id


def create_table_issue_origin():
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE ISSUE_ORIGIN(
                    ID INTEGER PRIMARY KEY,
                    ORIGIN      TEXT    NOT NULL,
                    ISSUE_ID    INT     NOT NULL,
                    FOREIGN KEY (ISSUE_ID) REFERENCES ISSUE(ID));''')
        print('create_table: issue_origin')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_issue_origin):' + str(ex))


def add_issue_origin(input_origin, input_issue_id):
    # init
    temp_id = 0
    check_status = True
    try:
        # check length
        input_origin = str(input_origin)
        if len(input_origin) > 128:
            check_status = False
        input_display = str(input_origin)
        if len(input_display) > 128:
            check_status = False
        # check relational id
        input_issue_id = int(input_issue_id)
        temp_list_issue = read_data('ISSUE')
        temp_id_list = []
        for temp_issue in temp_list_issue:
            temp_id_list.append(temp_issue[0])
        if input_issue_id not in temp_id_list:
            check_status = False
        # run sql
        if check_status:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"INSERT INTO ISSUE_ORIGIN (ORIGIN, ISSUE_ID) " \
                       f"VALUES (\"{input_origin}\",{input_issue_id})"
            temp_cmd.execute(sql_exec)
            temp_id = temp_cmd.lastrowid
            temp_conn.commit()
            temp_conn.close()
            print('add_issue_origin: ' + str(input_origin))
        else:
            print("add_issue_origin: input error")
    except Exception as ex:
        print('Exception(add_issue_origin):' + str(ex))
    finally:
        return temp_id


def check_issue_origin(input_origin):
    # init
    temp_result = False
    try:
        if os.path.isfile(db_file):
            sql_exec = "select ORIGIN from ISSUE_ORIGIN"
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            temp_cmd.execute(sql_exec)
            temp_data = [item[0] for item in temp_cmd.fetchall()]
            if input_origin in temp_data:
                temp_result = True
        else:
            print('database ' + str(db_file) + ' not found')
    except Exception as ex:
        print('Exception(init):' + str(ex))
    finally:
        return temp_result


def create_table_issue_name():
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE ISSUE_NAME(
                    ID INTEGER PRIMARY KEY,
                    ISSUE_ID    INT     NOT NULL,
                    LANGUAGE_ID INT     NOT NULL,
                    DISPLAY     TEXT    NOT NULL,
                    FOREIGN KEY (ISSUE_ID) REFERENCES ISSUE(ID),
                    FOREIGN KEY (LANGUAGE_ID) REFERENCES LANGUAGE(ID));''')
        print('create_table: issue_name')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_issue_name):' + str(ex))


def add_issue_name(input_issue_id, input_lang_id, input_display):
    # init
    temp_id = 0
    check_status = True
    try:
        # check length
        input_display = str(input_display)
        if len(input_display) > 128:
            check_status = False
        # check relational id
        input_issue_id = int(input_issue_id)
        temp_list_issue = read_data('ISSUE')
        temp_id_list = []
        for temp_issue in temp_list_issue:
            temp_id_list.append(temp_issue[0])
        if input_issue_id not in temp_id_list:
            check_status = False
        input_language_id = int(input_lang_id)
        temp_list_language = read_data('LANGUAGE')
        temp_id_list = []
        for temp_language in temp_list_language:
            temp_id_list.append(temp_language[0])
        if input_language_id not in temp_id_list:
            check_status = False
        # run sql
        if check_status:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"INSERT INTO ISSUE_NAME (ISSUE_ID, LANGUAGE_ID, DISPLAY) " \
                       f"VALUES ({input_issue_id},{input_lang_id}, \"{input_display}\")"
            temp_cmd.execute(sql_exec)
            temp_id = temp_cmd.lastrowid
            temp_conn.commit()
            temp_conn.close()
            print('add_issue_name: ' + str(input_display))
        else:
            print("add_issue_name: input error")
    except Exception as ex:
        print('Exception(add_issue_name):' + str(ex))
    finally:
        return temp_id


def update_issue_name(input_issue_id, input_lang_id, input_display):
    # init
    temp_id = 0
    check_status = True
    try:
        # input check
        input_display = str(input_display)
        if len(input_display) > 128:
            check_status = False
        # sql
        if check_status:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"UPDATE ISSUE_NAME SET DISPLAY=\"{input_display}\" " \
                       f"where ISSUE_ID={input_issue_id} and LANGUAGE_ID={input_lang_id}"
            temp_cmd.execute(sql_exec)
            temp_id = 1
            temp_conn.commit()
            temp_conn.close()
            print('update_issue_name(id): ' + str(temp_id))
        else:
            print('update_issue_name: input error')
    except Exception as ex:
        print('Exception(update_issue_name):' + str(ex))
    finally:
        return temp_id


def create_table_issue_description():
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE ISSUE_DESCRIPTION(
                    ID INTEGER PRIMARY KEY,
                    ISSUE_ID           INT     NOT NULL,
                    LANGUAGE_ID        INT     NOT NULL,
                    DISPLAY            TEXT    NOT NULL,
                    FOREIGN KEY (ISSUE_ID) REFERENCES ISSUE(ID),
                    FOREIGN KEY (LANGUAGE_ID) REFERENCES LANGUAGE(ID));''')
        print('create_table: issue_description')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_issue_description):' + str(ex))


def add_issue_description(input_issue_id, input_lang_id, input_display):
    # init
    temp_id = 0
    check_status = True
    try:
        # check ' and "
        input_display = input_display.replace("\'", "`")
        input_display = input_display.replace("\"", "`")
        # check length
        input_display = str(input_display)
        if len(input_display) > 2048:
            check_status = False
        # check relational id
        input_issue_id = int(input_issue_id)
        temp_list_issue = read_data('ISSUE')
        temp_id_list = []
        for temp_issue in temp_list_issue:
            temp_id_list.append(temp_issue[0])
        if input_issue_id not in temp_id_list:
            check_status = False
        input_language_id = int(input_lang_id)
        temp_list_language = read_data('LANGUAGE')
        temp_id_list = []
        for temp_language in temp_list_language:
            temp_id_list.append(temp_language[0])
        if input_language_id not in temp_id_list:
            check_status = False
        # run sql
        if check_status:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"INSERT INTO ISSUE_DESCRIPTION (ISSUE_ID, LANGUAGE_ID, DISPLAY) " \
                       f"VALUES ({input_issue_id},{input_lang_id}, \"{input_display}\")"
            temp_cmd.execute(sql_exec)
            temp_id = temp_cmd.lastrowid
            temp_conn.commit()
            temp_conn.close()
            print('add_issue_description: ' + str(input_display))
        else:
            print("add_issue_description: input error")
    except Exception as ex:
        print('Exception(add_issue_description):' + str(ex))
    finally:
        return temp_id


def update_issue_description(input_issue_id, input_lang_id, input_display):
    # init
    temp_id = 0
    check_status = True
    try:
        # input check
        input_display = str(input_display)
        input_display = input_display.replace("\'", "`")
        input_display = input_display.replace("\"", "`")
        if len(input_display) > 2048:
            check_status = False
        # sql
        if check_status:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"UPDATE ISSUE_DESCRIPTION SET DISPLAY=\"{input_display}\" " \
                       f"where ISSUE_ID={input_issue_id} and LANGUAGE_ID={input_lang_id}"
            temp_cmd.execute(sql_exec)
            temp_id = 1
            temp_conn.commit()
            temp_conn.close()
            print('update_issue_description(id): ' + str(temp_id))
        else:
            print('update_issue_description: input error')
    except Exception as ex:
        print('Exception(update_issue_description):' + str(ex))
    finally:
        return temp_id


def create_table_advice():
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE ADVICE(
                    ID INTEGER PRIMARY KEY,
                    NAME               TEXT    NOT NULL,
                    LANGUAGE_ID        INT     NOT NULL,
                    DISPLAY            TEXT    NOT NULL,
                    FOREIGN KEY (LANGUAGE_ID) REFERENCES LANGUAGE(ID));''')
        print('create_table: advice')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_advice):' + str(ex))


def add_solution(input_name, input_lang_id, input_display):
    # input check
    temp_id = 0
    check_status = True
    try:
        # check ' and "
        input_display = input_display.replace("\'", "`")
        input_display = input_display.replace("\"", "`")
        # check length
        input_name = str(input_name)
        if len(input_name) > 128:
            check_status = False
        input_display = str(input_display)
        if len(input_display) > 2048:
            check_status = False
        # check relational id
        input_language_id = int(input_lang_id)
        temp_list_language = read_data('LANGUAGE')
        temp_id_list = []
        for temp_language in temp_list_language:
            temp_id_list.append(temp_language[0])
        if input_language_id not in temp_id_list:
            check_status = False
        # run sql
        if check_status:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"INSERT INTO ADVICE (NAME, LANGUAGE_ID, DISPLAY) " \
                       f"VALUES (\"{input_name}\", {input_lang_id}, \"{input_display}\")"
            temp_cmd.execute(sql_exec)
            temp_id = temp_cmd.lastrowid
            temp_conn.commit()
            temp_conn.close()
            print('add_advice: ' + str(input_name))
        else:
            print("add_advice: input error")
    except Exception as ex:
        print('Exception(add_advice):' + str(ex))
    finally:
        return temp_id


def update_solution(input_id, input_name, input_lang_id, input_display):
    # input check
    temp_result = 0
    check_status = True
    try:
        # check ' and "
        input_display = input_display.replace("\'", "`")
        input_display = input_display.replace("\"", "`")
        # check length
        input_name = str(input_name)
        if len(input_name) > 128:
            check_status = False
        input_display = str(input_display)
        if len(input_display) > 2048:
            check_status = False
        # check relational id
        input_language_id = int(input_lang_id)
        temp_list_language = read_data('LANGUAGE')
        temp_id_list = []
        for temp_language in temp_list_language:
            temp_id_list.append(temp_language[0])
        if input_language_id not in temp_id_list:
            check_status = False
        # run sql
        if check_status:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"UPDATE ADVICE SET NAME=\"{input_name}\", DISPLAY=\"{input_display}\" where ID={input_id}"
            temp_cmd.execute(sql_exec)
            temp_result = 1
            temp_conn.commit()
            temp_conn.close()
            print('update_advice: ' + str(input_name))
        else:
            print("update_advice: input error")
    except Exception as ex:
        print('Exception(update_advice):' + str(ex))
    finally:
        return temp_result


def delete_solution(input_id):
    # init
    temp_id = 0
    check_status = True
    try:
        # input check
        input_id = int(input_id)
        if input_id < 0:
            check_status = False
        # sql
        if check_status:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"DELETE FROM ADVICE where ID={input_id};"
            temp_cmd.execute(sql_exec)
            temp_id = 1
            temp_conn.commit()
            temp_conn.close()
            print('remove_issue(id): ' + str(input_id))
    except Exception as ex:
        print('Exception:' + str(ex))
    finally:
        return temp_id


def read_data_advice_name(input_id):
    temp_list = []
    try:
        if os.path.isfile(db_file):
            sql_exec = f"select NAME from ADVICE where ID={input_id}"
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            temp_cmd.execute(sql_exec)
            temp_data = temp_cmd.fetchall()
            for temp_tuple in temp_data:
                temp_list.append(list(temp_tuple))
        else:
            print('database ' + str(db_file) + ' not found')
    except Exception as ex:
        print('Exception(read_data_advice_name):' + str(ex))
    finally:
        return temp_list[0][0]


def read_data_advice_display(input_id):
    temp_list = []
    try:
        if os.path.isfile(db_file):
            sql_exec = f"select DISPLAY from ADVICE where ID={input_id}"
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            temp_cmd.execute(sql_exec)
            temp_data = temp_cmd.fetchall()
            for temp_tuple in temp_data:
                temp_list.append(list(temp_tuple))
        else:
            print('database ' + str(db_file) + ' not found')
    except Exception as ex:
        print('Exception(read_data_advice_display):' + str(ex))
    finally:
        return temp_list[0][0]


def create_table_link_advice():
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE LINK_ADVICE(
                    ID INTEGER PRIMARY KEY,
                    ISSUE_ID     INT     NOT NULL,
                    ADVICE_ID    INT     NOT NULL,
                    FOREIGN KEY (ISSUE_ID) REFERENCES ISSUE(ID),
                    FOREIGN KEY (ADVICE_ID) REFERENCES ADVICE(ID));''')
        print('create_table: link_advice')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_link_advice):' + str(ex))


def add_link_advice(input_issue_id, input_advice_id):
    # init
    temp_id = 0
    check_status = True
    try:
        # check relation id
        input_issue_id = int(input_issue_id)
        temp_list_issue = read_data('ISSUE')
        temp_id_list = []
        for temp_issue in temp_list_issue:
            temp_id_list.append(temp_issue[0])
        if input_issue_id not in temp_id_list:
            check_status = False
        input_advice_id = int(input_advice_id)
        temp_list_advice = read_data('ADVICE')
        temp_id_list = []
        for temp_advice in temp_list_advice:
            temp_id_list.append(temp_advice[0])
        if input_advice_id not in temp_id_list:
            check_status = False
        # run sql
        if check_status:
            # sql
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"INSERT INTO LINK_ADVICE (ISSUE_ID, ADVICE_ID) " \
                       f"VALUES ({input_issue_id},{input_advice_id})"
            temp_cmd.execute(sql_exec)
            temp_id = temp_cmd.lastrowid
            temp_conn.commit()
            temp_conn.close()
            print('add_link_advice')
        else:
            print('add_link_advice: input error')
    except Exception as ex:
        print('Exception(add_link_advice):' + str(ex))
    finally:
        return temp_id


def update_link_advice(input_issue_id, input_advice_id):
    # init
    temp_id = 0
    check_status = True
    try:
        # check relation id
        input_issue_id = int(input_issue_id)
        temp_list_issue = read_data('ISSUE')
        temp_id_list = []
        for temp_issue in temp_list_issue:
            temp_id_list.append(temp_issue[0])
        if input_issue_id not in temp_id_list:
            check_status = False
        input_advice_id = int(input_advice_id)
        temp_list_advice = read_data('ADVICE')
        temp_id_list = []
        for temp_advice in temp_list_advice:
            temp_id_list.append(temp_advice[0])
        if input_advice_id not in temp_id_list:
            check_status = False
        # run sql
        if check_status:
            # sql
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"update LINK_ADVICE set ADVICE_ID={input_advice_id} where ID={input_issue_id}"
            temp_cmd.execute(sql_exec)
            temp_id = temp_cmd.lastrowid
            temp_conn.commit()
            temp_conn.close()
            print('add_link_advice')
        else:
            print('add_link_advice: input error')
    except Exception as ex:
        print('Exception(add_link_advice):' + str(ex))
    finally:
        return temp_id


def create_table_type():
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE TYPE(
                    ID INTEGER PRIMARY KEY,
                    NAME     INT     NOT NULL,
                    WEIGHT   INT     NOT NULL)''')
        print('create_table: type')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_type):' + str(ex))


def add_type(input_name, input_weight):
    # init
    temp_id = 0
    check_status = True
    try:
        # check duplicate
        temp_list = read_data('TYPE')
        for temp_data in temp_list:
            if input_name == temp_data[1]:
                temp_id = temp_data[0]
                return temp_id
        # check lengths
        input_name = str(input_name)
        if len(input_name) > 128:
            check_status = False
        # check range
        input_weight = int(input_weight)
        if not 0 <= input_weight <= 1000:
            check_status = False
        # run sql
        if check_status:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"INSERT INTO TYPE(NAME, WEIGHT) " \
                       f"VALUES (\"{input_name}\", {input_weight})"
            temp_cmd.execute(sql_exec)
            temp_id = temp_cmd.lastrowid
            temp_conn.commit()
            temp_conn.close()
            print('add_type: ' + str(input_name))
        else:
            print("add_type: input error")
    except Exception as ex:
        print('Exception(add_type):' + str(ex))
    finally:
        return temp_id


def read_type(input_id):
    try:
        temp_list = []
        try:
            if os.path.isfile(db_file):
                sql_exec = f"select * from TYPE where ISSUE_ID={input_id}"
                temp_conn = sqlite3.connect(db_file)
                temp_cmd = temp_conn.cursor()
                temp_cmd.execute(sql_exec)
                temp_data = temp_cmd.fetchall()
                for temp_tuple in temp_data:
                    temp_list.append(list(temp_tuple))
            else:
                print('database ' + str(db_file) + ' not found')
        except Exception as ex:
            print('Exception(read_type):' + str(ex))
        finally:
            return temp_list[0]
    except Exception as ex:
        print('Exception:' + str(ex))


def create_table_link_type():
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE LINK_TYPE(
                    ID           INTEGER PRIMARY KEY,
                    ISSUE_ID     INT     NOT NULL,
                    TYPE_ID      INT     NOT NULL,
                    FOREIGN KEY (ISSUE_ID) REFERENCES ISSUE(ID),
                    FOREIGN KEY (TYPE_ID) REFERENCES TYPE(ID));''')
        print('create_table: link_type')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_link_type):' + str(ex))


def add_link_type(input_issue_id, input_type_id):
    # init
    temp_id = 0
    check_status = True
    try:
        # check relation id
        input_issue_id = int(input_issue_id)
        temp_list_issue = read_data('ISSUE')
        temp_id_list = []
        for temp_issue in temp_list_issue:
            temp_id_list.append(temp_issue[0])
        if input_issue_id not in temp_id_list:
            check_status = False
        input_type_id = int(input_type_id)
        temp_list_type = read_data('TYPE')
        temp_id_list = []
        for temp_type in temp_list_type:
            temp_id_list.append(temp_type[0])
        if input_type_id not in temp_id_list:
            check_status = False
        # run sql
        if check_status:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"INSERT INTO LINK_TYPE (ISSUE_ID, TYPE_ID) " \
                       f"VALUES ({input_issue_id},{input_type_id})"
            temp_cmd.execute(sql_exec)
            temp_id = temp_cmd.lastrowid
            temp_conn.commit()
            temp_conn.close()
            print('add_link_type')
        else:
            print("add_link_type: input error")
    except Exception as ex:
        print('Exception(add_link_type):' + str(ex))
    finally:
        return temp_id


def read_link_advice(input_id):
    # init
    temp_id_list = []
    try:
        if os.path.isfile(db_file):
            sql_exec = f"select ID from LINK_ADVICE where ISSUE_ID={input_id}"
            temp_list = []
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            temp_cmd.execute(sql_exec)
            temp_data = temp_cmd.fetchall()
            for temp_tuple in temp_data:
                temp_list.append(list(temp_tuple))
            temp_id_list = temp_list[0]
        else:
            print('database ' + str(db_file) + ' not found')
    except Exception as ex:
        print('Exception(init):' + str(ex))
    finally:
        return temp_id_list


def create_table_reference():
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE REFERENCE(
                    ID INTEGER PRIMARY KEY,
                    NAME           TEXT    NOT NULL,
                    DISPLAY_NAME   INT     NOT NULL,
                    DISPLAY_LINK   INT     NOT NULL);''')
        print('create_table: reference')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))


def add_reference(input_name, input_title, input_url):
    # init
    temp_id = 0
    check_status = True

    try:
        # check length
        input_name = str(input_name)
        if len(input_name) > 128:
            check_status = False
        input_title = str(input_title)
        if len(input_title) > 128:
            check_status = False
        input_url = str(input_url)
        if len(input_url) > 512:
            check_status = False
        # run sql
        if not check_status:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"INSERT INTO REFERENCE(NAME, DISPLAY_NAME, DISPLAY_LINK) " \
                       f"VALUES (\"{input_name}\", \"{input_title}\", \"{input_url}\")"
            temp_cmd.execute(sql_exec)
            temp_id = temp_cmd.lastrowid
            temp_conn.commit()
            temp_conn.close()
            print('add_reference: ' + str(input_name))
        else:
            print("add_reference: input error")
    except Exception as ex:
        print('Exception(add_reference):' + str(ex))
    finally:
        return temp_id


def create_table_link_reference():
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE LINK_REFERENCE(
                    ID INTEGER PRIMARY KEY,
                    ISSUE_ID     INT     NOT NULL,
                    REFERENCE_ID INT     NOT NULL,
                    FOREIGN KEY (ISSUE_ID) REFERENCES ISSUE(ID),
                    FOREIGN KEY (REFERENCE_ID) REFERENCES REFERENCE(ID)
                    );''')
        print('create_table: link_reference')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_link_reference):' + str(ex))


def add_link_reference(input_issue_id, input_reference_id):
    # init
    temp_id = 0
    check_status = True
    try:
        # check relation id
        input_issue_id = int(input_issue_id)
        temp_list_issue = read_data('ISSUE')
        temp_id_list = []
        for temp_issue in temp_list_issue:
            temp_id_list.append(temp_issue[0])
        if input_issue_id not in temp_id_list:
            check_status = False
        input_reference_id = int(input_reference_id)
        temp_list_reference = read_data('TYPE')
        temp_id_list = []
        for temp_type in temp_list_reference:
            temp_id_list.append(temp_type[0])
        if input_reference_id not in temp_id_list:
            check_status = False
        # run sql
        if check_status:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"INSERT INTO LINK_TYPE (ISSUE_ID, TYPE_ID) " \
                       f"VALUES ({input_issue_id},{input_reference_id})"
            temp_cmd.execute(sql_exec)
            temp_id = temp_cmd.lastrowid
            temp_conn.commit()
            temp_conn.close()
            print('add_link_reference')
        else:
            print("add_link_reference: input error")
    except Exception as ex:
        print('Exception(add_link_reference):' + str(ex))
    finally:
        return temp_id


def update_status(input_status_name, input_status_value):
    # init
    check_status = True
    try:
        # input check
        input_display = str(input_status_name)
        if len(input_display) > 128:
            check_status = False
        if int(input_status_value) > 100:
            check_status = False
        if int(input_status_value) < 0:
            check_status = False
        # sql
        if check_status:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"UPDATE STATUS SET value=\"{input_status_value}\" " \
                       f"where type=\"{input_status_name}\""
            temp_cmd.execute(sql_exec)
            temp_conn.commit()
            temp_conn.close()
        else:
            print('update_status: input error')
    except Exception as ex:
        print('Exception(update_status):' + str(ex))
        check_status = False
    finally:
        return check_status


def create_table_status():
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE STATUS(
                    ID INTEGER PRIMARY KEY,
                    TYPE          TEXT    NOT NULL,
                    VALUE         INT     NOT NULL);''')
        print('create_table: issue')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_issue):' + str(ex))



def parser_eas():
    try:
        add_language('en-US')
        add_language('zh-TW')
        nmp = utils.custom_csv.read_file_to_dict("ithome.csv")
        for n in nmp:
            temp_score = 0
            if n['風險'] == 'H':
                temp_score = 75
            elif n['風險'] == 'M':
                temp_score = 50
            elif n['風險'] == 'L':
                temp_score = 25

            temp_cost = 0
            if n['修復難易度'] == 'H':
                temp_cost = 25
            elif n['修復難易度'] == 'M':
                temp_cost = 9
            elif n['修復難易度'] == 'L':
                temp_cost = 1
            if check_issue_origin(n['key']):
                continue
            temp_issue_id = add_issue(temp_score, 100, temp_cost)
            if temp_issue_id == 0:
                continue
            add_issue_origin(n['key'], temp_issue_id)
            add_issue_name(temp_issue_id, 1, n['細項(L3) EN'])
            add_issue_name(temp_issue_id, 2, n['細項(L3)'])
            add_issue_description(temp_issue_id, 1, n['詳細情況 EN'])
            add_issue_description(temp_issue_id, 2, n['詳細情況'])
            temp_advice_id = add_solution(n['細項(L3)'] + '(英文問題修復建議)', 1, n['修復 EN'])
            add_link_advice(temp_issue_id, temp_advice_id)
            temp_advice_id = add_solution(n['細項(L3)'] + '(中文問題修復建議)', 2, n['修復'])
            add_link_advice(temp_issue_id, temp_advice_id)

            temp_type_id = add_type(n['次類別(L2)'], 100)
            add_link_type(temp_issue_id, temp_type_id)

            temp_type_id = add_type(n['主類別(L1)'], 100)
            add_link_type(temp_issue_id, temp_type_id)

            if not n['ISO'] == '':
                temp_iso_list = n['ISO'].split('\n')
                for temp_iso in temp_iso_list:
                    if not temp_iso == '':
                        temp_type_id = add_type(temp_iso, 100)
                        add_link_type(temp_issue_id, temp_type_id)

            if not n['GDPR'] == '':
                temp_gdpr_list = n['GDPR'].split('\n')
                for temp_gdpr in temp_gdpr_list:
                    if not temp_gdpr == '':
                        temp_type_id = add_type(temp_gdpr, 100)
                        add_link_type(temp_issue_id, temp_type_id)

            if not n['PCI DSS'] == '':
                temp_pci_list = n['PCI DSS'].split('\n')
                for temp_pci in temp_pci_list:
                    if not temp_pci == '':
                        temp_type_id = add_type(temp_pci, 100)
                        add_link_type(temp_issue_id, temp_type_id)

            if not n['NIST CSF'] == '':
                temp_nist_list = n['PCI DSS'].split('\n')
                for temp_nist in temp_nist_list:
                    if not temp_nist == '':
                        temp_type_id = add_type(temp_nist, 100)
                        add_link_type(temp_issue_id, temp_type_id)

    except Exception as ex:
        print('Exception(init_db):' + str(ex))


def parser_vas():
    try:
        add_language(db_file, 'en-US')
        add_language(db_file, 'zh-TW')
        nmp = utils.custom_csv.read_file_to_dict("zap_report.csv")
        # id,type,origin,enabled,risk,cost,name_en,name_zh,desc_en,desc_zh,advice_en,advice_zh
        for n in nmp:
            temp_score = 0
            if n['risk'] == 'High':
                temp_score = 75
            elif n['risk'] == 'Medium':
                temp_score = 50
            elif n['risk'] == 'Low':
                temp_score = 25
            temp_cost = 0
            if n['cost'] == 'High':
                temp_cost = 25
            elif n['cost'] == 'Medium':
                temp_cost = 9
            elif n['cost'] == 'Low':
                temp_cost = 1
            temp_issue_id = add_issue(n['origin'], temp_score, temp_cost)
            if temp_issue_id == 0:
                continue
            add_issue_name(db_file, n['name_en'], temp_issue_id, 1, n['name_en'])
            add_issue_name(db_file, n['name_zh'], temp_issue_id, 2, n['name_zh'])
            add_issue_description(temp_issue_id, 1, n['desc_en'])
            add_issue_description(temp_issue_id, 2, n['desc_zh'])
            temp_advice_id = add_solution(db_file, n['name_en'] + '(英文問題修復建議)', 1, n['advice_en'])
            add_link_advice(db_file, temp_issue_id, temp_advice_id)
            temp_advice_id = add_solution(db_file, n['name_zh'] + '(中文問題修復建議)', 2, n['advice_zh'])
            add_link_advice(db_file, temp_issue_id, temp_advice_id)
            temp_type_id = add_type('OWASP 2021:' + n['type'], 100)
            add_link_type(temp_issue_id, temp_type_id)
    except Exception as ex:
        print('Exception(init_db):' + str(ex))


def parser_zap():
    list_alert = utils.custom_request.read_alert()
    for temp_alert in list_alert:
        if check_issue_origin(temp_alert[0]):
            continue

        temp_score = 0
        if temp_alert[3] == 'High':
            temp_score = 75
        elif temp_alert[3] == 'Medium':
            temp_score = 50
        elif temp_alert[3] == 'Low':
            temp_score = 25

        temp_issue_id = add_issue(temp_alert[0], temp_score, 0)
        add_issue_name(db_file, temp_alert[0], temp_issue_id, 1, temp_alert[0])
        add_issue_name(db_file, temp_alert[0], temp_issue_id, 2, temp_alert[0])
        add_issue_description(temp_issue_id, 1, temp_alert[1])
        add_issue_description(temp_issue_id, 2, temp_alert[1])
        temp_advice_id = add_solution(db_file, temp_alert[0] + '(英文問題修復建議)', 1, temp_alert[2])
        add_link_advice(db_file, temp_issue_id, temp_advice_id)
        temp_advice_id = add_solution(db_file, temp_alert[0] + '(中文問題修復建議)', 2, temp_alert[2])
        add_link_advice(db_file, temp_issue_id, temp_advice_id)
        for temp_type in temp_alert[4]:
            temp_type_id = add_type(temp_type, 100)
            add_link_type(temp_issue_id, temp_type_id)


def unit_test():
    add_user('user', 'passwd')
    add_issue('unitest origin', 50, 8)
    add_language('zh-tw')
    add_issue_name('test issue name', 1, 1, 'test issue name')
    add_issue_description(1, 1, 'test description')
    add_solution('test advice name', 1, 'test advice')
    add_link_advice(1, 1)
    add_type('test type name', 50)
    add_link_type(1, 1)
    add_reference('test name', 'test title', 'test url')
    add_link_reference(1, 1)


if __name__ == "__main__":
    # update_status('gpt_update', 1)
    create_table_status()
    # init()
    # unit_test()
    # parser_vas('test.db')
    # parser_eas()
    # print(check_issue_origin('Directory Browsing'))
