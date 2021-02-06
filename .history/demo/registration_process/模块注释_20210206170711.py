######################################################################
######################################################################
模块说明：
register_method.py 会员中心注册页表单填写方法封装，定位元素在此类中
cp_register.py      调用register_method.py中封装的方法，执行测试用例，
                    调用的方法：country_isuk(),browsertype(),quitdriver(),country_isuk(),get_url(),fill_inform()


模块方法与变量：
register_method.py：
form_operations() 类名，继承基本类Commonweb

方法：
    browsertype(browsername='Chrome')     浏览器驱动类型，默认以谷歌浏览器执行测试用例
    get_url(url,code,column,row)          访问url，根据非空值url/code访问不同域名
    country_isuk(country)                 判断注册国家是否为UK国家
    register_topup()                      去除注册页弹窗
    choose_lg(lang)                       注册页弹窗语言
    fill_inform(lang,fristname,lastname,emali,password,cn_country,en_country)  注册页表单填写
    closedriver()                         关闭浏览器
    quitdriver()                          退出浏览器进程


变量：
browsername:浏览器名称 如Firefox、Chrome
url: 域名
code:邀请码
column:保存数据的本地文档列数
row:保存数据的本地文档行数
country:国家名
lang:语言，EN或者简中
fristname:名字
lastname:姓氏
emali:邮箱
password:密码
cn_country:国家中文名
en_country:国家英文名

------------------------------------------------------------------------------------------------
cp_register.py
register_cp()          类名，继承unittest.TestCase
方法：
    setUp()                 预置条件
    tearDown()              环境恢复
    test_register(data)     执行测试用例

