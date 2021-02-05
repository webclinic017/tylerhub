#导包
from selenium import webdriver
import unittest
import ddt
import sys
import os
from register_method import formaction
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
print(testdata)

#实例化对象
web=Commonweb()
form=formaction()

#数据驱动
@ddt.ddt
class register_cp(unittest.TestCase,formaction):
    """会员中心注册页表单"""

         

    #环境恢复，退出并关闭浏览器进程
    def tearDown(self):
        web.close_browser()
        web.quit_browser()


    @ddt.data(*testdata)
    def test_register(self,data):
        #获取每组测试数据的下标
        self.data_index=testdata.index(data)
        form.get_url(data['专属链接'],data['邀请码'],'F',self.data_index)

        


if __name__=='__main__':
    unittest.main()
