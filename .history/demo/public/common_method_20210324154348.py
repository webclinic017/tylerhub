import time
from selenium import webdriver
from other_actions import public_method


pub_method=public_method()

class common_method():
    """
    此模块用于封装常用方法，例如登录会员中心/登录bos等
    """

    #初始化函数，赋值driver对象
    def __init__(self,driver):
        self.driver=driver

    #选择会员中心登录页语言
    

    