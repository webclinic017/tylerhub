'''
Author: tyler
Date: 2021-05-28 17:29:27
LastEditTime: 2021-05-28 18:12:29
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \tylerhub\demo\E-wallet_deposit\location_ewallet\location_deposti_of_ewallet.py
'''
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


class Ewallet_deposti():

    def broswertype(self,broswername='Chrome'):
        self.driver=common.open_browser(broswername)
        self.commethod=commonmethod(self.driver)

    def get_url(self,lang='CN'):
        try:
            common.open_web('https://at-bos-frontend-uat.atfxdev.com/login')
            time.sleep(1)
            #bos页面语言
            self.commethod.choose_bos_lang(lang)
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!get_url').error(msg)

    #登录bos
    def login_bos(self,username,psword):
        try:
            self.commethod.loginbos(username, psword)
        except Exception as msg:
            pub_method.log_output('!!--!!login_bos').error(msg)

    #查询电子钱包出金方式在会员中心是否开启
    def is_ewallet_open(self):
        
