'''
Author: tyler
Date: 2021-05-24 16:11:20
LastEditTime: 2021-08-31 16:58:23
LastEditors: Please set LastEditors
Description: Execution testcase
FilePath: \tylerhub\demo\registration_process\register_actions_bin\test_verify_data_bin.py
'''
import os
import sys

import allure
import pytest

path_public=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'public')
sys.path.append(path_public)
path_process=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_process+r'\register_positioning')


from about_data import Aboutdata
from browser_actions import Commonweb
from read_dataconfig import ReadConfig
from verify_message_location import Location_of_verify_data

#实例化
verify=Location_of_verify_data()
e=Aboutdata()
conFig=ReadConfig()
common=Commonweb()

#读取测试数据
excelpath=path_process+r'\test_excel_data\Account_number.xlsx'
rows=e.openexcel(excelpath,'Sheet1')
testdata=e.dict_data()

@allure.feature('验证审核后信息')
class Test_verify_data():

    def setup_class(self):
        verify.browsertype()
        #测试环境及登录bos用户配置，设置配置文件及更改environment参数即可
        verify.login_bos('sit',conFig.get_value('bos_login', 'username'),conFig.get_value('bos_login', 'password'))

    def teardown_class(self):
        verify.quitbrowser()

    # @allure.title('判断新开交易账号组别点差等信息是否正确')
    @allure.story('获取组别点差等信息')
    @pytest.mark.parametrize('data',testdata)
    def test_verfity(self,data):
        with allure.step('新开账号详情页'):
            verify.enter_details_page(int(data['主账号']))
        with allure.step('判断当前交易账号是否唯一，不唯一则跳过，唯一则验证开户信息：'):
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
                    with open(verify.screenshots_path('账号详情'),'rb') as f: #二进制打开截图文件
                        comtent=f.read()
                    allure.attach(comtent,'账号信息',allure.attachment_type.PNG)
                    verify.closebrowser()


if __name__=='__main__':
    pytest.main(['-s','-v',os.path.abspath(__file__),
    r'--alluredir={}\report\result'.format(path_process),'--disable-pytest-warnings'])
    os.system(r'allure generate {}\report\result -o {}\report\allure_report --clean'.format(path_process,path_process))
    os.system(r'allure serve {}\report\result'.format(path_process))