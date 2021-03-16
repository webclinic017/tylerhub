#导包
from selenium import webdriver
import unittest
import ddt
import sys
import os
from BeautifulReport import BeautifulReport

path_publick=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\publick'
sys.path.append(path_publick)
path_regpos=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+r'\register_positioning'
sys.path.append(path_regpos)
from register_method import form_operations
from about_data import exceldata

#读取测试文档数据
e=exceldata()
rows=e.openexcel(r'E:\test\country.xlsx','Sheet1') #测试文档的路径，sheet名,并获取总行数
testdata=e.dict_data()

#实例化对象
form=form_operations()

#数据驱动
@ddt.ddt
class register_cp(unittest.TestCase):
    """关键字驱动：会员中心注册页表单，调用form_operations类中封装的表单填写方法"""

    #预置条件
    def setUp(self):
        form.browsertype() #每个测试用例默认以谷歌浏览器打开
    
    #环境恢复，退出并关闭浏览器进程
    # def tearDown(self):
    #     form.quitdriver()

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
            form.get_url(data['专属链接'],data['邀请码'],'E',self.data_index+2)
            #填写注册表单,参数依次为：页面语言，名字，姓氏，邮箱，密码，中文国家名，英文国家名
            form.fill_inform('简中','test','tyler',data['邮箱'],'Tl123456',data['国家'],data['country'])
            #提交表单
            # form.submit()
            #断言
            # self.assertIn(form.register_success(),'Company Declaration 公司声明')
            #保存测试数据
            e.saveainfo(r'E:\test\account_number.xlsx',data['国家'],'A',self.data_index+2)
            e.saveainfo(r'E:\test\account_number.xlsx',data['邮箱'],'B',self.data_index+2)
            e.saveainfo(r'E:\test\account_number.xlsx',data['三字码'],'D',self.data_index+2)

if __name__=='__main__':
    #测试报告
    suit=unittest.defaultTestLoader.discover(os.path.dirname(os.path.abspath(__file__)),
    pattern='cp_register.py',top_level_dir=None)
    BeautifulReport(suit).report(filename='会员中心注册',description='注册流程',
    report_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+r'\cp_register_process_report')