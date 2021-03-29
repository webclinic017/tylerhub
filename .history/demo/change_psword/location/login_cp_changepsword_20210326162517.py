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

    #访问url
    def geturl(self):
        try:
            common.open_web('https://at-client-portal-uat.atfxdev.com/login')
            #去除弹窗
            self.remove_topup()
            time.sleep(1)
            #页面语言
            self.choose_language()
        except Exception as msg:
            pub_method.log_output('!!--!!geturl').error(msg)

    #去除登录页弹窗
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

    #登录会员中心
    def logincp(self,username,psword):
        try:
            self.commethod.login_cp(username,psword)

    