from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def test_google_homepage():
    # create a new Chrome session
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-running-insecure-content")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(30)
    driver.maximize_window()

    # navigate to the application home page
    driver.get("https://www.google.com")

    # get the search textbox
    search_field = driver.find_element(By.NAME,"q")
    search_field.clear()

    # enter search keyword and submit
    search_field.send_keys("Selenium WebDriver")
    search_field.submit()

    # get the list of elements which are displayed after the search
    # currently on result page using find_elements_by_class_name method
    lists = driver.find_elements(By.CLASS_NAME,"r")

    # check the page title
    assert driver.title == "Selenium WebDriver - Google Search"

    driver.quit()

test_google_homepage()