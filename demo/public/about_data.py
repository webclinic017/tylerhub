import xlrd
from openpyxl import load_workbook
import pymongo
import ssl

#全局取消证书验证
ssl._create_default_https_context=ssl._create_unverified_context()


class exceldata():
    """此文件用于提取excel表格中的数据，并封装成含多个字典的列表
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

    # 创建存储注册数据的函数，写入已存在的本地文档中,cloumn:列；row:行
    def saveainfo(self,excelpath,values,column,row):
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


    #连接mongodb数据库，查询指定字段内容
    def search_in_mongodb(self,username,password,database,muster,condition=None,value=None,filed=None,N=0):
        """
        username:用户名
        password：密码
        database：数据库
        muster：集合
        condition:搜索条件
        value:搜索条件的值
        N:查询条数，默认为0
        filed:需具体查询的字段
        """
        #2.0数据库链接
        try:
            self.uri='mongodb+srv://{}:{}@atfx2-dev-loa0g.azure.mongodb.net/atfx_test?\
authSource=admin&replicaSet=atfx2-dev-shard-0&readPreference=primary&appname=MongoDB%20Compass%20Community&\
retryWrites=true&ssl=true'.format(username,password)
            self.client=pymongo.MongoClient(self.uri)
            self.db=self.client[database]
            self.colletion=self.db[muster]
            if condition!=None and value!=None:
                self.list_data=[]
                if N==0:
                    if type(value)==int:
                        self.data=self.colletion.find({'{}'.format(condition):value})
                        if filed==None:
                            for i in self.data:
                                self.list_data.append(i)
                        else:
                            for i in self.data:
                                self.list_data.append(i[filed])
                    else:
                        self.data=self.colletion.find({'{}'.format(condition):'{}'.format(value)})
                        if filed==None:
                            for i in self.data:
                                self.list_data.append(i)
                        else:
                            for i in self.data:
                                self.list_data.append(i[filed])
                    print(self.list_data)
                    print('读取数据库数据条数：{}'.format(len(self.list_data)))
                    return self.list_data
                else:
                    if type(value)==int:
                        self.data=self.colletion.find({'{}'.format(condition):value}).limit(N)
                        if filed==None:
                            for i in self.data:
                                self.list_data.append(i)
                        else:
                            for i in self.data:
                                self.list_data.append(i[filed])
                    else:
                        self.data=self.colletion.find({'{}'.format(condition):'{}'.format(value)}).limit(N)
                        if filed==None:
                            for i in self.data:
                                self.list_data.append(i)
                        else:
                            for i in self.data:
                                self.list_data.append(i[filed])
                print(self.list_data)
                print('读取数据库数据条数：{}'.format(len(self.list_data)))
                return self.list_data
            else:
                self.list_data=[]
                if N==0:
                    self.data=self.colletion.find()
                    if filed==None:
                        for i in self.data:
                            self.list_data.append(i)
                    else:
                        for i in self.data:
                            self.list_data.append(i[filed])
                else:
                    self.data=self.colletion.find().limit(N)
                    if filed==None:
                        for i in self.data:
                            self.list_data.append(i)
                    else:
                        for i in self.data:
                            self.list_data.append(i[filed])
                print(self.list_data)
                print('读取数据库数据条数：{}'.format(len(self.list_data)))
                return self.list_data
        except Exception as msg:
            print('数据库链接或参数有误:{}'.format(msg))


    #连接mongodb数据库，查询多个字段内容    
    def searchs_for_mongodb(self,username,password,database,muster,condition=None,value=None,filed1=None,
    filed2=None,filed3=None,filed4=None,filed5=None,filed6=None,num=6,N=0):
        """
        username:用户名
        password：密码
        database：数据库
        muster：集合
        N:查询条数，默认为0(查询所有满足条件的数据)
        filed:需具体查询的字段
        num:每条数据具体查询的字段个数,默认最大为6(1~6)
        """
        try:
            self.uri='mongodb+srv://{}:{}@atfx2-dev-loa0g.azure.mongodb.net/atfx_test?\
authSource=admin&replicaSet=atfx2-dev-shard-0&readPreference=primary&appname=MongoDB%20Compass%20Community&\
retryWrites=true&ssl=true'.format(username,password)
            self.client=pymongo.MongoClient(self.uri)
            self.db=self.client[database]
            self.colletion=self.db[muster]
            self.list_search=[]
            if condition==None and value==None:
                if N==0:
                    self.data=self.colletion.find()
                    if num==1:
                        for i in self.data:
                            self.dict_search={}
                            self.dict_search[filed1]=i[filed1]
                            self.list_search.append(self.dict_search)
                    elif num==2:
                        for i in self.data:
                            self.dict_search={}
                            self.dict_search[filed1]=i[filed1]
                            self.dict_search[filed2]=i[filed2]
                            self.list_search.append(self.dict_search)
                    elif num==3:
                        for i in self.data:
                            self.dict_search={}
                            self.dict_search[filed1]=i[filed1]
                            self.dict_search[filed2]=i[filed2]
                            self.dict_search[filed3]=i[filed3]
                            self.list_search.append(self.dict_search)
                    elif num==4:
                        for i in self.data:
                            self.dict_search={}
                            self.dict_search[filed1]=i[filed1]
                            self.dict_search[filed2]=i[filed2]
                            self.dict_search[filed3]=i[filed3]
                            self.dict_search[filed4]=i[filed4]
                            self.list_search.append(self.dict_search)
                    elif num==5:
                        for i in self.data:
                            self.dict_search={}
                            self.dict_search[filed1]=i[filed1]
                            self.dict_search[filed2]=i[filed2]
                            self.dict_search[filed3]=i[filed3]
                            self.dict_search[filed4]=i[filed4]
                            self.dict_search[filed5]=i[filed5]
                            self.list_search.append(self.dict_search)
                    else:
                        for i in self.data:
                            self.dict_search={}
                            self.dict_search[filed1]=i[filed1]
                            self.dict_search[filed2]=i[filed2]
                            self.dict_search[filed3]=i[filed3]
                            self.dict_search[filed4]=i[filed4]
                            self.dict_search[filed5]=i[filed5]
                            self.dict_search[filed6]=i[filed6]
                            self.list_search.append(self.dict_search)
                else:
                    self.data=self.colletion.find().limit(N)
                    if num==1:
                        for i in self.data:
                            self.dict_search={}
                            self.dict_search[filed1]=i[filed1]
                            self.list_search.append(self.dict_search)
                    elif num==2:
                        for i in self.data:
                            self.dict_search={}
                            self.dict_search[filed1]=i[filed1]
                            self.dict_search[filed2]=i[filed2]
                            self.list_search.append(self.dict_search)
                    elif num==3:
                        for i in self.data:
                            self.dict_search={}
                            self.dict_search[filed1]=i[filed1]
                            self.dict_search[filed2]=i[filed2]
                            self.dict_search[filed3]=i[filed3]
                            self.list_search.append(self.dict_search)
                    elif num==4:
                        for i in self.data:
                            self.dict_search={}
                            self.dict_search[filed1]=i[filed1]
                            self.dict_search[filed2]=i[filed2]
                            self.dict_search[filed3]=i[filed3]
                            self.dict_search[filed4]=i[filed4]
                            self.list_search.append(self.dict_search)
                    elif num==5:
                        for i in self.data:
                            self.dict_search={}
                            self.dict_search[filed1]=i[filed1]
                            self.dict_search[filed2]=i[filed2]
                            self.dict_search[filed3]=i[filed3]
                            self.dict_search[filed4]=i[filed4]
                            self.dict_search[filed5]=i[filed5]
                            self.list_search.append(self.dict_search)
                    else:
                        for i in self.data:
                            self.dict_search={}
                            self.dict_search[filed1]=i[filed1]
                            self.dict_search[filed2]=i[filed2]
                            self.dict_search[filed3]=i[filed3]
                            self.dict_search[filed4]=i[filed4]
                            self.dict_search[filed5]=i[filed5]
                            self.dict_search[filed6]=i[filed6]
                            self.list_search.append(self.dict_search)                    
            else:
                if N==0:
                    if type(value)==int:
                        self.data=self.colletion.find({'{}'.format(condition):value})
                        if num==1:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.list_search.append(self.dict_search)
                        elif num==2:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.list_search.append(self.dict_search)
                        elif num==3:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.dict_search[filed3]=i[filed3]
                                self.list_search.append(self.dict_search)
                        elif num==4:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.dict_search[filed3]=i[filed3]
                                self.dict_search[filed4]=i[filed4]
                                self.list_search.append(self.dict_search)
                        elif num==5:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.dict_search[filed3]=i[filed3]
                                self.dict_search[filed4]=i[filed4]
                                self.dict_search[filed5]=i[filed5]
                                self.list_search.append(self.dict_search)
                        else:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.dict_search[filed3]=i[filed3]
                                self.dict_search[filed4]=i[filed4]
                                self.dict_search[filed5]=i[filed5]
                                self.dict_search[filed6]=i[filed6]
                                self.list_search.append(self.dict_search)
                    else:
                        self.data=self.colletion.find({'{}'.format(condition):'{}'.format(value)})   
                        if num==1:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.list_search.append(self.dict_search)
                        elif num==2:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.list_search.append(self.dict_search)
                        elif num==3:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.dict_search[filed3]=i[filed3]
                                self.list_search.append(self.dict_search)
                        elif num==4:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.dict_search[filed3]=i[filed3]
                                self.dict_search[filed4]=i[filed4]
                                self.list_search.append(self.dict_search)
                        elif num==5:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.dict_search[filed3]=i[filed3]
                                self.dict_search[filed4]=i[filed4]
                                self.dict_search[filed5]=i[filed5]
                                self.list_search.append(self.dict_search)
                        else:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.dict_search[filed3]=i[filed3]
                                self.dict_search[filed4]=i[filed4]
                                self.dict_search[filed5]=i[filed5]
                                self.dict_search[filed6]=i[filed6]
                                self.list_search.append(self.dict_search)
                else:
                    if type(value)==int:
                        self.data=self.colletion.find({'{}'.format(condition):value}).limit(N)
                        if num==1:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.list_search.append(self.dict_search)
                        elif num==2:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.list_search.append(self.dict_search)
                        elif num==3:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.dict_search[filed3]=i[filed3]
                                self.list_search.append(self.dict_search)
                        elif num==4:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.dict_search[filed3]=i[filed3]
                                self.dict_search[filed4]=i[filed4]
                                self.list_search.append(self.dict_search)
                        elif num==5:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.dict_search[filed3]=i[filed3]
                                self.dict_search[filed4]=i[filed4]
                                self.dict_search[filed5]=i[filed5]
                                self.list_search.append(self.dict_search)
                        else:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.dict_search[filed3]=i[filed3]
                                self.dict_search[filed4]=i[filed4]
                                self.dict_search[filed5]=i[filed5]
                                self.dict_search[filed6]=i[filed6]
                                self.list_search.append(self.dict_search)
                    else:
                        self.data=self.colletion.find({'{}'.format(condition):'{}'.format(value)}).limit(N)
                        if num==1:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.list_search.append(self.dict_search)
                        elif num==2:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.list_search.append(self.dict_search)
                        elif num==3:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.dict_search[filed3]=i[filed3]
                                self.list_search.append(self.dict_search)
                        elif num==4:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.dict_search[filed3]=i[filed3]
                                self.dict_search[filed4]=i[filed4]
                                self.list_search.append(self.dict_search)
                        elif num==5:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.dict_search[filed3]=i[filed3]
                                self.dict_search[filed4]=i[filed4]
                                self.dict_search[filed5]=i[filed5]
                                self.list_search.append(self.dict_search)
                        else:
                            for i in self.data:
                                self.dict_search={}
                                self.dict_search[filed1]=i[filed1]
                                self.dict_search[filed2]=i[filed2]
                                self.dict_search[filed3]=i[filed3]
                                self.dict_search[filed4]=i[filed4]
                                self.dict_search[filed5]=i[filed5]
                                self.dict_search[filed6]=i[filed6]
                                self.list_search.append(self.dict_search)
            print('数据库查询条数：{}，查询字段个数：{},如下：'.format(len(self.list_search),num))
            print(self.list_search)
            return self.list_search
        except Exception as msg:
            print('查询数据库失败，请检查链接/参数：{}'.format(msg))


    #数据库查询数据保存
    def save_mongodb_data(self,excelpath,username,password,database,muster,condition=None,value=None,filed1=None,filed2=None,
    filed3=None,filed4=None,filed5=None,filed6=None,column1=None,column2=None,column3=None,column4=None,column5=None,column6=None,num=6,N=0):
        try:
            self.mongo_data=self.searchs_for_mongodb(username,password,database,muster,condition,value,filed1,filed2,filed3,filed4,filed5,filed6,num,N)
            if num==1:
                for i in self.mongo_data:
                    self.saveainfo(excelpath, i[filed1], column1, self.mongo_data.index(i)+2)
            elif num==2:
                for i in self.mongo_data:
                    self.saveainfo(excelpath, i[filed1], column1, self.mongo_data.index(i)+2)
                    self.saveainfo(excelpath, i[filed2], column2, self.mongo_data.index(i)+2)
            elif num==3:
                for i in self.mongo_data:
                    self.saveainfo(excelpath, i[filed1], column1, self.mongo_data.index(i)+2)
                    self.saveainfo(excelpath, i[filed2], column2, self.mongo_data.index(i)+2)
                    self.saveainfo(excelpath, i[filed3], column3, self.mongo_data.index(i)+2) 
            elif num==4:
                for i in self.mongo_data:
                    self.saveainfo(excelpath, i[filed1], column1, self.mongo_data.index(i)+2)
                    self.saveainfo(excelpath, i[filed2], column2, self.mongo_data.index(i)+2)
                    self.saveainfo(excelpath, i[filed3], column3, self.mongo_data.index(i)+2) 
                    self.saveainfo(excelpath, i[filed2], column4, self.mongo_data.index(i)+2)
            elif num==5:
                for i in self.mongo_data:
                    self.saveainfo(excelpath, i[filed1], column1, self.mongo_data.index(i)+2)
                    self.saveainfo(excelpath, i[filed2], column2, self.mongo_data.index(i)+2)
                    self.saveainfo(excelpath, i[filed3], column3, self.mongo_data.index(i)+2)
                    self.saveainfo(excelpath, i[filed4], column4, self.mongo_data.index(i)+2)
                    self.saveainfo(excelpath, i[filed5], column5, self.mongo_data.index(i)+2)
            else:
                for i in self.mongo_data:
                    self.saveainfo(excelpath, i[filed1], column1, self.mongo_data.index(i)+2)
                    self.saveainfo(excelpath, i[filed2], column2, self.mongo_data.index(i)+2)
                    self.saveainfo(excelpath, i[filed3], column3, self.mongo_data.index(i)+2)
                    self.saveainfo(excelpath, i[filed4], column4, self.mongo_data.index(i)+2)
                    self.saveainfo(excelpath, i[filed5], column5, self.mongo_data.index(i)+2)
                    self.saveainfo(excelpath, i[filed6], column6, self.mongo_data.index(i)+2)
        except Exception as msg:
            print('保存数据库数据失败，请检查链接/参数：{}'.format(msg))


                

#测试
if __name__=='__main__':
    e=exceldata()
    # e.openexcel(r'D:\code\tylerhub\demo\registration_process\test_excel_data\account_number.xlsx','Sheet1')
    # a=e.dict_data()
    # print(a)
    # print(a[0]['邮箱'][0:2]=='14')
    # e.search_in_mongodb('atfx-dev-admin','m578A3MGrcR3pRXVU2pA','atfxgm-uat','atfx_ib_links','isDeleted',0,'link',1)
    # e.searchs_for_mongodb('atfx-dev-admin', 'm578A3MGrcR3pRXVU2pA', 'atfxgm-uat', 'atfx_ib_links','isDeleted',0,'currency','markup','leverage','mtGroup','link','spreadType',6,3)
    path=r'D:\code\tylerhub\demo\registration_process\test_excel_data\all_links.xlsx'
    e.save_mongodb_data(path,'atfx-dev-admin','m578A3MGrcR3pRXVU2pA','atfxgm-uat','atfx_ib_links',condition='isDeleted',value=0,
    filed1='link',column1='A',filed2='currency',column2='B',filed3='markup',column3='C',filed4='leverage',column4='D',filed5='mtGroup',column5='E',filed6='spreadType',column6='F',num=6)