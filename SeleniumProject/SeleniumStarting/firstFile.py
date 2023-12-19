from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
browserName = "chrome"
if browserName == "chrome":
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("http://www.google.com")
driver.find_element(By.NAME, "q").send_keys("selenium webdriver")
queryList = driver.find_elements(By.CSS_SELECTOR, "ul.erkvQe li span")
print(len(queryList))
for q in queryList:
    print(q.text)
time.sleep(10)
#driver.quit()

