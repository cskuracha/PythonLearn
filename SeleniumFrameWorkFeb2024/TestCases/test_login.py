import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pageObjects.loginPage import LoginPage
from utilities.readProperties import ReadConfig

class Test_001_Login:
    # baseURL = "https://admin-demo.nopcommerce.com/"
    # username = "admin@yourstore.com"
    # password = "admin"
    baseURL = ReadConfig.getApplicationUrl()
    username = ReadConfig.getUserEmail()
    password = ReadConfig.getUserPassword()

    def test_login(self, setup):
        self.driver = setup
        self.driver.get(self.baseURL)
        self.lp = LoginPage(self.driver)
        self.lp.setusername(self.username)
        self.lp.setpassword(self.password)
        self.lp.clicklogin()
        act_title = self.driver.title
        if act_title == "Dashboard / nopCommerce administration":
            assert True
        else:
            self.driver.save_screenshot(".\\Screenshots\\" + "test_loginTitle.png")
            self.driver.close()
            assert False