import time
import os
import sys
path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=path_demo+r'\public'
sys.path.append(path_public)
from browser_actions import Commonweb
from other_actions import public_method

class Common_method(Commonweb):
    global driver

    #去除登录页弹窗
    def login_topup(self):
        try:
            self.switch_windows(0)
            time.sleep(1)
            self.web_click('css,.blk-sure-btn')
        except Exception as msg:
            pub_method.log_output('!!--!!topup').error('页面弹窗去除失败：{}'.format(msg))

    #登录会员中心
    def logincp(self,username,psword):
        try:
            #切换窗口
            self.switch_windows(0)
            #输入用户名
            self.web_input('css,.el-input__inner',username,1)
            time.sleep(1)
            #输入密码
            self.web_input('css,.el-input__inner',psword,-1)
            time.sleep(1)
            #点击登录
            self.web_click('css,.login-btn',1)
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!lgoin_cp').error('登录会员中心失败：{}'.format(msg))

    def get(self,url):
        self.open_web(url)

