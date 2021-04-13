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

class withdrawal_actions_incp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        withdrawal.broswertype()
        withdrawal.get_url('tyler.tang','Tl123456')

    # def setUp(self):
    #     #预置条件，判断主账号及交易账号是否满足出金条件
    #     withdrawal.is_satisfy_withdrawal(1200008354,693005676)

    def test_withdrawal(self):
        #登录会员中心出金
        withdrawal.logincp('10000000027@uitest.com','Tl123456')
        withdrawal.withdrawal_action(693005664,500)


if __name__=='__main__':
    unittest.main()