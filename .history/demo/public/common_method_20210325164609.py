import time
from selenium import webdriver
from other_actions import public_method
from browser_actions import Commonweb

pub_method=public_method()
commom=Commonweb()

class commonmethod():
    """
    此模块用于封装常用方法，例如登录会员中心/登录bos等
    """
    global diriver
    #初始化函数，赋值driver对象
    def __init__(self,driver):
        self.driver=driver
        self.driver=commom.open_browser()

    def get(url):
        commom.open_web(url)

    #去除注册页弹窗
    def remove_register_topup(self):
        try:
            self.driver.find_element_by_css_selector('.blk-sure-btn').click()
        except Exception as msg:
            pub_method.log_output('!!--!!remove_register_topup').error(msg)

    #选择会员中心页面语言
    def choose_register_lang(self,lang):
        """
        lang值为简中、简体中文、EN、EN
        """
        try:
            time.sleep(1)
            self.driver.find_element_by_css_selector('.el-icon-arrow-down').click()
            time.sleep(1)
            if lang=='简中' or lang=='CN':
                self.driver.find_element_by_xpath('//li[contains(.,"简体中文")]').click()
            elif lang=='EN' or lang=='英语':
                self.driver.find_element_by_xpaht('//li[contains(.,"English")]').click()
            else:
                print('选择语言为简中/英语')
        except Exception as msg:
            pub_method.log_output('!!--!!choose_register_lang').error(msg)

    #登录会员中心
    def login_cp(self,username,psword):
        try:
            self.eles=self.driver.find_elements_by_css_selector('.el-input__inner')
            #输入用户名
            self.eles[1].send_keys(username)
            time.sleep(1)
            self.eles[-1].send_keys(psword)
            time.sleep(1)
            self.driver.find_element_by_css_selector('.login-btn').click()
        except Exception as msg:
            pub_method.log_output('!!--!!login_cp').error(msg)


    #选择bos页面语言
    def choose_bos_lang(self,lang):
        try:
            if lang=='CN' or lang=='简中':
                self.driver.find_element_by_css_selector('.ivu-icon-ios-arrow-down').click()
                time.sleep(1)
                self.driver.find_element_by_xpath('//li[@class="ivu-select-item"]').click()
            else:
                pass
        except Exception as msg:
            pub_method.log_output('!!--!!choose_bos_lang').error(msg)

    #登录bos
    def loginbos(self,username,psword):
        try:
            self.ele_bos=self.driver.find_elements_by_css_selector('.ivu-input-default')
            time.sleep(1)
            self.ele_bos[0].send_keys(username)
            time.sleep(1)
            self.ele_bos[1].send_keys(psword)
            time.sleep(1)
            self.driver.find_element_by_css_selector('.ivu-btn-large').click() #登录
        except Exception as msg:
            pub_method.log_output('!!--!!login_bos').error(msg)

    # #根据主账号获取验证码邮箱
    # def get_code(self,account):
    #     try:
    #         self.driver.find_element_by_css_selector('.ivu-input-default').send_keys(account)
            





    