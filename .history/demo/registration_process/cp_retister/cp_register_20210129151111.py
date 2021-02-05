#导包
from selenium import webdriver
import unittest
import ddt
import sys
import os
"""跨目录调用，需要将导入的包加入sys.path中"""
path=os.path.dirname(os.path.dirname(__file__))
path=os.path.join(path,'publick')
sys.path.append(path)
sys.path.append(path)
from browser_actions import Commonweb
from other_actions import public_method


#实例化封装的web操作类
web=Commonweb()

@ddt.ddt #数据驱动
class register_cp(unittest.TestCase):
    """会员中心注册页表单"""
    #定义全局变量
    global driver
    #默认使用谷歌浏览器
    driver=web.open_browser()

    def setUp(self):
        #访问url
        web.open_web('https://at-client-portal-sit.atfxdev.com/login')


    def test_register(self):
        print(1111)


if __name__=='__main__':
    unittest.main()
