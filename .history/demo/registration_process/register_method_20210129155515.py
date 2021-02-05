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
    #全局变量
    global driver

    def __init__(self):
        #默认以谷歌浏览器打开
        self.driver=web.open_browser()

        #根据链接/邀请码/直客注册
    def get_url(self,link,code,l,n): #link:专属链接；code:邀请码；l&n:文档中第几行第几列
        """判断是通过专属链接还是邀请码注册"""
        #去除弹窗
        if len(link)!=0:
            #通过ib专属链接注册
            web.open_web(link)
            ex.saveaccount(r'E:\test\account_number.xlsx', '专属链接', l, n)
            print('专属链接注册')
            #self.register_top()
        elif len(code)!=0:
            #通过邀请码
            web.open_web('https://at-client-portal-sit-proxy.ntdevops.com/register')
            time.sleep(1)
            web.web_input('css,div.el-form-item__content>div.invitationCode-input>textarea',code)
            ex.saveaccount(r'E:\test\account_number.xlsx', '邀请码', l, n)
            print('邀请码注册')
            #self.register_top()
        else:
            #直客注册
            web.open_web('https://at-client-portal-sit-proxy.ntdevops.com/register')
            ex.saveaccount(r'E:\test\account_number.xlsx', '直客', l, n)
            print('直客注册')
            #self.register_top()

























