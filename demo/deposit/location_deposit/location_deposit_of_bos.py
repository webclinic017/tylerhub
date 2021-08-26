import os
import random
import sys
import time
import datetime
path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=path_demo+r'\public'
sys.path.append(path_public)
from about_data import Aboutdata
from browser_actions import Commonweb
from common_method import Commonmethod
from randomdata import Random_data
from read_dataconfig import ReadConfig
from handlelog import MyLog

#实例化
common=Commonweb()
randomData=Random_data()
e=Aboutdata()
conFig=ReadConfig()
log=MyLog()

class Location_deposit_bos():
    """
    bos入金页面定位输入等操作
    """

    def broswertype(self,broswername='Chrome'):
        self.driver=common.open_browser(broswername)
        self.commethod=Commonmethod(self.driver)

    def get_url(self,environment,lang='CN'):
        try:
            common.open_web(conFig.get_value('bos_login', '{}'.format(environment)))
            time.sleep(1)
            self.commethod.choose_bos_lang(lang)
        except Exception as msg:
            log.my_logger('!!--!!get_url').error(msg)

    #登录bos并进入客户名单页
    def login_bos(self,username,psword):
        try:
            time.sleep(1)
            self.commethod.loginbos(username,psword)
            time.sleep(1)
            #客户管理
            common.display_click('css,.ivu-badge>span')
            #客户名单
            common.display_click('css,[data-old-padding-top] > [href="/client/clientListNew/:type*"]')
        except Exception as msg:
            log.my_logger('!!--!!login_bos').error(msg)

    #登出bos
    def logoutbos(self):
        try:
            #判断资金管理模块是展开
            if common.get_attributes('xpath,//*[@id="app"]/div/div/div[1]/div[1]/div[1]/div/ul/li[2]/ul', 'style')=='':
                common.display_click('css,.ivu-badge >span',3)
            else:
                pass
            time.sleep(1)
            common.display_click('xpath,//div[@class="scroll-content"]//li[@class="ivu-menu-item"]')
            time.sleep(2)
        except Exception as smg:
            log.my_logger('!!--!!logoutbos').error(msg)
        
    #刷新页面
    def refresh(self):
        try:
            common.general_refresh_()
        except Exception as msg:
            log.my_logger('!!--!!refresh').error(msg)

    #进入客户详情页
    def ender_detail_page(self,account):
        try:
            #清空输入框
            common.web_clear('css,.ivu-input-group-with-append > [placeholder]')
            time.sleep(1)
            #输入主账号搜索
            common.display_input('css,.ivu-input-group-with-append > [placeholder]',account)
            time.sleep(1)
            common.display_click('css,.ivu-btn-icon-only > .ivu-icon')
            time.sleep(1)
            #进入客户详情页
            common.display_click('css,div.ivu-table-overflowX>table>tbody.ivu-table-tbody>tr>td',1)
            #切换到详情页页面
            common.switch_windows(1)
            time.sleep(1)
            #点击真实交易账户信息
            common.display_click('css,[href="#tdAccount"]')
            time.sleep(2)
        except Exception as msg:
            log.my_logger('!!--!!login_bos').error(msg)

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

    
    #判断交易账号激活+暂停状态是否超过或等于5个
    def is_status_five(self):
        self.status_num=0
        for i in range(1,self.tdaccount_list_len+1):
            self.status=common.display_get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/'
            'div[1]/div[2]/table/tbody/tr[{}]/td[5]/div/div/span'.format(i))
            time.sleep(1)
            while self.status in ('暂停','激活','Suspended','Active'):
                self.status_num=self.status_num+1
                break
        print('交易账号激活+暂停状态总数为：{}'.format(self.status_num))
        return self.status_num


    #判断交易账户状态
    def tdaccount_status(self,tdaccount):
        #获取入金交易账号所在位置
        self.row=self.where_is_tdaccount_bos(tdaccount)
        #获取当前主账号下暂停+激活状态账号个数
        self.is_status_five()
        try:
            time.sleep(1)
            self.account_status=common.get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/'
            'div[1]/div[2]/table/tbody/tr[{}]/td[5]/div/div/span'.format(self.row))
            time.sleep(1)
            if self.account_status in ('停用','Closed'):
                time.sleep(1)
                #状态为停用时，更改交易账号状态
                common.display_click('css,div.ivu-table-fixed-body>table>tbody>tr>td>div>div>div>div>a',2*self.row-1) #编辑
                #更改交易账号状态，改为激活或者是暂停
                time.sleep(1)
                common.display_click('css,form.ivu-form-label-right>div>div>div>div>div>div.ivu-select-selection',4)
                time.sleep(1)
                #选择暂停状态
                common.display_click('css,.ivu-select-visible .ivu-select-dropdown-list > li',1) #0:激活 1：暂停
                time.sleep(1)
                #提交表单
                common.display_click('css,button.ivu-btn-success>span',1)
                #判断交易账户激活+暂停状态是否超过五个
                if self.status_num>=5:
                    common.display_click('xpath,//div[@class="ivu-modal-wrap"]//span',1) #去除提醒弹窗
                else:
                    pass
                print('修改交易账号为暂停状态')
                time.sleep(1)
            else:
                print('交易账号{}状态为:{}'.format(tdaccount,self.account_status))
        except Exception as msg:
            log.my_logger('!!--!!tdaccount_status').error(msg)

    #bos入金
    def deposit_action(self,account,tdaccount,amount):
        try:
            #资金管理
            common.display_click('css,.ivu-badge >span',3)
            #入金管理
            common.display_click('css,.ivu-badge >span',4)
            time.sleep(1)
            #新增
            common.display_click('css,.opration > button > span',1)
            #填写新增入金表单
            self.deposit_form(account,tdaccount,amount)
        except Exception as msg:
            log.my_logger('!!--!!deposit_action').error(msg)


    #入金表单
    def deposit_form(self,account,tdaccount,amount):
        try:
            #输入客户账号
            common.web_input('css,div>input.ivu-input',account,2)
            time.sleep(1)
            #选择交易账户
            common.display_click('css,form>div>div>div>div>div>div>div>i')
            time.sleep(1)
            common.display_click('xpath,//li[.="{}"]'.format(tdaccount))
            time.sleep(1)
            #选择入金币种
            common.display_click('css,form>div>div>div>div>div>div>div>i',1)
            time.sleep(1)
            common.display_click('xpath,//li[.="USD"]')
            time.sleep(1)
            #输入入金金额
            common.display_input('css,div>input.ivu-input',amount,5)
            time.sleep(1)
            #输入入金参考编号
            common.display_input('css,div>input.ivu-input','UITESTDeposit_'+randomData.get_rangenum(11),7)
            time.sleep(1)
            #输入备注
            common.display_input('css,[rows="2"]','UItest入金')
            time.sleep(1)
            #点击新增
            common.display_click('xpath,//div[@class="ivu-modal-wrap"]//span',3)
            time.sleep(1)
            #退出当前用户
            self.logoutbos()
        except Exception as msg:
            log.my_logger('!!--!!deposit_form').error(msg)

    #审核入金
    def review_deposit(self,username,psword,tdaccount):
        try:
            #登录新用户
            self.login_bos(username,psword)
            time.sleep(1)
            #资金管理
            common.display_click('css,.ivu-badge >span',3)
            #入金管理
            common.display_click('css,.ivu-badge >span',4)
            time.sleep(1)
            #筛选交易账号
            common.display_click('css,.ivu-select-single>div>div>i',2)
            time.sleep(1)
            common.display_click('css,.ivu-select-visible li',6)
            time.sleep(1)
            #输入交易账号
            common.display_input('css,.ivu-input-group > [placeholder]',tdaccount)
            time.sleep(1)
            #搜索
            common.display_click('css,.ivu-btn-icon-only > .ivu-icon')
            time.sleep(2)
            #勾选入金记录
            common.display_click('css,.ivu-table-tbody > tr .ivu-checkbox-input')
            time.sleep(1)
            #点击完成
            common.display_click('css,.ivu-btn-success > span')
            time.sleep(2)
            #获取完成后的文本
            print(common.display_get_text('css,.ivu-modal-confirm-body > div'))
            #点击确定
            common.web_click('css,.ivu-modal-confirm-footer span')
            time.sleep(1)
        except Exception as msg:
            log.my_logger('!!--!!review_deposit').error(msg)

    #获取审核成功后文本
    def deposit_success(self):
        try:
            time.sleep(1)
            self.successText=common.display_get_text('xpath,//*[@id="app"]/div/div/div[4]/div/div[3]/div/'
            'div[3]/div/div/div[1]/div[2]/table/tbody/tr[1]/td[3]/div/div/div/span')
            time.sleep(1)
            self.closebrowser()
            common.switch_windows(0)
            return self.successText
        except Exception as msg:
            log.my_logger('!!--!!deposit_success').error(msg)


    #用例执行
    def Deposit_bos_comply(self,account,tdaccount,username,psword,amount):
        try:
            #进入账号详情页
            self.ender_detail_page(account)
            #判断交易账号状态是否满足入金条件，如不满足，修改为满足
            self.tdaccount_status(tdaccount)
            #入金管理页面新增入金
            self.deposit_action(account,tdaccount,amount)
            #审核入金
            self.review_deposit(username,psword,tdaccount)
        except Exception as msg:
            log.my_logger('!!--!!Deposit_bos_comply').error(msg)

    def closebrowser(self):
        common.close_browser()

    def quitbrowser(self):
        common.quit_browser()
