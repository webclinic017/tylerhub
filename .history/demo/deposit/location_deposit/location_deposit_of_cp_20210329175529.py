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

class locations_of_deposit():

    def broswertype(self,broswername='Chrome'):
        self.driver=common.open_browser(broswername)
        self.commethod=commonmethod(self.driver)


    def deposit(self,username,psword):
        #登录会员中心
        self.commethod.login_cp(username,psword)
        #点击入金
        time.sleep(1)
        common.display_click('css,.side-nav-cell',2)
        #判断该账号是否可以入金
        time.sleep(1)
        for i in ['该账户暂时无法入金，请联系我们的客户服务','Deposit is not allow in this account, please contact our customer service']:
            if common.ele_is_displayed('xpath,//div[.="{}"]'.format(i)):
                print('该账号无入金权限')
            else:
                pass


    #判断该账号入金权限是否开启
    def _can_deposit(self):
        try:
            common
