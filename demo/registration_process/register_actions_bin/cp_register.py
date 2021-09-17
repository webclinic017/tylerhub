'''
Author: tyler
Date: 2021-05-13 10:43:00
LastEditTime: 2021-09-17 10:46:28
LastEditors: Please set LastEditors
Description: Perform cases of register
FilePath: \tylerhub\demo\registration_process\register_actions_bin\cp_register.py
'''
#导包
import os
import sys
import unittest

import ddt
from BeautifulReport import BeautifulReport

path_public=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'public')
sys.path.append(path_public)
path_process=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_process+r'\register_positioning')
from about_data import Aboutdata
from read_dataconfig import ReadConfig
from register_method import Form_operations

#实例化
conFig=ReadConfig()
form=Form_operations()

#读取测试文档数据
e=Aboutdata()
rows=e.openexcel(path_process+r'\test_excel_data\register_data.xlsx','Sheet1') #测试文档的路径，sheet名,并获取总行数
testdata=e.dict_data()


#数据驱动
@ddt.ddt
class Register_cp(unittest.TestCase):
    """关键字驱动：会员中心注册页表单，调用form_operations类中封装的表单填写方法"""

    #预置条件
    def setUp(self):
        form.browsertype() #每个测试用例默认以谷歌浏览器打开
    
    #环境恢复，退出并关闭浏览器进程
    def tearDown(self):
        form.quitdriver()

    @ddt.data(*testdata)
    def test_register(self,data):
        #获取每组测试数据的下标
        self.data_index=testdata.index(data)
        print('当前测试数据:国家：{},英文国家名：{}；三字码：{}；邮箱：{}；专属链接：{}；邀请码：{}'
        .format(data['国家'],data['country'],data['三字码'],data['邮箱'],data['专属链接'],data['邀请码']))

        #判断居中国家是否为UK国家
        if form.country_isuk(data['国家']):
            form.closedriver() #关闭浏览器
        else:
            #访问不同注册地址，专属链接/直客注册
            form.get_url('sit',data['专属链接'],data['邀请码'],'E',self.data_index+2)
            #填写注册表单,参数依次为：页面语言，名字，姓氏，邮箱，密码，中文国家名，英文国家名
            form.fill_inform('简中',conFig.get_value('cp_register','username'),'uitest勿动',data['邮箱'],conFig.get_value('cp_register', 'password'),data['国家'],data['country'])
            #提交表单
            form.submit()
            #断言
            self.assertIn(form.register_success(),'Company Declaration 公司声明')
            #保存测试数据
            
            e.saveainfo(path_process+r'\test_excel_data\account_number.xlsx',data['国家'],'A',self.data_index+2)
            e.saveainfo(path_process+r'\test_excel_data\account_number.xlsx',data['邮箱'],'B',self.data_index+2)
            e.saveainfo(path_process+r'\test_excel_data\account_number.xlsx',data['三字码'],'D',self.data_index+2)
            e.saveainfo(path_process+r'\test_excel_data\account_number.xlsx',data['地区'],'G',self.data_index+2)
            e.saveainfo(path_process+r'\test_excel_data\account_number.xlsx',data['邀请码'],'H',self.data_index+2)

if __name__=='__main__':
    #测试报告
    suit=unittest.defaultTestLoader.discover(os.path.dirname(os.path.abspath(__file__)),
    pattern='cp_register.py',top_level_dir=None)
    BeautifulReport(suit).report(filename='会员中心注册',description='注册流程',
    report_dir=path_process+r'\report')
