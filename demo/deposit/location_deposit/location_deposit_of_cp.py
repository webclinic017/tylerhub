import os
import random
import sys
import time
import datetime
path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=os.path.join(path_demo,'public')
sys.path.append(path_public)
from about_data import Aboutdata
from browser_actions import Commonweb
from common_method import Commonmethod
from randomdata import Random_data
from handlelog import MyLog
from read_dataconfig import ReadConfig


class Locations_of_deposit(object):
    """
    会员中心入金：初审通过的主账号，BOS判断主账号入金权限是否开启，再判断交易账号入金权限及MT4状态是否符合入金条件，才能入金
    """
    global common,randomData,dealData,log,conFig

    common=Commonweb()
    randomData=Random_data()
    dealData=Aboutdata()
    log=MyLog()
    conFig=ReadConfig()


    def broswertype(self,broswername='Chrome'):
        self.driver=common.open_browser(broswername)
        self.comMethod=Commonmethod()

    def get_url(self,environment,lang='CN'):
        try:
            common.open_web(conFig.get_value('cp_login', '{}'.format(environment)))
            time.sleep(1)
            #去除弹窗
            self.comMethod.remove_register_topup(common)
            #选择页面语言
            self.comMethod.choose_register_lang(common,lang)
            time.sleep(1)
            #新开窗口访问bos登录页
            common.js_openwindows(conFig.get_value('bos_login', '{}'.format(environment)))
            time.sleep(1)
            common.switch_windows(1)
            #选择页面语言
            self.comMethod.choose_bos_lang(common,lang)
        except Exception as msg:
            log.my_logger('!!--!!get_url').error(msg)

    #登录bos
    def login_bos(self,username,psword):
        try:
            common.switch_windows(1)
            time.sleep(1)
            self.comMethod.loginbos(common,username,psword)
            #判断页面是否加载完成
            while True:
                if common.ele_is_displayed('css,.ivu-spin-dot', 1):
                    continue
                else:
                    break
        except Exception as msg:
            log.my_logger('!!--!!login_bos').error(msg)


    #去除登录页弹窗
    def remove_topup(self):
        try:
            common.switch_windows(0)
            self.comMethod.remove_register_topup(common)
        except Exception as msg:
            log.my_logger('!!--!!remove_topup').error(msg)


    #进入账号详情页
    def ennter_the_details_page(self,account):
        try:
            common.switch_windows(1)
            #进入客户详情页
            common.display_click('css,.ivu-badge>span') #客户管理
            time.sleep(1)
            common.display_click('css,[data-old-padding-top] > [href="/client/clientListNew/:type*"]')#客户名单
            time.sleep(1)
            #清空输入框
            common.web_clear('css,.ivu-input-group-with-append > [placeholder]')
            time.sleep(1)
            #输入主账号搜索
            common.display_input('css,.ivu-input-group-with-append > [placeholder]',account)
            time.sleep(1)
            common.display_click('css,.ivu-btn-icon-only > .ivu-icon')
            time.sleep(1)
            while True:
                if common.ele_is_displayed('css,.ivu-spin-dot', 1):
                    continue
                else:
                    break
            #进入客户详情页
            common.display_click('css,div.ivu-table-overflowX>table>tbody.ivu-table-tbody>tr>td',1)
            #切换到详情页页面
            common.switch_windows(2)
            time.sleep(1)
            while True:
                if common.ele_is_displayed('css,.spin-icon-load', 1):
                    continue
                else:
                    break
            #主账户信息
            common.display_click('css,[href="#masterAccount"]')       
            time.sleep(2)
        except Exception as msg:
            log.my_logger('!!--!!serarch_account').error(msg)

    #判断该主账号是否开启入金权限
    def open_deposit_permissions(self,account):
        try:
            #进入账号详情页
            self.ennter_the_details_page(account)
            time.sleep(1)

            if common.get_attributes('css,label.switch>span.ivu-switch>input','value',2)=='false':#获取input标签下value的属性值
                time.sleep(1)
                #开启主账号入金权限
                common.display_click('css,label.switch>span.ivu-switch',2)
                time.sleep(1)
                #确认
                common.display_click('css,.ivu-modal-confirm-footer > .ivu-btn-primary')
                time.sleep(1)
                while True:
                    if common.ele_is_displayed('css,.spin-icon-load', 1):
                        continue
                    else:
                        break
                print('开启主账号入金控制开关')
            else:
                print('主账号入金控制已开启')
            
            if common.get_attributes('css,label.switch>span.ivu-switch>input','value',1)=='false':#获取input标签下value的属性值
                time.sleep(1)
                #开启主账号登录会员中心权限
                common.display_click('css,label.switch>span.ivu-switch',1)
                time.sleep(1)
                #确认
                common.display_click('css,.ivu-modal-confirm-footer > .ivu-btn-primary')
                time.sleep(1)
                while True:
                    if common.ele_is_displayed('css,.spin-icon-load', 1):
                        continue
                    else:
                        break
                print('开启主账号登录会员中心权限')
            else:
                print('主账号登录会员中心权限已开启')
            #真实账户信息
            common.display_click('css,[href="#tdAccount"]')
        except Exception as msg:
            log.my_logger('!!--!!open_deposit_permissions').error(msg)


    # #判断交易账号激活+暂停状态是否超过或等于5个
    # def is_status_five(self):
    #     self.status_num=0
    #     for i in range(1,self.tdaccount_list_len+1):
    #         self.status=common.display_get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/'
    #         'div[1]/div[2]/table/tbody/tr[{}]/td[5]/div/div/span'.format(i))
    #         while self.status in ('暂停','激活','Suspended','Active'):
    #             self.status_num=self.status_num+1
    #             break
    #     return self.status_num

    #遍历BOS交易账号列表，获取入金账号所在行数
    def where_is_tdaccount_bos(self,tdaccount):
        #获取交易账号列表的总行数
        self.tdaccount_list_len=common.get_lenofelement('xpath,//*[@id="tdAccount"]/div[2]/div/div/'
        'div[3]/div[1]/div[2]/table/tbody/tr/td[2]/div/span')
        time.sleep(1)
        for i in range(0,self.tdaccount_list_len):
            if str(common.get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/div[1]/div[2]/'
            'table/tbody/tr/td[1]/div/div/span',i))==str(tdaccount):
                return i+1
                break
    
    
   #判断交易账户状态
    def tdaccount_status(self,tdaccount,row):

        try:
            time.sleep(1)
            self.account_status=common.get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/'
            'div[1]/div[2]/table/tbody/tr[{}]/td[5]/div/div/span'.format(row))
            time.sleep(1)
            if self.account_status in ('停用','Closed'):
                time.sleep(1)
                #状态为停用时，更改交易账号状态
                common.display_click('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[{}]/td[1]/div/div/div/div/a[2]'.format(row)) #编辑
                #更改交易账号状态，改为激活或者是暂停
                time.sleep(2)
                common.display_click('css,form.ivu-form-label-right>div>div>div>div>div>div.ivu-select-selection',4)
                time.sleep(1)
                #选择激活状态
                common.display_click('css,.ivu-select-visible .ivu-select-dropdown-list > li') #0:激活 1：暂停
                time.sleep(1)
                #提交表单
                common.display_click('css,button.ivu-btn-success>span',1)
                time.sleep(3)

                #交易账户激活+暂停状态是否超过五个或未满足入金条件
                while True:
                    try:
                        if common.ele_is_displayed("xpath,//div[@class='ivu-modal-wrap']//span[.='确定']", 1):
                            common.display_click("xpath,//div[@class='ivu-modal-wrap']//span[.='确定']")
                            time.sleep(1.5)
                            continue
                        else:
                            break
                    except:
                        pass


                while True:
                    if common.ele_is_displayed('css,.spin-icon-load', 1):
                        continue
                    else:
                        break
                print('交易账号{}状态更改为激活'.format(tdaccount))
                return True
            elif self.account_status in ('Synchronizing','同步中'):
                print('交易账号{}状态为:{}'.format(tdaccount,self.account_status))
                self.closebrowser()
                self.logoutbos()
                return False
            else:
                print('交易账号{}状态为:{}'.format(tdaccount,self.account_status))
                return True
        except Exception as msg:
            log.my_logger('!!--!!tdaccount_status').error(msg)

    
    #判断交易账号入金按钮是否被勾选
    def deposti_is_selected(self,tdaccount,row):
        try:
            # 判断入金按钮是否被勾选
            time.sleep(1)
            #未勾选时
            if not common.is_element_selected('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/div[1]/'
            'div[2]/table/tbody/tr[{}]/td[8]/div/div/div/label/span/input'.format(row)):
                time.sleep(1)
                common.display_click('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/div[1]/div[4]/div[2]/table/tbody/tr[{}]/td[1]/div/div/div/div/a[2]'.format(row)) #编辑
                time.sleep(1)
                #勾选入金权限
                common.display_click('xpath,//div[@class="checkbox ivu-form-item"]//input[@class="ivu-checkbox-input"]')
                time.sleep(1)
                #提交
                common.display_click('css,button.ivu-btn-success>span',1)
                time.sleep(2)
                #交易账户激活+暂停状态是否超过五个或未满足入金条件
                while True:
                    try:
                        if common.ele_is_displayed("xpath,//div[@class='ivu-modal-wrap']//span[.='确定']", 1):
                            common.display_click("xpath,//div[@class='ivu-modal-wrap']//span[.='确定']")
                            time.sleep(1.5)
                            continue
                        else:
                            break
                    except:
                        pass


                while True:
                    if common.ele_is_displayed('css,.spin-icon-load', 1):
                        continue
                    else:
                        break
                print('已修改交易账号{}入金权限为勾选状态'.format(tdaccount))
            else:
                print('交易账号{}入金权限已勾选'.format(tdaccount))
            #关闭页面
            self.closebrowser()
        except Exception as msg:
            log.my_logger('!!--!!deposti_is_selected').error(msg)



    #遍历会员中心首页的交易账户列表，找到入金交易账户所处位置
    def where_is_traccount_cp(self,tdaccount):
        #获取首页交易账号列表长度
        self.len_incp=common.get_lenofelement('css,.account-number-cla')
        time.sleep(1)
        new_str=str(4)+str(tdaccount)
        for i in range(0,self.len_incp):
            if randomData.extract_numbers(common.get_text('css,.account-number-cla',i)) == new_str:
                return i+1
                break
    
    #获取入金交易账号余额
    def get_traccount_balance(self,tdaccount):
        try:
            self.cprows=self.where_is_traccount_cp(tdaccount)
            time.sleep(1)
            self.balance=common.display_get_text('xpath,//*[@id="bodyBgImg"]/div[1]/div[3]/div[2]/div[2]/div/div[1]/div[4]/div[1]/div[2]/div/div[1]/div/div/div[{}]/div[1]/div/div[4]/p/span[1]'.format(3+self.cprows))
            return self.balance
        except Exception as msg:
            log.my_logger('!!--!!get_traccount_balance').error(msg)

    #入金
    def deposit_actions(self,tdaccount,amount):
        try:
            #点击入金
            common.display_click("xpath,//span[.='入金']")
            time.sleep(1)
            while True:
                if 'none' in common.get_attributes('css,.el-loading-mask','style'):
                    break
                else:
                    continue
                
            #选择电子钱包neteller方式入金
            common.display_click('css,[title="电子钱包 Neteller"]')
            time.sleep(2)
            #选择交易账号
            common.display_click('xpath,//div[@class="el-input el-input--suffix"]/input[@class="el-input__inner"]')
            time.sleep(1)
            #选择入金账号
            common.display_click('xpath,//span[.="MT4 - {}(USD)"]'.format(tdaccount))
            time.sleep(0.5)
            common.web_input("css,[placeholder='请输入金金额']",amount)
            time.sleep(0.5)
            #输入随机邮箱
            common.web_input("css,[placeholder='请输入邮箱']",randomData.get_rangenemail(8))
            time.sleep(0.5)
            #确认提交
            common.display_click('css,.common-btn > span')
            time.sleep(2)
            #去除手续费弹窗
            if common.ele_is_displayed('css,.ok > span', 1):
                common.display_click('css,.ok > span')

            #勾选入金须知
            time.sleep(1)
            common.display_click('css,.el-checkbox__inner')
            time.sleep(0.5)
            #确认提交
            common.display_click('css,.el-button--info > span')
            time.sleep(1)
            common.switch_windows(0)
            while True:
                if common.ele_is_displayed('css,.el-icon-loading', 1):
                    continue
                else:
                    break
            
            print(common.display_get_text('css,.deposit-title-info'))
            #回到首页
            common.display_click('css,.menu .el-menu')
            #切换窗口，关闭页面
            common.switch_windows(2)
            self.closebrowser()
        except Exception as msg:
            log.my_logger('!!--!!deposit_actions').error(msg)

    
    #BOS审核入金请求
    def review_deposit(self,bos_username,bos_psword,tdaccount,path,column2,row):
        try:
            common.switch_windows(1)
            #资金管理
            common.display_click('css,.ivu-badge >span',3)
            #入金管理
            common.display_click('css,.ivu-badge >span',4)
            time.sleep(1)
            #筛选状态
            common.display_click('css,.ivu-select-multiple > .ivu-select-selection > div > .ivu-icon')
            time.sleep(0.5)
            #选择验证中状态
            common.display_click("xpath,//li[.='验证中']")
            time.sleep(1)
            #筛选交易账号
            common.display_doubleclick('css,.ivu-select-single>div>div>i',2)
            time.sleep(0.5)
            common.display_click("xpath,//li[.='交易账号']")
            time.sleep(1)
            #输入交易账号
            common.web_clear('css,.ivu-input-group > [placeholder]')
            time.sleep(0.5)
            common.display_input('css,.ivu-input-group > [placeholder]',tdaccount)
            time.sleep(1)
            #搜索
            common.display_click('css,.ivu-btn-icon-only > .ivu-icon')
            time.sleep(2)
            while True:
                if common.ele_is_displayed("xpath,//span[.='暂无数据']", 1):
                    continue
                else:
                    break
            #勾选入金记录
            common.display_click('css,.ivu-table-tbody > tr .ivu-checkbox-input')
            time.sleep(1)
            while True:
                if common.ele_is_displayed('css,.ivu-spin-dot', 1):
                    continue
                else:
                    break
            #转未处理
            common.display_click("xpath,//span[.='转未处理']")
            time.sleep(1)
            #登出bos
            self.logoutbos()
            self.comMethod.loginbos(common,bos_username,bos_psword)
            time.sleep(1)
            #判断页面是否加载完成
            while True:
                if common.ele_is_displayed('css,.ivu-spin-dot', 1):
                    continue
                else:
                    break
            #资金管理
            common.display_click('css,.ivu-badge >span',3)
            #入金管理
            common.display_click('css,.ivu-badge >span',4)
            #筛选交易账号
            common.display_click('css,.ivu-select-single>div>div>i',2)
            time.sleep(1)
            common.display_click("xpath,//li[.='交易账号']")
            time.sleep(1)
            #输入交易账号
            common.web_clear('css,.ivu-input-group > [placeholder]')
            time.sleep(0.5)
            common.display_input('css,.ivu-input-group > [placeholder]',tdaccount)
            time.sleep(1)
            #搜索
            common.display_click('css,.ivu-btn-icon-only > .ivu-icon')
            time.sleep(1)
            while True:
                if common.ele_is_displayed("xpath,//span[.='暂无数据']", 1):
                    continue
                else:
                    break
            time.sleep(2)
            common.display_click('css,.ivu-table-tbody > tr .ivu-checkbox-input')
            time.sleep(2)
            #处理完成
            common.display_click('css,.ivu-btn-success > span')
            time.sleep(1)
            while True:
                if common.ele_is_displayed('css,.ivu-spin-dot', 1):
                    continue
                else:
                    break
            #获取入金完成文本
            print(common.display_get_text('css,.ivu-modal-confirm-body > div'))
            #点击确定
            common.web_click('css,.ivu-modal-confirm-footer span')
            time.sleep(1)
            #回到会员中心首页，获取入金成功后的余额
            common.switch_windows(0)
            time.sleep(1)
            #刷新余额
            common.display_click("xpath,//div[@id='tab-live']")
            time.sleep(0.5)
            while True:
                if 'none' in common.get_attributes('css,.el-loading-mask', 'style'):
                    break
                else:
                    continue
            time.sleep(0.5)
            #获取交易账户余额
            print('交易账号{}入金后余额为:{}'.format(tdaccount,self.get_traccount_balance(tdaccount)))
            dealData.saveainfo(path,self.balance,column2,row)
        except Exception as msg:
            log.my_logger('!!--!!review_deposit').error(msg)

    #判断交易账号是否满足入金条件
    def is_traccount_can_deposit(self,account,tdaccount):
        """
        判断主账号及交易账号是否满足入金条件
        如不满足，修改为满足
        """
        try:
            #判断主账号是否开启入金权限
            self.open_deposit_permissions(account)
            #获取入金交易账号在交易列表中的行数
            self.rows=self.where_is_tdaccount_bos(tdaccount)
            #判断交易账号状态
            if self.tdaccount_status(tdaccount,self.rows):
                #判断交易账号入金按钮是否被勾选
                self.deposti_is_selected(tdaccount,self.rows)
                return True
            else:
                return False
        except Exception as msg:
            log.my_logger('!!--!!is_traccount_can_deposit').error(msg)


    def deposit_cp(self,tdaccount,username,psword,amount,bos_username,bos_psword,path,column1,column2,row):
        """
        满足入金条件后，会员中心入金并审核
        """
        try:
            #登录会员中心
            common.switch_windows(0)
            self.comMethod.login_cp(common,username,psword)
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
            #获取入金前交易账号余额
            print('交易账号 {} 入金前账号余额为： {}'.format(tdaccount,self.get_traccount_balance(tdaccount)))
            dealData.saveainfo(path,self.balance,column1,row)
            #入金
            self.deposit_actions(tdaccount,amount)
            #bos审核入金
            self.review_deposit(bos_username,bos_psword,tdaccount,path,column2,row)
            #登出cp
            self.logoutcp()
        except Exception as msg:
            log.my_logger('!!--!!deposit_cp').error(msg)

    #登出会员中心
    def logoutcp(self):
        try:
            common.switch_windows(0)
            self.comMethod.logout_cp(common)
        except Exception as msg:
            log.my_logger('!!--!!logoutcp').error(msg)

    #获取审核成功后文本
    def deposit_success(self):
        try:
            common.switch_windows(1)
            time.sleep(1)
            self.successText=common.display_get_text("xpath,//span[@class='tips']")
            time.sleep(1)
            #登出bos
            self.logoutbos()
            return self.successText
        except Exception as msg:
            log.my_logger('!!--!!deposit_success').error(msg)

    #登出bos
    def logoutbos(self):
        try:
            common.switch_windows(1)
            time.sleep(1)
            #判断资金管理模块是展开
            if common.get_attributes('xpath,//*[@id="app"]/div/div/div[1]/div[1]/div[1]/div/ul/li[2]/ul', 'style')=='':
                common.display_click('css,.ivu-badge >span',3)
            else:
                pass
            time.sleep(1)
            common.display_click('xpath,//div[@class="scroll-content"]//li[@class="ivu-menu-item"]')
            time.sleep(1)
        except Exception as smg:
            log.my_logger('!!--!!logoutbos').error(msg)

    def closebrowser(self):
        common.close_browser()

    def quitbrowser(self):
        common.quit_browser()