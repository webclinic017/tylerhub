'''
Author: tyler
Date: 2021-08-26 18:21:05
LastEditTime: 2021-08-27 16:28:01
LastEditors: Please set LastEditors
Description: Related operations such as page positioning
FilePath: \tylerhub\demo\cl_open_demoaccount\location\location_of_cl_opendome.py
'''
import os
import sys
import time
import random
path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=path_demo+r'\public'
path_public=os.path.join(path_demo,'public')
sys.path.append(path_public)
from about_data import Aboutdata
from browser_actions import Commonweb
from common_method import Commonmethod
from handle_database import Dadabase_operate
from handlelog import MyLog
from randomdata import Random_data
from read_dataconfig import ReadConfig


class Location_of_opendemo(object):
    """
    cl账号开通模拟账号页面定位等操作
    """

    global dealData,common,dataBase,log,randomData,conFig

    dealData=Aboutdata()
    common=Commonweb()
    dataBase=Dadabase_operate()
    log=MyLog()
    randomData=Random_data()
    conFig=ReadConfig()

    #赋值对象driver
    def broswertype(self,broswername=conFig.get_value('browser', 'default')):
        self.driver=common.open_browser(broswername)
        self.commeThod=Commonmethod(self.driver)

    #cp登录页
    def get_url(self,environment,lang='CN'):
        try:
            common.open_web(conFig.get_value('cp_login', '{}'.format(environment)))
            #去除登录页弹窗
            self.remove_login_topup()
            #选择页面语音，默认简中
            self.commeThod.choose_register_lang(lang)
        except Exception as msg:
            log.my_logger('!!--!!get_url').error(msg)


    #登录页弹唱
    def remove_login_topup(self):
        try:
            self.commeThod.remove_register_topup()
        except Exception as msg:
            log.my_logger('!!--!!remove_login_topup').error(msg)

    #登录cp
    def logincp(self,username,password):
        try:
            self.commeThod.login_cp(username, password)
        except Exception as msg:
            log.my_logger('!!--!!logincp').error(msg)

    #开通模拟账号
    def creat_demoaccount(self):
        time.sleep(1)
        try:
            while True:
                self.attribute=common.get_attributes('xpath,//div[@class="el-loading-mask"]','style')
                if 'display' not in self.attribute:
                    continue
                else:
                    break
            #点击模拟账号
            common.display_click('css,.el-tabs__item',1)
            time.sleep(1)
            #开立模拟账号
            common.display_click('css,.weak-apply-account-btn')
            time.sleep(1)
            #随机选择投资金额
            common.display_click('css,.el-input__inner',2)
            time.sleep(1)
            common.display_click('css,[x-placement="top-start"] li',random.randint(0, 5))
            time.sleep(1)
            #输入随机密码
            self.passWord=randomData.get_psword_type(8)
            common.display_input('css,.el-input__inner', self.passWord,-1)
            time.sleep(1)
            #点击下一步
            common.display_click('css,.el-button > span')
        except Exception as msg:
            log.my_logger('!!--!!creat_demoaccount').error(msg)

    #获取dmo账号信息
    def get_demoaccount_info(self):
        try:
            #获取创建成功后文本
            time.sleep(1)
            self.successText=common.display_get_text('css,.title')
            if '创建成功' in self.successText:
                

