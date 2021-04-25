import os
import sys
import time
import unittest
import ddt
import xlrd
from BeautifulReport import BeautifulReport
path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=path_demo+r'\public'
sys.path.append(path_public)
path_website=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from about_data import exceldata
from browser_actions import Commonweb
from other_actions import public_method

e=exceldata()
excelpath=path_website+r'\moudle_data\Cfds.xlsx'
rows=e.openexcel(excelpath,'Sheet1')
testdata=e.dict_data()

print(type(testdata[0]['Ex-Dividend Date']))
xlrd.xldate_as_tuple(testdata[0]['Ex-Dividend Date'])