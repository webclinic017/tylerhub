import time
from selenium import webdriver
from other_actions import public_method

pub_method=public_method()


class commonmethod():
    """
    此模块用于封装常用方法，例如登录会员中心/登录bos等
    """
    global diriver
    #初始化函数，赋值driver对象
    def __init__(self,driver):
        self.driver=driver
    
    #切换窗口
    def switchwindows(self,n):
        self.all_handles=self.driver.window_handles
        #切换窗口
        try:
            if n<len(self.all_handles):
                self.driver.switch_to.window(self.all_handles[n]) #切换窗口
            else:
                print('{}超过窗口句柄列表下标最大值'.format(n))
        except Exception as msg:
            pub_method.log_output('!!--!!switch_windows').error(msg)


    #去除注册页弹窗
    def remove_register_topup(self):
        try:
            time.sleep(1)
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
                self.driver.find_element_by_xpath('//li[contains(.,"English")]').click()
            elif lang=='zh-hant' or lang=='繁中':
                self.driver.find_element_by_xpath('//li[contains(.,"繁體中文")]').click()
            elif lang=='ar' or lang=='阿拉伯语':
                self.driver.find_element_by_xpath('//li[contains(.,"العربية")]').click()
            elif lang=='ur' or lang=='乌尔都语':
                self.driver.find_element_by_xpath('//li[contains(.,"اردو")]').click()
            elif lang=='id' or lang=='印尼':
                self.driver.find_element_by_xpath('//li[contains(.,"Bahasa indonesia")]').click()
            elif lang=='ko' or lang=='韩语':
                self.driver.find_element_by_xpath('//li[contains(.,"한국어")]').click()
            elif lang=='th' or lang=='泰语':
                self.driver.find_element_by_xpath('//li[contains(.,"ไทย")]').click()
            elif lang=='vi' or lang=='越南语':
                self.driver.find_element_by_xpath('//li[contains(.,"Tiếng Việt")]').click()
            else:
                print('请输入正确的页面语言')
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

    #登出会员中心
    def logout_cp(self):
        try:
            time.sleep(1)
            self.driver.find_element_by_css_selector('.el-icon--right').click()
            time.sleep(1)
            self.out_ele=self.driver.find_elements_by_css_selector('.drop-sub-title')
            time.sleep(1)
            self.out_ele[-1].click()
            time.sleep(1)
            self.quit_ele=self.driver.find_elements_by_css_selector('.logout-btn-confirm')
            time.sleep(1)
            self.quit_ele[-1].click()
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!lgoout_cp').error('登出会员中心失败：{}'.format(msg))

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
