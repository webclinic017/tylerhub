import os
import random
import sys
import time

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

class locathion_of_transfer():

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

    #登录页弹窗
    def remove_topup(self):
        try:
            self.commethod.remove_register_topup()
        except Exception as msg:
            pub_method.log_output('!!--!!remove_topup').error(msg)

    def ender_detail_page(self,account):
        try:
            #清空输入框
            common.switch_windows(1)
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
            #主账户信息
            common.display_click('css,[href="#masterAccount"]')
            time.sleep(10)
        except Exception as msg:
            pub_method.log_output('!!--!!ender_detail_page').error(msg)

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
    
    #判断主账号是IB/CL账号
    def type_is_ib(self,account):
        if int(float(str(account)[0:2]))==10:
            print('主账号为IB账号')
            return True
        else:
            print('主账号为CL账号')
            return False

    #判断交易账号是否为返佣账号
    def tdaccount_to_is_rebate(self,tdaccount):
        try:
            #获取IB账号下的返佣账号
            self.rebate_tdaccount=common.display_get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]'
            '/div[1]/div[2]/table/tbody/tr/td[1]/div/div/span',-2)
            print('该账号返佣账户为{}'.format(self.rebate_tdaccount))
            if str(tdaccount)==str(self.rebate_tdaccount):
                print('转入交易账号为返佣账号，转账类型为非返佣转返佣')
                return True
            else:
                print('转入交易账号为非返佣账户')
                return False
        except Exception as msg:
            pub_method.log_output('!!--!!tdaccount_to_is_rebate').error(msg)

    #判断转账账户类型是否满足转账给下级逻辑
    def is_account_satisfy_logic(self,account_from):
        try:
            #判断转出主账户是否为返佣账号
            if self.type_is_ib(account_from):
                print('转出主账户为IB，继续执行用例')
                return False
            else:
                return True
        except Exception as msg:
            pub_method.log_output('!!--!!is_account_satisfy_logic').error(msg)