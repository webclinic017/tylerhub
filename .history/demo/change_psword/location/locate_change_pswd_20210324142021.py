import sys
import os
import time
from pubmethod import pubfang
path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=path_demo+r'\public'
sys.path.append(path_public)
from browser_actions import Commonweb
from other_actions import public_method
from about_data import exceldata
from verification_code import time_used

comweb=Commonweb()
fan=pubfang()

class locat():

    def broswertype(self,broswername='Chrome'):
        self.driver=comweb.open_browser(broswername)
    
    def geturl(self):
        comweb.open_web('https://at-client-portal-uat.atfxdev.com/login')


    def clik(self):
        #去除弹窗
        fan.login_topup()
        #点击忘记密码
        comweb.display_click('css,div.rem-pwd-box>a')