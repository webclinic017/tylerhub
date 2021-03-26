import sys
import os
import time
from selenium import webdriver
# path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# path_public=path_demo+r'\public'
# sys.path.append(path_public)
# from browser_actions import Commonweb
# from other_actions import public_method
# from about_data import exceldata
# from verification_code import time_used



class pubfang():
    
    def __init__(self,driver):
        self.driver=driver

    def login_topup(self):
        self.driver.find_element_by_css_selector('div.rem-pwd-box>a')

