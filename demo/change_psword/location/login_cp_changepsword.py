import os
import random
import sys
import time

path_public=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'public')
sys.path.append(path_public)
from about_data import Aboutdata
from browser_actions import Commonweb
from common_method import Commonmethod
from handlelog import MyLog
from randomdata import Random_data
from read_dataconfig import ReadConfig


class Location():

    global driver,common,log,conFig,randomData,dealData

    common=Commonweb()
    log=MyLog()
    dealData=Aboutdata()
    conFig=ReadConfig()
    randomData=Random_data()

    #赋值对象driver
    def broswertype(self,broswername='Chrome'):
        self.driver=common.open_browser(broswername)
        self.commeThod=Commonmethod(self.driver)

    #访问url
    def geturl(self,environment,username,psword,lang='CN'):
        try:
            #cp
            common.open_web(conFig.get_value('cp_login', '{}'.format(environment)))
            #去除弹窗
            self.remove_topup()
            time.sleep(1)
            #页面语言
            self.commeThod.choose_register_lang(lang)
            #新开窗口访问bos登录页
            common.js_openwindows(conFig.get_value('bos_login', '{}'.format(environment)))
            time.sleep(1)
            common.switch_windows(1)
            #选择页面语言
            self.commeThod.choose_bos_lang(lang)
            #登录bos
            self.commeThod.loginbos(username,psword)
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
            self.commeThod.remove_register_topup()
        except Exception as msg:
            log.my_logger('!!--!!remove_topup').error(msg)

    #登录会员中心并发送验证码
    def login_and_send_emailcode(self,username,psword):
        try:
            #登录会员中心
            common.switch_windows(0)
            time.sleep(1)
            self.commeThod.login_cp(username,psword)
            time.sleep(2)
            #判断页面是否加载完成
            while True:
                if common.ele_is_displayed("css,[src='/static/img/loading.webm']",1):
                    continue
                else:
                    break
            time.sleep(1)
            while True:
                self.loading_attributes=common.get_attributes('css,.el-loading-mask', 'style')
                if 'none' in self.loading_attributes:
                    break
                else:
                    continue
            time.sleep(1)            
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
                elif common.ele_is_displayed("xpath,//div[@class='content']//div[@class='captcha']//div[3]", 1):
                    continue
                else:
                    break
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
            while True:
                if common.ele_is_displayed('css,.ivu-spin-dot', 1):
                    continue
                else:
                    break
            #进入详情页
            common.display_click('css,div.ivu-table-overflowX>table>tbody.ivu-table-tbody>tr>td',1)
            #点击邮件短信记录
            time.sleep(1)
            common.switch_windows(2)
            time.sleep(1)
            common.display_click("xpath,//a[.='邮件记录']")
            time.sleep(0.5)
            while True:
                common.display_click("xpath,//div[@class='emailRecord-page']//span[contains(.,'刷新')]")
                time.sleep(1)
                emailtext=common.get_text('css,.emailRecod-table .ivu-table-tip span')
                if not emailtext=='暂无数据':
                    break
                else:
                    continue
            time.sleep(1)
            common.web_click('css,.tips',1)
            time.sleep(1)
            #获取验证码文本
            code_text=common.display_get_text("css,[bgcolor='#ffffff'][width='598'] span")
            time.sleep(1)
            #提取验证码
            self.email_code=randomData.extract_numbers(code_text)
            time.sleep(1)
            #关闭当前页面
            self.closerbrowser()
            return self.email_code
        except Exception as msg:
            log.my_logger('!!--!!get_code').error(msg)

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
            common.display_input('css,.el-input__inner',self.email_code,2)
            #提交
            common.display_click('css,.el-button--primary.sendBtn > span')
            time.sleep(1)
            #生成随机新密码
            self.newpsword=randomData.get_psword_type(8)
            #输入新密码
            common.display_input("css,[placeholder='新密码']",self.newpsword)
            time.sleep(0.5)
            #确认新密码
            common.display_input("css,[placeholder='再次确认新密码']",self.newpsword)
            time.sleep(1)
            #提交
            common.display_click('css,.save>span')
            time.sleep(1)
            #存储测试数据
            dealData.saveainfo(excelpath,self.newpsword,column,row)
            time.sleep(1)
        except Exception as msg:
            log.my_logger('!!--!!change_psword').error(msg)

    #登出会员中心
    def logoutcp(self):
        self.commeThod.logout_cp()

    #捕获修改成功后的文本
    def get_sucessful_change(self):
        try:
            time.sleep(1)
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