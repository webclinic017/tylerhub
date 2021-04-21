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

    def test_transfer(self):
        transfer.ender_detail_page(1200008354)
    

if __name__=='__main__':
    unittest.main()