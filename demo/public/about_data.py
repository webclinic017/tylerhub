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
            if condition and value !=None:
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


#测试
if __name__=='__main__':
    e=exceldata()
    # e.openexcel(r'D:\code\tylerhub\demo\registration_process\test_excel_data\account_number.xlsx','Sheet1')
    # a=e.dict_data()
    # print(a)
    # print(a[0]['邮箱'][0:2]=='14')
    e.search_in_mongodb('atfx-dev-admin','m578A3MGrcR3pRXVU2pA','atfxgm-uat','atfx_ib_links','mtName','mt4','accountNumber')
