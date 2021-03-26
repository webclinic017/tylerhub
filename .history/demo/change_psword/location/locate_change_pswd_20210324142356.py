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
    global driver

    def broswertype(self,broswername='Chrome'):
        self.driver=comweb.open_browser(broswername)
    
    def geturl(self):
        comweb.open_web('https://at-client-portal-uat.atfxdev.com/login')


    def clik(self):
        comweb.display_click('css,.blk-sure-btn')
        #点击忘记密码
        fan.login_topup()