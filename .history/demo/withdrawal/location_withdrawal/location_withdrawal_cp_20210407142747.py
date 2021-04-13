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

class location_withdrawal_incp():

    def broswertype(self,broswername='Chrome'):
        self.driver=common.open_browser(broswername)
        self.commethod=commonmethod(self.driver)

    def get_url(self,username,psword,lang='CN'):
        try:
            common.open_web('https://at-client-portal-uat.atfxdev.com/login')
            time.sleep(1)
            #去除弹窗
            self.remove_topup()
            #选择页面语言
            self.commethod.choose_register_lang(lang)
            time.sleep(1)
            #新开窗口访问bos登录页
            common.js_openwindows('https://at-bos-frontend-uat.atfxdev.com/login')
            time.sleep(1)
            common.switch_windows(1)
            #选择页面语言
            self.commethod.choose_bos_lang(lang)
            #登录bos
            self.commethod.loginbos(username,psword)
            time.sleep(1)
            #客户管理
            common.display_click('css,.ivu-badge>span')
            #客户名单
            common.display_click('css,[data-old-padding-top] > [href="/client/clientListNew/:type*"]')
        except Exception as msg:
            pub_method.log_output('!!--!!get_url').error(msg)

    #去除登录页弹窗
    def remove_topup(self):
        try:
            common.switch_windows(0)
            self.commethod.remove_register_topup()
        except Exception as msg:
            pub_method.log_output('!!--!!remove_topup').error(msg)

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
            #切换窗口
            common.switch_windows(2)
            time.sleep(1)
            #真实账户信息
            common.display_click('css,[href="#tdAccount"]')
            time.sleep(5)
        except Exception as msg:
            pub_method.log_output('!!--!!ender_detail_page').error(msg)

    #遍历BOS交易账号列表，获取入金账号所在行数
    def where_is_traccount_bos(self,traccount):
        #获取交易账号列表的总行数
        self.tdaccount_list_len=common.get_lenofelement('xpath,//*[@id="tdAccount"]/div[2]/div/div/'
        'div[3]/div[1]/div[2]/table/tbody/tr/td[1]/div/div/span')
        time.sleep(1)
        for i in range(0,self.tdaccount_list_len):
            if str(common.get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/div[1]/div[2]/'
            'table/tbody/tr/td[1]/div/div/span',i))==str(traccount):
                return i+1
                break

    #判断主账号出金权限是否开启
    def account_is_openwithdrawal(self,account):
        try:
            #账户详情页
            self.ender_detail_page(account)
            #判断出金控制按钮是否开启
            if common.get_attributes('css,label.switch>span.ivu-switch>input','value',3)=='false':#获取input标签下value的属性值
                time.sleep(1)
                #开启主账号入金权限
                common.display_click('css,label.switch>span.ivu-switch',3)
                time.sleep(1)
                #确认
                common.display_click('css,.ivu-modal-confirm-footer > .ivu-btn-primary')
                time.sleep(3)
                print('开启主账号出金控制')
            else:
                print('主账号出金控制已开启')
        except Exception as msg:
            pub_method.log_output('!!--!!account_is_openwithdrawal').error(msg)

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
            pub_method.log_output('!!--!!tdaccount_status').error(msg)    

    #判断交易账号入金按钮是否被勾选
    def deposti_is_selected(self,traccount,row):
        try:
            # 判断出金按钮是否被勾选
            time.sleep(1)
            #未勾选时
            if not common.is_element_selected('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/div[1]/div[2]/'
            'table/tbody/tr[{}]/td[6]/div/div/div/label/span/input'.format(row),1):
                time.sleep(1)
                common.display_click('css,div.ivu-table-fixed-body>table>tbody>tr>td>div>div>div>div>a',2*row-1) #编辑
                time.sleep(1)
                #勾选出金权限
                common.display_click('xpath,//div[@class="checkbox ivu-form-item"]//input[@class="ivu-checkbox-input"]',1)
                time.sleep(1)
                #提交
                common.display_click('css,button.ivu-btn-success>span',1)
                time.sleep(1)
                print('已修改交易账号{}出金权限为勾选状态'.format(traccount))
            else:
                print('交易账号{}出金权限已勾选'.format(traccount))
            #关闭页面
            self.closebrowser()
        except Exception as msg:
            pub_method.log_output('!!--!!deposti_is_selected').error(msg)











