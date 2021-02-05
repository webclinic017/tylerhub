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

#实例化对象
ex=exceldata()
pub_method=public_method()

class formaction(Commonweb):
    """会员中心注册页表单方法封装"""

    #根据链接/邀请码/直客注册
    def get_url(self,url,code,column,row): #link:专属链接；code:邀请码；l&n:文档中第几行第几列
        """判断是通过专属链接还是邀请码注册"""
        self.browser()
        try:
            if len(url)!=0:
                #通过ib专属链接注册
                self.open_web(url)
                ex.saveainfo(r'E:\test\account_number.xlsx', '专属链接', column, row) #备注注册方式
                print('专属链接注册')
            elif len(code)!=0:
                #通过邀请码
                self.open_web('https://at-client-portal-sit.atfxdev.com/register')
                time.sleep(1)
                ex.saveainfo(r'E:\test\account_number.xlsx', '邀请码', column, row)#备注注册方式
                print('邀请码注册')
            else:
                #直客注册
                self.open_web('https://at-client-portal-sit.atfxdev.com/register')
                ex.saveainfo(r'E:\test\account_number.xlsx', '直客', column, row)#备注注册方式
        except Exception as msg:
            pub_method.log_output('!!--!!get_url').error('访问注册页异常{}'.format(msg))


            




















