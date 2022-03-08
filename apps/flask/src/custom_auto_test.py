import upload.test_sql11 as sql11

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium import webdriver

test = sql11.TestSql11()

test.driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
test.test_sql11()
print(test.driver.page_source)
test.teardown_method('test')


# test_class.teardown_method('test')

