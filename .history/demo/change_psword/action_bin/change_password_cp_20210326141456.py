import os
import sys
import unittest
import ddt
path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_psword=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_psword+r'\location')
from about_data import exceldata
from other_actions import public_method
from locate_change_pswd_cp import location


loca=location()
pub_method=public_method()
#读取测试数据
e=exceldata()
rows=e.openexcel(path_psword+r'\test_excel_data\test_data.xlsx','Sheet1') #测试文档的路径，sheet名,并获取总行数
testdata=e.dict_data()

@ddt.ddt
class _change_in_cp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        loca.broswertype()
        loca.geturl('tyler.tang','Tl123456')

    def tearDown(self):
        if self.data_index==testdata.index(testdata[-1]):
            loca.quitbroswer()
        else:
            loca.clear_bos_serch()


    @ddt.data(*testdata)
    def testchange(self,data):
        #获取每组测试数据的下标
        self.data_index=testdata.index(data)
        if self.data_index!=0:
            loca.remove_topup()
        loca.change_psword(datap['邮箱'],data['主账号'],path_psword+r'\test_excel_data\test_data.xlsx','C',self.data_index+2)
        print(loca.sucess_change())

if __name__=='__main__':
    unittest.main()