'''
Author: tyler
Date: 2021-09-02 10:18:01
LastEditTime: 2021-09-07 16:53:14
LastEditors: Please set LastEditors
Description: xecution use case
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

@allure.epic('账户设定添加电子钱包出金方式')
class Test_addEwallet(object):

    global addEwaller,conFig,dealData,testdata,excelpath
    addEwaller=Location_of_add_ewallet()
    conFig=ReadConfig()
    dealData=Aboutdata()

    #读取测试数据
    excelpath=os.path.join(path_project,r'test_data\add_ewallet.xlsx')
    rows=dealData.openexcel(excelpath,'Sheet1')
    testdata=dealData.dict_data()

    def setup_class(self):
        #默认谷歌浏览器打开
        addEwaller.broswertype()
        #cp，bos登录页
        addEwaller.get_url('sit')
        #登录bos
        addEwaller.login_bos(conFig.get_value('bos_login', 'username'), conFig.get_value('bos_login', 'password'))

    def teardown(self):
        if self.data_index==testdata.index(testdata[-1]):
            addEwaller.quitbrowser()
        else:
            addEwaller.logoutcp()

    @allure.feature('会员中心判断ewallet电子钱包是否超过三条，否则添加至三条，并且验证是否可以及数据库中是否添加成功')
    @allure.story('用例执行')
    @allure.description('读取测试文档数据，执行用例：登录CP判断电子钱包出金方式是否超过三条')
    @pytest.mark.parametrize('data',testdata)
    @pytest.mark.flaky(reruns=2, reruns_delay=2) #失败重跑
    def test_ewallet(self,data):
        print('当前测试数据：主账号：{}，邮箱：{}'.format(int(data['主账号']),data['邮箱']))

        with allure.step('获取当前测试数据下标'):
            self.data_index=testdata.index(data)
        if self.data_index!=0:
            addEwaller.remove_login_topup()

        with allure.step('进入账号详情页判断该账号居住国是否为中国'):
            addEwaller.details_page(int(data['主账号']))
            #居住国家为中国，跳过该用例
            if addEwaller.get_live_country():
                pytest.skip()
            else:
                with allure.step('登录会员中心判断电子钱包出金方式是否超过三条'):
                    addEwaller.logincp(data['邮箱'], data['密码'])
                    addEwaller.is_ewallet_morethan_three()
                    with open(addEwaller.screenshots_path('ewallet出金方式'),'rb') as f:
                        comtent=f.read()
                    allure.attach(comtent,'ewallet出金方式',allure.attachment_type.PNG)
                
                with allure.step('获取提示语'):
                    addEwaller.get_tips()
                    with open(addEwaller.screenshots_path('tips'),'rb') as f:
                        comtent=f.read()
                    allure.attach(comtent,'tips',allure.attachment_type.PNG)
                

                with allure.step('断言提示语是否正确'):
                    pytest.assume(addEwaller.tips == '每种电子钱包您最多可以添加3条，若需再新增，您需先删除其中一条。')

                with allure.step('若新增电子钱包出金方式，判断在出金模块是否可用'):
                    addEwaller.is_ewallet_available()
                    if addEwaller.times<3:
                        with open(addEwaller.screenshots_path('出金模块是否可用'),'rb') as f:
                            comtent=f.read()
                        allure.attach(comtent,'出金模块是否可用',allure.attachment_type.PNG)
                
                #断言新增电子琴钱包出金方式是否在会员中心可用及数据库中是否添加
                if addEwaller.times<3:
                    #查询数据库
                    addEwaller.search_mongodb_ewallet(int(data['主账号']))
                    pytest.assume(addEwaller.available_ewallet == 3)
                    with allure.step('断言新增电子钱包是否成功添加进数据库'):
                        for i in addEwaller.availableList:
                            pytest.assume(i in addEwaller.databaseList)


if __name__=='__main__':
    # pytest.main(['-s','-v',os.path.abspath(__file__)])
    pytest.main(['-s','-v',os.path.abspath(__file__),
    r'--alluredir={}\report\result'.format(path_project),'--disable-pytest-warnings'])
    os.system(r'allure generate {}\report\result -o {}\report\allure_report --clean'.format(path_project,path_project))
    os.system(r'allure serve {}\report\result'.format(path_project))