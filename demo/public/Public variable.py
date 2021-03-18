"""公共方法及变量释义"""
///
browser_actions.py 模块:
公共方法:
    open_browser(browsername='Chrome')       打开浏览器，默认为谷歌浏览器
    open_web(url)                            访问url
    find_element(locator,index=0)            定位页面元素(无论是否唯一)，默认下标为0
    is_element_isdisplayed(locator,index=0)  判断页面元素是否存在，若不存在，输出日志
    web_input(locator,values,index=0)        页面输入
    web_input(locator,index=0)               页面清空
    web_click(locator,index=0)               页面点击
    double_click(locator,index=0)            页面双击
    refresh_f5()                             强制刷新 
    suspension(locator,index=0)              鼠标悬浮
    get_screenpict(filename)                 截图当前页面
    close_browser()                          关闭浏览器
    quit_browser()                           退出浏览器进程
    display_findelement(element)             显示等待方法
    switch_windows(n)                        切换窗口
    switch_iframe(locator,index=0)           切换表单
    uploadimg()        

变量:
browsername:浏览器名称 如Firefox、Chrome
url：访问域名
locator：定位方法及元素值，格式‘定位方法，元素值’如 'css,#kw'
index：下标
values：输入的值
filename：文件夹名称
element：css定位方法的元素值
name:截图图片名称
n：下标

#############################################################################################
#############################################################################################
other_actions.py 模块:
公共方法:
    log_output(name)                           自定义日志输出
    get_rangenum(n)                            数字与字母组合的随机数
    get_purerange(n,type)                      数字或者纯字母组合随机数
    get_rangenemail(n)                         随机邮箱
    get_rangephone()                           随机手机号码


变量:
name:错误日志名称
n:位数
type：随机数类型

#############################################################################################
#############################################################################################
///