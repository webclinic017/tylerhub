'''
Author: tyler
Date: 2021-05-14 10:11:05
LastEditTime: 2022-05-17 16:17:24
LastEditors: Tyler96-QA 1718459369@qq.com
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



#统计某个函数的运行时间
def use_time(function):
  @wraps(function)
  def function_timer(*args, **kwargs):
    t0 = time.time()
    result = function(*args, **kwargs)
    t1 = time.time()
    print ("该函数 {} 运行 : {} seconds" .format(function.__name__, str(t1-t0)))
    return result
  return function_timer


"""需要在图鉴网注册账号，注册成功后可使用该接口进行图片识别，另外本地需
下载验证码图片截图，将截图路径放进接口参数中,注册地址：http://www.ttshitu.com/register.html"""
@use_time
def Base64_api(uname,pwd,img,typeid=3):
    #古老版本：需打开验证图片
    # img = img.convert('RGB')
    # buffered = BytesIO()
    # img.save(buffered, format="JPEG")
    # if version_info.major >= 3:
    #     b64 = str(base64.b64encode(buffered.getvalue()), encoding='utf-8')
    # else:
    #     b64 = str(base64.b64encode(buffered.getvalue()))
    # data = {"username": uname, "password": pwd, "image": b64}
    # result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    # if result['success']:
    #     return result["data"]["result"]
    # else:
    #     return result["message"]
    # return ""

    #新版本：传入验证码图片路径即可；注意：调用此方法时不要随意移动窗口
    #typeid说明：
    # 一、图片文字类型(默认 3 数英混合)：
    # 1 : 纯数字
    # 1001：纯数字2
    # 2 : 纯英文
    # 1002：纯英文2
    # 3 : 数英混合
    # 1003：数英混合2
    #  4 : 闪动GIF
    # 7 : 无感学习(独家)
    # 11 : 计算题
    # 1005:  快速计算题
    # 16 : 汉字
    # 32 : 通用文字识别(证件、单据)
    # 66:  问答题
    # 49 :recaptcha图片识别
    # 二、图片旋转角度类型：
    # 29 :  旋转类型
    #
    # 三、图片坐标点选类型：
    # 19 :  1个坐标
    # 20 :  3个坐标
    # 21 :  3 ~ 5个坐标
    # 22 :  5 ~ 8个坐标
    # 27 :  1 ~ 4个坐标
    # 48 : 轨迹类型
    #
    # 四、缺口识别
    # 18 : 缺口识别（需要2张图 一张目标图一张缺口图）
    # 33 : 单缺口识别（返回X轴坐标 只需要1张图）
    # 五、拼图识别
    # 53：拼图识别
    with open(img, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""



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
    result = Base64_api('tyler','123456',r'D:\code\tylerhub\demo\public\jietu\Screenshot2022-05-17-15.53.12.png')
    print(result)