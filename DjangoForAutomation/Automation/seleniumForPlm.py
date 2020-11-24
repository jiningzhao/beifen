from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chrome_option = webdriver.ChromeOptions()
chrome_option.add_argument('--start-maximized')
chrome_option.add_argument('--incognito')
chrome_option.add_argument('--blink-settings=imagesEnabled=false')
chrome_option.add_experimental_option('useAutomationExtension', False)
chrome_option.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(options=chrome_option)

driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)

assert "No results found." not in driver.page_source
driver.close()
