'''
Author: your name
Date: 2022-01-13 14:29:47
LastEditTime: 2022-05-18 17:42:15
LastEditors: Tyler96-QA 1718459369@qq.com
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \tylerhub\demo\change_email_language\location\location_of_email_language.py
'''
import os
import sys
import time
import random
import datetime

import langid

path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=os.path.join(path_demo,'public')
sys.path.append(path_public)
path_project=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from browser_actions import Commonweb
from common_method import Commonmethod
from handle_database import Database_operate
from handlelog import MyLog
from randomdata import Random_data
from read_dataconfig import ReadConfig
from about_data import Aboutdata



class Location_email_language_change(object):
    global common,dataBase,log,randomData,conFig,dealData

    common=Commonweb()
    dataBase=Database_operate()
    log=MyLog()
    randomData=Random_data()
    conFig=ReadConfig()
    dealData=Aboutdata()

    #赋值对象driver
    def broswertype(self,browsername=conFig.get_value('browser', 'default')):
        self.driver=common.open_browser(browsername)
        self.commeThod=Commonmethod(self.driver)

    #登录页
    def get_url(self,environment,username,password,lang='CN'):
        try:
            common.open_web(conFig.get_value('bos_login', '{}'.format(environment)))
            #选择bos页面语言,默认简中
            time.sleep(1)
            self.commeThod.choose_bos_lang(lang)
            #登录bos
            self.commeThod.loginbos(username, password)
            time.sleep(1)
            common.display_click('css,[width="200"] li .ivu-icon-ios-arrow-down')
            time.sleep(0.5)
            common.display_click("xpath,//span[.='登录会员中心']")
            time.sleep(1)
            #选择登录会员中心页面语言
            common.display_click('css,.ivu-form div i',-1)
            time.sleep(0.5)
            common.display_click("xpath,//li[.='简体中文']",-1)
            time.sleep(0.5)
        except Exception as msg:
            log.my_logger('!!--!!get_url').error(msg)


    #从bos登录会员中心
    def from_bos_to_cp(self,account):
        try:
            common.web_clear('css,[placeholder]')
            time.sleep(0.5)
            common.display_input('css,[placeholder]', account)
            time.sleep(0.5)
            #登录
            common.display_click("xpath,//span[.='登录']")
            time.sleep(2)
            common.switch_windows(1)
            time.sleep(1)
            #判断页面是否正在跳转
            while True:
                if common.ele_is_displayed("css,[src='/static/img/loading.webm']", 1):
                    continue
                else:
                    break
            time.sleep(1)
            while True:
                self.loading_attributes=common.get_attributes('css,.el-loading-mask', 'style')
                if 'none' in self.loading_attributes:
                    break
                else:
                    continue
        except Exception as msg:
            log.my_logger('!!--!!from_bos_to_cp').error(msg)

    #更改邮箱语音
    def change_emailLanguage(self,account,excelpath,column,column1,row):
        try:
            #获取修改前邮箱语言
            self.befor_lang=dataBase.search_in_mongodb(conFig.get_value('mongodb','uri'),'atfxgm-sit','atfx_account_info',{"accountNumber":account},'lang',N=1)[0]['lang']
            #保存
            dealData.saveainfo(excelpath, self.befor_lang, column, row)
            time.sleep(0.5)
            common.display_click('css,.el-icon--right.el-icon-arrow-down')
            time.sleep(0.5)
            common.display_click("xpath,//span[.='设置']")
            time.sleep(1)
            common.display_click("xpath,//div[@id='tab-fourth']")
            time.sleep(1)
            common.display_click('css,.opt-btn')
            time.sleep(0.5)
            common.display_click('css,.el-select__caret')
            time.sleep(0.5)
            #随机选择邮箱语言random.randint(1,9)
            self.index=random.randint(1,9)
            #判断随机选择邮箱语种
            time.sleep(1)
            if self.index==1:
                self.randomLanguage='cht'
            elif self.index==7:
                self.randomLanguage='ms'
            else:
                common.display_click('css,.el-select-dropdown__list > li > span',self.index)
                time.sleep(0.5)
                common.display_click('css,.el-select__caret')
                time.sleep(0.5)
                self.randomLanguage=common.check_language('css,.el-select-dropdown__list > li > span',self.index)
            time.sleep(0.5)
            
            common.display_click('css,.el-select-dropdown__list > li > span',self.index)
            time.sleep(0.5)
            #保存
            common.display_click('xpath,//span[.="保存"]')
            #保存修改后邮箱语言
            dealData.saveainfo(excelpath, self.randomLanguage, column1, row)
            print('修改后邮箱语言为{}'.format(self.randomLanguage))
        except Exception as msg:
            log.my_logger('!!--!!change_emailLanguage').error(msg)    

    def check_dataBase_language(self,account,excelpath,column,row):
        try:
            time.sleep(2)
            self.database_lang=dataBase.search_in_mongodb(conFig.get_value('mongodb','uri'),'atfxgm-sit','atfx_account_info',{"accountNumber":account},'lang',N=1)[0]['lang']
            if self.database_lang=='CHC':
                self.checkDataBase_emailLang='zh'
            elif self.database_lang=='CHT':
                self.checkDataBase_emailLang='cht'
            elif self.database_lang=='ENG':
                self.checkDataBase_emailLang='en'
            elif self.database_lang=='ARA':
                self.checkDataBase_emailLang='ar'
            elif self.database_lang=='URD':
                self.checkDataBase_emailLang='ur'
            elif self.database_lang=='IND':
                self.checkDataBase_emailLang='es'
            elif self.database_lang=='KOR':
                self.checkDataBase_emailLang='ko'
            elif self.database_lang=='MYS':
                self.checkDataBase_emailLang='ms'
            elif self.database_lang=='THA':
                self.checkDataBase_emailLang='th'
            else:
                self.checkDataBase_emailLang='vi'
            #保存修改后数据库邮箱语言
            dealData.saveainfo(excelpath, self.checkDataBase_emailLang, column, row)
            return self.checkDataBase_emailLang
        except Exception as msg:
            log.my_logger('!!--!!check_dataBase_language').error(msg)


    def closebrowser(self):
        common.close_browser()

    def quitbrowser(self):
        common.quit_browser()