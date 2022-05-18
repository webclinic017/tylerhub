'''
Author: your name
Date: 2022-01-13 14:30:22
LastEditTime: 2022-05-18 17:41:49
LastEditors: Tyler96-QA 1718459369@qq.com
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \tylerhub\demo\change_email_language\action_bin\test_change_emali_language.py
'''
import pytest
import os
import allure
import sys
import pytest_check as check
path_public=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'public')
sys.path.append(path_public)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
path_project=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_project+r'\location')
from about_data import Aboutdata
from read_dataconfig import ReadConfig
from location_of_email_language import Location_email_language_change

@allure.epic('修改邮箱语言并核对数据库lang字段')
class Test_change_emailLanguage(object):

    global changeLanguage,conFig,dealData,testdata,excelpath
    changeLanguage=Location_email_language_change()
    conFig=ReadConfig()
    dealData=Aboutdata()

    #读取测试数据
    excelpath=os.path.join(path_project,r'test_data\change_email_language.xlsx')
    rows=dealData.openexcel(excelpath,'Sheet1')
    testdata=dealData.dict_data()


    def setup_class(self):
        #默认谷歌浏览器打开
        changeLanguage.broswertype()
        changeLanguage.get_url('sit',conFig.get_value('bos_login', 'username'),conFig.get_value('bos_login', 'password'))


    def teardown(self):
        if self.data_index==testdata.index(testdata[-1]):
            changeLanguage.quitbrowser()
        else:
            changeLanguage.closebrowser()

    @pytest.mark.parametrize('data',testdata)
    @allure.feature('cp设置页面修改数据库邮箱语言')
    @allure.story('用例执行')
    @allure.description('读取测试文档数据，执行用例')
    def test_change_language(self,data):
        #当前测试数据下标
        with allure.step('获取当前测试数据下标'):
            self.data_index=testdata.index(data)

        with allure.step('根据主账号从BOS登录CP'):    
            changeLanguage.from_bos_to_cp(int(data['主账号']))

        with allure.step('修改邮箱语言，并保存相关测试数据至测试文档'):    
            changeLanguage.change_emailLanguage(int(data['主账号']),excelpath,'B','C',self.data_index+2)
        #查询数据库
        with allure.step('查询数据库'):  
            changeLanguage.check_dataBase_language(int(data['主账号']),excelpath,'D',self.data_index+2)
        
        with allure.step('断言修改后数据库lang字段：{}与页面邮箱语言：{}'.format(changeLanguage.checkDataBase_emailLang,changeLanguage.randomLanguage)):    
            check.equal(changeLanguage.randomLanguage, changeLanguage.checkDataBase_emailLang,
            '断言失败，修改后邮箱语言：{}，页面语言：{}'.format(changeLanguage.checkDataBase_emailLang,changeLanguage.randomLanguage))



if __name__=='__main__':
    # pytest.main(['-s','-v',os.path.abspath(__file__)])
    pytest.main(['-s','-v',os.path.abspath(__file__),
    r'--alluredir={}\report\result'.format(path_project),'--disable-pytest-warnings'])
    os.system(r'allure generate {}\report\result -o {}\report\allure_report --clean'.format(path_project,path_project))
    os.system(r'allure serve {}\report\result'.format(path_project))