import os
import sys
import time
import unittest
import ddt
from BeautifulReport import BeautifulReport
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

@ddt.ddt
class checkurl(unittest.TestCase):

    def setUp(cls):
        common.open_browser()

    @ddt.data(*testdata)
    def testurl(self,data):
        common.open_web(data['URL'])
        time.sleep(1)
        self.assertIn(common.display_get_text('css,.desc_404'),'哎哟抱歉，找不到您访问的内容或页面')

if __name__=='__main__':
    #测试报告
    suit=unittest.defaultTestLoader.discover(os.path.dirname(os.path.abspath(__file__)),
    pattern='AW5823.py',top_level_dir=None)
    BeautifulReport(suit).report(filename='URL',description='404',
    report_dir=path_demo+r'\website\404-URLreport')

