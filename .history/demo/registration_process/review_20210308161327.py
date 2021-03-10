from preliminary_review import 
import unittest
import ddt
import os
import sys
from preliminary_review import review_actions
path=os.path.dirname(os.path.dirname(__file__))
path=os.path.join(path,'publick')
sys.path.append(path)
from about_data import exceldata

#实例化对象
rev=review_actions()
rev=review_actions()
e=exceldata()
rows=e.openexcel(r'E:\test\account_number.xlsx','Sheet1') #测试文档的路径，sheet名,并获取总行数
testdata=e.dict_data()

@ddt.ddt
class review_account(unittest.TestCase):

    @classmethod
    def setUpClass(cls):


