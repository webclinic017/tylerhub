'''
Author: tyler
Date: 2021-05-28 17:29:27
LastEditTime: 2022-06-07 11:47:55
LastEditors: Tyler96-QA 1718459369@qq.com
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
from verification_code import use_time
from read_dataconfig import ReadConfig
from handlelog import MyLog

class Ewallet_deposti():

    global common,randomData,conFig,log

    common=Commonweb()
    randomData=Random_data()
    conFig=ReadConfig()
    log=MyLog()

    #赋值对象driver
    def broswertype(self,browsername=conFig.get_value('browser', 'default')):
        self.driver=common.open_browser(browsername)
        self.comMethod=Commonmethod()

    #登录页
    def get_url(self,environment,username,password,lang='CN'):
        try:
            common.open_web(conFig.get_value('bos_login', '{}'.format(environment)))
            #选择bos页面语言,默认简中
            time.sleep(1)
            self.comMethod.choose_bos_lang(common,lang)
            #登录bos
            self.comMethod.loginbos(common,username, password)
            #资金管理
            common.display_click('xpath,//div[@class="scroll-content"]//span[.="资金管理"]')
            time.sleep(1)
            #支付渠道管理
            common.display_click('xpath,//div[@class="scroll-content"]//span[.="支付渠道管理"]')
            time.sleep(1)
            while True:
                if common.ele_is_displayed('css,.spin-icon-load',2):
                    continue
                else:
                    break

        except Exception as msg:
            log.my_logger('!!--!!get_url').error(msg)


    #获取电子钱包入金在渠道支付列表中的位置
    def where_is_pay(self,payment_type):
        try:
            self.payment_num=common.get_lenofelement('css,.list-group div .second > div:nth-of-type(1)')
            time.sleep(1)
            for i in range(1,self.payment_num+1):
                self.payText=common.display_get_text('xpath,//*[@id="app"]/div/div/div[4]/div/'
                'div[2]/div/span/div[{}]/ul/li[2]/div[1]'.format(i))
                if self.payText==payment_type:
                    return i
                    break
        except Exception as msg:
            log.my_logger('!!--!!where_is_pay').error(msg)


    #查询电子钱包出金方式在会员中心是否开启
    def is_ewallet_open(self,payment_type):
        try:
            self.pay_num=self.where_is_pay(payment_type)
            time.sleep(1)
            print('{}支付渠道位于列表中第{}个'.format(payment_type,self.pay_num))
            self.payopen_num=common.get_attributes('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/div/span/div[{}]/ul/li[3]/div/span/input'.format(self.pay_num), 'value')
            time.sleep(0.5)
            if self.payopen_num !='1':
                common.display_click('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/div/span/div[{}]/ul/li[3]/div/span'.format(self.pay_num))
                time.sleep(1)
                common.js_scroll('top')
                #保存
                common.display_click('css,.ivu-btn-success > span')
                time.sleep(1)
                #确定
                common.display_click('css,.toastButton')
                print('开启支付渠道：{}'.format(payment_type))
            else:
                print('{} 已开启'.format(payment_type))
        except Exception as msg:
            log.my_logger('!!--!!is_ewallet_open').error(msg)

    
    #判断所有的电子钱包入金方式是否开启
    @use_time
    def is_all_ewallet_open(self,environment):
        try:
            self.payment_type_list=conFig.get_valueList('ewalletType','type')
            for i in self.payment_type_list:
                self.is_ewallet_open(i)
                while True:
                    if common.ele_is_displayed('css,.spin-icon-load', 1):
                        continue
                    else:
                        break
                time.sleep(1)
        except Exception as msg:
            log.my_logger('!!--!!is_all_ewallet_open').error(msg)
        finally:
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
            common.js_openwindows(conFig.get_value('bos_LiveExchangeRate',environment))
            time.sleep(1)
            #打开入金管理页面
            common.js_openwindows(conFig.get_value('bos_DepositList', environment))


    #bos登录cp进入入金页面
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
            common.switch_windows(3)
            time.sleep(1)
            #判断页面是否加载完成
            while True:
                if common.ele_is_displayed("css,[src='/static/img/loading.webm']",1):
                    continue
                else:
                    break
            time.sleep(1)
            while True:
                self.loading_attributes=common.get_attributes('css,.el-loading-mask', 'style')
                if 'none' in self.loading_attributes:
                    break
                else:
                    continue
            #入金
            common.display_click('xpath,//ul[2]//span[.="入金"]')
            time.sleep(1)
            while True:
                self.arrtuibe=common.get_attributes('css,.el-loading-mask', 'style')
                if 'none' not in self.arrtuibe:
                    continue
                else:
                    break
        except Exception as msg:
            log.my_logger('!!--!!bos_to_cp').error(msg)

    
    #判断电子钱包出金方式有几种
    def have_several_ewallet(self):
        try:
            self.ewallet_len=common.get_lenofelement('xpath,//*[contains(text(),"电子钱包")]/../../div[2]/div/div')
            print('当前账号电子钱包出金方式有{}种'.format(self.ewallet_len))
            
        except Exception as msg:
            log.my_logger('!!--!!is_all_ewallet_open').error(msg)



            

