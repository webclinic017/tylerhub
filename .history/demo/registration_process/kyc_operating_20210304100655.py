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

    @classmethod
    def setUpClass(cls):
        kyc.browsertype() #默认以谷歌浏览器打开
        #访问CP及bos登录页，选择页面语言
        kyc.loginweb('CN')
        #登录bos，并打开客户名单页
        kyc.login_bos('tyler.tang','Tl123456')

    
    def tearDown(self):
        #执行最后一个测试用例后关闭浏览器
        if self.data_index==testdata.index(testdata[-1]):
            kyc.quitdriver()
        else:
            #登出会员中心
            kyc.logout_cp()
            # #清空主账号搜索条件
            # kyc.clearaccount()

    @ddt.data(*testdata)
    def test_kyc(self,data):
        #获取每组测试数据的下标
        self.data_index=testdata.index(data)
        #除了第一个测试用例外，其他用例都必须点击登录页弹窗
        if self.data_index!=0:
            print(self.data_index)
            kyc.refresh_browser()
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            kyc.login_topup()
        else:
            pass
        print('当前测试数据:邮箱{}，主账号:{}'.format(data['邮箱'],data['主账号']))
        # #登录会员中心
        kyc.login_cp(data['邮箱'],'Tl123456')
        # kyc.get_on_kyc(data['主账号'])

if __name__=='__main__':
    unittest.main()