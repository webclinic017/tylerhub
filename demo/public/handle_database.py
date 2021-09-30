'''
Author: tyler
Date: 2021-08-26 18:27:17
LastEditTime: 2021-09-30 16:09:47
LastEditors: Please set LastEditors
Description: Query database and save
FilePath: \tylerhub\demo\public\handle_database.py
'''

import pymongo
import ssl
import  cx_Oracle
import pymysql
import os
import sys
from read_dataconfig import ReadConfig
from about_data import Aboutdata
from verification_code import use_time

#全局取消证书验证
ssl._create_default_https_context=ssl._create_unverified_context()

#添加oracle驱动程序(添加驱动后系统找不到allure程序/系统无法同时运行两个驱动程序)
#config_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'config')
# os.environ['path']=os.path.join(config_path,'instantclient_19_11')


class Dadabase_operate(object):
    """
    mysql,oracle,mongodb数据库查询与保存
    """
    global conFig,aboutData
    
    conFig=ReadConfig()
    aboutData=Aboutdata()

    #连接mongodb数据库查询数据
    @use_time #统计查询时间
    def search_in_mongodb(self,uri,database,muster,mongodbserch:dict=None,*args,N:int=0,sortTerm:list=[('_id',-1)])->list:
        
        """
        读取配置文件中的mongodb链接，传入查询条件查询指定数据库集合中的数据，默认最新数据排序并以列表形式返回
        :param uri:数据库链接
        :param database：数据库
        :param muster：集合
        :param mongodbserch:mongodb查询语句,字典,类似于sql语句 如{"$and": [{"latdec": 9.3547792}, {"watlev": "always dry"}]}
        :param N:查询条数，默认为0
        :param args:需具体查询的字段
        :param sortTerm:是否排序，字典。1升序，-1降序，_id,-1 查询最新数据
        :return 以列表类型返回查询数据
        """

        #2.0mongodb数据库链接
        try:
            self.client=pymongo.MongoClient(uri,ssl_cert_reqs=ssl.CERT_NONE)
            self.db=self.client[database]
            self.colletion=self.db[muster]
            #查询条件不为空
            if not mongodbserch==None:
                self.list_data=[]
                #查询所有数据
                if N==0:
                    self.data=self.colletion.find(mongodbserch).sort(sortTerm)
                    #查所有字段
                    if len(args)==0:
                        for i in self.data:
                            self.list_data.append(i)
                    #查询指定字段
                    else:
                        for i in self.data:
                            self.dict_search={}
                            for x in args:
                                self.dict_search[x]=i[x]
                            self.list_data.append(self.dict_search)    
                #查询部分数据
                else:
                    self.data=self.colletion.find(mongodbserch).limit(N).sort(sortTerm)
                    #查询所有字段
                    if len(args)==0:
                        for i in self.data:
                            self.list_data.append(i)
                        #查询指定字段
                    else:
                        for i in self.data:
                            self.dict_search={}
                            for x in args:
                                self.dict_search[x]=i[x]
                            self.list_data.append(self.dict_search)   
                print('返回数据库数据{}条'.format(len(self.list_data)))
                return self.list_data
            #查询条件为空时
            else:
                self.list_data=[]
                #查询所有数据
                if N==0:
                    self.data=self.colletion.find().sort(sortTerm)
                    #查询所有字段
                    if len(args)==0:
                        for i in self.data:
                            self.list_data.append(i)
                    #查询指定字段
                    else:
                        for i in self.data:
                            self.dict_search={}
                            for x in args:
                                self.dict_search[x]=i[x]
                            self.list_data.append(self.dict_search)    
                #查询部分数据
                else:
                    self.data=self.colletion.find().limit(N).sort(sortTerm)
                    #查询所有字段
                    if len(args)==0:
                        for i in self.data:
                            self.list_data.append(i)
                    #查询指定字段
                    else:
                        for i in self.data:
                            self.dict_search={}
                            for x in args:
                                self.dict_search[x]=i[x]
                            self.list_data.append(self.dict_search)    
                print('读取数据库数据{}条'.format(len(self.list_data)))
                return self.list_data
        except Exception as msg:
            print('数据库连接或参数有误,请检查用户密码,参数或本机ip是否能连接数据库:{}'.format(msg))


    #mongodb数据保存
    @use_time #统计函数运行时间
    def save_mongodb_data(self,excelpath,uri,database,muster,mongodbserch:dict=None,N:int=0,sortTerm:list=[('_id',-1)],**kwargs)->str:
        
        """
        调用save_mongodb_data查询，保存查询数据到本地文档
        :param excelpath:本地文档路径
        :param uri:数据库链接
        :param database：数据库
        :param muster：集合
        :param mongodbserch:mongodb查询语句,字典,类似于sql语句 如{"$and": [{"latdec": 9.3547792}, {"watlev": "always dry"}]}
        :param N:查询条数，默认为0
        :param sortTerm:是否排序，字典。1升序，-1降序，_id,-1 查询最新数据
        :param kwargs:键值对，key对应需查询字段，value对应查询字段保存在本地文档中列，如title='A',runtime='B',rated='C'
        """

        try:
            #拆分kwargs参数
            self.list_search=[]
            self.list_save=[]
            #获取key与value值
            for key,value in kwargs.items():
                self.list_search.append(key)
                self.list_save.append(value)
            #调用函数查询数据库
            self.mongo_data=self.search_in_mongodb(uri, database, muster,mongodbserch,*self.list_search,N=N,sortTerm=sortTerm)
            # #保存数据
            for i in self.list_search:
                for y in self.mongo_data:
                    aboutData.saveainfo(excelpath, y[i], self.list_save[self.list_search.index(i)], self.mongo_data.index(y)+2)

                print('字段"{}"保存在{}列'.format(i,self.list_save[self.list_search.index(i)]))
        except Exception as msg:
            print('请检查参数及数据库链接是否有误：{}'.format(msg))


#    #连接oracle数据库 
#     def serach_in_oracle(self,sql,type='single'):
#         try:
#             #连接
#             self.con = cx_Oracle.connect('{}/{}@{}:{}/{}'.format(conFig.get_value('oracle','username'),conFig.get_value('oracle','password'),
#             conFig.get_value('oracle','host'),conFig.get_value('oracle','port'),conFig.get_value('oracle','server_name')))
#             #创建游标
#             self.cursor= self.con.cursor()  
#             #执行sql
#             self.cursor.execute(sql)
#             if type=='single':
#             #获取单条数据
#                 self.data=self.cursor.fetchone()
#             else:
#             #获取所有数据
#                 self.data=self.cursor.fetchall()
#             self.cursor.close()
#             self.con.close()
#             return self.data
#         except Exception as msg:
#             print('请检查连接信息及sql语句是否正确：{}'.format(msg))


    #连接mysql数据库查询
    @use_time #统计函数运行时间
    def search_in_mysql(self,sql,host,user,psword,port:int,type='single')->str:
        """
        :param vartuple:host,username,password,db,port,charset=utf-8
        :param sql: 执行查询的sql语句
        :param type: 查询单条或者所有符合sql语句的数据
        :return 返回查询数据
        """
        try:
            #连接
            self.db = pymysql.connect(host=host,user=user,password=psword,port=port)
            #创建游标对象
            self.cursor=self.db.cursor()
            #执行sql语句
            self.cursor.execute(sql)
            #查询单条数据
            if type=='single':
                self.data=self.cursor.fetchone()
            #查询所有数据
            else:
                self.data=self.cursor.fetchall()
            self.cursor.close()
            self.db.close()
            return self.data
        except Exception as msg:
            print('请检查连接信息及sql语句是否正确：{}'.format(msg)) 

#测试
if __name__=='__main__':
    dataBase=Dadabase_operate()
    # dataBase.search_in_mongodb(conFig.get_value('mongodb_test', 'uri'), 'sample_mflix', 
    # 'movies',{"year":1915},'title','runtime',N=0)
    # excelpath=r'D:\code\tylerhub\demo\public\about_data.xlsx'
    # dataBase.save_mongodb_data(excelpath,conFig.get_value('mongodb_test', 'uri'),'sample_mflix','movies',
    # {"year":1915},N=0,sortTerm=[('_id',-1)],title='A',runtime='B',rated='C')
    # dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'), 'atfxgm-sit', 'atfx_trade_account',
    # {"accountNumber":1000005349},'tradeAccount',N=1)
    # encrypt_secret=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'), 'atclientpoolsit', 'usersgm',{"email":'tyler.tang@test.com'},'encrypt_secret',N=0)
    # print(encrypt_secret[0]['encrypt_secret'])
    times=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'), 
    'atfxgm-sit', 'atfx_withdrawal',{"tradeAccount":"672005304"},'createDate',N=1)[0]['createDate']
    print(times)