'''
Author: tyler
Date: 2021-05-28 17:32:52
LastEditTime: 2021-05-28 17:52:02
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \tylerhub\demo\E-wallet_deposit\e-wallet_deposit_bin\test_ewallet_deposti.py
'''
import os
import sys
import pytest

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_Ewallet=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_Ewallet+r'\location_ewallet')
from about_data import exceldata
from location_deposit_of_ewallet import Ewallet_deposti

ewallet=Ewallet_deposti()

class Test_Ewallet_deposit():

    def setup_class(self):
        ewallet.broswertype()
        ewallet.get_url()
        ewallet.login_bos('tyler.tang', 'Tl123456')

    def test_deposit_of_ewallet(self):
        print(988888)


if __name__=='__main__':
    pytest.main(['-v','-s',r'{}\e-wallet_deposit_bin\test_ewallet_deposit.py'.format(path_Ewallet)])