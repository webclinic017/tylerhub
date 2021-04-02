import os
import sys
import unittest

import ddt
from BeautifulReport import BeautifulReport

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_deposti=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_deposti+r'\location_deposit')
from about_data import exceldata
from location_deposit_of_cp import locations_of_deposit

deposit=locations_of_deposit()


class depositincp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        deposit.broswertype()
        deposit.get_url()

    def setUp(self):
        deposit.login_bos('tyler.tang','Tl123456')

    def tearDown(self):
        deposit.logoutcp()
        deposit.logoutbos()

    def test_deposti(self):
        #判断交易账号是否满足入金权限
        deposit.is_traccount_can_deposit(1200008354,693005666)
        deposit.deposit_cp(693005666,'10000000027@uitest.com','Tl123456',300,'tyler.tang2','Tl123456')
        
if __name__=='__main__':
    unittest.main()