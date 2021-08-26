'''
Author: tyler
Date: 2021-05-13 10:43:00
LastEditTime: 2021-08-25 10:02:40
LastEditors: Please set LastEditors
Description: Execution testcase
FilePath: \tylerhub\demo\withdrawal\withdrawal_bin\withdrawal_cp_bin.py
'''
import os
import sys
import pytest
import allure

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_withdrawal=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_withdrawal+r'\location_withdrawal')
from about_data import Aboutdata
from location_withdrawal_cp import Location_withdrawal_incp

withdrawal=Location_withdrawal_incp()
#读取测试文档数据
e=Aboutdata()
excelpath=path_withdrawal+r'\test_data\withdrawal_data.xlsx'
rows=e.openexcel(excelpath,'Sheet1') #测试文档的路径，sheet名,并获取总行数
testdata=e.dict_data()


@allure.feature('出金')
class Test_withdrawal_actions_incp():

    def setup_class(self):
        withdrawal.broswertype()
        withdrawal.get_url('tyler.tang','Tl123456')

    def teardown_class(self):
        withdrawal.quitbrowser()


    @allure.title('交易账号出金')
    @allure.description('读取测试文档数据，判断是否具有出金条件')
    @allure.story('IB/CL出金')
    @pytest.mark.parametrize('data',testdata)
    def test_withdrawal(self,data):
        print('当前测试数据：主账号：{}；交易账号：{}；出金金额：{}'.format(int(data['主账号']),int(data['交易账号']),data['出金金额']))
        with allure.step('获取当前测试数据下标'):
            self.data_index=testdata.index(data)
        
        #判断主账号，交易账号是否满足出金条件
        with allure.step('判断交易账号是否满足出金条件'):
            if withdrawal.is_satisfy_withdrawal(int(data['主账号']),int(data['交易账号'])):
                with allure.step('当前交易账号币种非USD，跳过该用例'):
                    if self.data_index==testdata.index(testdata[-1]):
                        withdrawal.quitbrowser()
                    pytest.skip()
            else:
                #出金,审核出金
                with allure.step('判断交易账号余额是否为0'):
                    if withdrawal.withdrawal_cp(data['邮箱'],data['密码'],int(data['交易账号']),int(data['出金金额']),excelpath,self.data_index+2):
                        with allure.step('当前交易账号余额为0，跳过该用例'):
                            if self.data_index==testdata.index(testdata[-1]):
                                withdrawal.quitbrowser()
                            pytest.skip()

if __name__=='__main__':
    #测试报告
    #pytest.main(['-v','-s',r'{}\withdrawal_bin\test_withdrawal_cp_bin.py'.format(path_withdrawal)])
    pytest.main(['-s',r'{}\withdrawal_bin\test_withdrawal_cp_bin.py'.format(path_withdrawal),
    r'--alluredir={}\withdrawal_report\report_data'.format(path_withdrawal),'--disable-pytest-warnings'])
    os.system(r'allure generate {}\withdrawal_report\report_data -o {}\withdrawal_report\new_report --clean'.format(path_withdrawal,path_withdrawal))
    os.system(r'allure serve {}\ithdrawal_report\report_data'.format(path_withdrawal))