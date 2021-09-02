'''
Author: your name
Date: 2021-09-02 10:18:01
LastEditTime: 2021-09-02 11:24:12
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \tylerhub\demo\add_ewallet_withdrawal\action_bin\test_add_ewallet.py
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
from location_of_add_ewallet import Location_of_add_ewallet

class Test_opendemo_cl(object):

    global addEwaller,conFig,dealData,testdata,excelpath
    addEwaller=Location_of_add_ewallet()
    conFig=ReadConfig()
    dealData=Aboutdata()

    # #读取测试数据
    # excelpath=os.path.join(path_project,'test_data\cl_open_demo.xlsx')


    def setup_class(self):
        #默认谷歌浏览器打开
        addEwaller.broswertype()
        #cp，bos登录页
        addEwaller.get_url('sit')
        #登录bos
        addEwaller.login_bos(conFig.get_value('bos_login', 'username'), conFig.get_value('bos_login', 'password'))

    
    def test_ewallet(self):
        addEwaller.details_page(1000005349)
        #居住国家为中国，跳过该用例
        if addEwaller.get_live_country():
            addEwaller.closebrowser()
            pytest.skip()









if __name__=='__main__':
    pytest.main(['-s','-v',os.path.abspath(__file__)])