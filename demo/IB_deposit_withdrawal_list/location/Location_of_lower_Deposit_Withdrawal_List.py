'''
Author: your name
Date: 2022-02-21 17:22:03
LastEditTime: 2022-03-29 17:19:22
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \tylerhub\demo\IB_deposit_withdrawal_list\location\Location_of_Deposit_Withdrawal_List.py
'''

import os
import sys
import time
import random
import datetime
import re
import pyperclip

path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=os.path.join(path_demo,'public')
sys.path.append(path_public)
path_project=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from browser_actions import Commonweb
from common_method import Commonmethod
from handle_database import Database_operate
from handlelog import MyLog
from read_dataconfig import ReadConfig
from about_data import Aboutdata


class Location_of_deposit_withdrawal(object):
    """
    页面定位等操作
    """

    global common,dataBase,log,conFig,dealData

    common=Commonweb()
    dataBase=Database_operate()
    log=MyLog()
    conFig=ReadConfig()
    dealData=Aboutdata()

    #赋值对象driver,设置下载文件路径
    def broswertype(self,download_path=os.path.join(path_project,'test_data'),browsername=conFig.get_value('browser', 'default')):
        self.driver=common.open_browser(download_path=download_path,browsername=browsername)
        self.comMethod=Commonmethod()


    #登录页
    def get_url(self,environment,username,password,lang='CN'):
        try:
            common.open_web(conFig.get_value('bos_login', '{}'.format(environment)))
            #选择bos页面语言,默认简中
            time.sleep(1)
            self.comMethod.choose_bos_lang(common,lang)
            #登录bos
            self.comMethod.loginbos(common,username, password)
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


    #查询mysql数据库，找到该IB下所有下级账号
    def search_ib_lower(self,account:int):
        try:
            self.IB_base=dataBase.search_in_mysql('SELECT path FROM client_relationship2_sit.relationship where path like "%{}%"'.format(account), conFig.get_value('mysql_AWS', 'host'), conFig.get_value('mysql_AWS','user'),conFig.get_value('mysql_AWS','password'),type='all')
            self.pattern=r'[10|12]\d{9}'
            
            self.serach_list=[]

            for i in self.IB_base:
                self.serach_list.append(re.findall(self.pattern,''.join(list(i))))

            self.serach_list2=[]

            for y in self.serach_list:
                for x in y:
                    self.serach_list2.append(x)
            #去重
            self.serach_list3=list(set(self.serach_list2))

            #删除主账号
            self.serach_list3.remove('{}'.format(account))

            print('当前IB账号{}存在{}个直属/非直属下级'.format(account,len(self.serach_list3)))
            return self.serach_list3
        except Exception as msg:
            log.my_logger('!!--!!search_ib_lower').error(msg)
 

    def logincp(self,account:int):
        #登录账号
        common.switch_windows(0)
        common.web_clear('css,[placeholder]')
        time.sleep(1)
        common.display_input('css,[placeholder]', account)
        time.sleep(0.5)
        #登录
        common.display_click('css,.ivu-btn > span',-1)
        time.sleep(2)
        #出入金记录页面
        common.switch_windows(1)
        #判断页面是否加载完成
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
        time.sleep(1)
        common.display_click('css,ul .el-submenu__icon-arrow',1)
        time.sleep(0.5)
        common.display_click('css,ul .el-submenu__icon-arrow',2)
        time.sleep(0.5)
        common.display_click('css,ul .el-submenu__icon-arrow',3)
        time.sleep(0.5)
        common.display_click("xpath,//span[.='下级出入金记录']")
        time.sleep(2)
        #每页条数-全部
        common.display_click('css,.el-select .el-select__caret',-1)
        time.sleep(0.5)
        common.display_click("xpath,//div[@class='formAndList']//span[.='全部']",-1)
        time.sleep(0.5)
        #选择时间-全部
        common.display_click('css,.el-select .el-select__caret',1)
        time.sleep(0.5)
        common.display_click("xpath,//span[.='全部']",-1)
        time.sleep(3)
        #所有下级出入金记录条数
        self.lenForlower=common.get_lenofelement('css,tbody > tr > .el-table_1_column_2 .account-txt')
        print('当前账号存在{}条下级出入金记录'.format(self.lenForlower))
        #遍历IB下级列表，找出存在出入金记录的账号
        self.lower_list=[]
        print('筛选下级出入金账号中，loading......')
        for y in range(0,self.lenForlower):
            if common.display_get_text('css,tbody > tr > .el-table_1_column_2 .account-txt',y) in self.serach_list3:
                self.lower_list.append(common.display_get_text('css,tbody > tr > .el-table_1_column_2 .account-txt',y))
        
        if len(self.lower_list)==0:
            return False
        else:
            #去重下级出入金账号列表
            self.deduplication_lower_list=list(set(self.lower_list))
            print('存在出入金记录的下级账号：{}'.format(self.deduplication_lower_list))
            #筛选
            common.display_click('css,.el-select .el-select__caret')
            time.sleep(0.5)
            common.display_click("xpath,//span[.='会员账号']",-1)
            time.sleep(0.5)
            return True
            
    
    #创建核对出金方法
    def verify_withdrawal(self,lower_account:int):
        try:
            #选择出金类型
            common.display_click('css,.el-select .el-select__caret',2)
            time.sleep(0.5)
            common.display_click("xpath,//span[.='出金']",-1)
            #输入需要查询出金的下级账号
            common.web_clear("css,[placeholder='搜索']")
            time.sleep(0.5)
            common.display_input("css,[placeholder='搜索']",lower_account)
            time.sleep(0.5)
            #搜索
            common.display_click('css,.el-button')
            time.sleep(2)
            #查询数据库
            self.lower_withdrawalDatabase=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),'atfxgm-sit', 'atfx_withdrawal',
            {"accountNumber":lower_account},'mtRefNo','accountNumber','tradeAccount','clnName','lastUpdateDate','mtAmt',N=0,sortTerm=[('_id',1)])
            
            if common.ele_is_displayed('css,.el-table__empty-text', 1):
                #该账号无出金记录
                return False
            else:
                #该账号存在出金记录
                print('数据库账号{}出金记录总数：{}'.format(lower_account,len(self.lower_withdrawalDatabase)))
                #处理页面数据
                self.len_withdrawal=common.get_lenofelement('css,tbody > tr > .el-table_1_column_1')
                print('页面账号{}出金记录条数：{}'.format(lower_account,self.len_withdrawal))
                self.withdrawal_list=[]
                for i in range(0,self.len_withdrawal):
                    self.withdrawal_dict={}
                    self.withdrawal_dict['mtRefNo']=common.display_get_text('css,tbody > tr > .el-table_1_column_1',i) #订单编号
                    self.withdrawal_dict['accountNumber']=int(common.display_get_text('css,tbody > tr > .el-table_1_column_2',i)) #会员账号
                    self.withdrawal_dict['tradeAccount']=int(common.display_get_text('css,tbody > tr > .el-table_1_column_3',i)) #交易账号
                    self.withdrawal_dict['clnName']=common.display_get_text('css,tbody > tr > .el-table_1_column_4',i) #姓名

                    self.timestr=(common.display_get_text('css,tbody > tr > .el-table_1_column_8',i))[0:-3]#时间
                    self.withdrawal_dict['lastUpdateDate']=(datetime.datetime.strptime(self.timestr,'%Y-%m-%d %H:%M'))+datetime.timedelta(hours=-3) #字符串转换成时间并减去数据库时差

                    self.withdrawal_dict['mtAmt']=-float(common.display_get_text('css,tbody > tr > .el-table_1_column_10',i)) #MT金额
                    self.withdrawal_list.append(self.withdrawal_dict)

                return True
        except Exception as msg:
            log.my_logger('!!--!!verify_withdrawal').error(msg)
            

    #创建核对入金方法
    def verify_deposit(self,lower_account:int):
        try:
            #选择入金类型
            common.display_click('css,.el-select .el-select__caret',2)
            time.sleep(0.5)
            common.display_click("xpath,//span[.='入金']",-1)
            time.sleep(0.5)
            #输入需要查询出金的下级账号
            common.web_clear("css,[placeholder='搜索']")
            time.sleep(0.5)
            common.display_input("css,[placeholder='搜索']",lower_account)
            time.sleep(0.5)
            #搜索
            common.display_click('css,.el-button')
            time.sleep(1)
            #查询数据库
            self.lower_depositDatabase=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),'atfxgm-sit', 'atfx_deposit',
            {"accountNumber":lower_account},'mtRefNo','accountNumber','tradeAccount','clnName','lastUpdateDate','mt4Amt',N=0,sortTerm=[('_id',1)])
            
            if common.ele_is_displayed('css,.el-table__empty-text', 1):
                #该账号无入金记录
                return False
            else:
                #该账号存在入金记录
                print('数据库账号{}入金记录总数：{}'.format(lower_account,len(self.lower_depositDatabase)))
                #处理页面数据
                self.len_deposit=common.get_lenofelement('css,tbody > tr > .el-table_1_column_1')
                print('页面账号{}入金记录条数：{}'.format(lower_account,self.len_deposit))
                self.deposit_list=[]
                for i in range(0,self.len_deposit):
                    self.deposit_dict={}
                    self.deposit_dict['mtRefNo']=common.display_get_text('css,tbody > tr > .el-table_1_column_1',i) #订单编号
                    self.deposit_dict['accountNumber']=int(common.display_get_text('css,tbody > tr > .el-table_1_column_2',i)) #会员账号
                    self.deposit_dict['tradeAccount']=int(common.display_get_text('css,tbody > tr > .el-table_1_column_3',i)) #交易账号
                    self.deposit_dict['clnName']=common.display_get_text('css,tbody > tr > .el-table_1_column_4',i) #姓名

                    self.timestr=(common.display_get_text('css,tbody > tr > .el-table_1_column_8',i))[0:-3]#时间
                    self.deposit_dict['lastUpdateDate']=(datetime.datetime.strptime(self.timestr,'%Y-%m-%d %H:%M'))+datetime.timedelta(hours=-3) #字符串转换成时间并减去数据库时差

                    self.deposit_dict['mt4Amt']=float(common.display_get_text('css,tbody > tr > .el-table_1_column_10',i)) #MT金额
                    self.deposit_list.append(self.deposit_dict)
                return True
        except Exception as msg:  
            log.my_logger('!!--!!verify_deposit').error(msg)


    #验证复制功能
    def verify_copy(self):
        try:
            #刷新页面
            common.general_refresh_()
            time.sleep(2)
            #查询所有
            common.display_click('css,.el-select .el-select__caret',1)
            time.sleep(0.5)
            common.display_click("xpath,//span[.='全部']",-1) #时间
            time.sleep(0.5)
            common.display_click('css,.el-select .el-select__caret',-1) #每页显示
            time.sleep(0.5)
            common.display_click("xpath,//span[.='全部']")
            time.sleep(1)
            #排序
            common.display_click('css,th .ascending')
            time.sleep(3)
            #点击复制按钮
            common.display_click('css,.lar')
            time.sleep(1)
            #获取复制内容

            self.copyData=pyperclip.paste()
            
            #处理复制数据
            self.copy_openList=[]
            for i in self.copyData:
                self.copy_openList.append(i.strip('\n')) #去除换行键
            time.sleep(1)

            #写进txt文本
            with open(os.path.join(os.path.join(path_project,'test_data'),'copy_data.txt'), 'w') as f:
                f.write(''.join(self.copy_openList))

            #txt转换成excel
            self.filename=os.path.join(os.path.join(path_project,'test_data'),'copy_data.txt')
            self.xlsxname=os.path.join(os.path.join(path_project,'test_data'),'copy_data.xlsx')
            dealData.txt_xlsx(self.filename, self.xlsxname)

            #读取复制数据
            dealData.openexcel(self.xlsxname,'sheet1')
            self.copyData=dealData.dict_data()


            #处理页面数据
            self.pageDataList=[]
            self.pageDataLen=common.get_lenofelement('css,tbody > tr > .el-table_1_column_1')
            print('处理页面数据中......')
            for i in range(0,self.pageDataLen):
                self.pageDict={}
                self.pageDict['订单编号']=common.display_get_text('css,tbody > tr > .el-table_1_column_1',i)
                self.pageDict['会员账号']=common.display_get_text('css,tbody > tr > .el-table_1_column_2',i)
                self.pageDict['交易账号']=common.display_get_text('css,tbody > tr > .el-table_1_column_3',i)
                self.pageDict['姓名']=common.display_get_text('css,tbody > tr > .el-table_1_column_4',i)
                self.pageDict['上级会员中心账号']=common.display_get_text('css,tbody > tr > .el-table_1_column_5',i)
                self.pageDict['上级返佣账号']=common.display_get_text('css,tbody > tr > .el-table_1_column_6',i)
                self.pageDict['上级名称']=common.display_get_text('css,tbody > tr > .el-table_1_column_7',i)
                self.pageDict['时间']=common.display_get_text('css,tbody > tr > .el-table_1_column_8',i)
                self.pageDict['备注']=common.display_get_text('css,tbody > tr > .el-table_1_column_9',i)
                self.pageDict['MT金额']=common.display_get_text('css,tbody > tr > .el-table_1_column_10',i)
                self.pageDataList.append(self.pageDict)

        except Exception as msg:  
            log.my_logger('!!--!!verify_copy').error(msg)

    #验证导出功能
    def verify_export(self):
        try:
            #点击导出
            common.display_click('css,.la-share-square')
            time.sleep(1)
            #获取下载文件名
            for root,dirname,filename in os.walk(os.path.join(path_project,'test_data')):
                for i in filename:
                    if re.findall('SUB_IB_CLIENT_DEPOSIT_WITHDRAWAL_LIST_...........xlsx',i)!=[]:
                        self.exportData_excel=''.join(re.findall('SUB_IB_CLIENT_DEPOSIT_WITHDRAWAL_LIST_...........xlsx',i)) #正则匹配下载文件名
                        break
                    else:
                        pass

            #读取下载文件
            dealData.openexcel(os.path.join(os.path.join(path_project,'test_data'),self.exportData_excel), 'Sheet1')
            self.exportDataList=dealData.dict_data()
        except Exception as msg:  
            log.my_logger('!!--!!verify_export').error(msg)        
    
    def closebrowser(self):
        common.close_browser()

    def quitbrowser(self):
        common.quit_browser()