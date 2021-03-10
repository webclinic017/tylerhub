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
        rev.browsertype() #默认谷歌浏览器驱动
        #登录bos
        rev.login_bos('tyler','Tl123456')

    def tearDown(self):
        #执行最后一个测试用例后关闭浏览器
        if self.data_index==testdata.index(testdata[-1]):
            rev.quitdriver()
        else:


    @ddt.data(*testdata)
    def test_review(self,data):
        #获取每组测试数据的下标
        self.data_index=testdata.index(data)
        rev.review_operation(data['主账号'])
        #断言
        self.assertIn(rev.get_success_text(),' 成功(初审) Successful (1st Review)')


