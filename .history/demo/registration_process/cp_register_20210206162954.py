#导包
from selenium import webdriver
import unittest
import ddt
import sys
import os
import time
from register_method import form_operations
"""跨目录调用，需要将导入的包加入sys.path中"""
path=os.path.dirname(os.path.dirname(__file__))
path=os.path.join(path,'publick')
sys.path.append(path)
from about_data import exceldata
from browser_actions import Commonweb

#读取测试文档数据
e=exceldata()
rows=e.openexcel(r'E:\test\country.xlsx','Sheet1') #测试文档的路径，sheet名,并获取总行数
testdata=e.dict_data()

#实例化对象
form=form_operations()

#数据驱动
@ddt.ddt
class register_cp(unittest.TestCase):
    """会员中心注册页表单，调用form_operations类中封装的表单填写方法"""

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
        
        print('当前测试数据:国家：{},英文国家名：{}；三字码：{}；邮箱：{}；专属链接：{}；邀请码：{}；点差类型：{}'
        .format(data['国家'],data['country'],data['三字码'],data['邮箱'],data['专属链接'],data['邀请码'],data['点差类型']))

        #判断居中国家是否为UK国家
        if form.country_isuk(data['国家']):
            form.closedriver() #关闭浏览器
        else:
            #访问不同注册地址，专属链接/直客注册
            form.get_url(data['专属链接'],data['邀请码'],'F',self.data_index+2)
            #填写注册表单,参数依次为：页面语言，名字，姓氏，邮箱，密码，中文国家名，英文国家名
            form.fill_inform('EN','test','tyler',data['邮箱'],'Tl123456',data['国家'],data['country'])
       
if __name__=='__main__':
    unittest.main()