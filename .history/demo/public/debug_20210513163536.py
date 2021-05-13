# from selenium import webdriver

# options=webdriver.ChromeOptions()
# options.add_argument('lang=zh_CN.UTF-8')
# options.add_argument('--incognito')
# options.add_argument('--start-maximized')

# driver=webdriver.Chrome(chrome_options=options)
# driver.get('https://www.baidu.com/')
# import logging
# def logout(name):
#     # 先创建一个logger
#     logger = logging.getLogger(name)  # 定义Logger的名字，之前直接用logging调用的名字是root，日志格式用%(name)s可以获得。这里的名字也可以自定义比如"TEST"
#     logger.setLevel(logging.DEBUG)  # 低于这个级别将被忽略，后面还可以设置输出级别
#     # 创建handler和输出级别
#     ch = logging.StreamHandler()  # 输出到屏幕的handler
#     ch.setLevel(logging.INFO)  # 输出级别和上面的忽略级别都不一样，可以看一下效果

#     # 创建日志格式，可以为每个handler创建不同的格式
#     ch_formatter = logging.Formatter('%(name)s %(asctime)s {%(levelname)s}:%(message)s',datefmt='%Y-%m-%d %H:%M:%S')  # 关键参数datefmt自定义日期格式

#     # 把上面的日志格式和handler关联起来
#     ch.setFormatter(ch_formatter)

#     # 将handler加入logger
#     logger.addHandler(ch)

#     return logger

# logout('test').info('thuehhth')
# # # 以上就完成了，下面来看一下输出的日志
# # logger.debug('logger test debug')
# # logger.info('logger test info')
# # logger.warning('logger test warning')
# # logger.error('logger test error')
# # logger.critical('logger test critical')

# from browser_actions import Commonweb
# from selenium import webdriver
# from other_actions import public_method
# import time

# c=Commonweb()
# p=public_method()
# c.open_browser()
# c.open_web('https://www.baidu.com/')
# time.sleep(2)
# c.double_click('css,.hot-refresh-text')
# time.sleep(3)
# c.suspension('css,.s-top-right-text')
# time.sleep(1)
# c.web_click('css,.soutu-btn')
# time.sleep(2)
# c.is_element_isdisplayed('css,.upload-pic')
# c.web_click('css,.upload-pic')
# time.sleep(1)
# c.uploadimg()
# time.sleep(2)
# c.get_screenpict('baidu')
# c.web_click('css,.upload-pic')
# time.sleep(1)
# c.uploadimg()

# import os
# import time
# print(os.getcwd())
# pictour_dir=os.path.join(os.sys.path[0],'pictour')
# print(pictour_dir)
# # # pict_name=time.strftime('%Y-%m-%d-%H.%M.%S',time.localtime(time.time()))
# # # print(pict_name)
# # # pri_path=os.path.join(os.path.join(os.getcwd(),'pictour'),time.strftime('%Y-%m-%d-%H.%M.%S',time.localtime(time.time())))
# # # print(pri_path)

# # print(os.sys.path[0]) #上级目录
# # print(os.__file__)
# # print(os.path.abspath(__file__))
# # os.mkdir('pictour')
# # pict_path=os.path.join(os.sys.path[0],'picture')
# # if not os.path.exists(pict_path):
# #     os.mkdir(pict_path)
# # pict_name=os.path.join(pict_path,'{}.png'.format(54564))
# # print(pict_name)
# # # print(pict_path)
# # # print(os.path.exists('D:\master\pictour'))

# # def c(a):
# #     return a+1
    
# # c=lambda a:a+1


# # def c(a):
# #     return c+2

# # d=lambda y:test(y)
# from browser_actions import Commonweb
# from other_actions import public_method
# import time
# import datetime

# c=Commonweb()
# p=public_method()
# c.open_browser()
# c.open_web('https://at-bos-frontend-uat.atfxdev.com/login')
# c.display_input('css,.ivu-input-default','tyler.tang')
# c.display_input('css,.ivu-input-default','Tl123456',1)
# c.display_click('css,.ivu-btn-large')
# c.display_click('css,.ivu-badge>span')
# c.display_click('css,[data-old-padding-top] > [href="/client/clientListNew/:type*"]')
# c.display_input('css,.ivu-input-group-with-append > [placeholder]','1200008354')
# time.sleep(1)
# c.display_click('css,.ivu-btn-icon-only > .ivu-icon')
# time.sleep(1)
# c.display_click('css,div.ivu-table-overflowX>table>tbody.ivu-table-tbody>tr>td',1)
# c.switch_windows(1)
# time.sleep(2)
# c.display_click('css,[href="#tdAccount"]')
# time.sleep(4)
# print(c.is_element_selected('css,.ivu-checkbox-input'))
# print(c.get_attributes('css,label.switch>span.ivu-switch>input','value',2))
# time.sleep(1)
# list_len=c.get_lenofelement('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/div[1]/div[2]/table/tbody/tr/td[1]/div/div/span')
# print(list_len)
# for i in range(0,list_len):
#     if str(c.get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/div[1]/div[2]/table/tbody/tr/td[1]/div/div/span',i))==str(693005664):
#         print(i+1)
#         break


# star=datetime.datetime.now()
# c.display_click('css,.s_btn')
# end=datetime.datetime.now()
# print(end-star)
# c.web_click('css,.blk-sure-btn')
# time.sleep(0.5)
# if c.is_displayed('css,.la-redo-alt',2):
#     print(1111)
# else:
#     print(2222)

# time.sleep(1)
# # c.display_input('css,.s_ipt','python')
# print(c.display_get_text('css,.title-content-title',1))
# c.display_click('css,.title-content-title')
# time.sleep(1)
# c.switch_windows(1)
# c.js_scroll('down')
# time.sleep(5)


# from selenium import webdriver
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# import time
# dr=webdriver.Chrome()
# dr.maximize_window()
# dr.get('https:\\www.baidu.com')

# ele=WebDriverWait(dr,10,0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.title-content-title')),message='timeout')
# print(ele)


#ele.click()

from browser_actions import Commonweb
import time

com=Commonweb()
com.open_browser()
com.open_web('https:\\www.baidu.com')
time.sleep(1)
com.display_click('css,.soutu-btn',-1)
time.sleep(2)
com.display_click('css,.upload-pic')
time.sleep(1)