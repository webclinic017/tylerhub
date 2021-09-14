'''
Author: tyler
Date: 2021-09-13 15:25:18
LastEditTime: 2021-09-14 10:56:41
LastEditors: Please set LastEditors
Description: about api
FilePath: \tylerhub\demo\public\api.py
'''
import requests
import json

class Api(object):

    """
    封装简单的api接口
    """
    def api_get(self,host,path=None,headers=None,params=None):
        """
        :param host:地址
        :param path:路径
        :param headers:请求头
        :param params:参数
        """
        self.url=''.join([host,path])
        self.r=requests.get(self.url,headers=headers,params=params)
        return self.r

    def api_post(self,host,path=None,headers=None,params=None,data:dict=None,json=None):
        """
        :param host:地址
        :param path:路径
        :param headers:请求头
        :param params:参数
        :param data:字典
        :param json:json格式参数
        """
        self.url=''.join([host,path])
        self.r=requests.post(self.url,headers=headers,params=params,data=data,json=json)
        return self.r



if __name__=='__main__':
    re=Api()
    # print(eval(re.api_get("http://httpbin.org/", "get",{"User-Agent":"test request headers"}).text)['headers']['User-Agent'])
    print(re.api_post("http://httpbin.org/", 'post',headers = {"User-Agent":"test request headers"},data={'key1':'value1','key2':'value2'}).text)
