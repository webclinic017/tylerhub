import time
import os
import sys
path=os.path.dirname(os.path.dirname(__file__))
path=os.path.join(path,'publick')
sys.path.append(path)
from browser_actions import Commonweb
from other_actions import public_method

pub_method=public_method()
class get account(Commonweb):
    global driver

    def __init__(self,browsername='Chrome'):
        self.driver=self.open_browser(browsername)
        


    def loginbos(self):

