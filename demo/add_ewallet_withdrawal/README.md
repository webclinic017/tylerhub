<!--
 * @Author: tyler
 * @Date: 2021-09-07 16:59:11
 * @LastEditTime: 2021-09-07 17:27:38
 * @LastEditors: Please set LastEditors
 * @Description: IModule notes
 * @FilePath: \tylerhub\demo\add_ewallet_withdrawal\README.md
-->

# 模块注释 :ok_woman:

## 环境依赖
***python3.6及以上版本***
### *部署步骤*：:blush:
    1.python3.6及以上版本下载
    2.必需第三方模块：selenium；allure-pytest；image；pymongo；pytest；selenium；WMI；xlrd(指定1.2.0版本)；allure
    3.alluer环境配置
***
## 模块功能 
**模块**         |      **功能**  
   ------------- | -------------  
location.location_of_add_ewallet.py          |    页面操作   
action_bin.test_add_ewallet.py   | 用例执行 
test_data       | *excel* 测试用例存放 
report    | 存放测试报告
log        |          存放日志         |

***

**脚本逻辑** 

    调用location_of_add_ewallet.py模块中方法，执行测试用例：登录bos判断当前账号是否满足居住国条件（非中国），登录cp，判断当前账号是否存在电子钱包出金方式，若存在，再判断某个渠道电子钱包出金方式是否超过三条，未超过则添加至三条获取提示语，并在出金模块验证是否可用，验证是否成功添加进数据库；若不存在，则默认添加skill渠道至三条，并获取提示语及验证数据库

**用例预置条件** 

    用例数据必须是kyc通过，且能出金的账号


## 命名方式 建议使用如下命名方式哦:smiley: 
    模块名：小写字母，单词间用_分割  about_data.py
    类名：首字母大写
    普通变量：小写字母，单词间用_分割 email_list;无下划线第二个单词大写开头（驼峰命名法）例：readConfig
    私有函数：以__双下划线开头小写字母，单词之间用分割  外部访问，引用会报错
    普通函数：小写字母，单词之间用_分割 get_rangenemail
*注释*：

_单下划线开头：弱“内部使用”标识，如：”from M import *”，将不导入所有以下划线开头的对象，包括包、模块、成员 ；

__双下划线开头：模块内的成员，表示私有成员，外部无法直接调用 

包和模块：模块应该使用尽可能短的、全小写命名，可以在模块命名时使用下划线以增强可读性。同样包的命名也应该是这样的，虽然其并不鼓励下划线

***
## 模块方法及变量释义
### 模块:
***[location_of_add_ewallet.py :](https://github.com/Tyler96-QA/tylerhub/blob/main/demo/add_ewallet_withdrawal/location/location_of_add_ewallet.py)*** 

*方法*

    broswertype(broswername)                                        赋值对象driver
    get_url(self,environment,lang='CN')                             cp/bos登录页
    remove_login_topup()                                            判断ip去除cp登录页弹窗
    logincp(username,password)                                      登录cp
    logoutcp()                                                      登出cp
    login_bos()                                                     登录bos  
    details_page(account)                                           账号详情页     
    get_live_country()                                              获取该账号居住国
    get_demoaccount(account)                                        数据库查询获取新开demo账号
    is_ewallet_morethan_three()                                     会员中心判断该账号电子钱包出金方式是否超过三条
    get_verify_code()                                               获取验证码
    get_tips()                                                      获取电子钱包超过三条后再次添加后的提示
    is_ewallet_available()                                          判断新增出金方式会员中心是否可用
    search_mongodb_ewallet()                                        查询数据库，判断新增电子钱包出金方式是否添加进库中
    screenshots_path()                                              截图,返回截图路径
    closebrowser()                                                  关闭当前页面
    quitbrowser()                                                   退出浏览器进程

*变量*

    broswername                                                     浏览器驱动，默认谷歌
    environment                                                     测试环境，sit/uat
    username                                                        登录用户名，bos读取配置文件中用户，cp读取测试文档中用户
    password                                                        登录密码，bos读取配置文件中密码，cp读取测试文档中密码
    account                                                         主账号
    tdAccount                                                       demo账号
    name                                                            截图名
***

### 模块:
***[test_add_ewallet.py:](https://github.com/Tyler96-QA/tylerhub/blob/main/demo/add_ewallet_withdrawal/action_bin/test_add_ewallet.py)*** 

*方法*

    setup_class()                                                   预置条件
    teardown()                                                      环境恢复
    test_ewallet()                                                  用例执行

*变量*

    testdata                                                        参数化用例