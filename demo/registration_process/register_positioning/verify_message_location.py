'''
Author: your name
Date: 2021-05-24 11:16:04
LastEditTime: 2021-05-27 14:21:17
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \tylerhub\demo\registration_process\register_positioning\verify_message_location.py
'''

import sys
import os
import time
path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=path_demo+r'\public'
sys.path.append(path_public)
from browser_actions import Commonweb
from other_actions import Public_method
from about_data import Exceldata
from common_method import Commonmethod

pub_method=Public_method()
common=Commonweb()

class location_of_verify_data():

    #默认以谷歌浏览器执行测试用例
    def browsertype(self,browsername='Chrome'):
        self.driver=common.open_browser(browsername)
        self.commethd=Commonmethod(self.driver)

    #登录bos
    def login_bos(self,username,psword,lang='CN'):
        try:
            common.open_web('https://at-bos-frontend-uat.atfxdev.com/login')
            time.sleep(1)
            #页面语言
            self.commethd.choose_bos_lang(lang)
            time.sleep(1)
            self.commethd.loginbos(username, psword)
            time.sleep(3)
            #客户管理
            common.display_click('css,.ivu-badge>span')
            time.sleep(1)
            #客户名单
            common.display_click('css,[data-old-padding-top] > [href="/client/clientListNew/:type*"]')
            time.sleep(2)
        except Exception as msg:
            log.my_logger('!!--!!login_bos').error(msg)

    #账户详情页
    def enter_details_page(self,account):
        try:
            common.switch_windows(0)
            time.sleep(2)
            #清空搜索框
            common.web_clear('css,.ivu-input-group-with-append > [placeholder]')
            time.sleep(1)
            #输入主账号查询
            common.display_input('css,.ivu-input-group-with-append > [placeholder]', account)
            time.sleep(1)
            common.display_click('css,.ivu-btn-icon-only > .ivu-icon')
            time.sleep(3)
            #进入账号详情页
            common.display_click('css,div.ivu-table-overflowX>table>tbody.ivu-table-tbody>tr>td',1)
            time.sleep(1)
            common.switch_windows(1)
            time.sleep(3)
            #真实账号信息
            common.display_click('css,[href="#tdAccount"]')
            time.sleep(3)
        except Exception as msg:
            log.my_logger('!!--!!enter_details_page').error(msg)

    #判断当前主账号是否只存在一个交易账号
    def is_traccount_onlyone(self):
        try:
            #判断当前主账号是否只存在一个交易账号
            time.sleep(1)
            self.account_len=common.get_lenofelement('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]'
            '/div[1]/div[2]/table/tbody/tr/td[2]/div/span')
            if self.account_len>1:
                return True
            else:
                common.display_click('xpath,//a[contains(.,"查看")]',-1) #查看
                time.sleep(1)
                return False
        except Exception as msg:
            log.my_logger('!!--!!is_traccount_onlyone').error(msg)

    #获取当前交易账号组别
    def get_group(self):
        try:
            self.group=common.display_get_text('css,[prop="group"]')
            return self.group
        except Exception as msg:
            log.my_logger('!!--!!get_group').error(msg)

    #获取当前交易账号杠杆
    def get_lever(self):
        try:
            self.lever=int(common.display_get_text('css,[prop="leverage"]'))
            return self.lever
        except Exception as msg:
            log.my_logger('!!--!!get_lever').error(msg)

    #获取当前交易账号点差类型
    def get_spreadType(self):
        try:
            self.spreadType=common.display_get_text('css,[prop="spreadType"]')
            return self.spreadType
        except Exception as msg:
            log.my_logger('!!--!!get_spreadType').error(msg)


    #获取当前交易账号加点
    def get_markup(self):
        try:
            self.markup=int(common.display_get_text('css,[prop="markup"]'))
            return self.markup
        except Exception as msg:
            log.my_logger('!!--!!get_markup').error(msg)
    
    #获取当前交易账号币种
    def get_currency(self):
        try:
            self.currency=common.display_get_text('css,[prop="currency"]')
            return self.currency
        except Exception as msg:
            log.my_logger('!!--!!get_currency').error(msg)


    #关闭当前页面
    def closebrowser(self):
        common.close_browser()
    
    #退出浏览器进程
    def quitbrowser(self):
        common.quit_browser()