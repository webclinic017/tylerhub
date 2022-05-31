import os
import random
import sys
import time

path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=os.path.join(path_demo,'public')
sys.path.append(path_public)
from about_data import Aboutdata
from browser_actions import Commonweb
from common_method import Commonmethod
from handlelog import MyLog
from randomdata import Random_data
from read_dataconfig import ReadConfig


class Location():
    """
    会员中心登录页改密
    """
    global driver,common,dealData,conFig,log,digital

    common=Commonweb()
    dealData=Aboutdata()
    conFig=ReadConfig()
    log=MyLog()
    digital=Random_data()
        
    #赋值对象driver
    def broswertype(self,broswername='Chrome'):
        self.driver=common.open_browser(broswername)
        self.comMethod=Commonmethod()
    
    #访问cp注册页和登录bos
    def geturl(self,environment,username,psword,lang='CN'):
        #cp,environment:uat/sit环境
        common.open_web(conFig.get_value('cp_login', '{}'.format(environment)))
        #去除弹窗
        self.remove_topup()
        #选择页面语言
        self.comMethod.choose_register_lang(common,lang)
        time.sleep(1)
        #js打开新窗口
        common.js_openwindows(conFig.get_value('bos_login', '{}'.format(environment)))
        time.sleep(1)
        common.switch_windows(1)
        #页面语言，默认为简中
        self.comMethod.choose_bos_lang(common,lang)
        time.sleep(1)
        #登录bos
        self.comMethod.loginbos(common,username,psword)
        time.sleep(1)
        #进入客户名单页面
        common.display_click('css,.ivu-badge')
        time.sleep(1)
        common.display_click('css,.ivu-menu-item',1)
        
        
    #去除登录页弹窗
    def remove_topup(self):
        common.switch_windows(0)
        self.comMethod.remove_register_topup(common)

    #忘记密码
    def change_psword(self,email,account,path,column,row):
        try:
            #忘记密码
            common.switch_windows(0)
            time.sleep(1)
            common.display_click('css,div.rem-pwd-box > a')
            time.sleep(1)
            #输入邮箱
            common.web_clear('css,.el-input__inner')
            time.sleep(1)
            common.display_input('css,.el-input__inner',email)
            time.sleep(1)
            #识别验证码
            while True:
                self.code=common.discern_code('tyler','123456','code','screenshot',"css,[width='150']")
                #填写验证码
                common.web_clear("css,[placeholder='验证码']")
                time.sleep(0.5)
                common.display_input("css,[placeholder='验证码']", self.code)
                time.sleep(0.5)
                common.display_click("xpath,//span[.='发送']")
                time.sleep(1)
                #判断验证码是否填写正确
                if common.ele_is_displayed('css,.el-form-item__error', 1):
                    continue
                else:
                    break
            time.sleep(1)
            #获取验证码
            self.get_code(account)
            #输入验证码
            common.switch_windows(0)
            common.display_input('css,.el-input__inner',self.email_code,2)
            time.sleep(1)
            #输入新密码
            self.psword=digital.get_psword_type(8)
            common.display_input('css,.el-input__inner',self.psword,3)
            time.sleep(1)
            #确认新密码
            common.display_input('css,.el-input__inner',self.psword,4)
            time.sleep(1)
            dealData.saveainfo(path,self.psword,column,row)
            #确认
            common.display_click('css,form.el-form .el-form-item__content > .el-button > span')
            time.sleep(1)
        except Exception as msg:
            log.my_logger('!!--!!change_psword').error(msg)

    #获取重置密码成功后的文本
    def sucess_change(self):
        time.sleep(1)
        self.text=common.display_get_text('css,.succ-tips')
        time.sleep(1)
        #回到登录页
        common.display_click('css,.b-confirm',-1)
        return self.text

    #获取验证码
    def get_code(self,account):
        try:
            common.switch_windows(1)
            #输入主账户搜索
            common.web_clear('css,.ivu-input-group-with-append > [placeholder]')
            time.sleep(0.5)
            common.display_input('css,.ivu-input-group-with-append > [placeholder]',account)
            time.sleep(1)
            #搜索
            common.web_click('css,.ivu-icon-ios-search',1)
            time.sleep(1)
            while True:
                if common.ele_is_displayed('css,.ivu-spin-dot', 1):
                    continue
                else:
                    break
            #进入详情页
            common.display_click('css,div.ivu-table-overflowX>table>tbody.ivu-table-tbody>tr>td',1)
            time.sleep(1)
            #点击邮件短信记录
            time.sleep(1)
            common.switch_windows(2)
            time.sleep(2)
            common.web_click("xpath,//a[.='邮件记录']")
            time.sleep(1)
            while True:
                common.display_click("xpath,//div[@class='emailRecord-page']//span[contains(.,'刷新')]")
                time.sleep(1)
                emailtext=common.get_text('css,.emailRecod-table .ivu-table-tip span')
                if not emailtext=='暂无数据':
                    break
                else:
                    continue
            time.sleep(1)
            #打开验证码邮件
            common.display_click('css,.tips',1)
            time.sleep(2)
            #获取验证码文本
            code_text=common.display_get_text('xpath,//div[@class="ivu-drawer-wrap"]//tr[2]//tr[4]/td[1]/span')
            #提取验证码
            self.email_code=digital.extract_numbers(code_text)
            #关闭当前页面
            self.closerbrowser()
            return self.email_code
        except Exception as msg:
            log.my_logger('!!--!!get_code').error(msg)


    def closerbrowser(self):
        common.close_browser()

    def quitbroswer(self):
        common.quit_browser()
