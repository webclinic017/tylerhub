'''
Author: tyler
Date: 2021-05-13 10:43:00
LastEditTime: 2021-09-22 15:54:40
LastEditors: Please set LastEditors
Description: This module is used to store random data and data processing.Including regular matching of the re module, etc
FilePath: tylerhub\demo\public\randomdata.py
'''
import logging
import random
import re
import time

"""此模块用于存放生成随机数据及数据的处理"""
class Random_data():

    #生成N位随机数字与字母组合随机数
    def get_rangenum(self,n):
        self.number=''.join(random.sample('0123456789abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',n))
        return self.number

    #生成N位数字与大小写字母组合的随机数(密码)
    def get_psword_type(self,N):
        if 1<N<=12:
            num_str=''.join(random.sample('0123456789',N-2))
            block_letter=random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            lowser_letter=random.choice('abcdefghijklmnopqrstuvwxyz')
            self.psword=block_letter+lowser_letter+num_str
            return self.psword
        else:
            print('N必须大于2小于12')

    #生成N位随机纯数字或者纯字母组合随机数
    def get_purerange(self,n,type):
        """
        :param type:letter;number
        """

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
        """str:包含数字的字符串"""
        try:
            return re.sub(r'\D','',str)
        except Exception as msg:
            self.log_output('!!--!!extract_numbers').error(msg)

    #正则提取字符串
    def regex(self,regextype,str)->str:
        """
        正则匹配，返回字符串,findall方法
        :param regextype:正则表达式
        :param str:匹配的字符串
        :return str
        """
        try:
            self.pattern=re.compile(regextype)
            self.set=self.pattern.findall(str)
            return ''.join(self.set)
        except Exception as msg:
            log.my_logger('!!--!!regex').error(msg)


    #生成x-y之间的单个随机整数
    def random_int(self,x,y):
        try:
            return random.randint(x,y)
        except Exception as msg:
            self.log_output('!!--!!random_int').error('请输入正确的参数：x<y:{}'.format(msg))
    

    #生成随机格式化日期(>18岁)
    def random_date(self):
        #设置开始时间元祖
        data1=(1976,1,1,0,0,0,0,0,0)
        #设置结束时间元祖
        data2=(2002,12,31,23,59,59,0,0,0)
        #开始时间戳
        startime=time.mktime(data1)
        #结束时间戳
        endtime=time.mktime(data2)
        #在开始和结束时间戳段内随机选取
        t=random.randint(startime, endtime)
        #生成时间元祖
        data_tuple=time.localtime(t)
        #格式化
        data_time=time.strftime('%Y-%m-%d',data_tuple)
        return data_time


            
#测试
if __name__=='__main__':
    pub=Random_data()
    # print((pub.extract_numbers('ID: 1000005357')))
    # print(pub.extract_numbers('ID: 1000005357')[0:2]=='10')
    # print(pub.random_int(10,20))
    # print(float(pub.extract_numbers('( 可取款金额 |3,065.65USD )'))/100)
    # print(pub.get_purerange(14,'number'))
    #pub.log_output('test').error('testttttt')
    # print(int(pub.extract_numbers('( 可取款金额 | 50,265.01 USD )'))/100)
    # print(float(int(pub.extract_numbers('您的出金申请將收取5.00USD美元手续费'))/100))
    print(int(pub.extract_numbers('0.00 USD')))





