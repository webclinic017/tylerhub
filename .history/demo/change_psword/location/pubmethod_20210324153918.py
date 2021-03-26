import time
from selenium import webdriver


comw=Commonweb()

class pubfang():
    
    def __init__(self,driver):
        self.driver=driver

    def login_topup(self):
        self.driver.find_element_by_css_selector('div.rem-pwd-box>a').click()

