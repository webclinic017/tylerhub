'''
Author: tyler
Date: 2021-09-08 15:05:37
LastEditTime: 2021-09-09 17:14:05
LastEditors: Please set LastEditors
Description: Execute testcase
FilePath: \tylerhub\demo\neteller_withdrawal\action_bin\test_neteller_withdrawal.py
'''
import pytest
import os
import allure
import sys
path_public=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'public')
sys.path.append(path_public)
path_project=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_project+r'\location')
from about_data import Aboutdata
from read_dataconfig import ReadConfig
from location_of_neteller_withdrawal import Location_of_netellerWithdrawal

class Test_neteller_withdrawal(object):

    global netteLler,conFig,dealData,testdata,excelpath
    netteLler=Location_of_netellerWithdrawal()
    conFig=ReadConfig()
    dealData=Aboutdata()

    # #读取测试数据
    # excelpath=os.path.join(path_project,r'test_data\add_ewallet.xlsx')
    # rows=dealData.openexcel(excelpath,'Sheet1')
    # testdata=dealData.dict_data()

    def setup_class(self):
        #默认谷歌浏览器打开
        netteLler.broswertype()
        #cp，bos登录页
        netteLler.get_url('sit')
        #登录bos
        netteLler.login_bos(conFig.get_value('bos_login', 'username'), conFig.get_value('bos_login', 'password'))

    def test_neteller(self):
        netteLler.logincp('tyler.tang@test.com','Tl123456')
        #判断出金账号余额
        if netteLler.is_balance_nil(672005304):
            pytest.skip()
        else:
            if netteLler.action_neteller(1000005349,672005304,55):
                pytest.skip()


if __name__=='__main__':
    pytest.main(['-s','-v',os.path.abspath(__file__)])