import os
import random
import sys
import time
import datetime
path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=path_demo+r'\public'
sys.path.append(path_public)
from about_data import exceldata
from browser_actions import Commonweb
from common_method import commonmethod
from other_actions import public_method

common=Commonweb()
pub_method=public_method()

"""
会员中心入金：初审通过的主账号，BOS判断主账号入金权限是否开启，再判断交易账号入金权限及MT4状态是否符合入金条件，才能入金
"""
class locations_of_deposit():

    def broswertype(self,broswername='Chrome'):
        self.driver=common.open_browser(broswername)
        self.commethod=commonmethod(self.driver)

    def get_url(self,username,psword,lang='CN'):
        try:
            common.open_web('https://at-client-portal-uat.atfxdev.com/login')
            time.sleep(1)
            #去除弹窗
            self.commethod.remove_register_topup()
            #选择页面语言
            self.commethod.choose_register_lang(lang)
            time.sleep(1)
            #登录bos进入客户名单页
            self.enter_bos(username,psword,lang)
        except Exception as msg:
            pub_method.log_output('!!--!!get_url').error(msg)

    #登录bos进入账号详情页
    def enter_bos(self,username,psword,lang='CN'):
        try:
            #新开窗口访问
            common.js_openwindows('https://at-bos-frontend-uat.atfxdev.com/login')
            time.sleep(1)
            common.switch_windows(1)
            #选择页面语言
            self.commethod.choose_bos_lang(lang)
            #登录bos
            self.commethod.loginbos(username,psword)
            time.sleep(1)
            #进入客户详情页
            common.display_click('css,.ivu-badge>span') #客户管理
            common.display_click('css,[data-old-padding-top] > [href="/client/clientListNew/:type*"]')#客户名单
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!enter_bos').error(msg)

    #进入账号详情页
    def ennter_the_details_page(self,account):
        try:
            common.switch_windows(1)
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
            common.switch_windows(2)
            time.sleep(1)
            #点击真实交易账户信息
            common.display_click('css,[href="#tdAccount"]')           
            time.sleep(5)
        except Exception as msg:
            pub_method.log_output('!!--!!serarch_account').error(msg)

    #判断交易账号是否满足入金条件
    def is_traccount_can_deposit(self,traccount):
        #判断主账号是否开启入金权限
        try:
            self.open_deposit_permissions()
            #获取入金交易账号在交易列表中的行数
            self.rows=self.where_is_traccount_bos(traccount)
            #判断交易账号状态
            self.tdaccount_status(traccount,self.rows)
            #判断交易账号入金按钮是否被勾选
            self.deposti_is_selected(traccount,self.rows)
        except Exception as msg:
            pub_method.log_output('!!--!!is_traccount_can_deposit').error(msg)
            

    #判断该主账号是否开启入金权限
    def open_deposit_permissions(self):
        try:
            if common.get_attributes('css,label.switch>span.ivu-switch>input','value',2)=='false':#获取input标签下value的属性值
                time.sleep(1)
                #开启主账号入金权限
                common.display_click('css,label.switch>span.ivu-switch',2)
                time.sleep(1)
                #确认
                common.display_click('css,.ivu-modal-confirm-footer > .ivu-btn-primary')
                time.sleep(3)
                print('开启主账号入金控制开关')
            else:
                print('主账号入金控制已开启')
        except Exception as msg:
            pub_method.log_output('!!--!!open_deposit_permissions').error(msg)

    #判断交易账户状态
    def tdaccount_status(self,traccount,row):
        try:
            time.sleep(1)
            self.account_status=common.get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/'
            'div[1]/div[2]/table/tbody/tr[{}]/td[5]/div/div/span'.format(row))
            time.sleep(1)
            if self.account_status in ('停用','Closed'):
                time.sleep(1)
                #状态为停用时，更改交易账号状态
                common.display_click('css,div.ivu-table-fixed-body>table>tbody>tr>td>div>div>div>div>a',2*row-1) #编辑
                #更改交易账号状态，改为激活或者是暂停
                time.sleep(1)
                common.display_click('css,form.ivu-form-label-right>div>div>div>div>div>div.ivu-select-selection',4)
                time.sleep(1)
                #选择暂停状态
                common.display_click('css,.ivu-select-visible .ivu-select-dropdown-list > li',1) #0:激活 1：暂停
                time.sleep(1)
                #提交表单
                common.display_click('css,button.ivu-btn-success>span',1)
                print('修改交易账号为暂停状态')
                time.sleep(1)
            else:
                print('交易账号{}状态为:{}'.format(traccount,self.account_status))
        except Exception as msg:
            pub_method.log_output('!!--!!is_tdaccount_can_deposit').error(msg)

    #判断交易账号入金按钮是否被勾选
    def deposti_is_selected(self,traccount,row):
        try:
            # 判断入金按钮是否被勾选
            time.sleep(1)
            #未勾选时
            if not common.is_element_selected('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/div[1]/div[2]/'
            'table/tbody/tr[{}]/td[6]/div/div/div/label/span/input'.format(row)):
                time.sleep(1)
                common.display_click('css,div.ivu-table-fixed-body>table>tbody>tr>td>div>div>div>div>a',2*row-1) #编辑
                time.sleep(1)
                #勾选入金权限
                common.display_click('xpath,//div[@class="checkbox ivu-form-item"]//input[@class="ivu-checkbox-input"]')
                time.sleep(1)
                #提交
                common.display_click('css,button.ivu-btn-success>span',1)
                time.sleep(1)
                print('已修改交易账号{}入金权限为勾选状态'.format(traccount))
            else:
                print('交易账号{}入金权限已勾选'.format(traccount))
        except Exception as msg:
            pub_method.log_output('!!--!!deposti_is_selected').error(msg)


    #遍历交易账号列表，获取入金账号所在行数
    def where_is_traccount_bos(self,account):
        #获取交易账号列表的总行数
        self.tdaccount_list_len=common.get_lenofelement('xpath,//*[@id="tdAccount"]/div[2]/div/div/'
        'div[3]/div[1]/div[2]/table/tbody/tr/td[1]/div/div/span')
        time.sleep(1)
        for i in range(0,self.tdaccount_list_len):
            if str(common.get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/div[1]/div[2]/'
            'table/tbody/tr/td[1]/div/div/span',i))==str(account):
                return i+1
                break

                
    def deposit_cp(self,traccount,username,psword):
        #登录会员中心
        common.switch_windows(0)
        self.commethod.login_cp(username,psword)
        time.sleep(3)
        #获取入金前交易账号余额
        self.get_before_balance(traccount)


    #遍历首页的交易账户列表，找到入金交易账户所处位置
    def where_is_traccount_cp(self,traccount):
        #获取首页交易账号列表长度
        self.len_incp=common.get_lenofelement('css,.account-number-cla')
        time.sleep(1)
        new_str=str(4)+str(traccount)
        for i in range(0,self.len_incp):
            if pub_method.extract_numbers(common.get_text('css,.account-number-cla'),i) == new_str:
                return i+1
                break
    
    #获取入金交易账号余额
    def get_before_balance(self,traccount):
        self.cprows=self.where_is_traccount_cp(traccount)
        time.sleep(1)
        self.before_balance=common.get_text('css,div.card-for-loop>div>div.el-card__body>div>p>span',4*self.cprows-4)
        print(self.before_balance)





if __name__=='__main__':
    de=locations_of_deposit()
    de.broswertype()
    de.deposit('EN','10000000027@uitest.com','Tl123456')
    
