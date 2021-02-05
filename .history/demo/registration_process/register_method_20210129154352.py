from selenium import webdriver
import unittest
import ddt
import sys
import os
"""跨目录调用，需要将导入的包加入sys.path中"""
path=os.path.dirname(os.path.dirname(__file__))
path=os.path.join(path,'publick')
sys.path.append(path)
from browser_actions import Commonweb
from other_actions import public_method

#实例化封装的web操作类
web=Commonweb()

class formaction():
    """会员中心注册页表单方法封装"""
    #全局变量
    global driver

    def __init__(self):
        #默认以谷歌浏览器打开
        self.driver=web.open_browser()

























