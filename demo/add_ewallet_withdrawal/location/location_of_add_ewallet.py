'''
Author: tyler
Date: 2021-09-02 10:17:39
LastEditTime: 2021-09-08 16:26:05
LastEditors: Please set LastEditors
Description: Related operations such as page positioning
FilePath: \tylerhub\demo\add_ewallet_withdrawal\location\location_of_add_ewallet.py
'''
import os
import sys
import time
import random

path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=os.path.join(path_demo,'public')
sys.path.append(path_public)

from browser_actions import Commonweb
from common_method import Commonmethod
from handle_database import Dadabase_operate
from handlelog import MyLog
from randomdata import Random_data
from read_dataconfig import ReadConfig

class Location_of_add_ewallet(object):
    """
    添加ewallet出金方式，页面定位等操作
    """

    global common,dataBase,log,randomData,conFig

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
            time.sleep(1)
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
                print('跳过该用例')
                self.closebrowser()
                return True
            else:
                return False
        except Exception as msg:
            log.my_logger('!!--!!get_live_country').error(msg)


    #在cp判断当前账号ewallet出金方式是否超过三条
    def is_ewallet_morethan_three(self):
        try:
            time.sleep(3)
            #进入账户设定页面
            common.display_click('css,.el-icon--right.el-icon-arrow-down')
            time.sleep(1)
            common.display_click('css,.el-client-menu > li > .drop-sub-title')
            time.sleep(2)
            #出金方式
            common.display_click('css,#tab-second')
            time.sleep(1)
            #判断当前账号是否存电子钱包出金方式
            if common.ele_is_displayed("xpath,//div[@class='bankinfo-page']/div[@class='info-row el-row']//div//span[.='渠道:']",2):
                print('当前账号存在电子钱包出金方式')
                #判断存在几种电子钱包出金方式
                self.ewalletType_len=common.get_lenofelement("xpath,//div[@class='bankinfo-page']/div\
                    [@class='info-row el-row']//div//span[.='渠道:']")
                self.ewallet_list=[]
                for i in range(0,self.ewalletType_len):
                    self.ewallet_dict={}
                    common.display_click("xpath,//div[@class='bankinfo-page']/div\
                        [@class='info-row el-row']//div//span[.='渠道:']",i)
                    time.sleep(1)
                    #获取当前出金类型存在几个出金方式
                    self.ewallet_len=common.get_lenofelement("xpath,//div[@class='bankinfo-page']/div[1]//div\
                        [@class='bank-row']/div[{}]//div/span[@class='del-btn c-float']".format(i+1))
                    #当该电子钱包出金方式大于等于三时：
                    if self.ewallet_len>=3:
                        #赋值ewallet
                        self.ewallet=common.get_text('css,.bankinfo-page > div div > .bankNo > .lev-val',i)
                        self.times=self.ewallet_len
                        print('{}电子钱包出金方式大于等于3条'.format(self.ewallet))
                        break
                    else:
                        self.ewalletText=common.get_text('css,.bankinfo-page > div div > .bankNo > .lev-val',i)
                        self.ewallet_dict[self.ewalletText]=self.ewallet_len
                        self.ewallet_list.append(self.ewallet_dict)
                        #赋值ewallet
                        self.ewallet=''.join(self.ewallet_list[0].keys())
                        self.times=int(self.ewallet_list[0][self.ewallet])
                    print('需添加{}条{}出金方式'.format(3-self.times,self.ewallet))
            else:
                print('当前账号不存在电子钱包出金方式')
                self.ewallet='Skrill'
                self.times=0
        except Exception as msg:
            log.my_logger('!!--!!is_ewallet_morethan_three').error(msg)
        
    

    #bos获取验证码
    def get_verify_code(self):
        try:
            common.switch_windows(2)
            #邮件记录
            common.display_click('xpath,//a[.="邮件记录"]')
            time.sleep(1)
            #刷新
            common.display_click("xpath,//div[@class='emailRecord-page']//span[contains(.,'刷新')]")
            time.sleep(2)
            #点击验证码邮件
            common.display_click('css,.tips',1)
            time.sleep(1)
            #获取验证码文本
            acc_text=common.get_text('xpath,//div[@class="ivu-drawer-wrap"]//tr[2]//tr[4]/td[1]/span')
            time.sleep(1)
            #提取验证码
            self.emailcode=randomData.extract_numbers(acc_text)
            self.closebrowser()
            return self.emailcode
        except Exception as msg:
            log.my_logger('!!--!!get_verify_code').error(msg)



    #获取提示
    def get_tips(self):
        try:
            #新增
            common.display_click('css,.el-button--default span span')
            time.sleep(1)
            #发送验证码
            common.display_click('css,.el-button--default.sendBtn')
            time.sleep(1)
            #获取验证码
            self.get_verify_code()
            #填写验证码
            common.switch_windows(0)
            common.display_input("css,[placeholder='验证码']", self.emailcode)
            time.sleep(1)
            #提交
            common.display_click('css,.el-button--primary.sendBtn > span')
            time.sleep(1)
            if self.times>=3:
                #选择超过三条的电子钱包出金方式
                common.display_click('css,.el-form > div .el-select__caret')
                time.sleep(1)
                common.display_click("xpath,//span[.='{}']".format(self.ewallet),-1)
                time.sleep(1)
                self.tips=common.display_get_text('css,.el-message__content')
                print(self.tips)
                common.display_click('css,.bankinfo-page > div .el-dialog__close',3)
                return self.tips
            else:
                for i in range(0,4-self.times):
                    #选择出金渠道
                    common.display_click('css,.el-form > div .el-select__caret')
                    time.sleep(1)
                    common.display_click("xpath,//span[.='{}']".format(self.ewallet),-1)
                    if i==3-self.times:
                        #捕获tips
                        time.sleep(1)
                        self.tips=common.display_get_text('css,.el-message__content')
                        print(self.tips)
                        common.display_click('css,.bankinfo-page > div .el-dialog__close',3)
                        return self.tips
                    else:
                        if self.ewallet=='M-Pesa':
                            #手机号
                            common.display_input('css,.el-input__inner', randomData.get_rangephone(),2)
                        else:
                            #邮箱
                            common.display_input('css,.el-input__inner', randomData.get_rangenemail(9),2)
                        time.sleep(1)
                        #提交并继续添加
                        common.display_click('css,.el-button--text > span')
                        time.sleep(2)
                        common.display_click('xpath,//span[.="继续添加"]')
        except Exception as msg:
            log.my_logger('!!--!!get_tips').error(msg)

       
    #判断新增出金方式会员中心是否可用
    def is_ewallet_available(self):
        try:
            if self.times<3:
                #出金
                common.switch_windows(0)
                time.sleep(1)
                common.display_click('xpath,//span[.="出金"]')
                #取款方式
                common.display_click('css,#typeSelection')
                time.sleep(1)
                #选择电子钱包
                common.display_click("xpath,//span[.='电子钱包']")
                time.sleep(1)
                #渠道
                common.display_click("css,[placeholder='渠道']")
                time.sleep(1)
                #选择之前添加的电子钱包入金方式
                common.display_click("xpath,//span[.='{}']".format(self.ewallet))
                time.sleep(1)
                #判断是否存在三条可用数据
                common.display_click("css,[placeholder='电邮']")
                time.sleep(1)
                self.available_ewallet=common.get_lenofelement("css,[x-placement='bottom-start'] li")
                #获取当前所有可用电邮/电话
                self.availableList=[]
                for i in range(0,self.available_ewallet):
                    self.availableList.append(common.display_get_text("css,[x-placement='bottom-start'] li > span",i))
                print('当前所有可用渠道支付方式：{}'.format(self.availableList))
            else:
                self.available_ewallet=self.times
        except Exception as msg:
            log.my_logger('!!--!!is_ewallet_available').error(msg)


    #查询数据库，判断新增电子钱包出金方式是否添加进库中
    def search_mongodb_ewallet(self,account):
        try:
            self.dabasData=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'), 'atfxgm-sit', 'atfx_bank_info',
            {"accountNumber":account},'eChannel',N=1)
            self.databaseList=[]
            for i in self.dabasData[0]['eChannel']:
                self.databaseList.append(i['payAccount'])
            print('数据库中所有可用支付方式：{}'.format(self.databaseList))
            return self.databaseList
        except Exception as msg:
            log.my_logger('!!--!!search_mongodb_ewallet').error(msg)
    
    
    #截图,返回截图路径
    def screenshots_path(self,name,filename='picture'):
        return common.get_screenpict_path(name)

    def closebrowser(self):
        common.close_browser()

    def quitbrowser(self):
        common.quit_browser()