import os
import random
import sys
import time
import unittest
import ddt
path_demo=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_public=path_demo+r'\public'
sys.path.append(path_public)
from about_data import exceldata
from browser_actions import Commonweb
from other_actions import public_method


common=Commonweb()

# @ddt.ddt
class checkurl(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        common.open_browser()

    # @ddt.data()
    def testurl(self):
        common.open_web('https://www.hyap.com/news/270.html')

if __name__=='__main__':
    unittest.main()

