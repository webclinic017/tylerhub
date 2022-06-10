'''
Author: tyler
Date: 2021-05-28 17:29:27
LastEditTime: 2022-06-10 18:06:29
LastEditors: Tyler Tang tyler.tang@6317.io
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
from randomdata import Random_data
class Ewallet_deposti():

    global common,randomData,conFig,log,ranDom

    common=Commonweb()
    randomData=Random_data()
    conFig=ReadConfig()
    log=MyLog()
    ranDom=Random_data()

    #赋值对象driver
    def broswertype(self,browsername=conFig.get_value('browser', 'default')):
        self.driver=common.open_browser(browsername)
        self.comMethod=Commonmethod()

    #登录页
    def get_url(self,environment,lang='CN'):
        try:
            common.open_web(conFig.get_value('bos_login', '{}'.format(environment)))
            #选择bos页面语言,默认简中
            time.sleep(1)
            self.comMethod.choose_bos_lang(common,lang)
        except Exception as msg:
            log.my_logger('!!--!!get_url').error(msg)

    #登录bos
    def login_bos(self,username, password):
        self.comMethod.loginbos(common,username, password)

    def logoutbos(self):
        #登出bos
        common.switch_windows(0)
        common.display_click("xpath,//div[@class='scroll-content']//span[.='客户管理']")
        time.sleep(0.5)
        common.display_click("xpath,//div[@class='scroll-content']//li[@class='ivu-menu-item']")
        time.sleep(2)
        common.general_refresh_()
        while True:
            if common.ele_is_displayed('css,.ivu-spin-dot', 1):
                continue
            else:
                break
    
    #bos登录cp进入入金页面
    def bos_to_cp(self,account):
        try:
            common.switch_windows(0)
            time.sleep(1)
            common.display_click("xpath,//span[.='客户管理']")
            time.sleep(0.5)
            common.display_click("xpath,//span[.='登录会员中心']")
            time.sleep(1)
            #选择登录cp语言
            common.display_click('css,.ivu-form div i',-1)
            time.sleep(0.5)
            common.display_click("xpath,//li[.='简体中文']",-1)
            time.sleep(1)
            common.web_clear('css,[placeholder]')
            time.sleep(0.5)
            common.web_input('css,[placeholder]',account)
            time.sleep(0.5)
            #登录
            common.display_click('xpath,//span[.="登录"]')
            time.sleep(2)
            common.switch_windows(1)
            time.sleep(2)
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
            common.display_click('xpath,//span[.="入金"]')
            time.sleep(2)
            #判断是否有入金须知弹窗
            if 'none' not in common.get_attributes('css,.declar-dialog-box div.el-dialog__wrapper', 'style'):
                common.display_click('css,.el-checkbox__inner') #勾选协议
                time.sleep(0.5)
                common.display_click('css,.confirm-btn') #确定
            else:
                pass
            while True:
                if 'none' not in common.get_attributes('css,.el-loading-mask', 'style'):
                    continue
                else:
                    break
        except Exception as msg:
            log.my_logger('!!--!!bos_to_cp').error(msg)

    
    #判断当前用户是否存在电子钱包的入金方式，若存在多个，随机选择一个渠道入金
    def judge_ewalletpay(self):
        try:
            #获取当前账号存在几种入金方式
            self.payTypeLen=common.get_lenofelement('css,.el-collapse-item__header')
            
            #截图，返回截图路径
            self.payTypePicPath=common.get_screenpict_path('入金方式')

            #判断是否存在电子钱包入金方式
            self.payTypeList=[]
            for i in range(0,self.payTypeLen):
                self.payTypeList.append(common.display_get_text('css,.el-collapse-item__header',i))
            if '电子钱包' in self.payTypeList:
                self.ewalletLen=common.get_lenofelement("xpath,/html/body/div[1]/div[3]/div[2]/div[2]/div\
                    /div[2]/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div[2]/div/div")
                print('当前账号存在电子钱包入金方式，且存在{}种渠道入金'.format(self.ewalletLen))
                return True
            else:
                print('当前账号不存在电子钱包入金方式')
                self.clsoebrowser()
                return False
        except Exception as msg:
            log.my_logger('!!--!!judge_ewalletpay').error(msg)

    #随机选择一种电子钱包入金渠道入金
    def deposit_ewallet(self,tradaccount,amount):
        try:
            while True:
                #随机选择一种渠道入金random.randint(1,self.ewalletLen)
                self.index=4
                self.ewalletType=common.display_get_text('xpath,/html/body/div[1]/div[3]/div[2]\
                    /div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div[2]/div/div[{}]/div[2]/p[1]'.format(self.index))
                print('选择{}渠道入金'.format(self.ewalletType))

                common.display_click('xpath,/html/body/div[1]/div[3]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div\
                    /div[1]/div/div/div/div[2]/div[2]/div/div[{}]/div[2]/p[1]'.format(self.index))
                time.sleep(2)
                common.display_click('css,.el-select__caret')
                time.sleep(1)
                #选择交易账号
                common.display_click("xpath,//span[.='MT4 - {}(USD)']".format(tradaccount))
                time.sleep(1)
                #输入入金金额
                common.web_clear("css,[placeholder='请输入金金额']")
                time.sleep(0.5)
                common.display_input("css,[placeholder='请输入金金额']", amount)
                time.sleep(0.5)
                #若存在邮箱/手机则输入邮箱/手机
                if common.ele_is_displayed("css,[placeholder='请输入邮箱']", 1):
                    common.web_clear("css,[placeholder='请输入邮箱']")
                    time.sleep(0.5)
                    common.display_input("css,[placeholder='请输入邮箱']", ranDom.get_rangenemail(11))
                    time.sleep(1)
                elif common.ele_is_displayed("css,[placeholder='请输入您的手机号']", 1):
                    common.web_clear("css,[placeholder='请输入您的手机号']") 
                    time.sleep(0.5)
                    common.display_input("css,[placeholder='请输入您的手机号']", ranDom.get_rangephone())
                    time.sleep(1) 
                else:
                    pass
                #下一步
                common.display_click("xpath,//span[contains(.,'下一步')]")
                time.sleep(1)
                #若出现入金手续费，去除弹窗
                if common.ele_is_displayed('css,.title_1', 1):
                    common.display_click('css,.ok > span')
                    time.sleep(1)
                else:
                    pass
                #勾选入金须知
                common.display_click('css,.el-checkbox__inner')
                time.sleep(0.5)
                common.display_click("xpath,//span[.='确定提交']")
                time.sleep(2)
                common.switch_windows(1)
                time.sleep(1)
                if common.ele_is_displayed('css,.deposit-title-info', 1):
                    if '完成入金手续' in common.display_get_text('css,.deposit-title-info'):
                        self.depositSuccessPicPath=common.get_screenpict_path('{}渠道入金成功待审核'.format(self.ewalletType))
                        time.sleep(1)
                        self.clsoebrowser()
                        common.switch_windows(1)
                        time.sleep(1)
                        self.clsoebrowser()
                        break
                    else:
                        pass
                else:
                    common.js_scroll('top')
                    self.depositFaildPicPath=common.get_screenpict('{}渠道入金失败'.format(self.ewalletType))
                    print('{}渠道入金失败'.format(self.ewalletType))
                    common.switch_windows(2)
                    self.clsoebrowser()
                    common.switch_windows(1)
                    common.display_click('xpath,//span[.="入金"]')
                    while True:
                        if 'none' not in common.get_attributes('css,.el-loading-mask', 'style'):
                            continue
                        else:
                            break
                    continue 
        except Exception as msg:
            log.my_logger('!!--!!deposit_ewallet').error(msg)

    #bos审核入金
    def review_deposit(self,tradaccount,environment,username,psword):
        try:
            #打开入金管理页面
            common.switch_windows(0)
            time.sleep(1)
            common.js_openwindows(conFig.get_value('bos_DepositList', environment))
            time.sleep(1)
            common.switch_windows(1)
            time.sleep(2)
            #选择验证中状态
            common.display_click('css,.ivu-select-multiple > .ivu-select-selection > div > .ivu-icon')
            time.sleep(0.5)
            common.display_click('css,.ivu-select-visible li',2)
            time.sleep(0.5)
            #输入交易账号查询
            common.display_doubleclick('css,.ivu-select-single .ivu-icon',2)
            time.sleep(0.5)
            common.display_click("xpath,//li[.='交易账号']")
            time.sleep(1)
            common.display_input("xpath,//div[@class='query-box']//input[@class='ivu-input ivu-input-default']", tradaccount)
            time.sleep(0.5)
            #搜索
            common.display_click('css,.ivu-btn-icon-only > .ivu-icon')
            time.sleep(1)
            while True:
                if 'none' not in common.get_attributes('css,.ivu-table-tip', 'style'):
                    continue
                else:
                    break
            #转未处理
            time.sleep(1)
            common.display_click('css,.ivu-table-tbody > tr .ivu-checkbox-input')
            time.sleep(1)
            while True:
                if common.ele_is_displayed('css,.ivu-spin-dot', 1):
                    continue
                else:
                    break
            common.display_click("xpath,//span[.='转未处理']")
            time.sleep(1)
            #登出bos
            common.display_click("xpath,//div[@class='scroll-content']//span[.='资金管理']")
            time.sleep(0.5)
            common.display_click("xpath,//div[@class='scroll-content']//li[@class='ivu-menu-item']")
            time.sleep(1)
            self.comMethod.loginbos(common, username, psword)
            common.display_click("xpath,//div[@class='scroll-content']//span[.='资金管理']")
            time.sleep(0.5)
            common.display_click("xpath,//li[@class='ivu-menu-submenu ivu-menu-opened']//span[.='入金管理']")
            time.sleep(1)
            #输入交易账号查询
            common.display_click('css,.ivu-select-single .ivu-icon',2)
            time.sleep(0.5)
            common.display_click("xpath,//li[.='交易账号']")
            time.sleep(1)
            common.display_input("xpath,//div[@class='query-box']//input[@class='ivu-input ivu-input-default']", tradaccount)
            time.sleep(0.5)
            #搜索
            common.display_click('css,.ivu-btn-icon-only > .ivu-icon')
            time.sleep(1)
            while True:
                if 'none' not in common.get_attributes('css,.ivu-table-tip', 'style'):
                    continue
                else:
                    break
            #转成功
            common.display_click('css,.ivu-table-tbody > tr .ivu-checkbox-input')
            time.sleep(1)
            while True:
                if common.ele_is_displayed('css,.ivu-spin-dot', 1):
                    continue
                else:
                    break
            common.display_click("xpath,//span[.='完成']")
            while True:
                if common.ele_is_displayed('css,.ivu-spin-dot', 1):
                    continue
                else:
                    break
            #截图bos审核入金成功
            self.reviewSuccessPicPath=common.get_screenpict_path('bos审核入金成功')
            print(common.display_get_text('css,.ivu-modal-confirm-body > div'))
            #点击确定
            common.display_click('css,.ivu-modal-confirm-footer span')
            time.sleep(1)
            #获取审核成功后的文本
            self.reviewSuccessText=common.display_get_text('xpath,//*[@id="app"]/div/div/div[4]/div/div/div/div/div[2]/div/div[2]/div[1]/div\
                /div[3]/div/div[3]/div/div/div[1]/div[2]/table/tbody/tr[1]/td[3]/div/div/div/span')
            time.sleep(1)
            self.clsoebrowser()
        except Exception as msg:
            log.my_logger('!!--!!review_deposit').error(msg)
    
    
    
    
    
    def clsoebrowser(self):
        common.close_browser()

    def quitbrowser(self):
        common.quit_browser()
            

