<!--
 * @Author: tyler
 * @Date: 2021-05-13 10:43:00
 * @LastEditTime: 2021-08-05 00:30:11
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \tylerhub\demo\public\README.mdd
-->
# 公共模块注释 请放心食用 :ok_woman:

## 环境依赖
***python3.6及以上版本***
### *部署步骤*：:blush:
    1.python3.6及以上版本下载
    2.必需第三方模块：selenium；allure-pytest；BeautifulReport；ddt；image；pymongo；cx_Oracle；PyMySQL；pytest；selenium；WMI；xlrd(指定1.2.0版本)；allure
    3.alluer环境配置
***
## 模块功能 
**模块**         |      **功能**  
   ------------- | -------------  
config          |    配置文件    
browser_actions.py   | selenium的二次封装，例页面点击，页面输入，截图等  
about_data.py       | *excel* 数据读取与存储，mongodb，mysql等数据库的连接 
ommon_method.py    | 公用方法，登录登出等 
handlelog.py        |          日志封装，低于debug级别的日志仅输出到控制台         |
other_actions.py | 生成随机数据，提取指定格式字符串等
read_dataconfig.py  | 读取配置文件
verification_code.py | 页面验证识别，统计方法运行时间等
***
## 命名方式 建议用如下命名方式哦:smiley: 
    模块名：小写字母，单词间用_分割  about_data.py
    类名：首字母大写
    普通变量：小写字母，单词间用_分割 email_list
    私有函数：以__双下划线开头小写字母，单词之间用分割  外部访问，引用会报错
    普通函数：小写字母，单词之间用_分割 get_rangenemail
*注释*：

_单下划线开头：弱“内部使用”标识，如：”from M import *”，将不导入所有以下划线开头的对象，包括包、模块、成员 ；

__双下划线开头：模块内的成员，表示私有成员，外部无法直接调用 

包和模块：模块应该使用尽可能短的、全小写命名，可以在模块命名时使用下划线以增强可读性。同样包的命名也应该是这样的，虽然其并不鼓励下划线

***
## 公共模块方法及变量释义
### 模块:
***[browser_actions.py:](https://github.com/Tyler96-QA/tylerhub/blob/main/demo/public/about_data.py)*** 

*公共方法*

    open_browser(browsername='Chrome')       打开浏览器，默认为谷歌浏览器
    open_web(url)                            访问url
    find_element(locator,index=0)            定位页面元素(无论是否唯一)，默认下标为0
    get_lenofelement(locator)                获取页面元素个数
    display_find_element(locator,index=0)    显示等待查找的元素是否唯一，不唯一取第n个值，唯一取唯一值
    get_attributes(locator,element,index=0)  显示等待获取页面某个元素的属性
    element_is_visible(locator,index=0)      判断元素是否可见,返回布尔值
    ele_is_displayed(locator,timeout,step=0.5) 设置等待时间查找页面元素是否可见(是否加载到了dom树中)
    is_element_selected(locator,index=0)     判断某个元素是否被选中，返回布尔值
    web_input(locator,values,index=0)        输入操作
    display_input(locator,values,index=0)    显示等待输入
    web_clear(locator,index=0)               清空输入框
    get_text(locator,index=0)                获取页面文本
    display_get_text(locator,index=0)        显示等待获取页面文本
    web_click(locator,index=0)               点击操作
    display_click(locator,index=0)           显示等待点击
    doubleclick(locator,index=0)             双击
    display_doubleclick(locator,index=0)     显示等待双击
    refresh_f5()                             强制刷新
    general_refresh_()                       刷新
    suspension(locator,index=0)              鼠标悬浮
    display_suspension(locator,index=0)      显示等待-鼠标悬停
    right_click(locator,index=0)             右键点击
    keyboard_operation(locator,keys,index=0) 其他键盘操作(针对搜索框/输入框)
    right_click_link(locator,index=0)        右键在新窗口打开链接打开链接
    get_screenpict(name,filename='picture')  截图,自定义保存截图的文件夹名称
    switch_windows(n)                        切换窗口,n为下标
    title()                                  获取当前页面的title
    switch_iframe(locator,index=0)           切换表单页
    upload_img(exe_path,pic_path)            上传图片
    js_openwindows(url)                      JS新开窗口
    js_scroll(site)                          JS控制滚动条
    js_scroll_inline(type,element,site,index=0) JS处理内嵌滚动条滚动
    element_focus(locator,index=0)           元素聚焦，移动页面至指定元素位置
    fixed_point_image(name,filename,locator,index=0) 截取屏幕，定点截图
    discern_code(username,psword,name,filename,locator,index=0) 调用三方接口，读取验证码
    close_browser()                           关闭当前页
    quit_browser()                            退出浏览器进程

*变量*:
    
    browsername:浏览器名称 如Firefox、Chrome
    url：访问域名
    locator：定位方法及元素值，格式‘定位方法，元素值’如 'css,#kw'
    index：下标
    timeout:等待时间
    step：步长
    values：输入值
    name:截图名称
    filename：文件夹名称
    exe_path：程序路径
    pic_path：图片路径
    type:id or calss
    site:down or top
    element：css定位方法的元素值
    username:图鉴网用户名
    psword：图鉴网密码
    n：下标
***
***[other_actions.py:](https://github.com/Tyler96-QA/tylerhub/blob/main/demo/public/other_actions.py)***

*公共方法*

    get_rangenum(n)                            数字与字母组合的随机数
    get_psword_type(N)                         生成N为数字与大小写字母组合的随机数
    get_purerange(n,type)                      数字或者纯字母组合随机数
    get_rangenemail(n)                         随机邮箱
    get_rangephone()                           随机手机号码
    extract_numbers(str)                       提取数字
    random_int(x,y)                            生成x-y之间的单个随机整数

*变量*

    n:位数
    type：随机数类型
    N:位数
    type:letter or number
    str:含有数字的字符串
    x,y:整数，x<y
***
***[about_data.py:](https://github.com/Tyler96-QA/tylerhub/blob/main/demo/public/about_data.py)***

*公共方法*

    openexcel(excelpath,sheetname)              提取excel表格中的数据
    saveainfo(excelpath,values,column,row)      创建存储注册数据的函数，写入已存在的本地文档中
    search_in_mongodb(username,password,database,muster,condition=None,value=None,filed=None,N=0)                  mongodb数据库查询
    serach_in_oracle                            oracle数据库查询

*变量*

    excelpath：文档路径
    sheetname：文档sheet名
    values：保存进文档的值
    column：列
    row：行
***
***[verification_code.py:](https://github.com/Tyler96-QA/tylerhub/blob/main/demo/public/verification_code.py)***

*公共方法*

    Base64_api(uname,pwd,img)                   图鉴网接口，识别验证码
    time_used(info="used")                      统计某个函数的运行时间
    skip_dependon(depend="")                    跳过某个用例（适用于unittest框架）

*变量*

    uname：图鉴网账号
    pwd：图鉴网密码
    img：被识别的验证码图片路径
***  
 ***[handlelog.py:](https://github.com/Tyler96-QA/tylerhub/blob/main/demo/public/handlelog.py)***  
    
 *公共方法*

    my_logger(name=read.get_value('log','name')) 输出日志到控制台及日志文件中,只有高于WARN级别的日志才会输出到日志文件中，其他级别日志仅输出到控制台

*变量*

    name：日志名称
 ***  
  ***[read_dataconfig.py:](https://github.com/Tyler96-QA/tylerhub/blob/main/demo/public/read_dataconfig.py)***     
  
  *公共方法*
  
    get_option(section,index=None)            获取section下的option值，列表返回，index值具体取第几项
    get_value(section,opthon)                 获取某个section节点下option的具体值
     
 *变量*
 
    section：节点
    opthon：节点中的key
    
