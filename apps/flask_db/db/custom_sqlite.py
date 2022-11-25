import sqlite3
import os
import utils.custom_csv


def init(db_file):
    try:
        if os.path.isfile(db_file):
            print('database ' + str(db_file) + ' already exist')
            os.remove(db_file)
        create_table_user(db_file)
        create_table_language(db_file)
        create_table_issue(db_file)
        create_table_issue_name(db_file)
        create_table_issue_description(db_file)
        create_table_issue_advice(db_file)
        create_table_link_advice(db_file)
        create_table_issue_reference(db_file)
        create_table_link_reference(db_file)
        create_table_issue_type(db_file)
        create_table_link_type(db_file)
        init_db(db_file)

        """
        create_table_list(db_file)
        create_table_type(db_file, "LEVEL_1")
        create_table_type(db_file, "LEVEL_2")
        create_table_type(db_file, "LEVEL_3")
        create_table_type(db_file, "REFERENCE")
        create_table_type(db_file, "ISO")
        create_table_type(db_file, "GDPR")
        create_table_type(db_file, "PCI_DSS")
        create_table_type(db_file, "NIST_CSF")
        create_table_type(db_file, "PDPA")
        init_db(db_file)
        """
    except Exception as ex:
        print('Exception(init):' + str(ex))


def create_table_user(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE USER(
                    ID       INT             PRIMARY KEY,
                    USERNAME VARCHAR(64)     NOT NULL UNIQUE,
                    PASSWORD VARCHAR(64)     NOT NULL);''')
        print('create_table: user')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_user):' + str(ex))


def create_table_language(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE LANGUAGE(
                    ID INTEGER PRIMARY KEY,
                    NAME VARCHAR(64)  NOT NULL);''')
        temp_conn.commit()
        temp_conn.close()
        print('create_table: language')
    except Exception as ex:
        print('Exception(create_table_language):' + str(ex))


def create_table_issue(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE ISSUE(
                    ID             INT          PRIMARY KEY,
                    ORIGIN         VARCHAR(512) NOT NULL UNIQUE,
                    CVSS           INT          NOT NULL,
                    WEIGHT         INT          NOT NULL,
                    RECOVERY_COST  INT          NOT NULL);''')
        print('create_table: issue')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_issue):' + str(ex))


def create_table_issue_name(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE ISSUE_NAME(
                    ID          INT     PRIMARY KEY,
                    NAME        VARCHAR(128)    NOT NULL UNIQUE,
                    ISSUE_ID    INT     NOT NULL,
                    LANGUAGE_ID INT     NOT NULL,
                    DISPLAY     INT     NOT NULL);''')
        print('create_table: issue_name')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_issue_name):' + str(ex))


def create_table_issue_description(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE ISSUE_DESCRIPTION(
                    ID          INT     PRIMARY KEY,
                    NAME        VARCHAR(128)    NOT NULL,
                    ISSUE_ID    INT     NOT NULL,
                    LANGUAGE_ID INT     NOT NULL,
                    DISPLAY     VARCHAR(512)    NOT NULL);''')
        print('create_table: issue_description')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_issue_description):' + str(ex))


def create_table_issue_advice(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE ISSUE_ADVICE(
                    ID          INT          PRIMARY KEY,
                    NAME        VARCHAR(128) NOT NULL,
                    LANGUAGE_ID INT          NOT NULL,
                    DISPLAY     VARCHAR(512)    NOT NULL);''')
        print('create_table: issue_advice')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_issue_advice):' + str(ex))


def create_table_link_advice(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE LINK_ADVICE(
                    ID        INT PRIMARY KEY,
                    ISSUE_ID  INT NOT NULL,
                    ADVICE_ID INT NOT NULL);''')
        print('create_table: link_advice')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_link_advice):' + str(ex))


def create_table_issue_reference(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE ISSUE_REFERENCE(
                    ID INTEGER PRIMARY KEY,
                    NAME          INT NOT NULL,
                    DISPLAY_TITLE INT NOT NULL,
                    DISPLAY_URL   INT NOT NULL);''')
        print('create_table: reference')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))


def create_table_link_reference(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE LINK_REFERENCE(
                    ID           INT PRIMARY KEY,
                    ISSUE_ID     INT NOT NULL,
                    REFERENCE_ID INT NOT NULL);''')
        print('create_table: link_reference')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_link_reference):' + str(ex))


def create_table_issue_type(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE ISSUE_REFERENCE(
                    ID     INT PRIMARY KEY,
                    NAME   INT NOT NULL,
                    WEIGHT INT NOT NULL);''')
        print('create_table: issue_type')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception:(create_table_issue_type)' + str(ex))


def create_table_link_type(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE ISSUE_TYPE(
                    ID       INT PRIMARY KEY,
                    ISSUE_ID INT NOT NULL,
                    TYPE_ID  INT NOT NULL);''')
        print('create_table: link_type')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(create_table_link_type):' + str(ex))


def add_issue_name(db_file, input_name, input_id_issue, input_id_language):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute(f"INSERT INTO ISSUE_NAME (NAME,ISSUE_ID,LANGUAGE_ID) "
                         f"VALUES(\'{input_name}\', {input_id_issue},{input_id_language})")
        print('create_table: reference_link')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))


def read_issue_name():
    pass


"""
def create_table_user(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE USER(
                    ID INTEGER PRIMARY KEY,
                    NAME           VARCHAR(512)    NOT NULL,
                    PASS           VARCHAR(512)    NOT NULL);''')
        print('create_table: user')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))
"""

"""
def create_table_list(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE TYPE(
                        ID     INTEGER PRIMARY KEY,
                        NAME   VARCHAR(512)    NOT NULL);''')
        print('create_table: type')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))
"""

"""
def create_table_list(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE TYPE(
                        ID     INTEGER PRIMARY KEY,
                        NAME   VARCHAR(512)    NOT NULL);''')
        print('create_table: type')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))
"""

"""
def create_table_type(db_file, type_name):
    try:
        temp_name = type_name.upper()
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE ''' + temp_name + '''(
                    ID INTEGER PRIMARY KEY,
                    NAME           VARCHAR(512)    NOT NULL,
                    VALUE          VARCHAR(512)    NOT NULL,
                    WEIGHT         VARCHAR(512)    NOT NULL);''')
        temp_conn.commit()
        temp_cmd.execute('''CREATE TABLE ISSUE_''' + temp_name + '''(
                            ID INTEGER PRIMARY KEY,
                            ISSUE_ID           INT    NOT NULL,
                            TYPE_ID       INT    NOT NULL);''')
        temp_conn.commit()
        temp_cmd.execute("INSERT INTO TYPE (NAME) VALUES(\'" + temp_name + "\')")
        temp_conn.commit()
        temp_conn.close()
        print('create_table: ' + temp_name)
    except Exception as ex:
        print('Exception(create_table_type):' + str(ex))
"""

"""
# id, origin, score, weight, cost, name_en, name_zh, desc_en, desc_zh, advice_en, advice_zh
def create_table_issue(db_file):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute('''CREATE TABLE ISSUE(
                    ID INTEGER PRIMARY KEY,
                    ORIGIN         VARCHAR(512)    NOT NULL,
                    CVSS           INT     NOT NULL,
                    WEIGHT         INT     NOT NULL,
                    COST           INT     NOT NULL,
                    NAME_EN        VARCHAR(512)    NOT NULL,
                    NAME_ZH        VARCHAR(512)    NOT NULL,
                    DESCRIPTION_EN VARCHAR(512)    NOT NULL,
                    DESCRIPTION_ZH VARCHAR(512)    NOT NULL,
                    ADVICE_EN      VARCHAR(512)    NOT NULL,
                    ADVICE_ZH      VARCHAR(512)    NOT NULL);''')
        print('create_table: issue')
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))
"""


def add_issue(db_file,
              origin,
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
        desc_en = desc_en.replace("\'", "`")
        desc_en = desc_en.replace("\"", "`")
        desc_zh = desc_zh.replace("\'", "`")
        desc_zh = desc_zh.replace("\"", "`")
        advice_en = advice_en.replace("\'", "`")
        advice_en = advice_en.replace("\"", "`")
        advice_zh = advice_zh.replace("\'", "`")
        advice_zh = advice_zh.replace("\"", "`")
        sql_exec = f"INSERT INTO ISSUE (ORIGIN,CVSS,WEIGHT,COST," \
                   f"NAME_EN,NAME_ZH,DESCRIPTION_EN,DESCRIPTION_ZH,ADVICE_EN,ADVICE_ZH) VALUES (" \
                   f"\"{origin}\"," \
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
        temp_conn.commit()

        sql_exec = f"INSERT INTO ISSUE_NAME (ORIGIN,CVSS,WEIGHT,COST," \
                   f"NAME_EN,NAME_ZH,DESCRIPTION_EN,DESCRIPTION_ZH,ADVICE_EN,ADVICE_ZH) VALUES (" \
                   f"\"{origin}\"," \
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
        temp_conn.commit()

        print('add_issue:  ' + str(origin))
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(add_issue):' + str(ex))


def init_db(db_file):
    try:
        add_user(db_file, 'cymetrics', 'aA@123456')
        try:
            add_user(db_file, 'cymetrics', 'aA@123456')
            nmp = utils.custom_csv.read_file_to_dict("ithome.csv")
            count = 1
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
                    temp_cost = 24
                elif n['修復難易度'] == 'M':
                    temp_cost = 8
                elif n['修復難易度'] == 'L':
                    temp_cost = 1

                # add_issue(db_file, n['key'], temp_score, '100', temp_cost,
                #           n['細項(L3) EN'], n['細項(L3)'], n['詳細情況 EN'], n['詳細情況'], n['修復 EN'], n['修復'])

                count += 1

        except Exception as ex:
            print('Exception(init_db):' + str(ex))

    except Exception as ex:
        print('Exception(init_db):' + str(ex))


"""
def init_db(db_file):
    import utils.custom_csv
    try:
        add_user(db_file, 'cymetrics', 'aA@123456')
        nmp = utils.custom_csv.read_file_to_dict("ithome.csv")
        count = 1
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

            add_issue(db_file, n['key'], temp_score, '100', temp_cost,
                      n['細項(L3) EN'], n['細項(L3)'], n['詳細情況 EN'], n['詳細情況'], n['修復 EN'], n['修復'])

            if not n['ISO'] == '':
                temp_iso_list = n['ISO'].split('\n')
                for temp_iso in temp_iso_list:
                    if not temp_iso == '':
                        add_type(db_file, 'ISO', temp_iso, '', 100)
                        add_issue_link(db_file, 'ISO', count, read_type_by_name(db_file, 'ISO', temp_iso))

            if not n['GDPR'] == '':
                temp_gdpr_list = n['GDPR'].split('\n')
                for temp_gdpr in temp_gdpr_list:
                    if not temp_gdpr == '':
                        add_type(db_file, 'GDPR', temp_gdpr, '', 100)
                        add_issue_link(db_file, 'GDPR', count, read_type_by_name(db_file, 'GDPR', temp_gdpr))

            count += 1

    except Exception as ex:
        print('Exception(init_db):' + str(ex))
"""


# id, issue_id, tag
def add_user(db_file, input_name, input_pass):
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


"""
def add_issue(db_file,
              origin,
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
        desc_en = desc_en.replace("\'", "`")
        desc_en = desc_en.replace("\"", "`")
        desc_zh = desc_zh.replace("\'", "`")
        desc_zh = desc_zh.replace("\"", "`")
        advice_en = advice_en.replace("\'", "`")
        advice_en = advice_en.replace("\"", "`")
        advice_zh = advice_zh.replace("\'", "`")
        advice_zh = advice_zh.replace("\"", "`")
        sql_exec = f"INSERT INTO ISSUE (ORIGIN,CVSS,WEIGHT,COST," \
                   f"NAME_EN,NAME_ZH,DESCRIPTION_EN,DESCRIPTION_ZH,ADVICE_EN,ADVICE_ZH) VALUES (" \
                   f"\"{origin}\"," \
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
        print('add_issue:  ' + str(origin))
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception(add_issue):' + str(ex))
"""

"""
def update_issue(db_file,
                 origin,
                 score,
                 weight,
                 cost,
                 name_en,
                 name_zh,
                 desc_en,
                 desc_zh,
                 advice_en,
                 advice_zh,
                 issue_id):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        sql_exec = f"UPDATE ISSUE SET " \
                   f"ORIGIN=\"{origin}\"," \
                   f"CVSS=\"{score}\"," \
                   f"WEIGHT=\"{weight}\"," \
                   f"COST=\"{cost}\"," \
                   f"NAME_EN=\"{name_en}\"," \
                   f"NAME_ZH=\"{name_zh}\"," \
                   f"DESCRIPTION_EN=\"{desc_en}\"," \
                   f"DESCRIPTION_ZH=\"{desc_zh}\"," \
                   f"ADVICE_EN=\"{advice_en}\"," \
                   f"ADVICE_ZH=\"{advice_zh}\" " \
                   f"where ID={issue_id};"
        temp_cmd.execute(sql_exec)
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))
"""

"""
def delete_issue(db_file, input_id):
    try:
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        sql_exec = f"DELETE FROM ISSUE where ID={input_id};"
        temp_cmd.execute(sql_exec)
        temp_conn.commit()
        temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))
"""

"""
def add_type(db_file, input_type, input_name, input_value, input_weight):
    try:
        # check
        temp_exist = False
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        sql_exec = f"select NAME from {input_type}"
        temp_cmd.execute(sql_exec)
        temp_data = [i[0] for i in temp_cmd.fetchall()]
        if input_name in temp_data:
            temp_exist = True
        if input_name == '':
            temp_exist = True
        # add
        if not temp_exist:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"INSERT INTO {input_type}(NAME,VALUE,WEIGHT) " \
                       f"VALUES (\'{input_name}\',\'{input_value}\',{input_weight})"
            temp_cmd.execute(sql_exec)
            temp_conn.commit()
            temp_conn.close()
            print('add_type:' + input_name)
    except Exception as ex:
        print('Exception(add_type):' + str(ex))
"""

"""
def read_type_by_name(db_file, input_type, input_name):
    try:
        if os.path.isfile(db_file):
            sql = f"select ID from {input_type} where NAME=\'{input_name}\'"
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            temp_cmd.execute(sql)
            temp_data = [i[0] for i in temp_cmd.fetchall()]
        else:
            print('database ' + str(db_file) + ' not found')
    except Exception as ex:
        print('Exception:' + str(ex))
    return temp_data[0]
"""

"""
def add_issue_link(db_file, input_type, input_issue_id, input_type_id):
    try:
        # check
        temp_exist = False
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        sql_exec = f"select * from ISSUE_{input_type}"
        temp_cmd.execute(sql_exec)
        temp_result = temp_cmd.fetchall()
        temp_data_issue = [i[0] for i in temp_result]
        temp_data_type = [i[1] for i in temp_result]
        if len(temp_data_issue) > 0:
            for i in range(0, len(temp_data_issue)):
                if temp_data_issue[i] == input_issue_id and temp_data_type[i] == input_type_id:
                    temp_exist = True
        # add
        if not temp_exist:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            sql_exec = f"INSERT INTO ISSUE_{input_type}(ISSUE_ID, TYPE_ID) " \
                       f"VALUES (\'{input_issue_id}\',\'{input_type_id}\')"
            temp_cmd.execute(sql_exec)
            temp_conn.commit()
            temp_conn.close()
            print('add_issue_link:' + input_type)
    except Exception as ex:
        print('Exception(add_issue_link):' + str(ex))
"""

"""
def read_issue_by_id(db_file, input_id):
    temp_data = []
    try:
        if os.path.isfile(db_file):
            sql = f"select ORIGIN, CVSS, WEIGHT, COST," \
                  f" NAME_ZH, NAME_EN, DESCRIPTION_ZH, DESCRIPTION_EN, ADVICE_ZH, ADVICE_EN" \
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
"""

"""
def read_list_by_id(db_file, input_id):
    temp_data = []
    try:
        if os.path.isfile(db_file):
            sql = f"select NAME from TYPE where ID=" + str(input_id) + ";"
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            temp_cmd.execute(sql)
            temp_data = [i[0] for i in temp_cmd.fetchall()]
        else:
            print('database ' + str(db_file) + ' not found')
    except Exception as ex:
        print('Exception:' + str(ex))
    return temp_data[0]
"""

"""
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
"""

"""
def read_data_issues(db_file):
    temp_data = ''
    if os.path.isfile(db_file):
        sql = "select * from ISSUE"
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute(sql)
        temp_data = temp_cmd.fetchall()
    else:
        print('database ' + str(db_file) + ' not found')
    return temp_data
"""


def read_data_users(db_file):
    temp_data = ''
    if os.path.isfile(db_file):
        sql = "select USERNAME,PASSWORD from USER"
        temp_conn = sqlite3.connect(db_file)
        temp_cmd = temp_conn.cursor()
        temp_cmd.execute(sql)
        temp_data = temp_cmd.fetchall()
    else:
        print('database ' + str(db_file) + ' not found')
    return temp_data


if __name__ == "__main__":
    init('test.db')
    # add_type('test.db', 'ISO', 'test name', 'test value', 100)
    # print('id: ' + str(read_type_by_name('test.db', 'ISO', 'test name')))
    # add_issue_link('test.db', 'ISO', 1, read_type_by_name('test.db', 'ISO', 'test name'))
    # add_user('test.db', 'u1', 'passwd')
    # add_testcase('test.db', 't1', 'test', 'test2.py', '1')
    # read_fields('test.db', 'TESTCASE')
    # read_testcase_id('test.db', 't1')
    # update_status_by_id('test.db', '1', 'test2')
    # read_data('test.db', 'ISSUE')
    # add_mission('test.db', "http://www.example.com", "Demo 公司 2", "入口網站")
    # read_data_mission('test.db')
    # read_issue_by_id('test.db', 5)
