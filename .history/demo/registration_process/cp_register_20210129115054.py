from demo import browser_actions

from selenium import webdriver
import unittest
import ddt

#实例化封装的web操作类
web=Commonweb()

@ddt.ddt #数据驱动
class register_cp(unittest.TestCase):
    global driver
    driver=web.open_browser()

    def setUp(self):
        web.open_web('https://at-client-portal-sit.atfxdev.com/login')


    def test_register