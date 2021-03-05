import sys
import os
import time
"""跨目录调用，需要将导入的包加入sys.path中"""
path=os.path.dirname(os.path.dirname(__file__))
path=os.path.join(path,'publick')
sys.path.append(path)
from browser_actions import Commonweb
from other_actions import public_method

class review_actions(Commonweb):
    
    global driver

    #默认以谷歌浏览器执行测试用例
    def browsertype(self,browsername='Chrome'):
        self.driver=self.open_browser(browsername)

    #登录bos并打开客户名单页
    def login_bos(self,username,psword):
        try:
            self.open_web('https://at-bos-frontend-sit.atfxdev.com/login')
            #选择页面语言
            self.bos_lang(lang)
            time.sleep(1)
            #输入bos用户名
            self.web_input('css,.ivu-input-default',username)
            time.sleep(1)
            #输入密码
            self.web_input('css,.ivu-input-default',psword,1)
            time.sleep(1)
            #点击登录
            self.web_click('css,.ivu-btn-large')
            time.sleep(1)
            #点击客户管理
            self.web_click('css,.ivu-badge')
            time.sleep(1)
            #点击客户名单
            self.web_click('css,.ivu-menu-item',1)
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!lgoin-bos').error('登录bos失败：{}'.format(msg))


    #选择bos登录页语言
    def bos_lang(self,lang='CN'):
        try:
            if lang=='CN' or lang=='简中':
                self.web_click('css,.ivu-icon-ios-arrow-down')
                time.sleep(1)
                self.web_click('css,.ivu-select-item') #选择页面语言为中文
            else:
                pass
        except Exception as msg:
            pub_method.log_output('!!--!!lang').error('bos页面语言选择错误,参数CN/EN：{}'.format(msg)) 

    

