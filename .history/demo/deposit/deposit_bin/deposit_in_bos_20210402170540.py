import os
import sys
import unittest
import time
import ddt
from BeautifulReport import BeautifulReport

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_deposit=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_deposit+r'\location_deposit')
from about_data import exceldata
from location_deposit_of_bos import location_deposit_bos

deposit=location_deposit_bos()
#读取测试文档数据
e=exceldata()
excelpath=path_deposit+r'\test_data\deposit_data.xlsx'
rows=e.openexcel(excelpath,'Sheet1') #测试文档的路径，sheet名,并获取总行数
testdata=e.dict_data()

@ddt.ddt
class deposit_bos(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        deposit.broswertype()
        deposit.get_url()

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
        print('当前测试账号：主账号：{}；交易账号：{}；入金金额；{}'.format(data['主账号'],data['交易账号'],data['入金金额']))
        deposit.login_bos('tyler.tang','Tl123456')
        deposit.deposit_bos_comply(data['主账号'],data['交易账号'],'tyler.tang2','Tl123456',int(float(data['入金金额'])))

if __name__=='__main__':
    #测试报告
    suit=unittest.defaultTestLoader.discover(os.path.dirname(os.path.abspath(__file__)),
    pattern='deposit_in_bos.py',top_level_dir=None)
    BeautifulReport(suit).report(filename='BOS入金',description='BOS入金流程',
    report_dir=path_deposit+r'\deposit_report')
