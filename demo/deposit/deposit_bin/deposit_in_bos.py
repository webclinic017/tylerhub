'''
Author: tyler
Date: 2021-05-13 10:43:00
LastEditTime: 2022-05-27 10:31:13
LastEditors: Tyler96-QA 1718459369@qq.com
Description: In User Settings Edit
FilePath: \tylerhub\demo\deposit\deposit_bin\deposit_in_bos.py
'''
import os
import sys
import time
import unittest

import ddt
from BeautifulReport import BeautifulReport

path_public=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'public')
sys.path.append(path_public)
path_deposit=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_deposit+r'\location_deposit')
from about_data import Aboutdata
from read_dataconfig import ReadConfig
from location_deposit_of_bos import Location_deposit_bos



@ddt.ddt
class Deposit_bos(unittest.TestCase):

    global dealData,deposit,conFig,excelpath,testdata
    
    deposit=Location_deposit_bos()
    conFig=ReadConfig()

    #读取测试文档数据
    dealData=Aboutdata()
    excelpath=os.path.join(path_deposit,'test_data\deposit_bos.xlsx')
    rows=dealData.openexcel(excelpath,'Sheet1')
    testdata=dealData.dict_data()

    @classmethod
    def setUpClass(cls):
        deposit.broswertype()
        deposit.get_url('sit')

    def tearDown(self):
        if self.data_index==testdata.index(testdata[-1]):
            deposit.quitbrowser()
        else:
            deposit.logoutbos()
            deposit.refresh()

    @ddt.data(*testdata)
    def test_deposti_bos(self,data):
        #获取每组测试数据的下标
        self.data_index=testdata.index(data)
        print('当前测试账号：主账号：{}；交易账号：{}；入金金额；{}'.format(int(data['主账号']),int(data['交易账号']),data['入金金额']))
        deposit.login_bos(conFig.get_value('bos_login', 'username'),conFig.get_value('bos_login', 'password'))
        if deposit.Deposit_bos_comply(int(data['主账号']),int(data['交易账号']),
        conFig.get_value('bos_login', 'username2'),conFig.get_value('bos_login', 'password'),int(float(data['入金金额']))):
            #断言
            self.assertEqual('成功', deposit.deposit_success())
        else:
            unittest.skip('交易账号{}状态为{}无法入金'.format(int(data['交易账号']),deposit.account_status))

if __name__=='__main__':
    #测试报告
    suit=unittest.defaultTestLoader.discover(os.path.dirname(os.path.abspath(__file__)),pattern='deposit_in_bos.py',top_level_dir=None)
    BeautifulReport(suit).report(filename='BOS入金',description='BOS入金流程',report_dir=path_deposit+r'\report')