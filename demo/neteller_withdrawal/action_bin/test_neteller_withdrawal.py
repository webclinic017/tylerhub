'''
Author: tyler
Date: 2021-09-08 15:05:37
LastEditTime: 2021-10-19 11:20:47
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
#需新增居住国判断，非中国才存在电子钱包出金方式，中国账号跳过用例，非中国判断是否存在neteller出金方式
@allure.epic('neteller出金')
class Test_neteller_withdrawal(object):

    global netteLler,conFig,dealData,testdata,excelpath
    netteLler=Location_of_netellerWithdrawal()
    conFig=ReadConfig()
    dealData=Aboutdata()

    #读取测试数据
    excelpath=os.path.join(path_project,r'test_data\neteller_withdrawal.xlsx')
    rows=dealData.openexcel(excelpath,'Sheet1')
    testdata=dealData.dict_data() 
    def setup_class(self):
        #默认谷歌浏览器打开
        netteLler.broswertype()
        #cp，bos登录页
        netteLler.get_url('sit')
        #登录bos
        netteLler.login_bos(conFig.get_value('bos_login', 'username'), conFig.get_value('bos_login', 'password'))


    def teardown(self):
        if self.data_index==testdata.index(testdata[-1]):
            netteLler.quitbrowser()
        else:
            netteLler.logoutcp()

    
    @allure.feature('判断是否存在neteller出金方式、判断交易账号余额、调用接口获取出金手续费')
    @allure.story('用例执行')
    @allure.description('读取测试文档数据，执行用例，判断出金方式；交易账号余额；出金手续费，断言手续费；保存cp，bos，数据库出金时间到本地文档')
    @pytest.mark.parametrize('data',testdata)
    @pytest.mark.flaky(reruns=2, reruns_delay=2) #失败重跑
    def test_neteller(self,data):
        print('当前测试数据：主账号：{}，邮箱：{}'.format(int(data['主账号']),data['邮箱']))
        with allure.step('获取当前测试数据下标'):
            self.data_index=testdata.index(data)
        if self.data_index!=0:
            netteLler.remove_login_topup()

        with allure.step('登录会员中心'):
            netteLler.logincp(data['邮箱'],data['密码'])
        
        with allure.step('判断当前出金交易账号余额，余额为0时跳过用例'):
            if netteLler.is_balance_nil(int(data['出金交易账号'])):
                pytest.skip()
            else:
                with allure.step('会员中心出金，调用接口查询手续费，当可出金金额为0时跳过用例'):
                    if netteLler.action_neteller(int(data['主账号']),int(data['出金交易账号']),
                    data['邮箱'],int(data['出金金额']),excelpath,'I',self.data_index+2):
                        pytest.skip()
                    else:
                        with open(netteLler.charge_path,'rb') as f:
                            comtent=f.read()
                        allure.attach(comtent,'是否存在出金手续费',allure.attachment_type.PNG)

                        with allure.step('断言出金手续费是否与接口返回手续费一致'):
                            pytest.assume(netteLler.charge == netteLler.api_charge)

                    with allure.step('bos审核出金，保存bos，cp，数据库出金时间到本地'):
                        netteLler.review_withdrawal(int(data['出金交易账号']),excelpath,'F',self.data_index+2)

                        with open(netteLler.review_path,'rb') as f:
                            comtent=f.read()
                        allure.attach(comtent,'bos审核',allure.attachment_type.PNG)

                        netteLler.check_cp(int(data['出金交易账号']),excelpath,'G','H',self.data_index+2)


if __name__=='__main__':
    # pytest.main(['-s','-v',os.path.abspath(__file__)])
    pytest.main(['-s','-v',os.path.abspath(__file__),
    r'--alluredir={}\report\result'.format(path_project),'--disable-pytest-warnings'])
    os.system(r'allure generate {}\report\result -o {}\report\allure_report --clean'.format(path_project,path_project))
    os.system(r'allure serve {}\report\result'.format(path_project))