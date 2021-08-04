import os
import random
import sys
import time

path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=path_demo+r'\public'
sys.path.append(path_public)
from about_data import Exceldata
from browser_actions import Commonweb
from common_method import Commonmethod
from other_actions import Public_method

common=Commonweb()
pub_method=Public_method()
excel=Exceldata()

class Location():
    global driver

    #赋值对象driver
    def broswertype(self,broswername='Chrome'):
        self.driver=common.open_browser(broswername)
        self.commethod=Commonmethod(self.driver)

    #访问url
    def geturl(self,username,psword,lang='CN'):
        try:
            common.open_web('https://at-client-portal-uat.atfxdev.com/login')
            #去除弹窗
            self.remove_topup()
            time.sleep(1)
            #页面语言
            self.commethod.choose_register_lang(lang)
            #新开窗口访问bos登录页
            common.js_openwindows('https://at-bos-frontend-uat.atfxdev.com/login')
            time.sleep(1)
            common.switch_windows(1)
            #选择页面语言
            self.commethod.choose_bos_lang(lang)
            #登录bos
            self.commethod.loginbos(username,psword)
            time.sleep(2)
            #进入客户名单页面
            common.display_click('css,.ivu-badge')
            time.sleep(1)
            common.display_click('css,.ivu-menu-item',1)
        except Exception as msg:
            log.my_logger('!!--!!geturl').error(msg)

    #去除登录页弹窗
    def remove_topup(self):
        try:
            self.commethod.remove_register_topup()
        except Exception as msg:
            log.my_logger('!!--!!remove_topup').error(msg)

    #登录会员中心并发送验证码
    def login_and_send_emailcode(self,username,psword):
        try:
            #登录会员中心
            common.switch_windows(0)
            time.sleep(1)
            self.commethod.login_cp(username,psword)
            time.sleep(6)
            #进入账号设定页面
            common.display_click('css,.el-icon--right.el-icon-arrow-down')
            time.sleep(1)
            common.display_click('css,.client-menu-index>span')
            time.sleep(1)
            #重设密码
            common.display_click('xpath,//div[@id="tab-third"]')
            time.sleep(1)
            #重置会员中心账号密码
            common.display_click('css,.password-page > div .opt-btn')
            time.sleep(1)
            #发送验证码
            common.display_click('css,.sendBtn>span')
            time.sleep(1)
        except Exception as msg:
            log.my_logger('!!--!!login_and_send_emailcode').error(msg)
        
    #获取验证码
    def get_emailcode(self,account):
        try:
            common.switch_windows(1)
            #输入主账户搜索
            common.web_clear('css,.ivu-input-default')
            time.sleep(1)
            common.display_input('css,.ivu-input-default',account)
            time.sleep(1)
            #搜索
            common.web_click('css,.ivu-icon-ios-search',1)
            time.sleep(1)
            #进入详情页
            common.display_click('css,div.ivu-table-overflowX>table>tbody.ivu-table-tbody>tr>td',1)
            #点击邮件短信记录
            time.sleep(2)
            common.switch_windows(2)
            time.sleep(1)
            common.display_click('css,.ivu-anchor-link-title',-2)
            time.sleep(1)
            #打开验证码邮件
            common.display_click('css,.tips',1)
            time.sleep(1)
            #获取验证码文本
            code_text=common.display_get_text('xpath,//div[@class="ivu-drawer-wrap"]//tr[2]//tr[4]/td[1]/span')
            time.sleep(1)
            #提取验证码
            self.email_code=pub_method.extract_numbers(code_text)
            time.sleep(1)
            #关闭当前页面
            self.closerbrowser()
            return self.email_code
        except Exception as msg:
            log.my_logger('!!--!!get_code').error(msg)

    #生成N为数字与大小写字母组合的随机数
    def get_psword_type(self,N):
        if 2<N<=12:
            num_str=''.join(random.sample('0123456789',N-2))
            block_letter=random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            lowser_letter=random.choice('abcdefghijklmnopqrstuvwxyz')
            self.psword=block_letter+lowser_letter+num_str
            return self.psword
        else:
            print('N必须大于2小于等于12')

    #修改密码
    def change_psword(self,username,psword,account,excelpath,column,row,N):
        try:
            #发送验证码
            self.login_and_send_emailcode(username,psword)
            #获取验证码
            self.get_emailcode(account)
            #填写验证码
            common.switch_windows(0)
            time.sleep(1)
            common.display_input('css,.el-input__inner',self.email_code,1)
            #提交
            common.display_click('css,.el-button--primary.sendBtn > span')
            time.sleep(1)
            #生成随机新密码
            self.get_psword_type(N)
            #输入新密码
            common.display_input('css,.el-input__inner',self.psword,2)
            #确认新密码
            common.display_input('css,.el-input__inner',self.psword,-1)
            time.sleep(1)
            #提交
            common.display_click('css,.save>span')
            #存储测试数据
            excel.saveainfo(excelpath,self.psword,column,row)
            time.sleep(1)
        except Exception as msg:
            log.my_logger('!!--!!change_psword').error(msg)

    #登出会员中心
    def logoutcp(self):
        self.commethod.logout_cp()

    #捕获修改成功后的文本
    def get_sucessful_change(self):
        try:
            self.sucesstext=common.display_get_text('css,.el-message__content')
            print(self.sucesstext)
            return self.sucesstext
        except Exception as smg:
            log.my_logger('!!--!!get_sucessful_change').error(msg)

    #关闭当前页面
    def closerbrowser(self):
        common.close_browser()

    #退出浏览器
    def quitbrowser(self):
        common.quit_browser()