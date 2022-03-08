from selenium import webdriver

driver=webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('http://mail.sina.com.cn/')
