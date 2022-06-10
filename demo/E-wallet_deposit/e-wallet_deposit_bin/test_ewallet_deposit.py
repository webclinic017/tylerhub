'''
Author: tyler
Date: 2021-05-28 17:32:52
LastEditTime: 2022-06-10 18:06:33
LastEditors: Tyler Tang tyler.tang@6317.io
Description: In User Settings Edit
FilePath: \tylerhub\demo\E-wallet_deposit\e-wallet_deposit_bin\test_ewallet_deposti.py
'''
import os
import sys

import allure
import pytest
import pytest_check as check

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_project=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_project+r'\location_ewallet')
from about_data import Aboutdata
from location_deposit_of_ewallet import Ewallet_deposti
from read_dataconfig import ReadConfig


class Test_Ewallet_deposit():
    global ewallet,conFig,excelpath,dealData,testdata

    ewallet=Ewallet_deposti()
    conFig=ReadConfig()
    dealData=Aboutdata()

    #读取测试数据
    excelpath=os.path.join(path_project,r'test_data\ewallet_deposit.xlsx')
    rows=dealData.openexcel(excelpath,'Sheet1')
    testdata=dealData.dict_data()

    def setup_class(self):
        ewallet.broswertype()
        #登录bos
        ewallet.get_url('sit')

    def setup(self):
        ewallet.login_bos(conFig.get_value('bos_login', 'username'),conFig.get_value('bos_login', 'password'))
    
    def teardown(self):
        if self.data_index==testdata.index(testdata[-1]):
            ewallet.quitbrowser()
        else:
            ewallet.logoutbos()

    @allure.feature('随机选择电子钱包中的一种渠道入金')
    @allure.title('ewallet入金测试报告')
    @allure.story('用例执行')
    @allure.description('读取测试文档数据，执行用例')
    @pytest.mark.parametrize('data',testdata)
    def test_deposit_of_ewallet(self,data):
        print('当前测试数据：主账号：{}，交易账号：{}，入金金额：{}'.format(int(data['主账号']),int(data['交易账号']),int(data['入金金额'])))    
        
        with allure.step('获取当前测试数据下标'):
            self.data_index=testdata.index(data)
        
        with allure.step('从bos登录cp'):
            ewallet.bos_to_cp(int(data['主账号']))
        
        with allure.step('判断当前交易账号是否存在电子钱包入金方式'):
            if ewallet.judge_ewalletpay():
                with allure.step('存在电子钱包入金方式'):

                    with open(ewallet.payTypePicPath,'rb') as f: #入金方式截图
                        comtent=f.read()
                    allure.attach(comtent,'入金方式',allure.attachment_type.PNG)
                    
                    with allure.step('随机选择一种渠道入金'):
                        ewallet.deposit_ewallet(int(data['交易账号']),int(data['入金金额']))

                        with open(ewallet.depositSuccessPicPath,'rb') as f: #渠道入金成功截图
                            comtent=f.read()
                        allure.attach(comtent,'渠道入金成功',allure.attachment_type.PNG)
                    
                    with allure.step('bos审核入金'):
                        ewallet.review_deposit(int(data['交易账号']),'sit',conFig.get_value('bos_login', 'username2'),conFig.get_value('bos_login', 'password'))
            
                        with open(ewallet.reviewSuccessPicPath,'rb') as f: #入金审核成功截图
                            comtent=f.read()
                        allure.attach(comtent,'BOS审核入金成功',allure.attachment_type.PNG)

                    with allure.step('断言是否审核成功'):
                        check.equal('成功',ewallet.reviewSuccessText)
            else:
                with allure.step('不存在电子钱包入金方式，用例跳过'):
                    pytest.skip()
        
        
if __name__=='__main__':
    # pytest.main(['-v','-s',r'{}\e-wallet_deposit_bin\test_ewallet_deposit.py'.format(path_project)])
    pytest.main(['-s','-v',os.path.abspath(__file__),
    r'--alluredir={}\report\result'.format(path_project),'--disable-pytest-warnings'])
    os.system(r'allure generate {}\report\result -o {}\report\allure_report --clean'.format(path_project,path_project))
    os.system(r'allure serve {}\report\result'.format(path_project))
