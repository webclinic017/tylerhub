import time
import os
import sys
path=os.path.dirname(os.path.dirname(__file__))
path=os.path.join(path,'publick')
sys.path.append(path)
from browser_actions import Commonweb
from other_actions import public_method

pub_method=public_method()
class get_account(Commonweb):
    global driver

    def __init__(self,browsername='Chrome'):
        self.driver=self.open_browser(browsername)

    def login_bos(self,username,psword,lang='CN'):
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
        except Exception as msg:
            pub_method.log_output('!!--!!login_bos').error(msg)

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

    #爬取数据并保存到本地
    def save_msg(self):
        #系统设定
        self.display_click('css,.ivu-icon-md-settings')
        #国家列表
        self.display_click('xpath,//li[@class="ivu-menu-submenu ivu-menu-opened"]//span[.="国家列表"]')
        #选择每页显示条数
        self.display_click('css,div.ivu-page-options-sizer span')
        #每页显示100条数据
        self.display_click('css,ul.ivu-select-dropdown-list>li.ivu-select-item',7)
        time.sleep(1)
        #内嵌滚动条滚到底部
        self.js_scroll_inline('class','ivu-table-overflowY','down')






if __name__=='__main__':
    get=get_account()
    get.login_bos('tyler.tang','Tl123456')
    get.save_msg()
