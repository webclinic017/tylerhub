from KYC_method import kyc_approve
from selenium import webdriver
import unittest
import ddt
path=os.path.dirname(os.path.dirname(__file__))
path=os.path.join(path,'publick')
sys.path.append(path)
from about_data import exceldata


#实例化对象
kyc=kyc_approve()
e=exceldata()
rows=e.openexcel(r'E:\test\country.xlsx','Sheet1') #测试文档的路径，sheet名,并获取总行数
testdata=e.dict_data()

@ddt.ddt
class kyc_actions(unittest.TestCase):

    def setUp(self):
        kyc.browsertype()

    def test(self):
        kyc.login_cp('CN','tyler.tang@qq.com','Tl123456')


if __name__=='__main__':
    unittest.main()