'''
Author: your name
Date: 2021-09-02 10:18:01
LastEditTime: 2021-09-06 17:35:55
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
        addEwaller.details_page(1200008143)
        #居住国家为中国，跳过该用例
        if addEwaller.get_live_country():
            pytest.skip()
        else:
            addEwaller.logincp('235345346@qq.com', 'Tl123456')
            addEwaller.is_ewallet_morethan_three()
            addEwaller.get_tips()
            #断言提示语是否正确
            pytest.assume(addEwaller.tips == '每种电子钱包您最多可以添加3条，若需再新增，您需先删除其中一条。')
            addEwaller.is_ewallet_available()
            #断言新增电子琴钱包出金方式是否在会员中心可用及数据库中是否添加
            if addEwaller.times<3:
                #查询数据库
                addEwaller.search_mongodb_ewallet(1200008143)
                pytest.assume(addEwaller.available_ewallet == 3)
                pytest.assume(''.join(addEwaller.availableList) in addEwaller.databaseList)
            







if __name__=='__main__':
    pytest.main(['-s','-v',os.path.abspath(__file__)])