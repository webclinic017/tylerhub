'''
Author:tyler
Date: 2021-08-26 18:21:36
LastEditTime: 2022-05-25 11:42:51
LastEditors: Tyler96-QA 1718459369@qq.com
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


@allure.epic('CL账号开通demo')
class Test_opendemo_cl(object):

    global openDemo,conFig,dealData,testdata,excelpath
    openDemo=Location_of_opendemo()
    conFig=ReadConfig()
    dealData=Aboutdata()

    #读取测试数据
    excelpath=os.path.join(path_project,'test_data\cl_open_demo.xlsx')
    rows=dealData.openexcel(excelpath,'Sheet1')
    testdata=dealData.dict_data()

    def setup_class(self):
        #默认谷歌浏览器打开
        openDemo.broswertype()
        #cp，bos登录页
        openDemo.get_url('sit')
        #登录bos
        openDemo.login_bos(conFig.get_value('bos_login', 'username'), conFig.get_value('bos_login', 'password'))


    def teardown(self):
        if self.data_index==testdata.index(testdata[-1]):
            openDemo.quitbrowser()
        else:
            openDemo.logoutcp()

        
    @allure.feature('CL账号新开demo,校验数据库demo账号信息,修改杠杆')
    @allure.story('用例执行')
    @allure.description('读取测试文档数据，执行用例：登录CP新开demo，bos获取demo账号信息与数据库比对，CP修改杠杆')
    @pytest.mark.parametrize('data',testdata)
    @pytest.mark.flaky(reruns=2, reruns_delay=2) #失败重跑
    def test_execution_demo(self,data):
        print('当前测试数据：主账号：{}'.format(int(data['主账号'])))
        with allure.step('获取当前测试数据下标'):
            self.data_index=testdata.index(data)
        if self.data_index!=0:
            openDemo.remove_login_topup()
        
        with allure.step('登录cp新开demo'):
            openDemo.details_page(int(data['主账号']))
            openDemo.logincp(data['邮箱'], data['密码'])
            openDemo.creat_demoaccount()
        
        with allure.step('查询数据库，获取新开demo账号信息'):
            if openDemo.get_demoaccount(int(data['主账号'])):
                print('demo账号创建失败，用例跳过')
                pytest.skip()
            else:
                openDemo.get_demo_info()
                openDemo.search_mongodb_demoinfo(int(data['主账号']))
        
        with allure.step('断言新开demo账号信息是否与数据库一致'):
            pytest.assume(openDemo.demoGroup == str(openDemo.serchDemodata[0]['group']))
            pytest.assume(openDemo.demoLever == int(openDemo.serchDemodata[0]['leverage']))
            pytest.assume(openDemo.demoSpread == str(openDemo.serchDemodata[0]['spreadType']))
            pytest.assume(openDemo.demoBit == int(openDemo.serchDemodata[0]['markup']))

        with allure.step('获取新开demo位于demo列表中第几个'):
            openDemo.where_demo_incp()

        with allure.step('修改demo账号杠杆'):
            openDemo.revise_demolever(openDemo.row)

        with allure.step('断言修改后杠杆是否与数据库一致'):
            openDemo.revise_mongolever(int(data['主账号']))
            pytest.assume(openDemo.reviseLever == int(openDemo.serchData[0]['leverage']))
        
        with allure.step('保存测试数据'):
            dealData.saveainfo(excelpath, openDemo.demoAccount, 'D', self.data_index+2)
            dealData.saveainfo(excelpath, openDemo.demoGroup, 'E', self.data_index+2)
            dealData.saveainfo(excelpath, openDemo.demoLever, 'F', self.data_index+2)
            dealData.saveainfo(excelpath, openDemo.demoBit, 'G', self.data_index+2)
            dealData.saveainfo(excelpath, openDemo.demoLever, 'H', self.data_index+2)
            dealData.saveainfo(excelpath, openDemo.reviseLever, 'I', self.data_index+2)


if __name__=='__main__':
    #pytest.main(['-s','-v',os.path.abspath(__file__)])
    pytest.main(['-s','-v',os.path.abspath(__file__),
    r'--alluredir={}\report\result'.format(path_project),'--disable-pytest-warnings'])
    os.system(r'allure generate {}\report\result -o {}\report\allure_report --clean'.format(path_project,path_project))
    os.system(r'allure serve {}\report\result'.format(path_project))