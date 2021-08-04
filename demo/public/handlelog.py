import logging
import os
import sys
from read_dataconfig import ReadConfig
import datetime

read=ReadConfig()

class MyLog():
    """
    系统日志输出，调用此方法时，需在项目路径下创建一个log文件用来存放log.log
    """
    def __init__(self):

        #在调用此方法/类的文件目录的父级的父级创建创建一个log文件
        self.moudlePath=os.path.join(os.path.dirname(os.path.dirname(sys._getframe().f_back.f_code.co_filename)),'log')
        self.lineNo = sys._getframe().f_back.f_lineno

    # @staticmethod
    def my_logger(self,name=read.get_value('log','name')):
        """
        输出日志到控制台及日志文件中,只有高于WARN级别的日志才会输出到日志文件中，其他级别日志仅输出到控制台
        """
        try:
            # 创建收集器，设置收集器的等级
            logger = logging.getLogger(name)
            logger.setLevel(read.get_value('log','level'))
            # 创建输出到控制台的渠道，设置等级
            sh_log = logging.StreamHandler()
            sh_log.setLevel(read.get_value('log','info_level'))
            logger.addHandler(sh_log)
            # 创建输出到文件的渠道，设置等级
            fh_log = logging.FileHandler(filename=os.path.join(self.moudlePath,'{}-log.log'.format(datetime.datetime.now().strftime('%Y-%m-%d'))), encoding="utf8")
            fh_log.setLevel(read.get_value('log','warn_level')) 
            logger.addHandler(fh_log)
            # 设置日志输出格式
            formater = '%(name)s - %(asctime)s - %(module)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
            fm_log = logging.Formatter(formater)
            sh_log.setFormatter(fm_log)
            fh_log.setFormatter(fm_log)
            return logger
        except Exception as msg:
            print('请检查当前文件父级目录下是否存在log文件夹：{}'.format(msg))


if __name__ == '__main__':
    log = MyLog()
    log.my_logger().error('itestet')
