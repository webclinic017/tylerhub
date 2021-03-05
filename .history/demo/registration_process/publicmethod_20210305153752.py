import time
import os
import sys
"""跨目录调用，需要将导入的包加入sys.path中"""
path=os.path.dirname(os.path.dirname(__file__))
path=os.path.join(path,'publick')
sys.path.append(path)
from browser_actions import Commonweb
from other_actions import public_method

pub_method=public_method()
class public(Commonweb):
    """此模块用于存放注册流程中的公共方法"""
    def login_cp(self,username,psword):
        try:
            #输入用户名
            self.web_input('css,.el-input__inner',username,1)
            time.sleep(1)
            #输入密码
            self.web_input('css,.el-input__inner',psword,3)
            time.sleep(1)
            #点击登录
            self.web_click('css,.login-btn')
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!lgoin_cp').error('登录会员中心失败：{}'.format(msg))


if __name__=='__main__':
    unittest.main()