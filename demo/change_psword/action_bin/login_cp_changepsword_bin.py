'''
Author: tyler
Date: 2021-05-13 10:43:00
LastEditTime: 2021-12-08 17:00:10
LastEditors: Please set LastEditors
Description: Enforcement change password testcase
FilePath: \tylerhub\demo\change_psword\action_bin\login_cp_changepsword_bin.py
'''
import os
import sys
import unittest

import ddt
from BeautifulReport import BeautifulReport

path_public=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'public')
sys.path.append(path_public)
path_psword=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_psword+r'\location')
from about_data import Aboutdata
from login_cp_changepsword import Location
from read_dataconfig import ReadConfig


@ddt.ddt
class Change_password(unittest.TestCase):

    global loca,conFig,testdata_path,dealData,testdata

    loca=Location()
    conFig=ReadConfig()

    testdata_path=os.path.join(path_psword,'test_excel_data\chang_psword_incp.xlsx')
    dealData=Aboutdata()
    rows=dealData.openexcel(testdata_path,'Sheet1')
    testdata=dealData.dict_data()

    @classmethod
    def setUpClass(cls):
        loca.broswertype()
        loca.geturl('sit',conFig.get_value('bos_login','username'),conFig.get_value('bos_login','password'))

    def tearDown(self):
        if self.data_index==testdata.index(testdata[-1]):
            loca.quitbrowser()
        else:
            loca.logoutcp()
        
    @ddt.data(*testdata)
    def test_change(self,data):
        #每组测试用例下标
        print('当前测试数据：邮箱{}，主账号：{}'.format(data['邮箱'],int(data['主账号'])))
        self.data_index=testdata.index(data)
        if self.data_index!=0:
            loca.remove_topup()
        else:
            pass
        loca.change_psword(data['邮箱'],data['旧密码'],int(data['主账号']),testdata_path,'C',self.data_index+2,8)
        self.assertIn(loca.get_sucessful_change(),'重设会员中心账号密码成功')

if __name__=='__main__':
    #测试报告
    suit=unittest.defaultTestLoader.discover(os.path.dirname(os.path.abspath(__file__)),
    pattern='login_cp_changepsword_bin.py',top_level_dir=None)
    BeautifulReport(suit).report(filename='登录后改密',description='账户设置也修改密码',
    report_dir=path_psword+r'\report')