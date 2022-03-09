'''
Author: your name
Date: 2022-02-21 17:22:37
LastEditTime: 2022-03-01 17:27:54
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \tylerhub\demo\IB_deposit_withdrawal_list\actions\Test_IB_Deposit_Withdrawal.py
'''
import pytest
import os
import allure
import sys
import pytest_check as check
path_public=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'public')
sys.path.append(path_public)
path_project=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_project+r'\location')
from about_data import Aboutdata
from read_dataconfig import ReadConfig
from Location_of_Deposit_Withdrawal_List import Location_of_deposit_withdrawal


class Test_IB_deposit_withdrawal_list(object):
    
    global IBVerifyList,conFig,dealData,testdata,excelpath
    IBVerifyList=Location_of_deposit_withdrawal()
    conFig=ReadConfig()
    dealData=Aboutdata()

    # #读取测试数据
    # excelpath=os.path.join(path_project,r'test_data\search_depositAndwithdrawal.xlsx')
    # rows=dealData.openexcel(excelpath,'Sheet1')
    # testdata=dealData.dict_data()

    def setup_class(self):
        #默认谷歌浏览器打开
        IBVerifyList.broswertype()
        #cp，bos登录页
        IBVerifyList.get_url('sit',conFig.get_value('bos_login', 'username'),conFig.get_value('bos_login', 'password'))


    def test_IB_list(self):
        IBVerifyList.logincp(1000005349)


if __name__=='__main__':
    pytest.main(['-s','-v',os.path.abspath(__file__)])








