'''
Author: tyler
Date: 2021-08-26 18:21:05
LastEditTime: 2022-05-25 11:42:44
LastEditors: Tyler96-QA 1718459369@qq.com
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
from handle_database import Database_operate
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
    dataBase=Database_operate()
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
            time.sleep(1)
            #判断页面是否加载完成
            while True:
                if common.ele_is_displayed('css,.ivu-spin-dot', 1):
                    continue
                else:
                    break
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


    #开通模拟账号
    def creat_demoaccount(self):
        time.sleep(1)
        try:
            #判断页面是否加载完成
            while True:
                if common.ele_is_displayed("css,[src='/static/img/loading.webm']", 1):
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
            #点击模拟账号
            common.display_click('css,#tab-demo')
            time.sleep(1)
            while True:
                self.demoLoading=common.get_attributes('css,.el-loading-mask','style')
                if 'none' in self.demoLoading:
                    break
                else:
                    continue
            #开立模拟账号
            common.display_click('xpath,//span[text()="开立模拟交易账号"]')
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
            time.sleep(1)
            while True:
                if common.ele_is_displayed('css,.circular', 1):
                    continue
                else:
                    break
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
                print('demo账号创建成功：{}'.format(self.demoAccount))
                
                #返回首页，demo账号列表
                common.display_click("xpath,//span[.='首页']")
                time.sleep(1)
                while True:
                    self.demoLoading=common.get_attributes('css,.el-loading-mask','style')
                    if 'none' in self.demoLoading:
                        break
                    else:
                        continue
                #demo账号列表
                common.display_click('css,#tab-demo')
                return True
            else:
                common.get_screenpict('creat_demo_failed')
                print('创建失败,截图保持在项目目录picture下')
                return False
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
            time.sleep(2)
            #获取demo账号
            self.bosDemo=int(common.display_get_text("xpath,//div[@class='ivu-drawer-wrap']//span"))
            time.sleep(1)
            #获取组别
            self.demoGroup=str(common.get_text("xpath,//div[@class='ivu-drawer-wrap']//span",2))
            print('新开demo账号{}组别：{}'.format(self.bosDemo,self.demoGroup))
            return self.demoGroup
        except Exception as msg:
            log.my_logger('!!--!!get_demo_group').error(msg)

    #获取demo账号杠杆
    def get_demo_lever(self):
        try:
            #获取杠杆
            self.demoLever=int(common.display_get_text("xpath,//div[@class='ivu-drawer-wrap']//span",6))
            print('新开demo账号{}杠杆：{}'.format(self.bosDemo,self.demoLever))
            return self.demoLever
        except Exception as msg:
            log.my_logger('!!--!!get_demo_lever').error(msg)
    
    #获取demo账号点差类型
    def get_demo_spreadtype(self):
        try:
            #获取点差类型
            self.demoSpread=str(common.display_get_text("xpath,//div[@class='ivu-drawer-wrap']//span",7))
            print('新开demo账号{}点差：{}'.format(self.bosDemo,self.demoSpread))
            return self.demoSpread
        except Exception as msg:
            log.my_logger('!!--!!get_demo_spreadtype').error(msg)

    #获取demo账号加点
    def get_demo_markup(self):
        try:
            #获取加点
            self.demoBit=int(common.display_get_text("xpath,//div[@class='ivu-drawer-wrap']//span",8))
            print('新开demo账号{}加点：{}'.format(self.bosDemo,self.demoBit))
            self.closebrowser()
            return self.demoBit
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
            time.sleep(1)
            #查询数据库
            self.serchDemodata=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'), 'atfxgm-sit', 'atfx_trade_account',
            {"$and": [{"accountNumber": account}, {"tradeAccount": "{}".format(self.demoAccount)}]},'group','leverage','spreadType','markup',N=1)
            #输出
            print('新开demo账号数据数据库信息，组别：{}，杠杆：{}，点差：{}，加点：{}'.format(self.serchDemodata[0]['group'],
            self.serchDemodata[0]['leverage'],self.serchDemodata[0]['spreadType'],self.serchDemodata[0]['markup']))
        except Exception as msg:
            log.my_logger('!!--!!search_mongodb_demoinfo').error(msg)


    #获取新开demo账号在cp所处位置
    def where_demo_incp(self):
        try:
            common.switch_windows(0)
            time.sleep(1)
            self.cpDemolist=common.get_lenofelement('css,.tradeAccount-info > div .el-card__body')
            time.sleep(1)
            print('当前账号已开通{}个demo交易账号'.format(self.cpDemolist))
            for i in range(0,self.cpDemolist):
                if self.demoAccount==int(randomData.regex(r'\d{9}', common.get_text('css,.tradeAccount-info > div .account-number-cla',i))):
                    print('新开demo账号位于第{}个'.format(i+1))
                    self.row=i
                    return self.row
                    break
                else:
                    continue
        except Exception as msg:
            log.my_logger('!!--!!where_demo_incp').error(msg)


    #修改demo账号杠杆
    def revise_demolever(self,index):
        try:
            #修改新开demo账号杠杆
            common.display_click('css,.tradeAccount-info > div span > i',index)
            time.sleep(2)
            #选择杠杆
            common.display_click('css,.el-select__caret')
            time.sleep(1)
            #获取修改后杠杆
            self.reviseLever=int(common.display_get_text('css,.el-select-dropdown__item span'))
            print('demo账号{}修改后杠杆为{}'.format(self.demoAccount,self.reviseLever))
            #选择修改杠杆
            common.display_click('css,.el-select-dropdown__item')
            time.sleep(1)
            #确定
            common.display_click('css,.submitEditBtn > span')
            time.sleep(1)
            return self.reviseLever
        except Exception as msg:
            log.my_logger('!!--!!revise_demolever').error(msg)

    #数据库查询修杠杆是否与修改后杠杆一致
    def revise_mongolever(self,account):
        try:
            self.serchData=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'), 'atfxgm-sit', 'atfx_trade_account',
            {"$and": [{"accountNumber": account}, {"tradeAccount": "{}".format(self.demoAccount)}]},'leverage',N=1)
            self.mongoReviselever=int(self.serchData[0]['leverage'])
            print('修改杠杆后，数据库{}账号杠杆为{}'.format(self.demoAccount,self.mongoReviselever))
            return self.mongoReviselever
        except Exception as msg:
            log.my_logger('!!--!!revise_mongolever').error(msg)


    #关闭当前页
    def closebrowser(self):
        common.close_browser()
    
    #退出浏览器进程
    def quitbrowser(self):
        common.quit_browser()
