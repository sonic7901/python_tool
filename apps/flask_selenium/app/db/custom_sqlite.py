import sqlite3
import os


def init(db_file):
    try:
        if os.path.isfile(db_file):
            print('database ' + str(db_file) + ' already exist')
        else:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            temp_cmd.execute('''CREATE TABLE USER(
            ID INT PRIMARY KEY     NOT NULL,
            NAME           TEXT    NOT NULL,
            PASS           TEXT    NOT NULL);''')
            print('database ' + str(db_file) + ' already created')
            temp_conn.commit()
            temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))


def add_user(db_file, input_name, input_pass):
    try:
        if os.path.isfile(db_file):
            init(db_file)
        else:
            temp_conn = sqlite3.connect(db_file)
            temp_cmd = temp_conn.cursor()
            temp_cmd.execute('''CREATE TABLE USER(
            ID INT PRIMARY KEY     NOT NULL,
            NAME           TEXT    NOT NULL,
            PASS           TEXT    NOT NULL);''')
            print('database ' + str(db_file) + ' already created')
            temp_conn.commit()
            temp_conn.close()
    except Exception as ex:
        print('Exception:' + str(ex))

def test():
    conn = sqlite3.connect('test.db')

    c = conn.cursor()

    print("数据库打开成功")

    c.execute('''CREATE TABLE COMPANY
           (ID INT PRIMARY KEY     NOT NULL,
           NAME           TEXT    NOT NULL,
           AGE            INT     NOT NULL,
           ADDRESS        CHAR(50),
           SALARY         REAL);''')

    print("数据表创建成功")

    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (1, 'Paul', 32, 'California', 20000.00 )")

    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")

    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")

    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")

    conn.commit()

    print("数据插入成功")

    conn.close()


if __name__ == "__main__":
    init('test.db')
