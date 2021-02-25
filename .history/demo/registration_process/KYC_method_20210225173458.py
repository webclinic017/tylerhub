import time
import os
import sys
"""跨目录调用，需要将导入的包加入sys.path中"""
path=os.path.dirname(os.path.dirname(__file__))
path=os.path.join(path,'publick')
sys.path.append(path)
from browser_actions import Commonweb
from other_actions import public_method

#实例化对象
pub_method=public_method()

#继承基本类
class kyc_approve(Commonweb):
    global driver

    #默认以谷歌浏览器执行测试用例
    def browsertype(self,browsername='Chrome'):
        self.driver=self.open_browser(browsername)

    #去除登录页弹窗
    def login_topup(self):
        try:
            self.web_click('css,.blk-sure-btn')
        except Exception as msg:
            pub_method.log_output('!!--!!topup').error('页面弹窗去除失败：{}'.format(msg))

    #访问会员中心及BOS登录页,选择页面语言
    def loginweb(self,lang):
        self.open_web('https://at-client-portal-sit.atfxdev.com/login')
        #点击弹窗
        self.login_topup()
        time.sleep(1)
        #选择页面语言
        self.cp_lang(lang)
        time.sleep(1)
        #新开窗口访问bos登录页
        self.js_openwindows('https://at-bos-frontend-sit.atfxdev.com/login')
        #切换窗口
        self.switch_iframe(1)
        #选择页面语言
        self.bos_lang(lang)
    
    #选择会员中心登录页语言
    def cp_lang(self,lang):
        try:
            self.web_click('css,.el-icon-arrow-down')
            if lang=='EN' or lang=='英语':
                self.web_click('css,.el-dropdown-menu__item')
            elif lang=='CN' or lang=='简中':
                self.web_click('css,.el-dropdown-menu__item',1)
        except Exception as msg:
            pub_method.log_output('!!--!!lang').error('cp页面语言选择错误,参数CN/EN：{}'.format(msg))

    #选择bos登录页语言
    def bos_lang(self,lang):
        try:
            if lang=='CN' or lang=='简中':
                self.web_click('css,.ivu-icon-ios-arrow-down')
                time.sleep(1)
                self.web_click('css,.ivu-select-item') #选择页面语言为中文
            else:
                pass
        except Exception as msg:
            pub_method.log_output('!!--!!lang').error('bos页面语言选择错误,参数CN/EN：{}'.format(msg)) 
   
    #登录会员中心
    def login_cp(self,lang,username,psword):
        try:
            #输入用户名
            self.web_input('css,.el-input__inner',username,1)
            time.sleep(1)
            #输入密码
            self.web_input('css,.el-input__inner',psword,3)
            time.sleep(1)
            #点击登录
            self.web_click('css,.login-btn')
        except Exception as msg:
            pub_method.log_output('!!--!!lgoin').error('登录会员中心失败：{}'.format(msg))

    #KYC认证操作
    def get_onkyc(self):
        #认证联系方式
        self.web_click('css,.el-button--primary')
        time.sleep(1)

