import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pageObjects.loginPage import LoginPage

class Test_001_Login:
    baseURL = "https://admin-demo.nopcommerce.com/"
    username = "admin@yourstore.com"
    password = "admin"

    def test_login(self, setup):
        self.driver = setup
        self.driver.get(self.baseURL)
        self.lp = LoginPage(self.driver)
        self.lp.setusername(self.username)
        self.lp.setpassword(self.password)
        self.lp.clicklogin()
        act_title = self.driver.title
        if act_title == "Dashboard / poCommerce administration":
            assert True
        else:
            self.driver.save_screenshot(".\\Screenshots\\" + "test_loginTitle.png")
            self.driver.close()
            assert False