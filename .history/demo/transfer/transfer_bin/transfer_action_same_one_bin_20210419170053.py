import os
import sys
import unittest

import ddt
from BeautifulReport import BeautifulReport

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_transfer=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_transfer+r'\transfer_location')
from about_data import exceldata
from location_transfer_same_one import location_of_transfer


transfer=location_of_transfer()
e=exceldata()
excelpath=path_transfer+r'\test_data\transfer_same_one.xlsx'
rows=e.openexcel(excelpath,'Sheet1')
testdata=e.dict_data()

@ddt.ddt
class transfertion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        transfer.broswertype()
        transfer.get_url('tyler.tang','Tl123456')
        return False

    @ddt.data(*testdata)
    def setUp(self,data):
        print(data['预期结果'])
        # if data['预期结果']=='fail':
        #     return False
        # else:
        #     return True

    def tearDown(self):
        if self.data_index==testdata.index(testdata[-1]):
            transfer.quitbrowser()
        else:
            transfer.logoutcp()


    #@unittest.skipIf(setUp,'预期结果为fail,跳过该测试用例')
    @ddt.data(*testdata)
    def test_transfer(self,data):
        self.data_index=testdata.index(data)

        print('当前测试数据：主账号：{}，转出交易账号：{}，转入交易账号：{}'.format(int(float(data['主账号'])),
        int(float(data['转出交易账号'])),int(float(data['转入交易账号']))))

        if self.data_index!=0:
            transfer.remove_topup()
        
        #判断主账号，交易账户是否满足转账条件
        transfer.is_satisfy_transfer(int(float(data['主账号'])),int(float(data['转出交易账号'])),int(float(data['转入交易账号'])))
        transfer.transfer_in_cp(data['邮箱'],data['密码'],int(float(data['主账号'])),
        int(float(data['转出交易账号'])),int(float(data['转入交易账号'])),int(float(data['转出金额'])),excelpath,self.data_index+2)


if __name__=='__main__':
    #测试报告
    suit=unittest.defaultTestLoader.discover(os.path.dirname(os.path.abspath(__file__)),
    pattern='transfer_action_same_one_bin.py',top_level_dir=None)
    BeautifulReport(suit).report(filename='同一主账户下的转账',description='转账流程',
    report_dir=path_transfer+r'\transfer_report')