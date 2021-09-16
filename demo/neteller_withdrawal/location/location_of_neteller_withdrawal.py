'''
Author: tyler
Date: 2021-09-08 15:05:02
LastEditTime: 2021-09-15 17:53:42
LastEditors: Please set LastEditors
Description: Related operations such as page positioning
FilePath: \tylerhub\demo\neteller_withdrawal\location\location_of_neteller_withdrawal.py
'''
import os
import sys
import time
import random

path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=os.path.join(path_demo,'public')
sys.path.append(path_public)

from about_data import Aboutdata
from browser_actions import Commonweb
from common_method import Commonmethod
from handle_database import Dadabase_operate
from handlelog import MyLog
from randomdata import Random_data
from read_dataconfig import ReadConfig
from api import Api

class Location_of_netellerWithdrawal(object):

    """
    neteller出金，页面定位等操作
    """

    global dealData,common,dataBase,log,randomData,conFig,api_request

    dealData=Aboutdata()
    common=Commonweb()
    dataBase=Dadabase_operate()
    log=MyLog()
    randomData=Random_data()
    conFig=ReadConfig()
    api_request=Api()

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

    
    #遍历会员中心首页的交易账户列表，找到入金交易账户所处位置
    def where_is_tradeaccount_cp(self,tradeaccount):
        #获取首页交易账号列表长度
        self.len_incp=common.get_lenofelement('css,.account-number-cla')
        time.sleep(1)
        new_str=str(4)+str(tradeaccount)
        for i in range(0,self.len_incp):
            if randomData.extract_numbers(common.get_text('css,.account-number-cla',i)) == new_str:
                return i+1
                break


    #获取出金交易账号余额
    def get_tradeaccount_balance(self,tradeaccount):
        try:
            self.cprows=self.where_is_tradeaccount_cp(tradeaccount)
            time.sleep(1)
            self.balance_text=common.display_get_text('css,div.card-for-loop>div>div.el-card__body>div>p>span',4*self.cprows-4)
            time.sleep(1)
            self.balance=float(self.balance_text.replace(',',''))
            print('当前交易账号{}余额为：{}'.format(tradeaccount,self.balance))
            return self.balance
        except Exception as msg:
            log.my_logger('!!--!!get_tradeaccount_balance').error(msg)



    #登出cp
    def logoutcp(self):
        try:
            common.switch_windows(0)
            time.sleep(1)
            self.commeThod.logout_cp()
            time.sleep(2)
        except Exception as msg:
            log.my_logger('!!--!!logoutcp').error(msg)


    #登录bos
    def login_bos(self,username,password):
        try:
            common.switch_windows(1)
            time.sleep(1)
            self.commeThod.loginbos(username, password)
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


    #bos获取验证码
    def get_verify_code(self):
        try:
            common.switch_windows(2)
            time.sleep(1)
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


    #判断出金交易账号余额是否为0
    def is_balance_nil(self,tradeaccount):
        try:
            time.sleep(3)
            while True:
                self.attribute=common.get_attributes('xpath,//div[@class="el-loading-mask"]','style')
                if 'display' not in self.attribute:
                    continue
                else:
                    break
            #获取出金交易账号余额
            self.balance=self.get_tradeaccount_balance(tradeaccount)
            if self.balance==0:
                return True
            else:
                return False
        except Exception as msg:
            log.my_logger('!!--!!is_balance_nil').error(msg)

    
    #判断当前账号是否存在neteller出金方式
    def is_exist_neteller(self):
        try:
            common.display_click('css,.el-icon--right.el-icon-arrow-down')
            time.sleep(1)
            #设置
            common.display_click('css,.el-client-menu > li',1)
            time.sleep(1)
            #出金方式
            common.display_click('css,#tab-second')
            time.sleep(2)
            #判断是否存在neteller出金方式
            if common.ele_is_displayed("xpath,//span[.='Neteller']", 2):
                #存在neteller出金方式
                return True
            else:
                #不存在neteller出金方式
                return False
        except Exception as msg:
            log.my_logger('!!--!!is_exist_neteller').error(msg)

    
    #添加neteller出金方式
    def add_neteller(self,account):
        try:
            common.display_click("xpath,//span/span[.='新增']")
            time.sleep(1)
            #发送验证码
            common.display_click('css,.el-button--default.sendBtn')
            time.sleep(1)
            #获取验证码
            common.switch_windows(1)
            #客户管理
            common.display_click("css,[width='200'] li .ivu-icon-ios-arrow-down")
            time.sleep(1)
            #客户名单
            common.display_click("xpath,//span[.='客户名单']")
            time.sleep(1)
            common.display_click("css,[width='200'] li .ivu-icon-ios-arrow-down")
            #进入账号详情页
            self.details_page(account)
            time.sleep(1)
            #获取验证码
            self.get_verify_code()
            time.sleep(1)
            #填写验证码
            common.switch_windows(0)
            time.sleep(1)
            common.display_input("css,[placeholder='验证码']", self.emailcode)
            time.sleep(1)
            #提交
            common.display_click('css,.el-button--primary.sendBtn > span')
            time.sleep(1)
            #渠道
            common.display_click('css,.el-form > div .el-select__caret')
            time.sleep(0.5)
            common.display_click("xpath,//span[.='Neteller']",-1)
            time.sleep(0.5)
            #邮箱
            common.display_input("css,[placeholder='电子邮件']", randomData.get_rangenemail(9))
            time.sleep(0.5)
            #提交
            common.display_click('css,.sub-btn > span')
            time.sleep(2)
            common.get_screenpict('添加neteller出金方式')
        except Exception as msg:
            log.my_logger('!!--!!add_neteller').error(msg)

    
    #出金,并判断出金交易账号余额是否大于出金金额
    def use_neteller_withdrawal(self,account,tradeaccount,username,amount,excelpath,column,row):
        try:
            time.sleep(1)
            common.display_click("xpath,//span[.='出金']")
            time.sleep(1)
            #选择交易账户
            common.display_click("css,[placeholder='交易账户']")
            time.sleep(0.5)
            common.display_click("xpath,//span[.='MT4 - {}']".format(tradeaccount))
            time.sleep(1)
            #取款方式
            common.display_click('css,#typeSelection')
            time.sleep(0.5)
            common.display_click("xpath,//span[.='电子钱包']")
            time.sleep(0.5)
            #渠道
            common.display_click("css,[placeholder='渠道']")
            time.sleep(0.5)
            common.display_click("xpath,//span[.='Neteller']")
            time.sleep(0.5)
            common.display_click("css,[placeholder='电邮']")
            time.sleep(0.5)
            common.display_click("css,[x-placement='bottom-start'] li > span")
            time.sleep(1)
            #获取当前交易账号可取款金额
            self.withdrawal_balance=int(randomData.extract_numbers(common.get_text('css,.balance')))/100
            if self.withdrawal_balance==0: #可出金金额为0
                print('当前交易账号可出金金额为0')
                return True
            else: #余额不为0时
                if self.withdrawal_balance<amount:#余额小于出金金额，默认出金余额的1/2
                    common.display_input("css,[placeholder='取款金额']",int(self.withdrawal_balance/2))
                    time.sleep(0.5)
                    #调用接口，查询当前出金手续费
                    self.api_get_charge(account,tradeaccount,username,int(self.withdrawal_balance/2))
                    time.sleep(1)
                else:#余额大于出金金额
                    common.display_input("css,[placeholder='取款金额']",amount)
                    time.sleep(0.5)
                    #调用接口，查询当前出金手续费
                    self.api_get_charge(account,tradeaccount,username,amount)
                    time.sleep(1)
                #验证码
                common.display_input("css,[placeholder='验证码']", 'gvls')
                time.sleep(1)
                #勾选取款须知
                common.display_click('css,.el-checkbox__inner')
                time.sleep(0.5)
                #提交
                common.display_click('css,.button_submit')
                time.sleep(2)
                #确认提交
                common.display_click('css,.allow_color')
                #截图
                self.charge_path=self.screenshots_path('出金手续费')
                time.sleep(1)
                if self.api_charge==0:
                    #获取页面手续费
                    print('当前出金不需要手续费')
                    self.charge=0
                else:
                    self.charge=float(int(randomData.extract_numbers(common.display_get_text('css,.content')))/100)
                    time.sleep(1)
                    #再次确认
                    common.display_click('css,.btn-confirm')
                    print('当前出金手续费为：{}'.format(self.charge))
                #保存接口手续费到本地
                dealData.saveainfo(excelpath, self.api_charge, column, row)
                return False
        except Exception as msg:
            log.my_logger('!!--!!use_neteller_withdrawal').error(msg)



    #出金
    def action_neteller(self,account,tradeaccount,username,amount,excelpath,column,row):
        try:
            if self.is_exist_neteller():#存在neteller出金方式
                self.use_neteller_withdrawal(account,tradeaccount,username,amount,excelpath,column,row)
            else:
                self.add_neteller(account)
                self.use_neteller_withdrawal(account,tradeaccount,username,amount,excelpath,column,row)
        except Exception as msg:
            log.my_logger('!!--!!use_neteller_withdrawal').error(msg)

    
    #调用接口，获取当前出金手续费
    def api_get_charge(self,account,tradeaccount,username,amount):
        #请求头
        headers_login={
            'accept':'application/json, text/plain, */*',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh,zh-CN;q=0.9,en;q=0.8',
            'content-type':'application/json;charset=UTF-8',
            'sec-ch-ua':'"Google Chrome";v="93","Not;A Brand";v="99", "Chromium";v="93"',
            'sec-fetch-dest':'empty',
            'sec-fetch-mode':'cors',
            'sec-fetch-site':'same-site',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
            }

        #查询数据库，获取加密后密码
        self.search=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'), 'atclientpoolsit', 
        'usersgm',{"email":username},'encrypt_secret')

        #参数
        data={
            "entity": "GM",
            "email": username,
            "password": self.search[0]['encrypt_secret'],
            "loginType": "email",
            "accountNumber":account
            }
        #调用登录接口,获取token
        self.api_data=api_request.api_post(conFig.get_value('api_login_cp', 'host'),conFig.get_value('api_login_cp', 'path'),
        headers=headers_login,json=data)

        #保存token到配置文件中
        conFig.modify('api_login_cp', 'x-token', self.api_data.json()['data']['storageValue']['id_token'])
        time.sleep(1)

        #调用查询手续费接口，获取当前出金手续费
        #请求头
        headers_charge={
            'accept':'application/json, text/plain, */*',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh,zh-CN;q=0.9,en;q=0.8',
            'content-type':'application/json;charset=UTF-8',
            'sec-ch-ua':'"Google Chrome";v="93","Not;A Brand";v="99", "Chromium";v="93"',
            'sec-fetch-dest':'empty',
            'sec-fetch-mode':'cors',
            'sec-fetch-site':'same-site',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
            'x-token':conFig.get_value('api_login_cp', 'x-token')
            }
        
        #请求参数
        data_charge={
            "entity": "GM", 
	        "accountNumber": account, 
            "channel":"ewallet",
            "country":"",
            "currency":"USD",
            "entity":"GM",
            "mtAmt":str(amount),
            "tradeAccount":tradeaccount,
            "tradeAccountServer": "mt4_s02", 
            "commissionTD": ""}
        
        #调用查询手续费接口，获取当前出金手续费
        self.api_data2=api_request.api_post(conFig.get_value('api_login_cp', 'host'),conFig.get_value('api_login_cp', 'path_charge'),
        headers=headers_charge,json=data_charge)
  

        self.api_charge=float((self.api_data2.json()['data']['charge']))
        print('当前出金账号接口返回手续费为：{}'.format(self.api_charge))
        return self.api_charge

    


    #bos审核出金
    def review_withdrawal(self,tradeaccount,excelpath,column,row):
        try:
            common.switch_windows(1)
            #资金管理
            common.display_click("css,[width='200'] li .ivu-icon-ios-arrow-down",1)
            time.sleep(0.5)
            #出金管理
            common.display_click("xpath,//span[.='出金管理']")
            time.sleep(0.5)
            common.display_click("css,[width='200'] li .ivu-icon-ios-arrow-down",1)
            time.sleep(0.5)
            #根据交易账号搜索
            common.display_click('css,.ivu-select-single .ivu-icon',2)
            time.sleep(0.5)
            common.display_click("xpath,//li[.='交易账号']")
            time.sleep(0.5)
            common.web_clear('css,.ivu-input-group > [placeholder]')
            time.sleep(0.5)
            common.display_input('css,.ivu-input-group > [placeholder]', tradeaccount)
            time.sleep(0.5)
            #搜索
            common.display_click('css,.ivu-btn-icon-only > .ivu-icon')
            time.sleep(2)
            #获取bos该笔出金时间
            self.withdrawal_bosTime=common.display_get_text('css,td .tips',5)
            #保存bos出金时间到本地
            dealData.saveainfo(excelpath, self.withdrawal_bosTime, column, row)
            time.sleep(1)
            #勾选当前交易账号出金
            common.display_click('css,.ivu-table-wrapper div tr input',1)
            time.sleep(1)
            #完成
            common.display_click('css,.ivu-btn-success.pull-left > span')
            time.sleep(2)
            #截图
            self.review_path=self.screenshots_path('审核成功')
        except Exception as msg:
            log.my_logger('!!--!!review_withdrawal').error(msg)
    
    
    #会员中心查看
    def check_cp(self,tradeaccount,excelpath,column1,column2,row):
        try:
            common.switch_windows(0)
            time.sleep(0.5)
            common.display_click("xpath,//span[contains(.,'查看我的出金记录')]")
            time.sleep(2)
            #cp创建时间
            self.withdrawal_cpTime=common.display_get_text("xpath,//tr[@class='el-table__row'][1]//span",5)
            time.sleep(0.5)
            #保存cp出金时间到本地
            dealData.saveainfo(excelpath, self.withdrawal_cpTime, column1, row)
            time.sleep(1)
            #状态
            self.withdrawal_cpStatus=common.display_get_text("xpath,//tr[@class='el-table__row'][1]//span",9)
            time.sleep(1)
            #数据库查询该交易账号出金创建时间
            self.withdrawal_mogoTime=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'), 
            'atfxgm-sit', 'atfx_withdrawal',{"tradeAccount":"{}".format(tradeaccount)},'createDate',N=1)[0]['createDate']
            dealData.saveainfo(excelpath, self.withdrawal_mogoTime, column2, row)
            print('数据库中该笔出金创建时间为：{}'.format(self.withdrawal_mogoTime))
        except Exception as msg:
            log.my_logger('!!--!!check_cp').error(msg)


    #截图,返回截图路径
    def screenshots_path(self,name,filename='picture'):
        return common.get_screenpict_path(name)
            
    
    def closebrowser(self):
        common.close_browser()

    def quitbrowser(self):
        common.quit_browser()