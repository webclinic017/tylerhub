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
        deposit.get_url('Tyler.tang','Tl123456')

    def test_deposti(self):
        print(1123)


if __name__=='__main__':
    unittest.main()