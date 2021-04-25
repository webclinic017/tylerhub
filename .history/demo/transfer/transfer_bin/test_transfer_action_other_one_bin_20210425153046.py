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
print(testdata)
data = [(1,2,3), (4,5,9), ('1', '2', '12')]
ids = [f'data{i}' for i in range(len(testdata))] # => 生成与数据数量相同的名称列表
print(ids)

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
        print('用例开始执行')

        # transfer.broswertype()
        # transfer.get_url('tyler.tang','Tl123456')o

    @pytest.mark.parametrize('data',testdata,ids=ids)
    def test_transfer(self,data):
        print(ids)
        # if ids=='data0':
        #     print('我是第一个测试用例')
        # else:
        #     print('我是第二个测试用例')
        
        print(int(data['转入主账号']))

        #判断转出主账户是否为返佣账号
        # if transfer.is_account_satisfy_logic(1000003759,67200977,1000004233,67201154):
        #     pytest.skip()
        # else:
        #     print('ib继续用例')
        

    # @pytest.mark.parametrize('a, b, c', data, ids=ids)
    # def test_add(a, b, c):
    #     print(f'\na,b,c的值:{a},{b},{c}')
    #     assert add(a, b) == c

        

    

if __name__=='__main__':
    pytest.main(['-v','-s',r'{}\transfer_bin\test_transfer_action_other_one_bin.py'.format(path_transfer)])