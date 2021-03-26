import os
import sys
import unittest
path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
#registration_process路径
path_psword=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_psword+r'\location')
from about_data import exceldata
from locate_change_pswd import locat


loc=locat()

class changeps(unittest.TestCase):
    def setUp(self):
        loc.broswertype()

    def testchange(self):
        loc.geturl()
        loc.clik()


if __name__=='__main__':
    unittest.main()