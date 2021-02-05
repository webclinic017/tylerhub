import sys
import os

path_test=path_test=__file__
print('test路径：{}'.format(path_test))
print('sys.path默认值：{}'.format(sys.path))
path=os.path.dirname(os.path.dirname(__file__))
path=os.path.join(path,'publick')
print('browser_actions路径：{}'.format(path))
