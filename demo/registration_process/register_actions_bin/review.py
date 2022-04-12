'''
Author: tyler
Date: 2021-08-18 16:08:10
LastEditTime: 2022-04-11 17:22:38
LastEditors: Please set LastEditors
Description: Execute test cases
FilePath: \tylerhub\demo\registration_process\register_actions_bin\review.py
'''
import os
import sys
import unittest

import ddt
from BeautifulReport import BeautifulReport

path_public=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'public')
sys.path.append(path_public)
path_process=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_process+r'\register_positioning')
from about_data import Aboutdata
from preliminary_review import Review_actions
from read_dataconfig import ReadConfig


@ddt.ddt
class Review_account(unittest.TestCase):

    global conFig,rev,dealData,testdata

    conFig=ReadConfig()
    rev=Review_actions()

    #读取测试数据
    dealData=Aboutdata()
    rows=dealData.openexcel(path_process+r'\test_excel_data\account_number.xlsx','Sheet1')
    testdata=dealData.dict_data()

    @classmethod
    def setUpClass(cls):
        rev.browsertype() #默认谷歌浏览器驱动
        #登录bos，默认页面语言为简中
        rev.login_bos('sit',conFig.get_value('bos_login', 'username'),conFig.get_value('bos_login','password'))

    def tearDown(self):
        #执行最后一个测试用例后关闭浏览器
        if self.data_index==testdata.index(testdata[-1]):
            rev.quitbrowser()
        else:
            if self.case=='':
                pass

    @ddt.data(*testdata)
    def test_review(self,data):
        #获取每组测试数据的下标
        self.data_index=testdata.index(data)
        self.case=data['邮箱']
        if self.case=='':
            print('用例为空，跳过')
        else:
            print('当前测试数据:邮箱：{}，主账号：{}'.format(data['邮箱'],int(data['主账号'])))
            rev.review_operation(int(data['主账号']))
            #断言
            self.assertIn('成功(初审)',rev.get_success_text())


if __name__=='__main__':
    suit=unittest.defaultTestLoader.discover(os.path.dirname(os.path.abspath(__file__)),
    pattern='review.py',top_level_dir=None)
    BeautifulReport(suit).report(filename='初审通过',description='审核流程',
    report_dir=path_process+r'\report')
