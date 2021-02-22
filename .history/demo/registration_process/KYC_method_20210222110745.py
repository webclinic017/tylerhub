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

    #选择登录页语言
    def lgoflgin(self,lang):
        try:
            self.web_click('css,el-icon-arrow-down')
            if lang=='EN' or lang=='英语':
                self.web_click('css,.el-dropdown-menu__item')
            elif lang=='CN' or lang=='简中':
                self.web_click('css,.el-dropdown-menu__item',1)
        except Exception as msg:
            pub_method.log_output('!!--!!lang').error('页面语言选择错误{}'.format(msg))
    
    #访问登录页
    def get_login(self,lang,username,psword):
        self.open_web('https://at-client-portal-sit.atfxdev.com/login')
        time.sleep(1)
        #选择页面语言
        self.lgoflgin(lang)
        time.sleep(1)
        #输入用户名
        self.web_input('css,.el-input__inner',username,3)
        time.sleep(1)
        #输入密码
        self.web_input('css,.el-input__inner',psword,5)
        time.sleep(1)
        #点击登录
        self.web_click('css,.login-btn',1)

