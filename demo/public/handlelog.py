import logging
import os

from read_dataconfig import ReadConfig
from handlepath import LOGDIR

read=ReadConfig()

class MyLog():
    """
    系统日志输出
    """

    # @staticmethod
    def my_logger(self,name=read.get_value('log','name')):
        """
        输出日志到控制台及日志文件中
        """
        try:
            # 创建收集器，设置收集器的等级
            logger = logging.getLogger(name)
            logger.setLevel(read.get_value('log','level'))
            # 创建输出到控制台的渠道，设置等级
            sh = logging.StreamHandler()
            sh.setLevel(read.get_value('log','info_level'))
            logger.addHandler(sh)
            # 创建输出到文件的渠道，设置等级
            fh = logging.FileHandler(filename=os.path.join(LOGDIR,"log.log"), encoding="utf8")
            fh.setLevel(read.get_value('log','info_level'))
            logger.addHandler(fh)
            # 设置日志输出格式
            formater = '%(name)s - %(asctime)s - %(module)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
            fm = logging.Formatter(formater)
            sh.setFormatter(fm)
            fh.setFormatter(fm)
            return logger
        except Exception as msg:
            print('请检查当前文件父级目录下是否存在log文件夹：{}'.format(msg))


if __name__ == '__main__':
    log = MyLog()
    log.my_logger().info('it is my test log message info')
