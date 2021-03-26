import os
import sys
import unittest
path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_psword=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_psword+r'\location')
from about_data import exceldata
from other_actions import public_method
from locate_change_pswd_cp import location


loca=location()
pub_method=public_method()

class _change_in_cp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        loca.broswertype()
        loca.geturl('tyler.tang','Tl123456')

    def testchange(self):
        loca.change_psword('10000000022@uitest.com','1200008351',pub_method.get_psword_type(8))

if __name__=='__main__':
    unittest.main()