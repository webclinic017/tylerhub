import xlrd
from openpyxl import load_workbook
import pymongo
import ssl
import  cx_Oracle
import pymysql
import os
import sys
from read_dataconfig import ReadConfig
config_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'config')


#全局取消证书验证
ssl._create_default_https_context=ssl._create_unverified_context()

#添加oracle驱动程序(添加驱动后系统找不到allure程序/系统无法同时运行两个驱动程序)
# os.environ['path']=os.path.join(config_path,'instantclient_19_11')

conFig=ReadConfig()

class Aboutdata():
    """此模块用于提取excel表格中的数据，并封装成含多个字典的列表
    文件格式为xlsx的后缀即可"""
    def openexcel(self,excelpath,sheetname):
        """excelpath为excel文件存储路径，sheetname为sheet名"""
        #打开excel表格
        self.data=xlrd.open_workbook(excelpath)
        #通过sheet名打开对应sheet表
        self.table=self.data.sheet_by_name(sheetname)
        #获取第一行数据作为key值,下标为0
        self.key=self.table.row_values(0)
        #获取总行数
        self.rows=self.table.nrows
        #获取总列数
        self.clos=self.table.ncols
        #返回行数
        return self.rows

    #将表中数据以含多个字典的列表的数据类型输出
    def dict_data(self):
        #判断表中有无数据
        if self.rows <= 1:
            print('该sheet表无数据')
        else:
            l=[]
            j=1
            for i in range(self.rows-1): #去除首行
                self.values=self.table.row_values(j)#第j行数据作为values
                s={}
                for x in range(self.clos):#根据列数
                    s[self.key[x]]=self.values[x] #每个循环的字典中，key列表中的第x项=valus列表中的第x项
                l.append(s) #i循环下，添加进列表l
                j=j+1
            return l

    def str_insert(self,old_str,pos:int,add_str)->str:
        """
        字符串指定位置添加字符串
        :param old_str : 被添加字符的字符串
        :param pos : 添加的位置
        :param add_str : 添加的字符串
        :return 返回新字符串
        """
        self.str_list=list(old_str)
        self.str_list.insert(pos, add_str)
        self.str_out=''.join(self.str_list)
        return self.str_out


    # 创建存储注册数据的函数，写入已存在的本地文档中,cloumn:列；row:行
    def saveainfo(self,excelpath,values,column,row:int)->str:
        """
        param:column 列
        param:row 行
        注：调用此函数时，不能打开需要写入数据的文档
        """
        try:
            workbook = load_workbook(filename=excelpath)
            sheet = workbook.active
            cel = sheet['{}{}'.format(column, row)]
            cel.value = values
            workbook.save(filename=excelpath)
        except Exception as msg:
            print('请勿打开需要写入文件的文档：{}'.format(msg))


    #连接mongodb数据库查询数据
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
        #2.0数据库链接
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
                print(self.list_data)
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
                print(self.list_data)
                print('读取数据库数据{}条'.format(len(self.list_data)))
                return self.list_data
        except Exception as msg:
            print('数据库连接或参数有误,请检查用户密码,参数或本机ip是否能连接数据库:{}'.format(msg))


    #mongodb数据保存
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
                    self.saveainfo(excelpath, y[i], self.list_save[self.list_search.index(i)], self.mongo_data.index(y)+2)

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
    e=Aboutdata()
    # e.openexcel(r'D:\code\tylerhub\demo\registration_process\test_excel_data\account_number.xlsx','Sheet1')
    # a=e.dict_data()
    # print(a)
    # print(a[0]['邮箱'][0:2]=='14')
    # e.search_in_mongodb('atfx-dev-admin','m578A3MGrcR3pRXVU2pA','atfxgm-uat','atfx_ib_links','isDeleted',0,'link',1)
    # e.searchs_for_mongodb('atfx-dev-admin', 'm578A3MGrcR3pRXVU2pA', 'atfxgm-uat', 'atfx_ib_links','isDeleted',0,'currency','markup','leverage','mtGroup','link','spreadType',6,3)
    # path=r'D:\code\tylerhub\demo\registration_process\test_excel_data\all_links.xlsx'
    # e.save_mongodb_data(path,'atfx-dev-admin','m578A3MGrcR3pRXVU2pA','atfxgm-uat','atfx_ib_links',condition='isDeleted',value=0,
    # link='A',currency='B',markup='C',leverage='D',mtGroup='E',spreadType='F',num=6)
    # print(11)
    #print(e.serach_in_oracle("SELECT * FROM (SELECT NOTE FROM HQYTZSC.MBMESSAGE WHERE REVMBNO='17688937072'  ORDER BY DTMAKEDATE DESC)  WHERE ROWNUM<2"))
    # e.search_in_mysql(sql="SELECT * FROM client_relationship2_sit.relationship where node_Id='100004'",
    # host=conFig.get_value('mysql_AWS', 'host'),user=conFig.get_value('mysql_AWS', 'user'),
    # psword=conFig.get_value('mysql_AWS', 'password'),port=conFig.get_int('mysql_AWS', 'port'))
    # e.openexcel(r'D:\code\tylerhub\demo\registration_process\test_excel_data\account_number.xlsx', 'Sheet1')
    # a=e.dict_data()
    # print(a)
    # print(a[0]['主账号']=='')
    # e.search_in_mongodb(conFig.get_value('mongodb_test', 'uri'), 'sample_mflix', 
    # 'movies',{"year":1915},'title','runtime',N=0)
    excelpath=r'D:\code\tylerhub\demo\public\about_data.xlsx'
    e.save_mongodb_data(excelpath,conFig.get_value('mongodb_test', 'uri'),'sample_mflix','movies',
    {"year":1915},N=0,sortTerm=[('_id',-1)],title='A',runtime='B',rated='C')