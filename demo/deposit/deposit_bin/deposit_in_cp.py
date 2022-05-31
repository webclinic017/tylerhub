'''
Author: tyler
Date: 2021-05-13 10:43:00
LastEditTime: 2022-05-31 10:45:23
LastEditors: Tyler Tang tyler.tang@6317.io
Description: Execution testcase
FilePath: \tylerhub\demo\deposit\deposit_bin\deposit_in_cp.py
'''
import os
import sys
import unittest

import ddt
from BeautifulReport import BeautifulReport

path_public=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'public')
sys.path.append(path_public)
path_deposit=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_deposit+r'\location_deposit')
from about_data import Aboutdata
from read_dataconfig import ReadConfig
from location_deposit_of_cp import Locations_of_deposit


@ddt.ddt
class Depositin_cp(unittest.TestCase):

    global conFig,deposit,excelpath,testdata
    #实例化
    conFig=ReadConfig()
    deposit=Locations_of_deposit()

    #读取测试文档数据
    dealData=Aboutdata()
    excelpath=os.path.join(path_deposit,'test_data\deposit_cp.xlsx')
    rows=dealData.openexcel(excelpath,'Sheet1')
    testdata=dealData.dict_data()

    @classmethod
    def setUpClass(cls):
        deposit.broswertype()
        deposit.get_url('sit')

    def setUp(self):
        deposit.login_bos(conFig.get_value('bos_login', 'username'),conFig.get_value('bos_login', 'password'))

    def tearDown(self):
        if self.data_index==testdata.index(testdata[-1]):
            deposit.quitbrowser()


    @ddt.data(*testdata)
    def test_deposti(self,data):
        #获取每组测试数据的下标
        self.data_index=testdata.index(data)
        print('当前测试数据：主账号：{}，交易账号：{}，入金金额：{}'.format(int(data['主账号']),int(data['交易账号']),float(data['入金金额'])))
        if self.data_index!=0:
            deposit.remove_topup()
        #判断交易账号是否满足入金权限
        if deposit.is_traccount_can_deposit(int(data['主账号']),int(data['交易账号'])):
            #会员中心入金
            deposit.deposit_cp(int(data['交易账号']),data['邮箱'],data['登录密码'],int(float(data['入金金额'])),
            conFig.get_value('bos_login', 'username2'),conFig.get_value('bos_login', 'password'),excelpath,'F','G',self.data_index+2)
            #断言
            self.assertEqual('成功', deposit.deposit_success())
        else:
            print('跳过该用例')
            unittest.skip('交易账号状态同步中无法入金')
        
if __name__=='__main__':
    #测试报告
    suit=unittest.defaultTestLoader.discover(os.path.dirname(os.path.abspath(__file__)),pattern='deposit_in_cp.py',top_level_dir=None)
    BeautifulReport(suit).report(filename='会员中心入金',description='入金流程',report_dir=path_deposit+r'\report')
