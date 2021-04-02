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

class locations_of_deposit():

    def broswertype(self,broswername='Chrome'):
        self.driver=common.open_browser(broswername)
        self.commethod=commonmethod(self.driver)

    def logincp(self,username,psword):
        common.open_web('https://at-client-portal-uat.atfxdev.com/login')
        time.sleep(1)
        #去除弹窗
        self.commethod.remove_register_topup()
        time.sleep(1)
        #登录
        self.commethod.login_cp(username,psword)



    def deposit(self,username,psword):
        self.logincp(username,psword)
        #点击入金
        time.sleep(1)
        common.display_click('css,.side-nav-cell',2)
        #判断该账号是否可以入金
        time.sleep(1)
        star=datetime.datetime.now()
        if common.ele_is_displayed('xpath,//div[.="{}"]'.format('该账户暂时无法入金，请联系我们的客户服务'),2):
            print('该账号无入金权限')
        else:
            print(55555)
        # for i in ['该账户暂时无法入金，请联系我们的客户服务','Deposit is not allow in this account, please contact our customer service']:
        #     if common.ele_is_displayed('xpath,//div[.="{}"]'.format(i),2):
        #         print('该账号无入金权限')
        #     else:
        #         pass
        print(datetime.datetime.now()-star)

if __name__=='__main__':
    de=locations_of_deposit()
    de.broswertype()
    de.deposit('10000000027@uitest.com','Tl123456')
    
