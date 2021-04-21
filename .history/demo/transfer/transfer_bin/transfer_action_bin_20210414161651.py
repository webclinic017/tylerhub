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
from location_transfer import transfer_location

transfer=transfer_location()


class transfer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        transfer.broswertype()
        transfer.get_url('tyler.tang','Tl123456')

    def test_transfer(self):
        print(8888)
    

if __name__=='__main__':
    unittest.main()