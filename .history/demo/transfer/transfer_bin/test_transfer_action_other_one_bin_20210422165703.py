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


class Test_transfer_other_account():

    def setup_class(self):
        transfer.broswertype()
        transfer.get_url('tyler.tang', 'Tl123456')

    def is_bateaccount(self):
        transfer.is_fanyong_account(100003759)

    def test_transfer(self):
        if self.is_bateaccount():
            pytest.skip('交易账号为返佣账户，跳过')
        else:
            print(555555)
        

    

if __name__=='__main__':
    pytest.main(['-v','-s',r'{}\transfer_bin\test_transfer_action_other_one_bin.py'.format(path_transfer)])