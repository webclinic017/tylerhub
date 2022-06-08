'''
Author: tyler
Date: 2021-08-18 16:08:10
LastEditTime: 2022-06-07 10:30:47
LastEditors: Tyler96-QA 1718459369@qq.com
Description: Read configuration file
FilePath: \tylerhub\demo\public\read_dataconfig.py
'''
import configparser
import os

class ReadConfig():

    """
    读取配置文件数据,配置文件路径默认为当前文件父级目录下的data_config.ini文件
    如需读取其他配置文件路径，请将参数传入类中
    """
    def __init__(self,filepath=None):

        if filepath:
            self.configpath=filepath
        else:
            self.configpath=os.path.join(os.path.dirname(os.path.abspath(__file__)),'config\config.ini')
        
        self.config=configparser.RawConfigParser()
        self.config.read(self.configpath,encoding='utf-8')#读取配置文件

    def get_option(self,section,index=None):
        """
        获取section下的option值，列表返回，index值具体取第几项
        """
        #判断该section是否存在
        if self.config.has_section(section):
            if index:
                return self.config.options(section)[index]
            else:
                return self.config.options(section)
        else:
            print('请检查配置文件是否存在该section节点')

    def get_value(self,section,opthon)->str:
        """
        获取某个section节点下option的具体值,返回字符串
        """
        if self.config.has_section(section):
            return self.config.get(section,opthon)
        else:
            print('请检查配置文件是否存在该section节点')


    def get_valueList(self,section,opthon)->list:
        """
        获取某个section节点下option的具体值，返回列表
        """
        if self.config.has_section(section):
            return list(i for i in (self.config.get(section,opthon)).split(','))
        else:
            print('请检查配置文件是否存在该section节点')

    
    def get_int(self,section,opthon):
        """
        获取指定section节点下的opthon值，并以int类型返回
        """
        if self.config.has_section(section):
            return self.config.getint(section,opthon)
        else:
            print('请检查配置文件是否存在该section节点')

    def modify(self,section,options,value):
        if self.config.has_section(section):
            fb=open(self.configpath,'w',encoding='utf-8')
            self.config.set(section, options, value)
            #保存
            self.config.write(fb)
            fb.close()
        else:
            print('请检查配置文件是否存在该section节点')


if __name__=='__main__':
    conFig=ReadConfig()
    conFig.modify('login_cpToken', 'x-token', '中国')
    # print(conFig.get_option('mysql',0))
    print(conFig.get_value('ip','ip'))
    # print(type(conFig.get_int('ip','ip')))