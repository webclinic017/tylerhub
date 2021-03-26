import sys
import os
import time
import random
path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=path_demo+r'\public'
sys.path.append(path_public)
from browser_actions import Commonweb
from other_actions import public_method
from common_method import commonmethod


pub_method=public_method()
excel=exceldata()
class review_actions(Commonweb):
    
    global driver

    #默认以谷歌浏览器执行测试用例
    def browsertype(self,browsername='Chrome'):
        self.driver=self.open_browser(browsername)
        self.commethd=commonmethod(self.driver)

    #登录bos并打开客户名单页
    def login_bos(self,username,psword,lang='CN'):
        try:
            self.open_web('https://at-bos-frontend-uat.atfxdev.com/login')
            #选择页面语言
            self.commethd.choose_bos_lang(lang)
            time.sleep(1)
            #登录
            self.commethd.loginbos(username,psword)
            #点击客户管理
            self.display_click('css,.ivu-badge')
            time.sleep(1)
            #点击客户名单
            self.display_click('css,.ivu-menu-item',1)
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!lgoin-bos').error('登录bos失败：{}'.format(msg))

    #初审
    def review_operation(self,account):
        try:
            #根据主账号搜索
            self.web_input('css,.ivu-input-default',account) #输入主账户
            time.sleep(1)
            self.web_click('css,.ivu-icon-ios-search',1) #点击搜索按钮
            time.sleep(1)
            #点击主账号进入账号详情页
            self.web_click('css,div.ivu-table-overflowX>table>tbody>tr>td',1)
            time.sleep(1)
            self.switch_windows(1)
            time.sleep(1)
            #IB账户
            if account[0:2]=='10':
                self.ibtype()
            else:
                pass
            #指派
            self.js_scroll('top')
            time.sleep(1)
            self.display_click('css,.ivu-btn-info')
            time.sleep(1)
            self.display_click('css,div.ivu-row-flex-center>button.ivu-btn-default')
            time.sleep(5)
            #选择审核状态
            self.display_click('css,div.ivu-dropdown-rel>button.ivu-btn-default')
            time.sleep(1)
            #成功初审
            self.display_click('css,ul.ivu-dropdown-menu>li.ivu-dropdown-item',1)
            time.sleep(1)
            #输入随机邮编
            self.web_input('css,div.ivu-form-item-required>div>div>input',pub_method.get_purerange(6,'number'),1)
            time.sleep(3)
            #点击确定
            self.web_click('css,button.ivu-btn-primary>span>span',2)
            time.sleep(2)
            self.closerweb()
        except Exception as msg:
            pub_method.log_output('!!--!!review_operation').error(msg) 

    #清空主账号搜索条件
    def clear_serach(self):
        self.switch_windows(0)
        time.sleep(1)
        self.web_clear('css,.ivu-input-default')

    #获取初审成功后的文本
    def get_success_text(self):
        try:
            #获取文本
            return self.display_get_text('css,div.ivu-dropdown-rel>button.ivu-btn-default>span>span')
            time.sleep(2)
            self.closerweb()
        except Exception as msg:
            pub_method.log_output('!!--!!get_success_text').error(msg)

    def ibtype(self):
        try:
            #移动到底部
            self.js_scroll('down')
            time.sleep(3)
            #点击返佣申请表格
            self.display_click('css,div#ibRebate > .ivu-collapse-header')
            #打开审核开关
            self.display_click('css,.ivu-switch-default',-1)
            time.sleep(2)
            self.web_click('css,div.ivu-modal-confirm-footer > .ivu-btn-primary > span')
            time.sleep(3)
            #双击代理代码
            self.display_doubleclick('css,div.input-item-page-enabled>div>div')
            time.sleep(1)
            #清空默认代理代码
            self.web_clear('css,.ivu-input-small')
            time.sleep(1)
            #输入随机代理代码
            self.display_input('css,.ivu-input-small',pub_method.get_rangenum(8))
            time.sleep(1)
            #保存
            self.web_click('css,.ivu-icon-md-checkmark')
            time.sleep(5)
            self.js_scroll('down')
            time.sleep(1)
            #双击代理连接
            self.display_doubleclick('css,div.input-item-page-enabled>div>div')
            time.sleep(1)
            #点击下拉框
            self.web_click('css,.ivu-select-input')
            time.sleep(1)
            #选择代理链接
            self.web_click('xpath,//li[.="A001"]')
            time.sleep(1)
            self.web_click('css,.ivu-icon-md-checkmark')
            time.sleep(1)
            #保存
            self.web_click('css,.ivu-icon-md-checkmark')
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!ibtype').error(msg)

    #截图
    def get_img(self,name,filename='review_failed'):
        self.get_screenpict(name,filename)

    #关闭页面
    def closerweb(self):
        self.close_browser()

    #退出浏览器
    def quitbrowser(self):
        self.quit_browser()
    
if __name__=='__main__':
    print(pub_method.get_rangenum(8))
    print(pub_method.get_purerange(8,'number'))