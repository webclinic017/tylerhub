import os
import random
import sys
import time
import datetime
path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=path_demo+r'\public'
sys.path.append(path_public)
from about_data import exceldata
from browser_actions import Commonweb
from common_method import commonmethod
from other_actions import public_method

common=Commonweb()
pub_method=public_method()
e=exceldata()


class location_deposit_bos():

    def broswertype(self,broswername='Chrome'):
        self.driver=common.open_browser(broswername)
        self.commethod=commonmethod(self.driver)

    def get_url(self,lang='CN'):
        try:
            common.open_web('https://at-bos-frontend-uat.atfxdev.com/login')
            self.commethod.choose_bos_lang(lang)
        except Exception as msg:
            pub_method.log_output('!!--!!get_url').error(msg)

    #登录bos并进入客户名单页
    def login_bos(self,username,psword):
        try:
            common.switch_windows(0)
            time.sleep(1)
            self.commethod.loginbos(username,psword)
            time.sleep(1)
            #客户管理
            common.display_click('css,.ivu-badge>span')
            #客户名单
            common.display_click('css,[data-old-padding-top] > [href="/client/clientListNew/:type*"]')
        except Exception as msg:
            pub_method.log_output('!!--!!login_bos').error(msg)

    