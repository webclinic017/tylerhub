import time
from selenium import webdriver
from other_actions import public_method


pub_method=public_method()

class commonmethod():
    """
    此模块用于封装常用方法，例如登录会员中心/登录bos等
    """

    #初始化函数，赋值driver对象
    def __init__(self,driver):
        self.driver=driver

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
            if lang=='简中' or lang=='简体中文':
                self.driver.find_element_by_xpath('//li[contains(.,"简体中文")]').click()
            elif lang=='EN' or lang=='英语':
                self.driver.find_element_by_xpaht('//li[contains(.,"English")]').click()
            else:
                print('选择语言为简中/英语')
        except Exception as msg:
            pub_method.log_output('!!--!!choose_register_lang').error(msg)


    