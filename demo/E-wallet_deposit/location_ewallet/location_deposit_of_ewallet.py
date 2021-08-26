'''
Author: tyler
Date: 2021-05-28 17:29:27
LastEditTime: 2021-08-04 22:03:21
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
from about_data import Aboutdata
from browser_actions import Commonweb
from common_method import Commonmethod
from randomdata import Random_data
from verification_code import time_used

common=Commonweb()
randomData=Random_data()


class Ewallet_deposti():

    def broswertype(self,broswername='Chrome'):
        self.driver=common.open_browser(broswername)
        self.commethod=Commonmethod(self.driver)

    def get_url(self,url,username,psword,lang='CN'):
        try:
            common.open_web(url)
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
            log.my_logger('!!--!!get_url').error(msg)

    #登录bos
    def login_bos(self,username,psword):
        try:
            self.commethod.loginbos(username, psword)
        except Exception as msg:
            log.my_logger('!!--!!login_bos').error(msg)

    #bos登录cp
    def bos_to_cp(self,account):
        try:
            common.switch_windows(0)
            time.sleep(1)
            common.web_clear('css,[placeholder]')
            time.sleep(1)
            common.web_input('css,[placeholder]',account)
            #登录
            common.display_click('xpath,//span[.="登录"]')
            time.sleep(1)
        except Exception as msg:
            log.my_logger('!!--!!bos_to_cp').error(msg)

    #判断支付渠道页面是否处于加载状态
    def is_page_loading(self):
        try:
            while True:
                if common.ele_is_displayed('css,.spin-icon-load',2):
                    continue
                else:
                    break
        except Exception as msg:
            log.my_logger('!!--!!is_page_loading').error(msg)


    #获取电子钱包入金在渠道支付列表中的位置
    def where_is_pay(self,payment_type):
        try:
            self.payment_num=common.get_lenofelement('css,.list-group div .second > div:nth-of-type(1)')
            time.sleep(1)
            for i in range(1,self.payment_num+1):
                self.paytext=common.display_get_text('xpath,//*[@id="app"]/div/div/div[4]/div/'
                'div[2]/div/span/div[{}]/ul/li[2]/div[1]'.format(i))
                if self.paytext==payment_type:
                    return i
                    break
        except Exception as msg:
            log.my_logger('!!--!!where_is_pay').error(msg)


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
                time.sleep(1)
                common.display_click('css,.pull-right > span')
                time.sleep(1)
                print('开启支付渠道：{}'.format(payment_type))
            else:
                print('{} 已开启'.format(payment_type))
        except Exception as msg:
            log.my_logger('!!--!!is_ewallet_open').error(msg)

    #判断所有的电子钱包入金方式是否开启
    @time_used('统计所有电子钱包入金渠道是否开启耗时')
    def is_all_ewallet_open(self):
        try:
            self.payment_type_list=['Neteller','渠道輪巡組','dusupay','RPN P2P','thunderx KHR','Expay QRCode','Skrill','Qubepay2',
            'Cardpay Uganda','Payment Asia','wintechTHB','PapayaTHB']
            for i in self.payment_type_list:
                self.is_ewallet_open(i)
                time.sleep(1)
        except Exception as msg:
            log.my_logger('!!--!!is_all_ewallet_open').error(msg)
        finally:
            #再次点击保存
            common.display_click('css,.pull-right')
            time.sleep(1)
            common.display_click('xpath,//div[@class="scroll-content"]//span[.="客户管理"]') #客户管理
            time.sleep(1)
            common.display_click('xpath,//li[@class="ivu-menu-submenu ivu-menu-opened"]//span[.="登录会员中心"]')
            time.sleep(1)
            #语言
            common.display_click('css,.ivu-form div i',-1)
            time.sleep(1)
            common.display_click('xpath,//li[.="简体中文"]',-1)
            time.sleep(1)
            #打开即时汇率页面
            common.js_openwindows('https://at-bos-frontend-uat.atfxdev.com/management/instantRate')
            time.sleep(1)
            #打开入金管理页面
            common.js_openwindows('https://at-bos-frontend-uat.atfxdev.com/management/depositList')


    #入金页面loading处理
    def is_deposit_loading(self):
        try:
            common.switch_windows(3)
            time.sleep(4)
            #登录后页面loading
            while True:
                self.login_attribute=common.get_attributes('xpath,//div[@class="el-loading-mask"]','style')
                if 'display' not in self.login_attribute:
                    continue
                else:
                    break
            time.sleep(1)
            #入金
            common.display_click('xpath,//ul[2]//span[.="入金"]')
            time.sleep(2)
            while True:
                self.arrtuibe=common.get_attributes('css,.el-loading-mask', 'style')
                if 'display' not in self.arrtuibe:
                    continue
                else:
                    break
        except Exception as msg:
            log.my_logger('!!--!!is_deposit_loading').error(msg)


    #判断电子钱包出金方式有几种
    def have_several_ewallet(self):
        try:
            self.ewallet_len=common.get_lenofelement('xpath,//*[contains(text(),"电子钱包")]/../../div[2]/div/div')
            print('当前账号电子钱包出金方式有{}种'.format(self.ewallet_len))
            
        except Exception as msg:
            log.my_logger('!!--!!is_all_ewallet_open').error(msg)



            

