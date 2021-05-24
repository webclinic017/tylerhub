'''
Author: your name
Date: 2021-05-24 16:11:20
LastEditTime: 2021-05-24 18:13:15
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \tylerhub\demo\registration_process\register_actions_bin\test_verify_data_bin.py
'''
import pytest
import os
import sys
# import allure

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_process=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_process+r'\register_positioning')
from about_data import exceldata
from verify_message_location import location_of_verify_data

verify=location_of_verify_data()



class Test_verify_data():

    def setup_class(self):
        verify.browsertype()
        verify.login_bos('tyler.tang', 'Tl123456')

    def test_verfity(self):
        verify.enter_details_page(1000003759)
        if verify.is_traccount_onlyone():
            pytest.skip()
        else:
            print('继续用例')




if __name__=='__main__':
    pytest.main(['-v','-s',r'{}\register_actions_bin\test_verify_data_bin.py'.format(path_process)])




