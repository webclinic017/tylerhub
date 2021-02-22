from KYC_method import kyc_approve
from selenium import webdriver
import unittest


#实例化对象
kyc=kyc_approve()

class kyc_actions(unittest.TestCase):

    def setUp(self):
        kyc.browsertype()

    def test(self):
        kyc.get_login('https://at-client-portal-sit.atfxdev.com/login')


if __name__=='__main__':
    unittest.main()