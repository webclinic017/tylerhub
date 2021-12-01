'''
Author: tyler
Date: 2021-05-13 10:43:00
LastEditTime: 2021-12-01 17:01:27
LastEditors: Please set LastEditors
Description: Execute kyc test case
FilePath: \tylerhub\demo\registration_process\register_actions_bin\kyc_operating.py
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
from KYC_method import Kyc_approve
from read_dataconfig import ReadConfig


@ddt.ddt
class Kyc_actions(unittest.TestCase):
    """关键字驱动：完成邮箱注册及KYC表单操作,账号类型包括IB和CL以及中国区账号的处理"""

    global kyc,conFig,dealData,testdata

    kyc=Kyc_approve()
    conFig=ReadConfig()
    dealData=Aboutdata()
    rows=dealData.openexcel(path_process+r'\test_excel_data\Account_number.xlsx','Sheet1') #测试文档的路径，sheet名,并获取总行数
    testdata=dealData.dict_data()

    @classmethod
    def setUpClass(cls):
        kyc.browsertype() #默认以谷歌浏览器打开
        #访问CP及bos登录页，选择页面语言
        kyc.loginweb('sit','CN')
        #登录bos，并打开客户名单页
        kyc.login_bos(conFig.get_value('bos_login', 'username'),conFig.get_value('bos_login', 'password'))


    def tearDown(self):
        #执行最后一个测试用例后关闭浏览器
        if self.data_index==testdata.index(testdata[-1]):
            kyc.quitdriver()
        else:
            if self.case=='':
                pass
            else:
                #登出会员中心
                kyc.logout_cp()


    @ddt.data(*dealData.dict_data())
    def test_kyc(self,data):
        #获取每组测试数据的下标
        self.data_index=testdata.index(data)
        self.case=data['邮箱']
        if self.case=='':
            print('用例为空，跳过')
            pass
        else:
            self.region=data['地区']
            #除了第一个测试用例外，其他用例都必须点击登录页弹窗
            if self.data_index!=0:
                kyc.login_topup()
            else:
                pass
            #登录会员中心
            kyc.login_cp(data['邮箱'],'Tl123456')
            #获取主账号并保存
            dealData.saveainfo(path_process+r'\test_excel_data\Account_number.xlsx',kyc.get_account_(),'C',self.data_index+2)
            print('当前测试数据:邮箱{}'.format(data['邮箱']))
            #KYC表单认证
            kyc.get_on_kyc(data['地区'])
            #断言
            self.assertIn(kyc.get_kyc_success(),'您的资料正在审批中，您可查看 “季度市场展望” ，了解更多行情资讯 Your information is under review, you can check the "Quarterly Market Outlook" for more market information')


if __name__=='__main__':
    suit=unittest.defaultTestLoader.discover(os.path.dirname(os.path.abspath(__file__)),
    pattern='kyc_operating.py',top_level_dir=None)
    BeautifulReport(suit).report(filename='kyc认证',description='kyc认证流程',
    report_dir=path_process+r'\report')