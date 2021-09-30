'''
Author: tyler
Date: 2021-09-27 15:13:40
LastEditTime: 2021-09-30 10:33:41
LastEditors: Please set LastEditors
Description: Execute testcase
FilePath: \tylerhub\demo\deposit_withdrawal_list\action_bin\test_deposti_withdrawal.py
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
from location_of_deposti_withdrawal_List import Location_of_deposit_withdrawal

class Test_deposti_withdrawal_list(object):

    global verifyList,conFig,dealData,testdata,excelpath
    verifyList=Location_of_deposit_withdrawal()
    conFig=ReadConfig()
    dealData=Aboutdata()

    # #读取测试数据
    # excelpath=os.path.join(path_project,r'test_data\walaopay_deposit.xlsx')
    # rows=dealData.openexcel(excelpath,'Sheet1')
    # testdata=dealData.dict_data()

    def setup_class(self):
        #默认谷歌浏览器打开
        verifyList.broswertype()
        #cp，bos登录页
        verifyList.get_url('sit',conFig.get_value('bos_login', 'username'),conFig.get_value('bos_login', 'password'))

    def test_verify_deposit_withdrawal_list(self):
        verifyList.logincp(1000005349)
        verifyList.serch_list(1000005349)
        

if __name__=='__main__':
    pytest.main(['-s','-v',os.path.abspath(__file__)])