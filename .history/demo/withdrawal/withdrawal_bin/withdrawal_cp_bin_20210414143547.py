import os
import sys
import unittest

import ddt
from BeautifulReport import BeautifulReport

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_withdrawal=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_withdrawal+r'\location_withdrawal')
from about_data import exceldata
from location_withdrawal_cp import location_withdrawal_incp
from verification_code import skip_dependon

withdrawal=location_withdrawal_incp()
#读取测试文档数据
e=exceldata()
excelpath=path_withdrawal+r'\test_data\withdrawal_data.xlsx'
rows=e.openexcel(excelpath,'Sheet1') #测试文档的路径，sheet名,并获取总行数
testdata=e.dict_data()

@ddt.ddt
class withdrawal_actions_incp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        withdrawal.broswertype()
        withdrawal.get_url('tyler.tang','Tl123456')

    def tearDown(self):
        if self.data_index==testdata.index(testdata[-1]):
            withdrawal.quitbrowser()
        else:
            withdrawal.logoutcp()


    @ddt.data(*testdata)
    def test_withdrawal(self,data):
        self.data_index=testdata.index(data)
        #判断主账号，交易账号是否满足出金条件
        print('当前测试数据：主账号：{}；交易账号：{}；出金金额：{}'.format(int(data['主账号']),int(data['交易账号']),data['出金金额']))
        withdrawal.is_satisfy_withdrawal(int(data['主账号']),int(data['交易账号']))
        if self.data_index!=0:
            withdrawal.remove_topup()
        #出金审核出金
        withdrawal.withdrawal_cp(data['邮箱'],data['密码'],int(data['交易账号']),int(data['出金金额']),excelpath,self.data_index+2)


if __name__=='__main__':
    #测试报告
    suit=unittest.defaultTestLoader.discover(os.path.dirname(os.path.abspath(__file__)),
    pattern='withdrawal_cp_bin.py',top_level_dir=None)
    BeautifulReport(suit).report(filename='会员中心出金',description='出金流程',
    report_dir=path_withdrawal+r'\withdrawal_report')
