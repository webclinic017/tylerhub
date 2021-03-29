import os
import random
import sys
import time

path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=path_demo+r'\public'
sys.path.append(path_public)
from about_data import exceldata
from browser_actions import Commonweb
from common_method import commonmethod
from other_actions import public_method

common=Commonweb()
pub_method=public_method()


class location():
    global driver

    #赋值对象driver
    def broswertype(self,broswername='Chrome'):
        self.driver=commom.open_browser(broswername)
        self.commethod=commonmethod(self.driver)

    #登录会员中心
    def login_cp(self,username,psword):

    #去除页面弹窗
    def remove_topup(self):
        try:
            self.commethod.remove_register_topup()
        except Exception as msg:
            pub_method.log_output('!!--!!remove_topup').error(msg)



    #选择会员中心页面语言
    def choose_language(self,lang='CN'):
        try:
            self.commethod.choose_register_lang(lang)
        except Exception as msg:
            pub_method.log_output('!!--!!choose_language').error(msg)

    