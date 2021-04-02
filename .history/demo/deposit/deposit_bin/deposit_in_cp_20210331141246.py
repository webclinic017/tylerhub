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
        deposit.get_url('tyler.tang','Tl123456')

    def test_deposti(self):
        #进入账号详情页
        deposit.ennter_the_details_page('1200008354')
        #判断主账号权限是否开启
        deposit.open_deposit_permissions()
        deposit.tdaccount_status(693005665)
        deposit.deposti_is_selected(693005660)

if __name__=='__main__':
    unittest.main()