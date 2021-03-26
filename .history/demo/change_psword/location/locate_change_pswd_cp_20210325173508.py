import sys
import os
import time
path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=path_demo+r'\public'
sys.path.append(path_public)
from browser_actions import Commonweb
from other_actions import public_method
from about_data import exceldata
from verification_code import time_used
from common_method import commonmethod

commom=Commonweb()


class location():
    global driver
    
    # #赋值对象driver
    def broswertype(self):
        self.driver=commom.open_browser()
        self.commethod=commonmethod(commom.open_browser())
    
    #访问cp注册页和登录bos
    def geturl(self,username,psword,lang='CN'):
        #cp
        commom.open_web('https://at-client-portal-uat.atfxdev.com/login')
        #去除弹窗
        self.remove_topup()
        #选择页面语言
        self.commethod.choose_register_lang(lang)
        time.sleep(1)
        #js打开新窗口
        commom.js_openwindows('https://at-bos-frontend-uat.atfxdev.com/login')
        time.sleep(1)
        commom.switch_windows(1)
        #页面语言，默认为简中
        self.commethod.choose_bos_lang(lang)
        time.sleep(1)
        #登录bos
        self.commethod.loginbos(username,psword)
        time.sleep(1)
        #进入客户名单页面
        commom.display_click('css,.ivu-badge')
        time.sleep(1)
        commom.display_click('css,.ivu-menu-item',1)

        
    #去除登录页弹窗
    def remove_topup(self):
        self.commethod.remove_register_topup()

    #忘记密码
    def clik(self,email):
        #忘记密码
        commom.switch_windows(0)
        time.sleep(1)
        comweb.display_click('css,div.rem-pwd-box > a')
        time.sleep(1)
        #输入邮箱
        commom.display_input('css,.el-input__inner',email)
        time.sleep(1)
        #发送验证码
        commom.display_click('css,div.b-send > .el-button')
        #获取验证码


    #获取验证码
    def get_code(self,account):
        commom.switch_windows(1)
        #输入主账户搜索
        commom.display_input('css,.ivu-input-default',account)
        time.sleep(1)
        #搜索
        commom.web_click('css,.ivu-icon-ios-search',1)
        time.sleep(1)
        #进入详情页
        commom.display_click('css,div.ivu-table-overflowX>table>tbody.ivu-table-tbody>tr>td',1)




