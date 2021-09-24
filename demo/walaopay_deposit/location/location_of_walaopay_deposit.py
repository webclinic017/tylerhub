'''
Author: tyler
Date: 2021-09-17 15:00:40
LastEditTime: 2021-09-24 10:44:39
LastEditors: Please set LastEditors
Description: Page operation
FilePath: \tylerhub\demo\walaopay_withdrawal\location\location_of_walaopay_withdrawal.py
'''
import os
import sys
import time
import random

path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=os.path.join(path_demo,'public')
sys.path.append(path_public)
path_project=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from browser_actions import Commonweb
from common_method import Commonmethod
from handle_database import Dadabase_operate
from handlelog import MyLog
from randomdata import Random_data
from read_dataconfig import ReadConfig
from about_data import Aboutdata

class Location_of_walaopay(object):
    """
    页面定位等操作
    """

    global common,common2,dataBase,log,randomData,conFig,dealData

    common=Commonweb()
    common2=Commonweb()
    dataBase=Dadabase_operate()
    log=MyLog()
    randomData=Random_data()
    conFig=ReadConfig()
    dealData=Aboutdata()

    #赋值对象driver
    def broswertype(self,broswername=conFig.get_value('browser', 'default')):
        self.driver=common.open_browser(broswername)
        self.commeThod=Commonmethod(self.driver)
        self.driver2=common2.open_browser(broswername)
        self.commeThod2=Commonmethod(self.driver2)


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


    #登录bos,并进入客户名单
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
            common.display_click('css,[width="200"] li .ivu-icon-ios-arrow-down')
            time.sleep(0.5)
            #右键打开新页面
            common.display_click('css,[width="200"] li .ivu-icon-ios-arrow-down',1)
            time.sleep(0.5)
            #支付渠道管理
            common.right_click_link("xpath,//span[.='支付渠道管理']")
            time.sleep(1)
            common.switch_windows(2)
            while True:
                
                if common.ele_is_displayed('css,.spin-icon-load',2):
                    continue
                else:
                    break
            #判断walaopay myr支付方式在列表中位置
            self.channelLen=common.get_lenofelement('css,.list-group-item')
            time.sleep(1)
            for i in range(0,self.channelLen):
                if common.display_get_text('css,.list-group div .second > div:nth-of-type(1)',i)=='WalaoPay MYR':
                    if not common.display_get_text('css,.list-group div .second > div:nth-of-type(2) span span span',i)=='开启':
                        common.display_click('css,.list-group div .second > div:nth-of-type(2) span span span',i) #开启
                        time.sleep(1)
                        common.js_scroll('top')
                        time.sleep(0.5)
                        #保存
                        common.display_click('css,.pull-right > span')
                        time.sleep(1)
                        common.display_click('css,.toastButton')
                        time.sleep(2)
                        common.general_refresh_()
                        time.sleep(1)
                        while True:
                            if common.ele_is_displayed('css,.spin-icon-load',2):
                                continue
                            else:
                                break
                        for y in range(0,self.channelLen):
                            if common.display_get_text('css,.list-group div .second > div:nth-of-type(1)',y)=='WalaoPay MYR':
                                common.display_click("xpath,//div[@class='list-group']/span[1]/\
                                    div[{}]//i[@class='ivu-icon ivu-icon-md-arrow-dropdown']".format(y+1))
                                common.js_scroll_inline('class', 'wrap-content', 2000)
                                time.sleep(0.5)
                                common.js_scroll('top')
                                print('开启WalaoPay MYR入金渠道')
                                break
                    else:
                        common.display_click("xpath,//div[@class='list-group']/span[1]/\
                            div[{}]//i[@class='ivu-icon ivu-icon-md-arrow-dropdown']".format(i+1))
                        common.js_scroll_inline('class', 'wrap-content', 2000)
                        time.sleep(0.5)
                        common.js_scroll('top')
                        print('WalaoPay MYR渠道已开启')
                        break
                else:
                    pass
            common.right_click_link("xpath,//span[.='入金管理']")
            time.sleep(1)
            common.switch_windows(3)
            time.sleep(2)
            common.display_click('css,.ivu-select-single .ivu-icon',2)
            time.sleep(0.5)
            common.display_click("xpath,//li[.='交易账号']")
        except Exception as msg:
            log.my_logger('!!--!!login_bos').error(msg)

     
    def new_driver(self,environment,username,password,lang='CN'):
        #浏览器新进程，登录bos第二个账号
        common2.open_web(conFig.get_value('bos_login', '{}'.format(environment)))
        self.commeThod2.choose_bos_lang(lang)
        #登录
        self.commeThod2.loginbos(username,password)
        #进入入金管理页面
        time.sleep(1)
        common2.display_click('css,[width="200"] li .ivu-icon-ios-arrow-down',1)
        time.sleep(0.5)
        common2.display_click("xpath,//span[.='入金管理']")
        time.sleep(1)
        common2.display_click('css,.ivu-select-single .ivu-icon',2)
        time.sleep(0.5)
        common2.display_click("xpath,//li[.='交易账号']")



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
            common.switch_windows(4)
            time.sleep(3)
            #基本资料
            common.display_click("xpath,//a[.='基本资料']")
            time.sleep(1)
            #获取该账号居住国家
            self.liveCountry=common.display_get_text("xpath,//div[@class='page']//div[7]//span")
            print('该账号居住国家为{}'.format(self.liveCountry))
            time.sleep(1)
            self.closebrowser()
        except Exception as msg:
            log.my_logger('!!--!!get_live_country').error(msg)


    #进入账号详情页，获取账号国家，并判断该账号是否存在walaopay入金方式
    def is_have_walaopay(self,account):
        try:
            common.switch_windows(1)
            self.details_page(account)
            time.sleep(1)
            self.get_live_country()
            time.sleep(1)
            common.switch_windows(2)
            time.sleep(1)
            self.countryLen=common.get_lenofelement('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/div/\
            span/div[40]/div/div/div/div[2]/div/div/div[1]/div[2]/ul/li/span')
            #判断当前账号居住国家是否在未支持国家列表中
            for i in range(0,self.countryLen):
                if self.liveCountry == common.display_get_text('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/\
                    div/span/div[40]/div/div/div/div[2]/div/div/div[1]/div[2]/ul/li/span',i):
                    common.display_click('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/div/\
                        span/div[40]/div/div/div/div[2]/div/div/div[1]/div[2]/ul/li/label',i)
                    time.sleep(0.5)
                    #添加进支持国家列表中
                    common.display_click('css,.ivu-transfer-operation > button > span',1)
                    time.sleep(1)
                    #保存
                    common.display_click('css,.pull-right > span')
                    time.sleep(1)
                    common.display_click('css,.toastButton')
                    print('将{}添加进WalaoPay MYR入金渠道国家列表中'.format(self.liveCountry))
                    break
                else:
                    pass
        except Exception as msg:
            log.my_logger('!!--!!is_have_walaopay').error(msg)

    
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


    #cp首页获取交易账号余额
    def get_tradeaccount_balance(self,tradeaccount):
        try:
            time.sleep(2)
            while True:
                self.attribute=common.get_attributes('xpath,//div[@class="el-loading-mask"]','style')
                if 'display' not in self.attribute:
                    continue
                else:
                    break
            self.cprows=self.where_is_tradeaccount_cp(tradeaccount)
            time.sleep(1)
            self.balance_text=common.display_get_text('css,div.card-for-loop>div>div.el-card__body>div>p>span',4*self.cprows-4)
            time.sleep(1)
            self.balance=float(self.balance_text.replace(',',''))
            print('当前交易账号{}余额为：{}'.format(tradeaccount,self.balance))
            return self.balance
        except Exception as msg:
            log.my_logger('!!--!!get_tradeaccount_balance').error(msg)


    #获取WalaoPay MYR入金渠道最低最高入金金额
    def get_highestAndlowest(self,tradeaccount,excelpath,column,row):
        try:
            self.get_tradeaccount_balance(tradeaccount)
            dealData.saveainfo(excelpath, self.balance, column, row)
            #入金
            common.display_click("xpath,//li[.='入金']",1)
            time.sleep(1)
            #选择walaopay
            common.display_click("xpath,//p[.='WalaoPay MYR']")
            time.sleep(1)
            #获取当前入金渠道最高最低入金金额
            self.lowestDeposit=int(randomData.extract_numbers(common.display_get_text("xpath,//span[@class='currency-span']")))
            time.sleep(0.5)
            print('WalaoPay MYR最低入金金额：{}'.format(self.lowestDeposit))
            self.highestDeposit=int(randomData.extract_numbers(common.display_get_text("xpath,//span[@class='currency-span']",1)))
            print('WalaoPay MYR最高入金金额：{}'.format(self.highestDeposit))
        except Exception as msg:
            log.my_logger('!!--!!get_highestAndlowest').error(msg)

    
    #数据库查询入金汇率
    def get_mongodb_charge(self):
        try:
            self.baseCharge=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'), 
                'atfxgm-sit', 'atfx_float_rate',{"$and": [{"fromCcy":"USD"}, {"toCcy": "MYR"}]},'depositRate',N=1)[0]['depositRate']
            return self.baseCharge
        except Exception as msg:
            log.my_logger('!!--!!get_mongodb_charge').error(msg)

    
    #最低金额入金
    def lowest_deposit(self,tradeaccount):
        try:
            #交易账号
            common.display_click("css,[placeholder='请选择交易账号']")
            time.sleep(1)
            common.display_click("xpath,//span[.='MT4 - {}(USD)']".format(tradeaccount))
            time.sleep(1)
            common.display_input("css,[placeholder='请输入金金额']", self.lowestDeposit-1)
            time.sleep(1)
            #截图
            self.path1=common.get_screenpict_path('低于最低金额时')
            common.web_clear("css,[placeholder='请输入金金额']")
            time.sleep(0.5)
            common.display_input("css,[placeholder='请输入金金额']", self.lowestDeposit)
            time.sleep(0.5)
            #确认提交
            common.display_click('css,.common-btn > span')
            time.sleep(1)
            #获取入金参考汇率及转换金额
            self.exchangeRate=float(randomData.extract_numbers(common.display_get_text('css,.transfer-table-box > div .tansfer-account-txt',3)))/100000000
            print('入金参考汇率为：{}'.format(self.exchangeRate))
            #查询数据库入金参考汇率
            self.get_mongodb_charge()
            #转换金额
            self.exchangeAmount=int(randomData.extract_numbers(common.display_get_text('css,.transfer-table-box > div .tansfer-account-txt',5)))
            print('页面转换金额为：{}MYR'.format(self.exchangeAmount))
            print('根据入金金额及汇率转换金额为：{}USD*{}={}MYR'.format(self.lowestDeposit,self.baseCharge,round(self.lowestDeposit*self.baseCharge)))
            #入金手续费
            self.depositCharge=int(randomData.extract_numbers(common.display_get_text('css,.transfer-table-box > div .tansfer-account-txt',6)))
            print('入金手续费为：{}'.format(self.depositCharge))
            #确认提交
            common.display_click('css,.common-btn > span')
            time.sleep(1)
            common.switch_windows(4)
            self.closebrowser()
        except Exception as msg:
            log.my_logger('!!--!!lowest_deposit').error(msg)    

    
    #最高金额入金
    def highest_deposit(self,tradeaccount):
        try:
            #入金
            common.display_click("xpath,//li[.='入金']",1)
            time.sleep(1)
            #选择walaopay
            common.display_click("xpath,//p[.='WalaoPay MYR']")
            time.sleep(1)
            #交易账号
            common.display_click("css,[placeholder='请选择交易账号']")
            time.sleep(1)
            common.display_click("xpath,//span[.='MT4 - {}(USD)']".format(tradeaccount))
            time.sleep(1)
            common.display_input("css,[placeholder='请输入金金额']", self.highestDeposit+1)
            time.sleep(1)
            #截图
            self.path2=common.get_screenpict_path('高于最高金额时')
            common.web_clear("css,[placeholder='请输入金金额']")
            time.sleep(0.5)
            common.display_input("css,[placeholder='请输入金金额']", self.highestDeposit)
            time.sleep(0.5)
            #确认提交
            common.display_click('css,.common-btn > span')
            time.sleep(1)
            #转换金额
            self.exchangeAmount2=int(randomData.extract_numbers(common.display_get_text('css,.transfer-table-box > div .tansfer-account-txt',5)))
            print('转换金额为：{}MYR'.format(self.exchangeAmount2))
            print('根据入金金额及汇率转换金额为：{}USD*{}={}MYR'.format(self.highestDeposit,self.baseCharge,round(self.highestDeposit*self.baseCharge)))
            #入金手续费
            self.depositCharge=int(randomData.extract_numbers(common.display_get_text('css,.transfer-table-box > div .tansfer-account-txt',6)))
            print('入金手续费为：{}'.format(self.depositCharge))
            #确认提交
            common.display_click('css,.common-btn > span')
            time.sleep(1)
            common.switch_windows(4)
            self.closebrowser()
        except Exception as msg:
            log.my_logger('!!--!!highest_deposit').error(msg)    
    
    
    
    #上传入金凭证
    def upload_certificate(self):
        try:
            #出入金记录
            common.switch_windows(0)
            common.display_click("xpath,//span[.='出入金记录']")
            time.sleep(1)
            common.display_click('css,.el-tag__close')
            time.sleep(2)
            #上传按钮
            common.display_click("xpath,//i[@class='las la-upload upload_icon']")
            time.sleep(2)
            common.upload_img(path_project+r'\test_data\upimg.exe', path_project+r'\test_data\code.jpg')
        except Exception as msg:
            log.my_logger('!!--!!upload_certificate').error(msg)    


    
    #入金最低最高金额，上传入金凭证
    def action(self,tradeaccount):
        #最低金额入金
        self.lowest_deposit(tradeaccount)
        #上传凭证
        self.upload_certificate()
        #最高金额入金
        self.highest_deposit(tradeaccount)
        #上传凭证
        self.upload_certificate()

    
    #bos入金审核
    def bos_verify(self,tradeaccount):
        try:
            common.switch_windows(3)
            #输入交易账号查询
            common.web_clear('css,.ivu-input-group > [placeholder]')
            time.sleep(0.5)
            common.display_input('css,.ivu-input-group > [placeholder]', tradeaccount)
            time.sleep(0.5)
            #查询
            common.display_click('css,.ivu-btn-icon-only')
            time.sleep(1)
            #判断当前入金是否被上锁
            if common.display_get_text("xpath,//span[@class='tips']")=='上锁':
                common.display_click('css,.ivu-table-tbody > tr .ivu-checkbox-input')
                time.sleep(1)
                common.display_click('css,.ivu-table-tbody > tr .ivu-checkbox-input',1)
                time.sleep(1)
                common.display_click("xpath,//span[.='解锁']")
                time.sleep(1)
            else:
                pass
            #勾选最低最高入金金额，转未处理
            common.display_click('css,.ivu-table-tbody > tr .ivu-checkbox-input')
            time.sleep(1)
            common.display_click('css,.ivu-table-tbody > tr .ivu-checkbox-input',1)
            time.sleep(1)
            common.display_click("xpath,//span[.='转未处理']")
            time.sleep(1.5)
            common.get_screenpict_path('最高最低入金转未处理')
            #bos第二个账户进行审核
            common2.web_clear('css,.ivu-input-group > [placeholder]')
            time.sleep(0.5)
            common2.display_input('css,.ivu-input-group > [placeholder]', tradeaccount)
            time.sleep(0.5)
            #查询
            common2.display_click('css,.ivu-btn-icon-only')
            time.sleep(1)
            #勾选最低最高入金金额，转未处理
            common2.display_click('css,.ivu-table-tbody > tr .ivu-checkbox-input')
            time.sleep(1)
            common2.display_click('css,.ivu-table-tbody > tr .ivu-checkbox-input',1)
            time.sleep(1)
            common2.display_click("xpath,//span[.='完成']")
            time.sleep(1.5)
            common2.display_click("xpath,//span[.='确定']")
            time.sleep(1)
            self.path3=common2.get_screenpict_path('最高最低入金转完成')
        except Exception as msg:
            log.my_logger('!!--!!bos_verify').error(msg)   

    #获取入金成功后，交易账号余额
    def after_deposti(self,tradeaccount,excelpath,column,row):
        try:
            common.switch_windows(0)
            #首页
            common.display_click("xpath,//span[.='首页']")
            self.get_tradeaccount_balance(tradeaccount)
            dealData.saveainfo(excelpath, self.balance, column, row)
        except Exception as msg:
            log.my_logger('!!--!!bos_verify').error(msg)      

    def closebrowser(self):
        common.close_browser()

    def quitbrowser(self):
        common.quit_browser()
        common2.quit_browser()