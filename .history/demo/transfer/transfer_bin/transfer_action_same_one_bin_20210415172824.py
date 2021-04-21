import os
import sys
import unittest

import ddt
from BeautifulReport import BeautifulReport

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_transfer=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_transfer+r'\transfer_location')
from about_data import exceldata
from location_transfer_same_one import location_of_transfer


transfer=location_of_transfer()


class transfertion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        transfer.broswertype()
        transfer.get_url('tyler.tang','Tl123456')


    @unittest.skipIf(transfer.isok)
    def test_transfer(self):
        #判断主账号，交易账户是否满足转账条件
        #transfer.is_satisfy_transfer(1000003759,652002181,65200904)
        transfer.transfer_in_cp('lemon.lin@newtype.io','Tl123456',652002181,65200904)


  
if __name__=='__main__':
    unittest.main()