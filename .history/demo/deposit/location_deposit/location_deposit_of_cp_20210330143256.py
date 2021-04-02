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

class locations_of_deposit():

    def broswertype(self,broswername='Chrome'):
        self.driver=common.open_browser(broswername)
        self.commethod=commonmethod(self.driver)

    def logincp(self,lang,username,psword):
        common.open_web('https://at-client-portal-uat.atfxdev.com/login')
        time.sleep(1)
        #去除弹窗
        self.commethod.remove_register_topup()
        #选择页面语言
        self.commethod.choose_register_lang(lang)
        time.sleep(1)
        #登录
        self.commethod.login_cp(username,psword)



    def deposit(self,username,psword,lang='CN'):
        #登录会员中心
        self.logincp(lang,username,psword)
        #点击入金
        time.sleep(1)
        common.display_click('css,.side-nav-cell',2)
        #判断该账号是否可以入金
        time.sleep(1)
        star=datetime.datetime.now()
        if lang=='CN' or lang=='简中':
            if common.ele_is_displayed('xpath,//div[.="该账户暂时无法入金，请联系我们的客户服务"]',2):
                print('该账号无入金权限')
            else:
                pass
        elif lang=='EN' or lang=='英语':
            if common.ele_is_displayed('xpath,//div[.="Deposit is not allow in this account, please contact our customer service"]',2):
                print('The account has no deposit permissions')
            else:
                pass
        print(datetime.datetime.now()-star)

    #开启账号入金权限
    def Open_deposit_permissions(self,username,psword,account,lang='CN'):
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
            #清空输入框
            common.web_clear('css,.ivu-input-group-with-append > [placeholder]')
            time.sleep(1)
            #输入主账号搜索
            common.display_input('css,.ivu-input-group-with-append > [placeholder]',account)
            time.sleep(1)
            common.display_click('css,.ivu-btn-icon-only > .ivu-icon')
            #进入客户详情页
            common.display_click('css,div.ivu-table-overflowX>table>tbody.ivu-table-tbody>tr>td',1)
            #切换到详情页页面
            common.switch_windows(2)
            #滑动到底部
            common.js_scroll('down')
            time.sleep(3)
            #判断该主账号是否开启入金权限
            if common.get_attributes('css,label.switch>span.ivu-switch>input','value',2)=='false':#获取input标签下value的属性值
                #开启主账号入金权限
                common.display_click('css,label.switch>span.ivu-switch',2)
                time.sleep(1)
                #确认
                common.display_click('css,.ivu-modal-confirm-footer > .ivu-btn-primary')
                time.sleep(3)
                

                


label.switch>span.ivu-switch-checked>input

if __name__=='__main__':
    de=locations_of_deposit()
    de.broswertype()
    de.deposit('EN','10000000027@uitest.com','Tl123456')
    
