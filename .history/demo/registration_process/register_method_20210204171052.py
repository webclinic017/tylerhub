from selenium import webdriver
import unittest
import ddt
import sys
import os
import time
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

#创建继承基础类的注册页表单操作模块
class form_operations(Commonweb):
    """会员中心注册页表单方法封装，注册页表单填写"""

    #根据链接/邀请码/直客注册
    def get_url(self,url,code,column,row): #link:专属链接；code:邀请码；l&n:文档中第几行第几列 
        """判断是通过专属链接还是邀请码注册"""
        try:
            if len(url)!=0:
                #通过ib专属链接注册
                self.open_web(url)
                ex.saveainfo(r'E:\test\account_number.xlsx','专属链接', column, row) #
                time.sleep(2)
                self.register_topup()
                print('专属链接注册')
            elif len(code)!=0:
                #通过邀请码
                self.open_web('https://at-client-portal-sit.atfxdev.com/register')
                time.sleep(2)
                ex.saveainfo(r'E:\test\account_number.xlsx','邀请码', column, row)#备注注册方式
                self.register_topup()
                print('邀请码注册')
            else:
                #直客注册
                self.open_web('https://at-client-portal-sit.atfxdev.com/register')
                ex.saveainfo(r'E:\test\account_number.xlsx','直客', column, row)#备注注册方式
                time.sleep(2)
                self.register_topup()
        except Exception as msg:
            pub_method.log_output('!!--!!get_url').error('访问注册页异常{}'.format(msg))

    #判断注册国家是否为UK国家
    def country_isuk(self,country):
        self.uk_list=['阿尔巴尼亚','安道尔','奥地利','波斯尼亚和黑塞哥维那','保加利亚','克罗地亚','塞浦路斯','捷克共和国',
                      '丹麦','爱沙尼亚','芬兰','佐治亚州','德国','直布罗陀','希腊','匈牙利','冰岛','爱尔兰','意大利',
                      '拉脱维亚','列支敦士登','立陶宛','卢森堡','马其顿','马耳他','摩纳哥','黑山共和国','荷兰','挪威',
                      '葡萄牙','塞尔维亚共和国','罗马尼亚','圣马力诺','斯洛伐克','斯洛文尼亚','西班牙','西班牙','瑞典','瑞士','英国']           
        if country in self.uk_list:
            print('AT Global Markets Limited 不接受居住在这个国家的个人申请。')
            return True
        else:
            return False

    #去除注册页弹窗
    def register_topup(self):
        try:
            self.web_click('css,.blk-sure-btn')
        except Exception as msg:
            pub_method.log_output('!!--!!topup').error('注册页弹窗去除失败：{}'.format(msg))


    #关闭浏览器
    def closedriver(self):
        self.close_browser()

    #退出浏览器
    def quitdriver(self):
        self.quit_browser()






















