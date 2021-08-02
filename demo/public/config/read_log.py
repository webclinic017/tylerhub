import logging
from logging import config
import os

conf_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'logging.conf')

class MyLog(object):

    def __init__(self):

        config.fileConfig(conf_path)
        self.logger = logging.getLogger('fileAndConsole')

    @property
    def my_logger(self):

        return self.logger

if __name__ == '__main__':
    log = MyLog()
    log.my_logger.error('it is my test log message info')
