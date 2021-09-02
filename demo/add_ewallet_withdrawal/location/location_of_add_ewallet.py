'''
Author: tyler
Date: 2021-09-02 10:17:39
LastEditTime: 2021-09-02 11:25:54
LastEditors: Please set LastEditors
Description: Related operations such as page positioning
FilePath: \tylerhub\demo\add_ewallet_withdrawal\location\location_of_add_ewallet.py
'''
import os
import sys
import time

path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=path_demo+r'\public'
path_public=os.path.join(path_demo,'public')
sys.path.append(path_public)
from about_data import Aboutdata
from browser_actions import Commonweb
from common_method import Commonmethod
from handle_database import Dadabase_operate
from handlelog import MyLog
from randomdata import Random_data
from read_dataconfig import ReadConfig

class Location_of_add_ewallet(object):
    """
    cl账号开通模拟账号页面定位等操作
    """

    global dealData,common,dataBase,log,randomData,conFig

    dealData=Aboutdata()
    common=Commonweb()
    dataBase=Dadabase_operate()
    log=MyLog()
    randomData=Random_data()
    conFig=ReadConfig()

    #赋值对象driver
    def broswertype(self,broswername=conFig.get_value('browser', 'default')):
        self.driver=common.open_browser(broswername)
        self.commeThod=Commonmethod(self.driver)

    #登录页
    def get_url(self,environment,lang='CN'):
        try:
            common.open_web(conFig.get_value('cp_login', '{}'.format(environment)))
            #去除登录页弹窗
            self.remove_login_topup()
            #选择页面语音，默认简中
            self.commeThod.choose_register_lang(lang)
            #新开窗口访问
            common.js_openwindows(conFig.get_value('bos_login', '{}'.format(environment)))
            time.sleep(1)
            common.switch_windows(1)
            #选择bos页面语言,默认简中
            self.commeThod.choose_bos_lang(lang)
        except Exception as msg:
            log.my_logger('!!--!!get_url').error(msg)


    #登录页弹窗
    def remove_login_topup(self):
        try:
            common.switch_windows(0)
            time.sleep(1)
            self.commeThod.remove_register_topup()
        except Exception as msg:
            log.my_logger('!!--!!remove_login_topup').error(msg)

    #登录cp
    def logincp(self,username,password):
        try:
            common.switch_windows(0)
            time.sleep(1)
            self.commeThod.login_cp(username, password)
        except Exception as msg:
            log.my_logger('!!--!!logincp').error(msg)

    #登出cp
    def logoutcp(self):
        try:
            common.switch_windows(0)
            time.sleep(1)
            self.commeThod.logout_cp()
        except Exception as msg:
            log.my_logger('!!--!!logoutcp').error(msg)


    #登录bos
    def login_bos(self,username,password):
        try:
            common.switch_windows(1)
            time.sleep(1)
            self.commeThod.loginbos(username, password)
            time.sleep(2)
            #客户管理
            common.display_click('css,[width="200"] li .ivu-icon-ios-arrow-down')
            time.sleep(1)
            #客户名单
            common.display_click('xpath,//div[@class="scroll-content"]//a[.="客户名单"]')
            time.sleep(1)
        except Exception as msg:
            log.my_logger('!!--!!login_bos').error(msg)

   #进入账号详情页
    def details_page(self,account):
        try:
            common.switch_windows(1)
            time.sleep(1)
            self.commeThod.enter_details_page(account)
        except Exception as msg:
            log.my_logger('!!--!!details_page').error(msg)


    #获取该账号居住国家
    def get_live_country(self):
        try:
            common.switch_windows(2)
            time.sleep(3)
            #基本资料
            common.display_click("xpath,//a[.='基本资料']")
            time.sleep(1)
            #获取该账号居住国家
            self.liveCountry=common.display_get_text("xpath,//div[@class='page']//div[7]//span")
            print('该账号居住国家为{}'.format(self.liveCountry))
            time.sleep(1)
            if self.liveCountry=='中国':
                return True
            else:
                return False
        except Exception as msg:
            log.my_logger('!!--!!details_page').error(msg)


























































































    def closebrowser(self):
        common.close_browser()

    def quitbrowser(self):
        common.quit_browser()















