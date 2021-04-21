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

class location_of_transfer():

    def broswertype(self,broswername='Chrome'):
        self.driver=common.open_browser(broswername)
        self.commethod=commonmethod(self.driver)

    def get_url(self,username,psword,lang='CN'):
        try:
            common.open_web('https://at-bos-frontend-uat.atfxdev.com/login')
            time.sleep(1)
            self.commethod.choose_bos_lang(lang)
            time.sleep(1)
            self.commethod.loginbos(username,psword)
            #客户管理
            common.display_click('css,.ivu-badge>span')
            time.sleep(1)
            #客户名单
            common.display_click('css,[data-old-padding-top] > [href="/client/clientListNew/:type*"]')
        except Exception as msg:
            pub_method.log_output('!!--!!get_url').error(msg)

    #进入客户详情页
    def ender_detail_page(self,account):
        try:
            #清空输入框
            common.switch_windows(0)
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
            common.switch_windows(1)
            time.sleep(1)
            #主账户信息
            common.display_click('css,[href="#masterAccount"]')
            time.sleep(7)
        except Exception as msg:
            pub_method.log_output('!!--!!ender_detail_page').error(msg)

    #判断主账号转账控制是否开启
    def transfer_control_on(self,account):
        try:
            #账户详情页
            self.ender_detail_page(account)
            if common.get_attributes('css,label.switch>span.ivu-switch>input','value',-1)=='false':
                time.sleep(1)
                #开启转账控制权限
                common.display_click('css,label.switch>span.ivu-switch',-1)
                time.sleep(1)
                #确定
                common.display_click('css,.ivu-modal-confirm-footer > .ivu-btn-primary')
                print('开启主账号转账控制')
            else:
                print('主账号转账控制已开启')
                pass
            #真实账户信息
            common.display_click('css,[href="#tdAccount"]')
        except Exception as msg:
            pub_method.log_output('!!--!!transfer_control_on').error(msg)




