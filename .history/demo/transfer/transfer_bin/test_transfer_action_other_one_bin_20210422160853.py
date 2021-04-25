import os
import sys
import pytest

import ddt
from BeautifulReport import BeautifulReport

path_public=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+r'\public'
sys.path.append(path_public)
path_transfer=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_transfer+r'\transfer_location')
from about_data import exceldata




class Test_transfer():
    



if __name__=='__main__':
    pytest.main(['-v','-s','test_transfer_action_other_one_bin.py'])