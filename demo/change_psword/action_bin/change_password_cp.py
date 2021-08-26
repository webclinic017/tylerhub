'''
Author: tyler
Date: 2021-05-13 10:43:00
LastEditTime: 2021-08-24 10:47:34
LastEditors: Please set LastEditors
Description: Enforcement change password testcase
FilePath: \tylerhub\demo\change_psword\action_bin\Change_password_cp.py
'''
import os
import sys
import unittest

import ddt
from BeautifulReport import BeautifulReport

path_public=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'public')
print(path_public)
sys.path.append(path_public)
path_psword=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_psword+r'\location')
from about_data import Aboutdata
from locate_change_pswd_cp import Location
from read_dataconfig import ReadConfig

#实例化
loca=Location()
conFig=ReadConfig()

#读取测试数据
e=Aboutdata()
rows=e.openexcel(path_psword+r'\test_excel_data\test_data.xlsx','Sheet1') #测试文档的路径，sheet名,并获取总行数
testdata=e.dict_data()

@ddt.ddt
class Change_in_cp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        loca.broswertype()
        loca.geturl('sit',conFig.get_value('bos_login', 'username'),conFig.get_value('bos_login', 'password'))

    def tearDown(self):
        if self.data_index==testdata.index(testdata[-1]):
            loca.quitbroswer()
        else:
            loca.clear_bos_serch()

    @ddt.data(*testdata)
    def testchange(self,data):
        #获取每组测试数据的下标
        self.data_index=testdata.index(data)
        print('当前测试数据：邮箱：{}，主账号：{}'.format(data['邮箱'],int(data['主账号'])))
        if self.data_index!=0:
            loca.remove_topup()
        loca.change_psword(data['邮箱'],int(data['主账号']),path_psword+r'\test_excel_data\test_data.xlsx','C',self.data_index+2)
        #断言
        self.assertIn(loca.sucess_change(),'密码更新成功！Password update successful!')

if __name__=='__main__':
    #测试报告
    suit=unittest.defaultTestLoader.discover(os.path.dirname(os.path.abspath(__file__)),
    pattern='change_password_cp.py',top_level_dir=None)
    BeautifulReport(suit).report(filename='忘记密码页面修改密码密',description='非同名账号忘记密码页面修改修改密码流程',
    report_dir=path_psword+r'\report')
