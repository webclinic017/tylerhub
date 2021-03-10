######################################################################
######################################################################
注册：

模块说明：
register_method.py 会员中心注册页表单填写方法封装，定位元素在此类中
cp_register.py      关键字驱动，调用创建的方法：
                    country_isuk(),browsertype(),quitdriver(),country_isuk(),get_url(),fill_inform()


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
    submit()                              提交注册页表单
    fistcp_top()                          去除首次登录会员中心弹窗
    register_success()                    登录成功后获取文本

"""
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
"""
------------------------------------------------------------------------------------------------
cp_register.py
register_cp()          类名，继承unittest.TestCase
方法：
    setUp()                 预置条件
    tearDown()              环境恢复
    test_register(data)     执行测试用例
        关键字驱动：country_isuk();closedriver();get_url();fill_inform()


###################################################################################
###################################################################################
KYC认证流程：

kyc_method.py  kyc流程方法封装   
kyc_operating.py  关键字驱动kyc_method.py中的方法

模块方法与变量：
kyc_method.py ：
类：kyc_approve(),继承基本类Commonweb
方法：
browsertype(browsername='Chrome')           默认谷歌浏览器执行用例
login_topup()                               去除会员中心登录页弹窗
cp_lang(lang)                               选择会员中心登录页语言                        
bos_lang(lang)                              选择bos登录页语言
loginweb(lang)                              访问会员中心及BOS登录页,选择页面语言
login_cp(username,psword)                   登录会员中心
fisrtcp_top()                               去除首次登录会员中心的弹窗
get_account_()                              获取登录成功后的主账号
is_rebate_type()                            判断是否为返佣账号，如是，点击返佣申请表格
logout_cp()                                 登出会员中心
login_bos(username,psword)                  登录bos
verification_emali()                        验证邮箱
upload_ID_photo()                           上传证件照
choose_data_gender()                        随机选择出生日期与性别
submit()                                    提交表单
get_emailcode_()                            获取邮箱验证码
get_on_kyc()                                KYC认证表单操作
clearaccount()                              清空主账号搜索条件
get_kyc_success()                           KYC成功后的文本
closedriver()                               关闭页面 
quitdriver()                                退出浏览器

"""
变量：
lang  页面语言，EN;英语 or CN;简中
username  登录用户名
psword    登录密码
"""
------------------------------------------------------------------------------------------------
kyc_operating.py
类：kyc_actions() 继承unittest.TestCase
方法：
    setUp()                 预置条件
    tearDown()              环境恢复
    test_kyc(data)     执行测试用例
        关键字驱动：loginweb();login_bos();quitdriver();logout_cp();clearaccount();
        login_topup();login_cp();fisrtcp_top();get_account_();get_on_kyc();get_kyc_success()


################################################################################################
################################################################################################

初审流程：
preliminary_review.py  初审方法封装
review.py       关键字驱动preliminary_review.py中的方法

模块方法与变量：
preliminary_review.py：
review_actions(),继承基本类Commonweb
方法：
browsertype(browsername='Chrome')                   默认浏览器类型
login_bos(username,psword,lang='CN')                登录bos
bos_lang(lang='CN')                                 选择bos登录页语言
review_operation(account)                           主账号查询
clear_serach()                                      清空主账号搜索条件
get_success_text()                                  获取初审成功后的文本
ibtype()                                            代理代码代理链接等操作
get_img(name,filename='review_failed')              截图
closerweb()                                         关闭页面
quitbrowser()                                       退出浏览器

"""
变量：
username：登录用户名
psword：登录密码
lang:页面语言：EN;英语 or CN;简中
name:截图名称
filename：保存截图文件名
"""
------------------------------------------------------------------------------------------------
review.py
review_account() 继承unittest.TestCase
方法：
    setUp()                 预置条件
    tearDown()              环境恢复
    test_kyc(data)     执行测试用例
        关键字驱动：login_bos();quitdriver();logout_cp();clear_serach();review_operation()
        
################################################################################################
################################################################################################