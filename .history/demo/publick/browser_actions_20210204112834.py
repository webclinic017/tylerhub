from selenium import webdriver
import time
from other_actions import *
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

#实例化公共方法模块
pub_method=public_method()
"""此模块用于存放浏览器相关操作方法"""

class Commonweb():
    """浏览器驱动，访问url等自定义基类方法"""
    #定义全局变量
    global driver

    def __init__(self,browsername='Chrome'):

        try:

            if browsername=='firefox' or browsername=='Firefox' or browsername=='fx': #火狐浏览器
                #配置浏览器
                options=webdriver.FirefoxOptions()
                #设置浏览器配置
                options.add_argument('lang=zh_CN.UTF-8') #初始化浏览器默认编码格式
                options.add_argument('--incognito') #无痕模式
                options.add_argument('--start-maximized') #浏览器全频
                self.driver=webdriver.Firefox(firefox_options=options) #添加配置
                self.driver.implicitly_wait(20) #隐式等待20s
            elif browsername=='chrome' or browsername=='Chrome':
                #配置浏览器
                options=webdriver.ChromeOptions()
                #设置浏览器配置
                options.add_argument('lang=zh_CN.UTF-8') #初始化浏览器默认编码格式
                options.add_argument('--incognito') #无痕模式
                options.add_argument('--start-maximized') #浏览器全频
                self.driver=webdriver.Chrome(chrome_options=options)#添加配置
                self.driver.implicitly_wait(20) #隐式等待20s
            else:
                pub_method.log_output('!!--!!driver_browser').info('没有找到这种浏览器驱动，你可以尝试输入firefox、Firefox、fx、chrome、Chrome')
            return self.driver
        except Exception as msg:
            pub_method.log_output('!!--!!driver_name'
    # def open_browser(self,browsername='Chrome'):
    #     """打开浏览器，浏览器名称：Firefox，Chrome，默认以谷歌浏览器打开"""
    #     try:
    #         if browsername=='firefox' or browsername=='Firefox' or browsername=='fx': #火狐浏览器
    #             #配置浏览器
    #             options=webdriver.FirefoxOptions()
    #             #设置浏览器配置
    #             options.add_argument('lang=zh_CN.UTF-8') #初始化浏览器默认编码格式
    #             options.add_argument('--incognito') #无痕模式
    #             options.add_argument('--start-maximized') #浏览器全频
    #             self.driver=webdriver.Firefox(firefox_options=options) #添加配置
    #             self.driver.implicitly_wait(20) #隐式等待20s
    #         elif browsername=='chrome' or browsername=='Chrome':
    #             #配置浏览器
    #             options=webdriver.ChromeOptions()
    #             #设置浏览器配置
    #             options.add_argument('lang=zh_CN.UTF-8') #初始化浏览器默认编码格式
    #             options.add_argument('--incognito') #无痕模式
    #             options.add_argument('--start-maximized') #浏览器全频
    #             self.driver=webdriver.Chrome(chrome_options=options)#添加配置
    #             self.driver.implicitly_wait(20) #隐式等待20s
    #         else:
    #             pub_method.log_output('!!--!!driver_browser').info('没有找到这种浏览器驱动，你可以尝试输入firefox、Firefox、fx、chrome、Chrome')
    #         return self.driver
    #     except Exception as msg:
    #         pub_method.log_output('!!--!!driver_name').error('启动浏览器异常{}'.format(msg))
    def a(self):
        print(5)
    #访问url
    def open_web(self,url):
        try:
            self.driver.get(url)
        except Exception as msg:
            pub_method.log_output('!!--!!url_error').warning('请输入正确的域名'.format(msg))

    #自定义查找页面元素
    def find_elements(self,locator):
        """
        locator:变量格式为‘定位方法，属性的值’例：css,.kw;class,kw
        """
        #切片locator变量的值
        method,values=locator.split(',',maxsplit=1)
        try:
            if 'css' in method:
                return self.driver.find_elements_by_css_selector(values) #css定位
            elif 'xpath' in method:
                return self.driver.find_elements_by_xpath(values) #xpath定位
            elif 'name' in method:
                return self.driver.find_elements_by_name(values) #name定位
            elif 'id' in method:
                return self.driver.find_elements_by_id(values) #id定位
            elif 'class' in method:
                return self.driver.find_elements_by_class_name(values) #class定位
            elif 'partial' and 'link' in method:
                return self.driver.find_elements_by_partial_link_text(values) #部分文本定位
            elif 'link' in method:
                return self.driver.find_elements_by_link_text(values) #全部文本定位
            elif 'tag' in method:
                return self.driver.find_elements_by_tag_name(values) #通过标签名定位
            else:
                pub_method.log_output('!!--!!location_element').info('定位方法错误')
        except Exception as msg:
            pub_method.log_output('!!--!!find_elements').error('元素不存在或者不可见：{}'.format(msg))

    #判断页面元素是否唯一,若唯一，取第一个值，若不唯一，取第*个值
    def find_element(self,locator,index=0):
        """index参数为0或者正整数，列表下标"""
        self.elements=self.find_elements(locator)
        try:
            if len(self.elements)==1:#元素唯一
                return self.elements[index]
            elif len(self.elements)!=1 and index<len(self.elements): #不唯一取第index个值
                return self.elements[index]
            else:
                pub_method.log_output('!!--!!index_error').info('index值错误，超过列表下标')
        except Exception as msg:
            pub_method.log_output('!!--!!nosuch_elements').error(msg)

    #判断元素是否可见
    def is_element_isdisplayed(self,locator,index=0):
        try:
            self.find_element(locator,index=0)
            return True,'元素可见'
        except Exception as msg:
            pub_method.log_output('!!--!!nosuch_elements').error(msg)

    #输入操作
    def web_input(self,locator,values,index=0): #注：element变量格式与find_element方法中locator变量格式一致
        try:
            return self.find_element(locator,index).send_keys(values)
        except Exception as msg:
            pub_method.log_output('!!--!!error').error(msg)

    #清空输入框
    def web_clear(self,locator,index=0):
        try:
            self.input=self.find_element(locator,index)
            self.input.send_keys(Keys.CONTROL,'a') #全选
            self.input.clear()
            #return self.find_element(locator,index).clear()
        except Exception as msg:
            pub_method.log_output('!!--!!error').e

    #点击操作
    def web_click(self,locator,index=0):
        try:
            self.element=self.find_element(locator,index)
            return ActionChains(self.driver).click(self.element).perform()
        except Exception as msg:
            pub_method.log_output('!!--!!click_error').error(msg)

    #双击
    def double_click(self,locator,index=0):
        try:
            self.ele=self.find_element(locator,index)
            ActionChains(self.driver).double_click(self.ele).perform()
        except Exception as msg:
            pub_method.log_output('!!--!!error').error(msg)

    #强制刷新
    def refresh_f5(self):
        """强制刷新"""
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys((Keys.F5)).key_up(Keys.CONTROL).perform()

    #鼠标悬浮
    def suspension(self,locator,index=0):
        try:
            self.ele=self.find_element(locator,index)
            ActionChains(self.driver).move_to_element(self.ele).perform()
        except Exception as msg:
            pub_method.log_output('!!--!!error').error(msg)

    #截图,自定义保存截图的文件夹名称
    def get_screenpict(self,name,filename='picture',):
        self.pict_name=time.strftime('%Y-%m-%d-%H.%M.%S',time.localtime(time.time())) #当前时间命名图片名
        self.pictdir_path=os.path.join(os.sys.path[0],filename)  #在当前路径下创建保存截图的文件夹
        #判断储存截图文件夹是否存在，如不存在则创建
        if not os.path.exists(self.pictdir_path):
            os.mkdir(self.pictdir_path)
        #截图保存
        return self.driver.get_screenshot_as_file(os.path.join(self.pictdir_path,'{}{}.png'.format(name,self.pict_name)))

    #关闭浏览器
    def close_browser(self):
        try:
            self.driver.close()
        except Exception as msg:
            pub_method.log_output('close_browser').error('浏览器关闭异常:{}'.format(msg))
        
    #退出浏览器进程
    def quit_browser(self):
        try:
            self.driver.quit()
        except Exception as msg:
            pub_method.log_output('qiut_browser').error('浏览器退出异常{}'.format(msg))

    #封装显示等待方法,等待10s，每1s询问一次
    def display_findelement(self,element):
        return WebDriverWait(self.driver,10,1).until(lambda x:x.find_element_by_css_selector(element))

    #切换窗口,n为下标
    def switch_windows(self,n):
        #获取所有窗口句柄
        self.all_handles=self.driver.window_handles
        #切换窗口
        try:
            if n<len(self.all_handles):
                self.driver.switch_to.window(self.all_handles[n]) #切换窗口
                print('当前窗口title:{}'.format(self.driver.title),'当前窗口句柄:{}'.format(self.driver.current_window_handle))
            else:
                print('{}超过窗口句柄列表下标最大值'.format(n))
        except Exception as msg:
            pub_method.log_output('!!--!!switch_windows').error(msg)

    #切换表单页
    def switch_iframe(self,locator,index=0):
        """存在嵌套页面，需要切换表单后定位"""
        try:
            self.frame=self.find_element(locator,index)
            self.driver.switch_to_frame(self.frame) 
        except Exception as msg:
            pub_method.log_output('!!--!!switch_frame').error(msg)

    #上传图片
    def uploadimg(self):
        """调用本地程序上传图片"""
        try:
            os.system(r'E:\test\client_kyc.exe')
        except Exception as msg:
            pub_method.log_output('!!--!!uploadimg').error(msg)   

        
    #浏览器后退与前进
    # """注释：谷歌浏览器无痕模式打开新窗口无前进或后退操作"""
    # def browser_actions(self,act):
    #     try:
    #         if act=='back':
    #             self.driver.back()
    #         else:
    #             self.driver.forward()
    #     except Exception as msg:
    #         pub_method.log_output('browser_back').error('浏览器前进后退失败:{}'.format(msg))