from KYC_method import kyc_approve
from selenium import webdriver
import unittest
import ddt
import os
import sys
path=os.path.dirname(os.path.dirname(__file__))
path=os.path.join(path,'publick')
sys.path.append(path)
from about_data import exceldata

#实例化对象
kyc=kyc_approve()
e=exceldata()
rows=e.openexcel(r'E:\test\account_number.xlsx','Sheet1') #测试文档的路径，sheet名,并获取总行数
testdata=e.dict_data()

@ddt.ddt
class kyc_actions(unittest.TestCase):

    @classmethod #仅执行一次
    def setUpClass(cls):
        kyc.browsertype() #默认以谷歌浏览器打开
        #访问CP及BOS登录页，选择页面语言
        kyc.loginweb('CN')
        kyc.login_bos('tyler.tang','Tl123456')

    @ddt.data(*testdata)
    def test_kyc(self,data):
        #获取每组测试数据的下标
        self.data_index=testdata.index(data)
        if self.data_index!=0:
            kyc.login_topup()
        #登录会员中心
        kyc.login_cp(data['邮箱'],'Tl123456')
        


if __name__=='__main__':
    unittest.main()