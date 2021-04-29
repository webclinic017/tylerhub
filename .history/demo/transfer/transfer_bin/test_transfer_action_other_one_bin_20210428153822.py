import os
import sys
import pytest

import ddt
import allure
from BeautifulReport import BeautifulReport
path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_transfer=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_transfer+r'\transfer_location')
from about_data import exceldata
from location_transfer_other_one import locathion_of_transfer


transfer=locathion_of_transfer()
e=exceldata()
excelpath=path_transfer+r'\test_data\transfer_other_one.xlsx'
rows=e.openexcel(excelpath,'Sheet1')
testdata=e.dict_data()


@allure.feature('转账下级')
class Test_transfer_other_account():
    """
    转账给下级逻辑：
    转出主账户必须为IB，转出交易账号必须为返佣账号
    若转入主账户为CL，转入交易账号可以为CL账户下的任一交易账号
    若转入主账号为IB，转入交易账户只能为下级IB的返佣账号
    判断逻辑：
    判断转出主账户是否为IB，否，则跳过
    再判断转入主账号是否为IB，否，则对转入交易账号不做判断
    是，则对转入交易账号做返佣账户判断
    """

    def setup_class(self):
        transfer.broswertype()
        transfer.get_url('tyler.tang','Tl123456')

    # def teardown(self):
    #     if self.data_index==testdata.index(testdata[-1]):
    #         transfer.quitbrowser()

    @allure.story('判断账号是否满足转账权限')
    @pytest.mark.parametrize('data',testdata)
    def test_transfer(self,data):
        print('当前测试数据--转出主账号：{}，转出交易账号：{}，转入主账号：{}，转入交易账号：{}'.format(int(data['转出主账号']),
        int(data['转出交易账号']),int(data['转入主账号']),int(data['转入交易账号'])))
        
        # self.data_index=testdata.index(data)
        # if self.data_index!=0:
        #     transfer.remove_topup()

        # #判断转出主账户是否为返佣账号
        # if transfer.is_account_satisfy_logic(int(data['转出主账号']),int(data['转出交易账号']),int(data['转入主账号']),int(data['转入交易账号'])):
        #     pytest.skip()
        # else:
        #     #获取转入交易账号余额，为0时跳过用例
        #     if transfer.transfer_incp(data['邮箱'], data['密码'],int(data['转入主账号']),
        #     int(data['转出交易账号']),int(data['转入交易账号']),float(data['转账金额'])):
        #         print('转出交易账户余额为0，跳过此用例')
        #         #登出会员中心
        #         transfer.logout_cp()
        #         pytest.skip()
        #     else:
        #         #断言
        #         assert transfer.is_transfer_successful(int(data['转出主账号'])) in ('转账成功','Transfer Success','success'), '转账成功'


if __name__=='__main__':
    #pytest.main(['-v','-s',r'{}\transfer_bin\test_transfer_action_other_one_bin.py'.format(path_transfer)])
    #pytest.main(['--alluredir',r'{}\transfer_bin\test_transfer_action_other_one_bin.py'.format(path_transfer)])
    #os.system('allure generate r{}\transfer_bin\test_transfer_action_other_one_bin.py -o r{}\transfer_report --clean'.format(path_transfer,path_transfer))
    pytest.main(['-v','-s','--alluredir',r'{}\transfer_report_other_one\report_data'.format(path_transfer),'--disable-pytest-warnings'])
    os.system(r'allure generate {}\transfer_report_other_one\report_data\ -o {}\transfer_report_other_one\new_report --clean'.format(path_transfer,path_transfer))
    # pytest.main(['--allure generate r{}\transfer_report -o ./transfer_report --clean'.format(path_transfer)])