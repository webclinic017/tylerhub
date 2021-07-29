"""公共方法及变量释义"""
///
模块：browser_actions.py
公共方法:
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


变量:
browsername:浏览器名称 如Firefox、Chrome
url：访问域名
locator：定位方法及元素值，格式‘定位方法，元素值’如 'css,#kw'
index：下标
timeout:等待时间
step：步长
values：输入的值
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

#############################################################################################
#############################################################################################
模块：other_actions.py 
公共方法:
    log_output(name)                           自定义日志输出
    get_rangenum(n)                            数字与字母组合的随机数
    get_psword_type(N)                         生成N为数字与大小写字母组合的随机数
    get_purerange(n,type)                      数字或者纯字母组合随机数
    get_rangenemail(n)                         随机邮箱
    get_rangephone()                           随机手机号码
    extract_numbers(str)                       提取数字
    random_int(x,y)                            生成x-y之间的单个随机整数


变量:
name:错误日志名称
n:位数
type：随机数类型
N:位数
type:letter or number
str:含有数字的字符串
x,y:整数，x<y


#############################################################################################
#############################################################################################
模块：about_data.py
公共方法：
    openexcel(excelpath,sheetname)              提取excel表格中的数据
    saveainfo(excelpath,values,column,row)      创建存储注册数据的函数，写入已存在的本地文档中
    search_in_mongodb(username,password,database,muster,condition=None,value=None,filed=None,N=0)


变量：
excelpath：文档路径
sheetname：文档sheet名
values：保存进文档的值
column：列
row：行


#############################################################################################
#############################################################################################

模块：verification_code.py
公共方法：
    base64_api(uname,pwd,img)                   图鉴网接口，识别验证码
    time_used(info="used")                      统计某个函数的运行时间
    skip_dependon(depend="")                    跳过某个用例（适用于unittest框架）


变量：
uname：图鉴网账号
pwd：图鉴网密码
img：被识别的验证码图片路径
///