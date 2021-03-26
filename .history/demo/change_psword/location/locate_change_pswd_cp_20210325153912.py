import sys
import os
import time
path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=path_demo+r'\public'
sys.path.append(path_public)
from browser_actions import Commonweb
from other_actions import public_method
from about_data import exceldata
from verification_code import time_used
from common_method import commonmethod

commom=Commonweb()


class locat():
    global driver

    def broswertype(self,broswername='Chrome'):
        self.driver=comweb.open_browser(broswername)
        self.commethod=commonmethod(self.driver)
    
    #访问cp注册页和登录bos
    def geturl(self,username,psword,lang='CN'):
        #cp
        commom.open_web('https://at-client-portal-uat.atfxdev.com/login')
        #去除弹窗
        self.remove_topup()
        #选择页面语言
        self.commethod.choose_register_lang(lang)
        #js打开新窗口
        commom.js_openwindows('https://at-bos-frontend-uat.atfxdev.com/login')
        time.sleep(1)
        commom.switch_windows(1)
        #页面语言，默认为简中
        self.commethod.choose_bos_lang(lang)
        time.sleep(1)
        #登录bos
        self.commethod.loginbos(username,psword)
        time.sleep(1)
        #进入客户名单页面
        commom.display_click('css,.ivu-badge')
        time.sleep(1)
        commom.display_click('css,.ivu-menu-item',1)

        


    #去除登录页弹窗
    def remove_topup(self):
        self.commethod.remove_register_topup()


    def clik(self):
        comweb.display_click('css,.blk-sure-btn')
        #点击忘记密码
        self.fan.login_topup()
        time.sleep(6)

