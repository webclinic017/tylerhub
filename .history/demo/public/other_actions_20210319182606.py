import logging
import random
import re
import time
import functools
from verification_code import *

"""此模块用于存放公共方法"""
class public_method():
    
    #创建日志函数，打印日志报告,错误级别：debug、info、warning、error、critical
    def log_output(self,name): #参数name为日志名字
        #创建一个logger
        self.logger = logging.getLogger(name) #定义Logger的名字，之前直接用logging调用的名字是root，日志格式用%(name)s可以获得。这里的名字也可以自定义比如"TEST"
        self.logger.setLevel(logging.DEBUG) #低于这个级别将被忽略，后面可以设置输出级别
        # 创建handler和输出级别
        self.output_log = logging.StreamHandler()  # 输出到屏幕的handler
        self.output_log.setLevel(logging.INFO)  # 输出级别和上面的忽略级别都不一样，可以看一下效果
        # 关键参数datefmt自定义日期格式    
        self.ch_formatter = logging.Formatter('%(name)s %(asctime)s {%(levelname)s}:%(message)s',datefmt='%Y-%m-%d %H:%M:%S')
        # 把上面的日志格式和输出到屏幕的handler关联起来
        self.output_log.setFormatter(self.ch_formatter)
        # 将handler加入logger
        self.logger.addHandler(self.output_log)
        #返回输出日志级别
        return self.logger

    #生成N位随机数字与字母组合随机数
    def get_rangenum(self,n):
        self.number=''.join(random.sample('0123456789abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',n))
        return self.number

    #生成N位随机纯数字或者纯字母组合随机数
    def get_purerange(self,n,type):
        if type=='letter':
            self.string=''.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ',n))
            return self.string
        elif type=='number':
            times=n
            list=[]
            while times>0:
                list.append(str(random.randint(0,9)))
                times=times-1
            self.string=''.join(list)
            return self.string
        else:
            print('type变量请输入letter或number，生成随机纯数字或字母组合')

    #生成n位数随机邮箱
    def get_rangenemail(self,n):
        self.get_rangenum(n)
        self.email_list = ['@qq.com','@163.com','@gmail.com',]
        self.email = ''.join(self.number+str(random.choice(self.email_list))) # 随机生成联通号码
        return self.email

    #随机手机号
    def get_rangephone(self):
        #开头
        self.phone_list=['186','136','151','188','173']
        self.phonenum=random.choice(self.phone_list)+''.join(random.sample('0123456789',8))
        return self.phonenum

    #提取数字
    def extract_numbers(self,str):
        try:
            return re.sub(r'\D','',str)
        except Exception as msg:
            self.log_output('!!--!!extract_numbers').error(msg)

    @time_me('ddd')
    #生成x-y之间的单个随机整数
    def random_int(self,x,y):
        try:
            return random.randint(x,y)
        except Exception as msg:
            self.log_output('!!--!!random_int').error('请输入正确的参数：x<y:{}'.format(msg))

#测试
if __name__=='__main__':
    pub=public_method()
    # print((pub.extract_numbers('ID: 1000005357')))
    # print(pub.extract_numbers('ID: 1000005357')[0:2]=='10')
    print(pub.random_int(10,20))