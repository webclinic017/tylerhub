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
e=exceldata()


class location_deposit_bos():

    def broswertype(self,broswername='Chrome'):
        self.driver=common.open_browser(broswername)
        self.commethod=commonmethod(self.driver)

    def get_url(self,lang='CN'):
        try:
            common.open_web('https://at-bos-frontend-uat.atfxdev.com/login')
            self.commethod.choose_bos_lang(lang)
        except Exception as msg:
            pub_method.log_output('!!--!!get_url').error(msg)

    #登录bos并进入客户名单页
    def login_bos(self,username,psword):
        try:
            common.switch_windows(0)
            time.sleep(1)
            self.commethod.loginbos(username,psword)
            time.sleep(1)
            #客户管理
            common.display_click('css,.ivu-badge>span')
            #客户名单
            common.display_click('css,[data-old-padding-top] > [href="/client/clientListNew/:type*"]')
        except Exception as msg:
            pub_method.log_output('!!--!!login_bos').error(msg)

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
        except Exception as msg:
            pub_method.log_output('!!--!!login_bos').error(msg)

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

    #判断交易账户状态
    def tdaccount_status(self,traccount):
        self.row=self.where_is_traccount_bos(traccount)
        try:
            time.sleep(1)
            self.account_status=common.get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/'
            'div[1]/div[2]/table/tbody/tr[{}]/td[5]/div/div/span'.format(self.row))
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