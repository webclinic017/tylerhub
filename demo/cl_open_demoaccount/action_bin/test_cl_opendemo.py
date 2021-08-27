'''
Author:tyler
Date: 2021-08-26 18:21:36
LastEditTime: 2021-08-27 17:22:14
LastEditors: Please set LastEditors
Description: Execution use case
FilePath: \tylerhub\demo\cl_open_demoaccount\action_bin\test_cl_opendemo.py
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
from location_of_cl_opendome import Location_of_opendemo


class Test_opendemo_cl(object):

    global openDemo,conFig,dealData
    openDemo=Location_of_opendemo()
    conFig=ReadConfig()
    dealData=Aboutdata()

    def setup_class(self):
        #默认谷歌浏览器打开
        openDemo.broswertype()
        #cp登录页
        openDemo.get_url('sit')

    def test_execution_demo(self):
        openDemo.logincp('tyler.tang@test.com', 'Tl123456')
        openDemo.creat_demoaccount()
        openDemo.get_demoaccount(1000005349)
        
if __name__=='__main__':
    pytest.main(['-s','-v',os.path.abspath(__file__)])