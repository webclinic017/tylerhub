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
pub_method=public_method()


class location():
    global driver
    
    # #赋值对象driver
    def broswertype(self,broswername='Chrome'):
        self.driver=commom.open_browser(broswername)
        self.commethod=commonmethod(self.driver)
    
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
    def change_psword(self,email,account,newpsword):
        try:
            #忘记密码
            commom.switch_windows(0)
            time.sleep(1)
            commom.display_click('css,div.rem-pwd-box > a')
            time.sleep(1)
            #输入邮箱
            commom.web_clear('css,.el-input__inner')
            time.sleep(1)
            commom.display_input('css,.el-input__inner',email)
            time.sleep(1)
            #发送验证码
            commom.display_click('css,div.b-send > .el-button')
            #获取验证码
            self.get_code(account)
            #输入验证码
            commom.switch_windows(0)
            commom.display_input('css,.el-input__inner',self.email_code,1)
            time.sleep(1)
            #输入新密码
            commom.display_input('css,.el-input__inner',newpsword,2)
            time.sleep(1)
            #确认新密码
            commom.display_input('css,.el-input__inner',newpsword,3)
            #确认
            commom.display_click('css,form.el-form .el-form-item__content > .el-button > span')
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!change_psword').error(msg)

    #获取重置密码成功后的文本
    def sucess_change(self):
        time.sleep(1)
        self.text=commom.display_get_text('css,.succ-tips')
        time.sleep(1)
        #回到登录页
        commom.display_click('css,.b-confirm',-1)
        return self.text

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
        #点击邮件短信记录
        time.sleep(2)
        commom.switch_windows(2)
        time.sleep(1)
        commom.display_click('css,.ivu-anchor-link-title',-2)
        time.sleep(1)
        #打开验证码邮件
        commom.display_click('css,.tips',1)
        time.sleep(1)
        #获取验证码文本
        code_text=commom.get_text('xpath,//div[@class="ivu-drawer-wrap"]//tr[2]//tr[4]/td[1]/span')
        #提取验证码
        self.email_code=pub_method.extract_numbers(code_text)
        #关闭当前页面
        self.closerbrowser()
        return self.email_code


    def closerbrowser(self):
        commom.close_browser()

    def quitbroswer(self):
        commom.quit_browser()