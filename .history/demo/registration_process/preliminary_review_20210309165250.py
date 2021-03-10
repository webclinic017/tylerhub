import sys
import os
import time
import random
"""跨目录调用，需要将导入的包加入sys.path中"""
path=os.path.dirname(os.path.dirname(__file__))
path=os.path.join(path,'publick')
sys.path.append(path)
from browser_actions import Commonweb
from other_actions import public_method

pub_method=public_method()

class review_actions(Commonweb):
    
    global driver

    #默认以谷歌浏览器执行测试用例
    def browsertype(self,browsername='Chrome'):
        self.driver=self.open_browser(browsername)

    #登录bos并打开客户名单页
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

    #输入主账号查询
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
            time.sleep(2)
            #选择审核状态
            self.display_click('css,div.ivu-dropdown-rel>button.ivu-btn-default')
            time.sleep(1)
            #成功初审
            self.display_click('css,ul.ivu-dropdown-menu>li.ivu-dropdown-item',1)
            time.sleep(1)
            if account[0:2]=='12':
                #选择账户区域
                self.display_click('css,.ivu-select-input',1)
                time.sleep(1)
                #随机选择区域
                self.display_click('css,div.ivu-select-visible>div>ul>li.ivu-select-item',random.randint(0,4))
                time.sleep(1)
            else:
                pass
            #输入随机邮编
            self.web_input('css,div.ivu-form-item-required>div>div>input',pub_method.get_purerange(6,'number'),1)
            time.sleep(1)
            #点击确定
            self.web_click('css,button.ivu-btn-primary>span>span',2)
            time.sleep(1)
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
            return self.get_text('css,div.ivu-dropdown-rel>button.ivu-btn-default>span>span')
        except Exception as msg:
            pub_method.log_output('!!--!!get_success_text').error(msg)

    def ibtype(self):
        try:
            #点击主账户信息
            self.web_click('css,.ivu-anchor-link-title',2)
            # time.sleep(1)
            # while True:
            #     if self.is_element_isdisplayed('css,div.input-item-page-enabled>div>div'):
            #         self.display_doubleclick('css,div.input-item-page-enabled>div>div')
            #         break
            #     else:
            #         continue
            # #双击代理代码
            # self.display_doubleclick('css,div.input-item-page-enabled>div>div')
            # time.sleep(1)
            # #清空默认代理代码
            # self.web_clear('css,.ivu-input-small')
            # time.sleep(1)
            # #输入随机代理代码
            # self.web_input('css,.ivu-input-small',pub_method.get_rangenum(8))
            # time.sleep(1)
            # #保存
            # self.web_click('css,.ivu-icon-md-checkmark')
            while True:
                if self.is_element_isdisplayed('css,div.input-item-page-enabled>div>div'):
                    print(1111)
                    time.sleep(1)
                    self.display_doubleclick('css,div.input-item-page-enabled>div>div')
                    break
                else:
                    continue
            # #双击代理连接
            # self.display_doubleclick('css,div.input-item-page-enabled>div>div')
            # time.sleep(1)
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
            #点击返佣申请表格
            self.web_click('css,.ivu-collapse-header',4)
            time.sleep(1)
            #打开审核开关
            self.web_click('css,.ivu-switch-default',-1)
            time.sleep(1)
            self.web_click('css,div.ivu-modal-confirm-footer > .ivu-btn-primary > span')
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