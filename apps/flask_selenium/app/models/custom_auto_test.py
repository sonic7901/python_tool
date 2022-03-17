from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium import webdriver


def select_test(input_id):
    temp_result = ""
    try:
        pass
        # auto testcase start
        if input_id == '1':
            import app.upload.test_resetdb
            test = app.upload.test_resetdb.TestResetdb()
            test.driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
            test.test_resetdb()
            temp_result = test.driver.page_source
            test.teardown_method('test')
            print("testcase:" + "1")
        if input_id == '2':
            import app.upload.test_resetdb
            test = app.upload.test_resetdb.TestResetdb()
            test.driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
            test.test_resetdb()
            temp_result = test.driver.page_source
            test.teardown_method('test')
            print("testcase:" + "2")
        if input_id == '3':
            import app.upload.test_resetdb
            test = app.upload.test_resetdb.TestResetdb()
            test.driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
            test.test_resetdb()
            temp_result = test.driver.page_source
            test.teardown_method('test')
            print("testcase:" + "3")
        # auto testcase end
    except Exception as ex:
        print('Exception:' + str(ex))
    # auto testcase start
    return temp_result


# print(select_test('9'))
"""
def test_start():
    test = sql11.TestSql11()
    test.driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    test.test_sql11()
    test.teardown_method('test')
"""

