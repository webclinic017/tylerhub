'''
Author: tyler
Date: 2021-05-28 17:29:27
LastEditTime: 2021-05-31 11:48:55
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

    def get_url(self,username,psword,lang='CN'):
        try:
            common.open_web('https://at-bos-frontend-uat.atfxdev.com/login')
            time.sleep(1)
            #bos页面语言
            self.commethod.choose_bos_lang(lang)
            time.sleep(1)
            self.login_bos(username, psword)
            time.sleep(2)
            #资金管理
            common.display_click('xpath,//div[@class="scroll-content"]//span[.="资金管理"]')
            time.sleep(1)
            #支付渠道管理
            common.display_click('xpath,//div[@class="scroll-content"]//span[.="支付渠道管理"]')
        except Exception as msg:
            pub_method.log_output('!!--!!get_url').error(msg)

    #登录bos
    def login_bos(self,username,psword):
        try:
            self.commethod.loginbos(username, psword)
        except Exception as msg:
            pub_method.log_output('!!--!!login_bos').error(msg)

    #判断支付渠道页面是否处于加载状态
    def is_page_loading(self):
        try:
            while True:
                if common.ele_is_displayed('css,.spin-icon-load',2):
                    continue
                else:
                    break
        except Exception as msg:
            pub_method.log_output('!!--!!is_page_loading').error(msg)


    #获取电子钱包入金在渠道支付列表中的位置
    def where_is_pay(self,payment_type):
        try:
            for i in range(1,89):
                #获取
                self.paytext=common.display_get_text('xpath,//*[@id="app"]/div/div/div[4]/div/'
                'div[2]/div/span/div[{}]/ul/li[2]/div[1]'.format(i))
                if self.paytext==payment_type:
                    return i
                    break
        except Exception as msg:
            pub_method.log_output('!!--!!where_is_pay').error(msg)


    #查询电子钱包出金方式在会员中心是否开启
    def is_ewallet_open(self,payment_type):
        try:
            self.pay_num=self.where_is_pay(payment_type)
            time.sleep(1)
            self.payopen_text=common.display_get_text('xpath,//*[@id="app"]/div/div/div[4]/div/'
            'div[2]/div/span/div[{}]/ul/li[2]/div[2]/span/span/span'.format(self.pay_num))
            time.sleep(1)
            if self.payopen_text=='关闭':
                common.display_click('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/div/'
                'span/div[{}]/ul/li[2]/div[2]/span/span/span'.format(self.pay_num))
                print('开启支付渠道：{}'.format(payment_type))
            else:
                print('{}已开启'.format(payment_type))
        except Exception as msg:
            pub_method.log_output('!!--!!is_ewallet_open').error(msg)


        
