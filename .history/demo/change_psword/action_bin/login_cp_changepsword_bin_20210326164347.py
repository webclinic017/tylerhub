import os
import sys
import unittest

import ddt

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_psword=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_psword+r'\location')
from about_data import exceldata
from login_cp_changepsword import location

loca=location()


class change_password(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        loca.broswertype()
        loca.geturl('tyler.tang','Tl123456')

    def test_change(self):
        print(133)

if __name__=='__main__':
    unittest.main()