import os
import sys
import unittest

import ddt
from BeautifulReport import BeautifulReport

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_deposit=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_deposit+r'\location_deposit')
from about_data import exceldata
from location_deposit_of_cp import locations_of_deposit

deposit=locations_of_deposit()
#读取测试文档数据
e=exceldata()
excelpath=path_deposit+r'\test_data\deposit_data.xlsx'
rows=e.openexcel(excelpath,'Sheet1') #测试文档的路径，sheet名,并获取总行数
testdata=e.dict_data()

@ddt.ddt
class depositincp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        deposit.broswertype()
        deposit.get_url()

    def setUp(self):
        deposit.login_bos('tyler.tang','Tl123456')

    def tearDown(self):
        if self.data_index==testdata.index(testdata[-1]):
            deposit.quitbrowser()
        else:
            deposit.logoutcp()
            deposit.logoutbos()

    @ddt.data(*testdata)
    def test_deposti(self,data):
        #获取每组测试数据的下标
        self.data_index=testdata.index(data)
        if self.data_index!=0:
            deposit.remove_topup()
        #判断交易账号是否满足入金权限
        deposit.is_traccount_can_deposit(data['主账号'],data['交易账号'])
        #会员中心入金
        deposit.deposit_cp(data['交易账号'],data['邮箱'],data['登录密码'],data['入金金额'],'tyler.tang2','Tl123456',excelpath,self.data_index+2)
        
if __name__=='__main__':
    #测试报告
    suit=unittest.defaultTestLoader.discover(os.path.dirname(os.path.abspath(__file__)),
    pattern='deposit_in_cp.py',top_level_dir=None)
    BeautifulReport(suit).report(filename='会员中心入金',description='入金流程',
    report_dir=path_deposit+r'\deposit_report')
