import os
import sys
import unittest

import ddt
from BeautifulReport import BeautifulReport

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_deposit=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_deposit+r'\location_deposit')
from about_data import exceldata
from location_deposit_of_bos import location_deposit_bos

deposit=location_deposit_bos()
#读取测试文档数据
# e=exceldata()
# excelpath=path_deposit+r'\test_data\deposit_data.xlsx'
# rows=e.openexcel(excelpath,'Sheet1') #测试文档的路径，sheet名,并获取总行数
# testdata=e.dict_data()


class deposit_bos(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        deposit.get_url()

    def test_deposti_bos(self):
        print(1323)



if __name__=='__main__':
    unittest.main()