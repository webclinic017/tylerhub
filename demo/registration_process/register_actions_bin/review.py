import os
import sys
import unittest

import ddt
from BeautifulReport import BeautifulReport

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_process=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_process+r'\register_positioning')
from about_data import Exceldata
from preliminary_review import review_actions

#实例化对象
rev=review_actions()
e=Exceldata()
rows=e.openexcel(path_process+r'\test_excel_data\account_number.xlsx','Sheet1') #测试文档的路径，sheet名,并获取总行数
testdata=e.dict_data()

@ddt.ddt
class review_account(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        rev.browsertype() #默认谷歌浏览器驱动
        #登录bos，默认页面语言为简中
        rev.login_bos('tyler.tang','Tl123456')

    def tearDown(self):
        #执行最后一个测试用例后关闭浏览器
        if self.data_index==testdata.index(testdata[-1]):
            rev.quitbrowser()
        else:
            rev.clear_serach()

    @ddt.data(*testdata)
    def test_review(self,data):
        #获取每组测试数据的下标
        self.data_index=testdata.index(data)
        print('当前测试数据:邮箱：{}，主账号：{}'.format(data['邮箱'],data['主账号']))
        rev.review_operation(data['主账号'])
        #断言
        self.assertIn(rev.get_success_text(),' 成功(初审) Successful (1st Review)')


if __name__=='__main__':
    suit=unittest.defaultTestLoader.discover(os.path.dirname(os.path.abspath(__file__)),
    pattern='review.py',top_level_dir=None)
    BeautifulReport(suit).report(filename='初审通过',description='审核流程',
    report_dir=path_process+r'\cp_register_process_report')