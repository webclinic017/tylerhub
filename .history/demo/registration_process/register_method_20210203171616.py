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
from about_data import exceldata

#实例化封装的web操作类
web=Commonweb()
ex=exceldata()

class formaction():
    """会员中心注册页表单方法封装"""
    
    #根据链接/邀请码/直客注册
    def get_url(self,url): #link:专属链接；code:邀请码；l&n:文档中第几行第几列
        """判断是通过专属链接还是邀请码注册"""
        web.open_web(self.url)



web.open_browser()
f=formaction()
f.get_url('https://baidu.com/')


















