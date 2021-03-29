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
    def geturl(self,username,psword,lang='CN'):
        try:
            common.open_web('https://at-client-portal-uat.atfxdev.com/login')
            #去除弹窗
            self.remove_topup()
            time.sleep(1)
            #页面语言
            self.choose_cplanguage(lang)
            #新开窗口访问bos登录页
            common.js_openwindows('https://at-bos-frontend-uat.atfxdev.com/login')
            time.sleep(1)
            common.switch_windows(1)
            #选择页面语言
            self.commethod.choose_bos_lang(lang)
            #登录bos
            self.commethod.loginbos(username,psword)
            time.sleep(1)
            #进入客户名单页面
            commom.display_click('css,.ivu-badge')
            time.sleep(1)
            commom.display_click('css,.ivu-menu-item',1)
        except Exception as msg:
            pub_method.log_output('!!--!!geturl').error(msg)

    #去除登录页弹窗
    def remove_topup(self):
        try:
            self.commethod.remove_register_topup()
        except Exception as msg:
            pub_method.log_output('!!--!!remove_topup').error(msg)

    #选择会员中心页面语言
    def choose_cplanguage(self,lang):
        try:
            self.commethod.choose_register_lang(lang)
        except Exception as msg:
            pub_method.log_output('!!--!!choose_cplanguage').error(msg)




    