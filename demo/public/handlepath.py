import os

#项目目录路径
BASEDIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#用例数据目录路径
DATADIR=os.path.join(BASEDIR, 'data')

#测试报告目录路径
REPORTDIR=os.path.join(BASEDIR, 'report')

#日志输出目录路径
LOGDIR=os.path.join(BASEDIR, 'log')