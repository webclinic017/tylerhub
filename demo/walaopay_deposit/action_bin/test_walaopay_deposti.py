'''
Author: tyler
Date: 2021-09-17 15:06:27
LastEditTime: 2021-09-24 10:45:01
LastEditors: Please set LastEditors
Description: Execute testcase
FilePath: \tylerhub\demo\walaopay_withdrawal\action_bin\test_walaopay_withdrawal.py
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
from location_of_walaopay_deposit import Location_of_walaopay

@allure.epic('walao pay入金')
class Test_addEwallet(object):

    global walaoPay,conFig,dealData,testdata,excelpath
    walaoPay=Location_of_walaopay()
    conFig=ReadConfig()
    dealData=Aboutdata()

    #读取测试数据
    excelpath=os.path.join(path_project,r'test_data\walaopay_deposit.xlsx')
    rows=dealData.openexcel(excelpath,'Sheet1')
    testdata=dealData.dict_data()

    def setup_class(self):
        #默认谷歌浏览器打开
        walaoPay.broswertype()
        #cp，bos登录页
        walaoPay.get_url('sit')
        #登录bos
        walaoPay.login_bos(conFig.get_value('bos_login', 'username'), conFig.get_value('bos_login', 'password'))
        #登录bos第二个账号
        walaoPay.new_driver('sit',conFig.get_value('bos_login', 'username2'),conFig.get_value('bos_login', 'password'))

    def teardown(self):
        if self.data_index==testdata.index(testdata[-1]):
            walaoPay.quitbrowser()
        else:
            walaoPay.logoutcp()


    @allure.feature('bos判断walaopay入金方式是否开启，判断当前账号是否存在该入金方式，测试最低最高金额入金')
    @allure.story('用例执行')
    @allure.description('读取测试文档数据，执行用例')
    @pytest.mark.parametrize('data',testdata)
    @pytest.mark.flaky(reruns=2, reruns_delay=2) #失败重跑
    def test_walaopay(self,data):
        print('当前测试数据：主账号：{}，邮箱：{}'.format(int(data['主账号']),data['邮箱']))
        with allure.step('获取当前测试数据下标'):
            self.data_index=testdata.index(data)
        if self.data_index!=0:
            walaoPay.remove_login_topup()

        with allure.step('判断当前账号是否存在walaopay入金方式，不存在则添加walaopay入金方式'):
            walaoPay.is_have_walaopay(int(data['主账号']))

        with allure.step('登录cp'):
            walaoPay.logincp(data['邮箱'],data['密码'])
        
        with allure.step('首页获取当前交易账号余额并保存到本地，获取walaopay入金方式最低最高入金金额'):
            walaoPay.get_highestAndlowest(int(data['交易账号']),excelpath,'E',self.data_index+2)
        
        with allure.step('最低最高金额入金'):
            walaoPay.action(int(data['交易账号']))
            
            with open(walaoPay.path1,'rb') as f:
                comtent=f.read()
            allure.attach(comtent,'低于最低金额入金',allure.attachment_type.PNG)
            with open(walaoPay.path2,'rb') as f:
                comtent=f.read()
            allure.attach(comtent,'高于最高金额入金',allure.attachment_type.PNG)
            
            with allure.step('断言汇率是否与数据库一致,转换金额是否计算正确'):
                pytest.assume(walaoPay.exchangeRate==walaoPay.baseCharge)
                pytest.assume(walaoPay.exchangeAmount==round(walaoPay.lowestDeposit*walaoPay.baseCharge))
                # pytest.assume(walaoPay.exchangeAmount2==round(walaoPay.highestDeposit*walaoPay.baseCharge))
        
        with allure.step('bos审核入金'):
            walaoPay.bos_verify(int(data['交易账号']))
            with open(walaoPay.path3,'rb') as f:
                comtent=f.read()
            allure.attach(comtent,'审核最低最高金额入金',allure.attachment_type.PNG)

        with allure.step('入金成功后获取交易账号余额'):
            walaoPay.after_deposti(int(data['交易账号']), excelpath, 'F', self.data_index+2)    


if __name__=='__main__':
    # pytest.main(['-s','-v',os.path.abspath(__file__)])
    pytest.main(['-s','-v',os.path.abspath(__file__),
    r'--alluredir={}\report\result'.format(path_project),'--disable-pytest-warnings'])
    os.system(r'allure generate {}\report\result -o {}\report\allure_report --clean'.format(path_project,path_project))
    os.system(r'allure serve {}\report\result'.format(path_project))