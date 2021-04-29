import os
import sys
import pytest

import ddt
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



    @pytest.mark.parametrize('data',testdata)
    def test_transfer(self,data):
        print('当前测试数据--转出主账号：{}，转出交易账号：{}，转入主账号：{}，转入交易账号：{}'.format(int(data['转出主账号']),
        int(data['转出交易账号']),int(data['转入主账号']),int(data['转入交易账号'])))
        if 3>2:
            pytest.skip()
        #判断转出主账户是否为返佣账号
        if transfer.is_account_satisfy_logic(int(data['转出主账号']),int(data['转出交易账号']),int(data['转入主账号']),int(data['转入交易账号'])):
            pytest.skip()
        else:
            #获取转入交易账号余额，为0时跳过用例
            if transfer.transfer_incp(data['邮箱'], data['密码'],int(data['转入主账号']),
            int(data['转出交易账号']),int(data['转入交易账号']),float(data['转账金额'])):
                print('转出交易账户余额为0，跳过此用例')
                #登出会员中心
                transfer.logout_cp()
                pytest.skip()
            else:
                print('继续执行用例')



        

    

if __name__=='__main__':
    pytest.main(['-v','-s',r'{}\transfer_bin\test_transfer_action_other_one_bin.py'.format(path_transfer)])