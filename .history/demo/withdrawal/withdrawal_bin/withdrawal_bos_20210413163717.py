import os
import sys
import unittest

import ddt
from BeautifulReport import BeautifulReport

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_withdrawal=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_withdrawal+r'\location_withdrawal')
from about_data import exceldata

class withdrawal_inbos(unittest.TestCase):
    
    def test1(self):
        print('结果')
        return 1<2

    @unittest.skip(test1,'跳过')
    def test2(self):
        print('cdddd')

    def test3(self):
        print(5555)

if __name__=='__main__':
    unittest.main()