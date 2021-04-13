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

    @ddt.data(*testdata)
    def setUp(self,data):
        #预置条件，判断主账号及交易账号是否满足出金条件
        withdrawal.is_satisfy_withdrawal(data['主账号'],data['交易账号'])

    def tearDown(self):
        #登出会员中心
        withdrawal.logoutcp()

    @ddt.data(*testdata)
    def test_withdrawal(self,data):
        #出金审核出金
        withdrawal.withdrawal_cp(data['邮箱'],data['密码'],data['交易账号'],data['出金金额'])



if __name__=='__main__':
    unittest.main()