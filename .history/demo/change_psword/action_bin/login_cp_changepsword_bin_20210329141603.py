import os
import sys
import unittest

import ddt

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_psword=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_psword+r'\location')
from about_data import exceldata
from login_cp_changepsword import location

loca=location()
#测试文档路径
testdata_path=path_psword+r'\test_excel_data\test_data.xlsx'
#读取测试数据
e=exceldata()
rows=e.openexcel(testdata_path,'Sheet1')
testdata=e.dict_data()

@ddt.ddt
class change_password(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        loca.broswertype()
        loca.geturl('tyler.tang','Tl123456')

    def tearDown(self):
        if self.data_index==testdata.index(testdata[-1]):
            loca.quitbrowser()
        else:
            loca.logoutcp()
        
    @ddt.data(*testdata)
    def test_change(self,data):
        #每组测试用例下标
        print('当前测试数据：邮箱{}，主账号：{}'.format(data['邮箱'],data['主账号']))
        if self.data_index!=0:
            loca.remove_topup()
        else:
            pass
        self.data_index=testdata.index(data)
        loca.change_psword(data['邮箱'],data['旧密码'],data['主账号'],testdata_path,'C',self.data_index+2,8)
        self.assertIn(loca.get_sucessful_change(),'重设会员中心账号密码成功')

if __name__=='__main__':
    unittest.main()