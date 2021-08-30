'''
Author: tyler
Date: 2021-08-26 18:21:05
LastEditTime: 2021-08-30 12:03:35
LastEditors: Please set LastEditors
Description: Related operations such as page positioning
FilePath: \tylerhub\demo\cl_open_demoaccount\location\location_of_cl_opendome.py
'''
import os
import sys
import time
import random
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



class Location_of_opendemo(object):
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

    #cp登录页
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

    #登录bos
    def login_bos(self,username,password):
        try:
            common.switch_windows(1)
            time.sleep(1)
            self.commeThod.loginbos(username, password)
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


    #开通模拟账号
    def creat_demoaccount(self):
        time.sleep(1)
        try:
            while True:
                self.attribute=common.get_attributes('xpath,//div[@class="el-loading-mask"]','style')
                if 'display' not in self.attribute:
                    continue
                else:
                    break
            #点击模拟账号
            common.display_click('css,.el-tabs__item',1)
            time.sleep(1)
            #开立模拟账号
            common.display_click('css,.weak-apply-account-btn')
            time.sleep(1)
            #随机选择投资金额
            common.display_click('css,.el-input__inner',2)
            time.sleep(1)
            common.display_click('css,[x-placement="top-start"] li',random.randint(0, 5))
            time.sleep(1)
            #输入随机密码
            self.passWord=randomData.get_psword_type(8)
            common.display_input('css,.el-input__inner', self.passWord,-1)
            time.sleep(1)
            #点击下一步
            common.display_click('css,.el-button > span')
        except Exception as msg:
            log.my_logger('!!--!!creat_demoaccount').error(msg)

    #获取dmo账号
    def get_demoaccount(self,account:int):
        try:
            #获取创建成功后文本
            time.sleep(1)
            self.successText=common.display_get_text('css,.title')
            if '创建完成' in self.successText:
                #查询数据库获取最新创建的demo账号
                self.serchData=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'), 'atfxgm-sit', 'atfx_trade_account',
                {"accountNumber":account},'tradeAccount',N=1)
                self.demoAccount=int(self.serchData[0]['tradeAccount'])
                return self.demoAccount
                print('demo账号创建成功：{}'.format(self.demoAccount))
            else:
                common.get_screenpict('creat_demo_failed')
                print('创建失败,截图保持在项目目录picture下')
        except Exception as msg:
            log.my_logger('!!--!!get_demoaccount').error(msg)
        

    #获取demo账号组别
    def get_demo_group(self):
        try:
            common.switch_windows(2)
            time.sleep(1)
            #模拟账号信息
            common.display_click('css,[href="#demoAccount"]')
            time.sleep(1)
            #刷新
            common.display_click("xpath,//div[@id='demoAccount']//span[.='刷新']")
            time.sleep(1)
            #查看新开模拟账号信息
            common.display_click("xpath,//div[@id='demoAccount']//div[@class='ivu-table-fixed-right']//tr[@class='ivu-table-row']//a[contains(.,'查看')]")
            time.sleep(1)
            #获取组别
            self.demoGroup=str(common.get_text("xpath,//div[@class='ivu-drawer-wrap']//span",2))
            return self.demoGroup
        except Exception as msg:
            log.my_logger('!!--!!get_demo_group').error(msg)

    #获取demo账号杠杆
    def get_demo_lever(self):
        try:
            #获取杠杆
            self.demoLever=int(common.display_get_text("xpath,//div[@class='ivu-drawer-wrap']//span",6))
            return self.demoLever
        except Exception as msg:
            log.my_logger('!!--!!get_demo_lever').error(msg)
    
    #获取demo账号点差类型
    def get_demo_spreadtype(self):
        try:
            #获取点差类型
            self.demoSpread=str(common.display_get_text("xpath,//div[@class='ivu-drawer-wrap']//span",7))
            return self.demoSpread
        except Exception as msg:
            log.my_logger('!!--!!get_demo_spreadtype').error(msg)

    #获取demo账号加点
    def get_demo_markup(self):
        try:
            #获取加点
            self.demoBit=int(common.display_get_text("xpath,//div[@class='ivu-drawer-wrap']//span",8))
            return self.demoBit
            self.closebrowser()
        except Exception as msg:
            log.my_logger('!!--!!get_demo_markup').error(msg)

    #bos获取demo账号信息
    def get_demo_info(self):
        #调用方法，变量赋值
        self.get_demo_group()
        self.get_demo_lever()
        self.get_demo_spreadtype()
        self.get_demo_markup()

    #查询数据库，获取新开demo账号组别
    def search_mongodb_demoinfo(self,account):
        try:
            #查询数据库
            self.serchDemodata=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'), 'atfxgm-sit', 'atfx_trade_account',
            {"$and": [{"accountNumber": account}, {"tradeAccount": "{}".format(self.demoAccount)}]},'group','leverage','spreadType','markup',N=1)
            return self.serchDemodata
        except Exception as msg:
            log.my_logger('!!--!!search_mongodb_demoinfo').error(msg)





















    #关闭当前页
    def closebrowser(self):
        common.close_browser()
    
    #退出浏览器进程
    def quitbrowser(self):
        common.quit_browser()