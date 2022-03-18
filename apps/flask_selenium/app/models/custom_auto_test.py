from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium import webdriver


def select_test(input_id):
    temp_result = ""
    try:
        pass
        # auto testcase start
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

