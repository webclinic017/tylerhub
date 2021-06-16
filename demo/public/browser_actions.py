import os
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from other_actions import *
from verification_code import base64_api

#实例化公共方法模块
pub_method=public_method()

class Commonweb():
    """selenium二次封装：浏览器驱动，访问url等自定义基类方法"""
    #定义全局变量
    global driver

    def open_browser(self,browsername='Chrome'):
        """打开浏览器，浏览器名称：Firefox，Chrome，默认以谷歌浏览器打开"""
        try:
            if browsername=='firefox' or browsername=='Firefox' or browsername=='fx': #火狐浏览器
                #配置浏览器
                options=webdriver.FirefoxOptions()
                #设置浏览器配置
                options.add_argument('lang=zh_CN.UTF-8') #初始化浏览器默认编码格式
                options.add_argument('--incognito') #无痕模式
                options.add_argument('--start-maximized') #浏览器全频
                self.driver=webdriver.Firefox(options=options) #添加配置
                self.driver.implicitly_wait(5) #隐式等待5s
            elif browsername=='chrome' or browsername=='Chrome':
                #配置浏览器
                options=webdriver.ChromeOptions()
                #设置浏览器配置
                options.add_argument('lang=zh_CN.UTF-8') #初始化浏览器默认编码格式
                options.add_argument('--incognito') #无痕模式
                options.add_argument('--start-maximized') #浏览器全频
                self.driver=webdriver.Chrome(options=options)#添加配置
                self.driver.implicitly_wait(5) #隐式等待5s
            else:
                pub_method.log_output('!!--!!driver_browser').info('没有找到这种浏览器驱动，你可以尝试输入firefox、Firefox、fx、chrome、Chrome')
            return self.driver
        except Exception as msg:
            pub_method.log_output('!!--!!driver_name').error('启动浏览器异常{}'.format(msg))

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
        #切片locator值
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

    #获取页面元素的个数
    def get_lenofelement(self,locator):
        try:
            return len(self.find_elements(locator))
        except Exception as msg:
            pub_method.log_output('!!--!!get_lenofelement').error(msg)

    #显示等待查找页面元素,timeout=5s，每0.5s询问一次
    def display_find_elements(self,locator,timeout=5,step=0.5):
        #切片
        method,values=locator.split(',',maxsplit=1)
        try:
            if 'css' in method:
                return WebDriverWait(self.driver,timeout,step).until(lambda x:x.find_elements_by_css_selector(values))
            elif 'xpath' in method:
                return WebDriverWait(self.driver,timeout,step).until(lambda x:x.find_elements_by_xpath(values))
            elif 'name' in method:
                return WebDriverWait(self.driver,timeout,step).until(lambda x:x.find_elements_by_name(values))
            elif 'id' in method:
                return WebDriverWait(self.driver,timeout,step).until(lambda x:x.find_elements_by_id(values))
            elif 'class' in method:
                return WebDriverWait(self.driver,timeout,step).until(lambda x:x.find_elements_by_class_name(values))
            elif 'partial' and 'link' in method:
                return WebDriverWait(self.driver,timeout,step).until(lambda x:x.find_elements_by_partial_link_text(values))
            elif 'link' in method:
                return WebDriverWait(self.driver,timeout,step).until(lambda x:x.find_elements_by_link_text(values))
            elif 'tag' in method:
                return WebDriverWait(self.driver,timeout,step).until(lambda x:x.find_elements_by_tag_name(values))
            else:
                pub_method.log_output('!!--!!location_element').info('定位方法错误')
        except Exception as msg:
            pub_method.log_output('!!--!!display_finds_element').error('元素不存在或者不可见：{}'.format(msg))

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
            pub_method.log_output('!!--!!find_element').error(msg)

    #判断显示等待查找的元素是否唯一，不唯一取第n个值，唯一取唯一值
    def display_find_element(self,locator,index=0):
        self.display_elements=self.display_find_elements(locator)
        try:
            if len(self.display_elements)==1:
                return self.display_elements[index]
            elif len(self.display_elements)!=1 and index<len(self.display_elements):
                return self.display_elements[index]
            else:
                pub_method.log_output('!!--!!index_error').info('index值错误，超过列表下标')                
        except Exception as msg:
            pub_method.log_output('!!--!!nosuch_elements').error(msg)
    
    #显示等待获取页面某个元素的属性
    def get_attributes(self,locator,element,index=0):
        try:
            return self.display_find_element(locator,index).get_attribute(element)
        except Exception as msg:
            pub_method.log_output('!!--!!get_attributes').error(msg)

    #判断元素是否可见
    def element_is_visible(self,locator,index=0):
        try:
            self.boll=self.find_element(locator,index)
            return self.boll.is_displayed()
        except Exception as msg:
            pub_method.log_output('!!--!!element_is_visible').error(msg) 

    #设置等待时间查找页面元素是否可见(是否加载到了dom树中)
    def ele_is_displayed(self,locator,timeout,step=0.5):
        """
        timeout:自定义等待时间，与隐式等待时间不同，可缩短页面等待时间
        """
        method,values=locator.split(',',maxsplit=1)
        try:
            if 'css' in method:
                try:
                    WebDriverWait(self.driver,timeout,step).until(EC.presence_of_element_located((By.CSS_SELECTOR,values)))
                    return True
                except:
                    return False
            elif 'xpath' in method:
                try:
                    WebDriverWait(self.driver,timeout,step).until(EC.presence_of_element_located((By.XPATH,values)))
                    return True
                except:
                    return False
            elif 'id' in method:
                try:
                    WebDriverWait(self.driver,timeout,step).until(EC.presence_of_element_located((By.ID,values)))
                    return True
                except:
                    return False
            elif 'name' in method:
                try:
                    WebDriverWait(self.driver,timeout,step).until(EC.presence_of_element_located((By.NAME,values)))
                    return True
                except:
                    return False
            else:
                print('请输入正确的定位方法或者等待时间')
        except Exception as msg:
            pub_method.log_output('!!--!!is_displayed').error(msg)






    #判断某个元素是否被选中
    def is_element_selected(self,locator,index=0):
        try:
            return self.find_element(locator,index).is_selected()
        except:
            return False

    #输入操作
    def web_input(self,locator,values,index=0): #注：element变量格式与find_element方法中locator变量格式一致
        try:
            return self.find_element(locator,index).send_keys(values)
        except Exception as msg:
            pub_method.log_output('!!--!!input_error').error(msg)

    #显示等待输入
    def display_input(self,locator,values,index=0):
        try:
            return self.display_find_element(locator,index).send_keys(values)
        except Exception as msg:
            pub_method.log_output('!!--!!display_input').error(msg)

    #清空输入框
    def web_clear(self,locator,index=0):
        try:
            self.input=self.find_element(locator,index)
            self.input.send_keys(Keys.CONTROL,'a') #全选
            self.input.clear()
            #return self.find_element(locator,index).clear()
        except Exception as msg:
            pub_method.log_output('!!--!!clear_error').error(msg)

    #获取页面文本
    def get_text(self,locator,index=0):
        try:
            return self.find_element(locator,index).text
        except Exception as msg:
            pub_method.log_output('!!--!!get_text_error').error(msg)

    #显示等待获取页面文本
    def display_get_text(self,locator,index=0):
        try:
            return self.display_find_element(locator,index).text
        except Exception as msg:
             pub_method.log_output('!!--!!display_get_text').error(msg)

    #点击操作
    def web_click(self,locator,index=0):
        try:
            return self.find_element(locator,index).click()
            # self.element=self.find_element(locator,index)
            # return ActionChains(self.driver).click(self.element).perform()
        except Exception as msg:
            pub_method.log_output('!!--!!click_error').error(msg)

    #显示等待点击
    def display_click(self,locator,index=0):
        try:
            return self.display_find_element(locator,index).click()
        except Exception as msg:
            pub_method.log_output('!!--!!display_click').error(msg)      

    #双击
    def doubleclick(self,locator,index=0):
        try:
            self.ele=self.find_element(locator,index)
            ActionChains(self.driver).double_click(self.ele).perform()
        except Exception as msg:
            pub_method.log_output('!!--!!doubleclick_error').error(msg)

    #显示等待双击
    def display_doubleclick(self,locator,index=0):
        try:
            self.ele=self.display_find_element(locator,index)
            ActionChains(self.driver).double_click(self.ele).perform()
        except Exception as msg:
            pub_method.log_output('!!--!!display_doubleclick').error(msg)

    #强制刷新
    def refresh_f5(self):
        """强制刷新"""
        return ActionChains(self.driver).key_down(Keys.CONTROL).send_keys((Keys.F5)).key_up(Keys.CONTROL).perform()
    
    #刷新
    def general_refresh_(self):
        try:
            self.driver.refresh()
        except Exception as msg:
            pub_method.log_output('!!--!!refresh').error(msg)

    #鼠标悬浮
    def suspension(self,locator,index=0):
        try:
            self.ele=self.find_element(locator,index)
            ActionChains(self.driver).move_to_element(self.ele).perform()
        except Exception as msg:
            pub_method.log_output('!!--!!suspension_error').error(msg)

    #显示等待-鼠标悬停
    def display_suspension(self,locator,index=0):
        try:
            self.ele=self.display_find_element(locator,index)
            ActionChains(self.driver).move_to_element(self.ele).perform()
        except Exception as msg:
            pub_method.log_output('!!--!!suspension').error(msg)


    #右键点击
    def right_click(self,locator,index=0):
        try:
            self.ele=self.display_find_element(locator,index)
            ActionChains(self.driver).context_click(self.ele).perform()
        except Exception as msg:
            pub_method.log_output('!!--!!right_click').error(msg)

    #其他键盘操作(针对搜索框/输入框)
    def keyboard_operation(self,locator,keys,index=0):
        """
        keys:a,全选;c:粘贴;v:复制；x:剪切
        """
        try:
            self.ele=self.display_find_element(locator,index)
            self.ele.send_keys(Keys.CONTROL,keys)
        except Exception as msg:
            pub_method.log_output('!!--!!keyboard_operation').error(msg)

    #右键在新窗口打开链接打开链接
    def right_click_link(self,locator,index=0):
        try:
            self.ele=self.display_find_element(locator,index)
            self.ele.send_keys(Keys.CONTROL + Keys.ENTER)
        except Exception as msg:
            pub_method.log_output('!!--!!right_click_link').error(msg)      

    #截图,自定义保存截图的文件夹名称
    def get_screenpict(self,name,filename='picture',):
        """
        name:截图名称
        filename:保存截图文件名称
        """
        self.pict_name=time.strftime('%Y-%m-%d-%H.%M.%S',time.localtime(time.time())) #当前时间命名图片名
        self.pictdir_path=os.path.join(os.sys.path[0],filename)  #在当前路径下创建保存截图的文件夹
        #判断储存截图文件夹是否存在，如不存在则创建
        if not os.path.exists(self.pictdir_path):
            os.mkdir(self.pictdir_path)
        #截图保存
        self.picture=self.driver.get_screenshot_as_file(os.path.join(self.pictdir_path,'{}{}.png'.format(name,self.pict_name)))
        return self.picture
        
    #切换窗口,n为下标
    def switch_windows(self,n):
        #获取所有窗口句柄
        self.all_handles=self.driver.window_handles
        #切换窗口
        try:
            if n<len(self.all_handles):
                self.driver.switch_to.window(self.all_handles[n]) #切换窗口
            else:
                print('{}超过窗口句柄列表下标最大值'.format(n))
        except Exception as msg:
            pub_method.log_output('!!--!!switch_windows').error(msg)

    #获取当前页面的title
    def title(self):
        try:
            return(self.driver.title)
        except Exception as msg:
            pub_method.log_output('!!--!!title').error(msg)

    #切换表单页
    def switch_iframe(self,locator,index=0):
        """存在嵌套页面，需要切换表单后定位"""
        try:
            self.frame=self.find_element(locator,index)
            self.driver.switch_to_frame(self.frame) 
        except Exception as msg:
            pub_method.log_output('!!--!!switch_frame').error(msg)

    #上传图片
    def upload_img(self,exe_path,pic_path):
        """调用本地程序上传图片,path:本地程序路径"""
        try:
            os.system('{} {}'.format(exe_path,pic_path))
        except Exception as msg:
            pub_method.log_output('!!--!!upload').error(msg)   

    #JS新开窗口
    def js_openwindows(self,url):
        self.js = 'window.open("{}")'.format(url)
        self.driver.execute_script(self.js)

    #JS控制滚动条
    def js_scroll(self,site):
        """
        site:top or down,
        Control window movement
        """
        try:
            if site=='down':
                self.js='document.documentElement.scrollTop=10000'
                #回到底部
                self.driver.execute_script(self.js)
            elif site=='top':
                self.js='document.documentElement.scrollTop=0'
                #回到顶部
                self.driver.execute_script(self.js)
            else:
                print('site参数：顶部：{}；底部：{}'.format('top','down'))
        except Exception as msg:
            pub_method.log_output('!!--!!js_scroll').error(msg)

    #JS处理内嵌滚动条滚动
    def js_scroll_inline(self,type,element,site,index=0):
        """
        JS处理内嵌滚动条目前只封装了两种方法：通过ID和CLASSNAME两种
        type:id or calss
        site:down or top
        """
        try:
            #通过ID属性，回到顶部
            if type=='ID' or type=='id' and site=='top':
                self.js='document.getElementsByid({})["{}"].scrollTop =0 '.format(element,index)
                self.driver.execute_script(self.js)
            #通过ID属性，回到底部
            elif type=='ID' or type=='id' and site=='down':
                self.js='document.getElementsByid({})["{}"].scrollTop =10000'.format(element,index)
                self.driver.execute_script(self.js)
            #通过class属性，回到顶部
            elif type=='class' and site=='top':
                self.js='document.getElementsByClassName("{}")[{}].scrollTop =0 '.format(element,index)
                self.driver.execute_script(self.js)
            #通过class属性，回到底部
            elif type=='class' and site=='down':
                self.js='document.getElementsByClassName("{}")[{}].scrollTop =10000 '.format(element,index)
                self.driver.execute_script(self.js)
            else:
                print('参数错误请检查')
        except Exception as msg:
            pub_method.log_output('!!--!!js_scroll_inline').error(msg)

    #元素聚焦，移动页面至指定元素位置
    def element_focus(self,locator,index=0):
        try:
           self.focus=self.display_find_element(locator,index) 
           self.driver.execute_script('return arguments[0].scrollIntoView();',self.focus)
        except Exception as msg:
            pub_method.log_output('!!--!!js_scroll_inline').error(msg)


    #截取屏幕，定点截图
    def fixed_point_image(self,name,filename,locator,index=0):
        """
        截取屏幕，抓取元素定位处的截图
        name:屏幕截图名称
        filename：保存截图的文件，默认为在当前路径下创建文件，已存在则不创建
        locator：元素定位方法与元素值
        """
        try:
            #截取当前屏幕
            self.get_screenpict(name,filename)
            #获取验证码图片元素定位
            img_ele=self.find_element(locator,index)
            #得到验证码图片左上角及右下角的xy左坐标
            #得到该元素左上角的 x，y 坐标和右下角的 x，y 坐标
            left=img_ele.location.get('x')
            lefty=img_ele.location.get('y')
            right=left+img_ele.size.get('width')
            righty=lefty+img_ele.size.get('height')
            #打开之前的截屏
            self.image=Image.open(os.path.join(self.pictdir_path,'{}{}.png'.format(name,self.pict_name)))
            #裁剪截图，裁剪范围为之前获取的左上角至右下角区域
            self.new_image=self.image.crop((left,lefty,right,righty))
            #保存裁剪的图片
            self.new_image_path=os.path.join(self.pictdir_path,'Screenshot{}.png'.format(self.pict_name))
            self.new_image.save(self.new_image_path)
            return self.new_image_path
        except Exception as msg:
            pub_method.log_output('coed_img').error(msg)

    #调用三方接口，读取验证码
    def discern_code(self,username,psword,name,filename,locator,index=0):
        """
        username:图鉴网用户名
        psword:图鉴网密码
        name:屏幕截图名称
        filename：保存截图的文件，默认为在当前路径下创建文件，已存在则不创建
        locator：元素定位方法与元素值
        """ 
        try:
            #获取验证码图片,并打开
            self.img=Image.open(self.fixed_point_image(name,filename,locator,index=0))
            self.result_code=base64_api(username,psword,self.img)
            return self.result_code
        except Exception as msg:
            pub_method.log_output('discern_code').error(msg)  

    #关闭当前页
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