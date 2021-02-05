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
class register_cp(unittest.TestCase):
    """会员中心注册页表单"""
        #全局变量
    global driver
    
    @ddt.data(*testdata)
    def test_register(self):
        print(1111)
        form.get_url(data['专属链接'],data['邀请码'])

        


if __name__=='__main__':
    unittest.main()
