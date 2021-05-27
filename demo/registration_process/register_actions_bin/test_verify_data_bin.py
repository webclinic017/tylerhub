'''
Author: your name
Date: 2021-05-24 16:11:20
LastEditTime: 2021-05-27 11:05:03
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \tylerhub\demo\registration_process\register_actions_bin\test_verify_data_bin.py
'''
import pytest
import os
import sys
import allure

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_process=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_process+r'\register_positioning')
from about_data import exceldata
from verify_message_location import location_of_verify_data

verify=location_of_verify_data()
e=exceldata()
excelpath=path_process+r'\test_excel_data\account_number.xlsx'
rows=e.openexcel(excelpath,'Sheet1')
testdata=e.dict_data()

class Test_verify_data():

    def setup_class(self):
        verify.browsertype()
        verify.login_bos('tyler.tang', 'Tl123456')

    def teardown_class(self):
        verify.quitbrowser()

    @allure.title('判断新开交易账号组别点差等信息是否正确')
    @allure.story('获取组别点差等信息')
    @pytest.mark.parametrize('data',testdata)
    def test_verfity(self,data):
        with allure.step('新开账号详情页'):
            verify.enter_details_page(int(data['主账号']))
        with allure.step('判断当前交易账号是否唯一，不唯一则跳过'):
            if verify.is_traccount_onlyone():
                with allure.step('存在多个交易账号，跳过此用例'):
                    verify.closebrowser()
                    pytest.skip()
            else:
                with allure.step('断言，判断当前交易账号开户信息是否与链接一致'):
                #断言
                    pytest.assume(verify.get_group() == data['组别'])
                    pytest.assume(verify.get_lever() == int(data['杠杆']))
                    pytest.assume(verify.get_spreadType() == data['点差'])
                    pytest.assume(verify.get_markup() == int(data['加点']))
                    pytest.assume(verify.get_currency() == data['币种'])
                    verify.closebrowser()


if __name__=='__main__':
    #pytest.main(['-v','-s',r'{}\register_actions_bin\test_verify_data_bin.py'.format(path_process)])
    pytest.main(['-s','-v',r'{}\register_actions_bin\test_verify_data_bin.py'.format(path_process),
    r'--alluredir={}\cp_register_process_report\report_data'.format(path_process),'--disable-pytest-warnings'])
    os.system(r'allure generate {}\cp_register_process_report\report_data -o {}\cp_register_process_report\new_report --clean'.format(path_process,path_process))
    os.system(r'allure serve {}\cp_register_process_report\report_data'.format(path_process))



