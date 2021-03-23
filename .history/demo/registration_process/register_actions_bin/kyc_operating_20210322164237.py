import os
import sys
import unittest
import ddt
from BeautifulReport import BeautifulReport

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_process=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_process+r'\register_positioning')
from about_data import exceldata
from KYC_method import kyc_approve

#实例化对象
kyc=kyc_approve()
e=exceldata()
rows=e.openexcel(path_process+r'\test_excel_data\account_number.xlsx','Sheet1') #测试文档的路径，sheet名,并获取总行数
testdata=e.dict_data()

@ddt.ddt
class kyc_actions(unittest.TestCase):
    """关键字驱动：完成邮箱注册及KYC表单操作"""

    @classmethod
    def setUpClass(cls):
        kyc.browsertype() #默认以谷歌浏览器打开
        #访问CP及bos登录页，选择页面语言
        kyc.loginweb('CN',self.country_type)
        #登录bos，并打开客户名单页
        kyc.login_bos('tyler.tang','Tl123456')

    def tearDown(self):
        #执行最后一个测试用例后关闭浏览器
        if self.data_index==testdata.index(testdata[-1]):
            kyc.quitdriver()
        else:
            #登出会员中心
            kyc.logout_cp()
            if not self.country_type=='中国':
                #清空主账号搜索条件
                kyc.clearaccount()
            else:
                pass

    @ddt.data(*e.dict_data())
    def test_kyc(self,data):
        #获取每组测试数据的下标
        self.data_index=testdata.index(data)
        self.country_type=data['国家']
        #除了第一个测试用例外，其他用例都必须点击登录页弹窗
        if self.data_index!=0:
            kyc.login_topup()
        else:
            pass
        #登录会员中心
        kyc.login_cp(data['邮箱'],'Tl123456')
        #去除首次登录会员中心的弹窗
        kyc.fisrtcp_top()
        #获取主账号并保存
        e.saveainfo(path_process+r'\test_excel_data\account_number.xlsx',kyc.get_account_(),'C',self.data_index+2)
        print('当前测试数据:邮箱{}'.format(data['邮箱']))
        #KYC表单认证
        kyc.get_on_kyc(data['地区'])
        #断言
        self.assertIn(kyc.get_kyc_success(),'成功提交个人验证资料！Successfully submitted personal verification information!')

if __name__=='__main__':
    suit=unittest.defaultTestLoader.discover(os.path.dirname(os.path.abspath(__file__)),
    pattern='kyc_operating.py',top_level_dir=None)
    BeautifulReport(suit).report(filename='kyc认证',description='kyc认证流程',
    report_dir=path_process+r'\cp_register_process_report')
