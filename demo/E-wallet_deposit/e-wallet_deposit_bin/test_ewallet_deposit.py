'''
Author: tyler
Date: 2021-05-28 17:32:52
LastEditTime: 2022-06-08 09:56:54
LastEditors: Tyler96-QA 1718459369@qq.com
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
from about_data import Aboutdata
from location_deposit_of_ewallet import Ewallet_deposti
from read_dataconfig import ReadConfig


class Test_Ewallet_deposit():
    global ewallet,conFig

    ewallet=Ewallet_deposti()
    conFig=ReadConfig()

    def setup_class(self):
        ewallet.broswertype()
        #登录bos，进入支付渠道管理页面
        ewallet.get_url('sit',conFig.get_value('bos_login', 'username'),conFig.get_value('bos_login', 'password'))
        
        ewallet.is_all_ewallet_open('sit')
        
    def test_deposit_of_ewallet(self):
        ewallet.bos_to_cp('1000003759')
       
        
        


if __name__=='__main__':
    pytest.main(['-v','-s',r'{}\e-wallet_deposit_bin\test_ewallet_deposit.py'.format(path_Ewallet)])