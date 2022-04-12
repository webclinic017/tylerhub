'''
Author: your name
Date: 2022-03-29 17:16:00
LastEditTime: 2022-04-07 16:53:09
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \tylerhub\demo\IB_Close_Open_Order_List\actions_bin\Test_ib_close_open_order_list.py
'''
import pytest
import os
import allure
import sys
import pytest_check as check
path_public=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'public')
sys.path.append(path_public)
path_project=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(path_project)
sys.path.append(path_project+r'\location')
from about_data import Aboutdata
from read_dataconfig import ReadConfig
from Location_of_ib__close_open_order_list import Location_of_IB_CloseOpen_OrderList

class Test_IB_CloseOpen_OrderList(object):

        
    global VerifOrderyList,conFig,dealData,testdata,excelpath
    VerifOrderyList=Location_of_IB_CloseOpen_OrderList()
    conFig=ReadConfig()
    dealData=Aboutdata()

    # #读取测试数据
    # excelpath=os.path.join(path_project,r'test_data\IB_lowerData.xlsx')
    # rows=dealData.openexcel(excelpath,'Sheet1')
    # testdata=dealData.dict_data()
    
    def setup_class(self):
        #默认谷歌浏览器打开
        VerifOrderyList.broswertype()
        #cp，bos登录
        VerifOrderyList.get_url('sit',conFig.get_value('bos_login', 'username'),conFig.get_value('bos_login', 'password'))


    def test_IB_Order_List(self):
        VerifOrderyList.search_ib_lower(1000005349)
        VerifOrderyList.logincp(1000005349)
        if VerifOrderyList.filter_lower_openOrder():
            for i in VerifOrderyList.tradeAccount_list2:
                if VerifOrderyList.search_period_openOrder(i):
                    print('断言open_orderList,mysql_openOrder')
                else:
                    print('断言长度')
        else:
            pytest.skip()


            
if __name__=='__main__':
    pytest.main(['-s','-v',os.path.abspath(__file__)])















