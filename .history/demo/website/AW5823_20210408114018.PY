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
#读取测试文档数据
e=exceldata()
excelpath=path_demo+r'\website\url.xlsx'
rows=e.openexcel(excelpath,'Sheet1') #测试文档的路径，sheet名,并获取总行数
testdata=e.dict_data()

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

