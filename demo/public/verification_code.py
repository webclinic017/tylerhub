'''
Author: tyler
Date: 2021-05-14 10:11:05
LastEditTime: 2021-06-02 16:35:56
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \tylerhub\demo\public\verification_code.py
'''
import base64
import datetime
import functools
import json
import time
from functools import wraps
from io import BytesIO
from sys import version_info

import requests
from PIL import Image

"""需要在图鉴网注册账号，注册成功后可使用该接口进行图片识别，另外本地需
下载验证码图片截图，将截图路径放进接口参数中,注册地址：http://www.ttshitu.com/register.html"""

def base64_api(uname,pwd,img):
    img = img.convert('RGB')
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    if version_info.major >= 3:
        b64 = str(base64.b64encode(buffered.getvalue()), encoding='utf-8')
    else:
        b64 = str(base64.b64encode(buffered.getvalue()))
    data = {"username": uname, "password": pwd, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""

#统计某个函数的运行时间
def time_used(info="used"):
    """
    注：使用此装饰器时，被修饰的函数最终不能有返回值
    """
    def _time_me(function):
        @functools.wraps(function)
        def _wrapper(*args, **kwargs):
            start = datetime.datetime.now()
            function(*args, **kwargs)
            print ('{} {} {}'.format(function.__name__, info,datetime.datetime.now()-start))
        return _wrapper
    return _time_me


#跳过某个用例
def skip_dependon(depend=""):
    """
    :param depend: 依赖的用例函数名，默认为空
    :return: wraper_func
    """
    def wraper_func(test_func):
        @wraps(test_func)
        def inner_func(self):
            if depend == test_func.__name__:
                raise ValueError("{} cannot depend on itself".format(depend))
            failures = str([fail[0] for fail in self._outcome.result.failures])
            errors = str([error[0] for error in self._outcome.result.errors])
            skipped = str([error[0] for error in self._outcome.result.skipped])
            flag = (depend in failures) or (depend in errors) or (depend in skipped)
            if failures.find(depend) != -1:
                test = unittest.skipIf(flag, "{} failed".format(depend))(test_func)
            elif errors.find(depend) != -1:
                test = unittest.skipIf(flag, "{} error".format(depend))(test_func)
            elif skipped.find(depend) != -1:
                test = unittest.skipIf(flag, "{} skipped".format(depend))(test_func)
            else:
                test = test_func
            return test(self)
        return inner_func
    return wraper_func

#测试
if __name__ == "__main__":
    result = base64_api('tyler','123456',img) #注册的账号，密码，验证码截图路径
