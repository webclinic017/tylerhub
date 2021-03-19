import json
import requests
import base64
from io import BytesIO
from PIL import Image
from sys import version_info
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
def time_me(info="used"):

    def _time_me(fn):
        @functools.wraps(fn)
        def _wrapper(*args, **kwargs):
            start = time.perf_counter()
            fn(*args, **kwargs)
            print ("%s %s %s" % (fn.__name__, info, time.perf_counter() - start), "second")
        return _wrapper
    return _time_me




#测试
if __name__ == "__main__":
    result = base64_api('tyler','123456',img) #注册的账号，密码，验证码截图路径
