'''
Author: tyler
Date: 2021-05-13 10:43:00
LastEditTime: 2021-05-19 11:23:36
LastEditors: Please set LastEditors
Description: Executive document of withdrawal
FilePath: \tylerhub\demo\transfer\transfer_bin\test_transfer_action_other_one_bin.py
'''
import os
import sys
import allure
import pytest

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_transfer=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_transfer+r'\transfer_location')
from about_data import Aboutdata
from location_transfer_other_one import Locathion_of_transfer

transfer=Locathion_of_transfer()
e=Aboutdata()
excelpath=path_transfer+r'\test_data\transfer_other_one.xlsx'
rows=e.openexcel(excelpath,'Sheet1')
testdata=e.dict_data()


@allure.feature('转账')
class Test_transfer_other_account():

    def setup_class(self):
        transfer.broswertype()
        transfer.get_url('tyler.tang','Tl123456')

    def teardown(self):
        if self.data_index==testdata.index(testdata[-1]):
            with allure.step('执行最后一个测试用例时推出浏览器进程'):
                transfer.quitbrowser()

    @allure.title('上级代理给下级代理/客户转账')
    @allure.description('读取测试文档数据，转账给下级客户或者代理')
    @allure.story('转账下级')
    @pytest.mark.parametrize('data',testdata)
    def test_transfer(self,data):
        print('当前测试数据--转出主账号：{}，转出交易账号：{}，转入主账号：{}，转入交易账号：{}'.format(int(data['转出主账号']),
        int(data['转出交易账号']),int(data['转入主账号']),int(data['转入交易账号'])))

        with allure.step('获取当前测试数据下标'):
            self.data_index=testdata.index(data)

        #判断账号条件
        with allure.step('判断转出转入的主账号，交易账号是否满足转账条件'):
            if transfer.is_account_satisfy_logic(int(data['转出主账号']),int(data['转出交易账号']),int(data['转入主账号']),int(data['转入交易账号'])):
                with allure.step('不满足转账条件后跳过当前用例'):
                    pytest.skip()
            else:
                #获取转入交易账号余额，为0时跳过用例
                with allure.step('判断转出交易账号余额是否为0'):
                    if transfer.transfer_incp(data['邮箱'], data['密码'],int(data['转入主账号']),
                    int(data['转出交易账号']),int(data['转入交易账号']),float(data['转账金额'])):
                        print('转出交易账户余额为0，跳过此用例')
                        #登出会员中心
                        with allure.step('转入主账号余额为0，登出会员中心，跳过此用例执行下一用例'):
                            transfer.logout_cp()
                            transfer.remove_topup()
                            pytest.skip()
                    else:
                        #断言
                        with allure.step('判断转账是否需要审核，是否成功及断言用例是否通过'):
                            assert transfer.is_transfer_successful(int(data['转出主账号'])) in ('转账成功','Transfer Success','success'), '转账成功'

if __name__=='__main__':
    #pytest.main(['-v','-s',r'{}\transfer_bin\test_transfer_action_other_one_bin.py'.format(path_transfer)])
    pytest.main(['-s',r'{}\transfer_bin\test_transfer_action_other_one_bin.py'.format(path_transfer),
    r'--alluredir={}\transfer_report_other_one\report_data'.format(path_transfer),'--disable-pytest-warnings'])
    os.system(r'allure generate {}\transfer_report_other_one\report_data -o {}\transfer_report_other_one\new_report --clean'.format(path_transfer,path_transfer))
    os.system(r'allure serve {}\transfer_report_other_one\report_data'.format(path_transfer))
