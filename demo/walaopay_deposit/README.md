<!--
 * @Author: tyler
 * @Date: 2021-09-07 16:59:11
 * @LastEditTime: 2021-09-24 11:46:14
 * @LastEditors: Please set LastEditors
 * @Description: IModule notes
 * @FilePath: \tylerhub\demo\add_ewallet_withdrawal\README.md
-->

# 模块注释 :ok_woman:

## 环境依赖
***python3.6及以上版本***
### *部署步骤*：:blush:
    1.python3.6及以上版本下载
    2.必需第三方模块：selenium；allure-pytest；image；pymongo；pytest；selenium；WMI；xlrd(指定1.2.0版本)；allure等
    3.alluer环境配置
***
## 模块功能 
**模块**         |      **功能**  
   ------------- | -------------  
location.location_of_walaopay_deposit.py          |    页面操作   
action_bin.test_walaopay_deposit.py   | 用例执行 
test_data       | *excel* 测试用例存放 
report    | 存放测试报告
log        |          存放日志         |

***

**脚本逻辑** 

    调用location_of_walaopay_deposit.py模块中方法，执行测试用例。预置条件：判断walaopay入金方式是否开启，获取出金账号居住国家，判断该国家是否存在walaopay入金方式。若不存在，则将该国家添加进walaopay入金国家列表中，登录会员中心入金最低最高金额，查询汇率，并与数据库入金汇率对比；登录bos审核入金，获取入金前后交易账号余额

**用例预置条件** 

    用例数据必须是kyc通过，且能入金的账号


## 命名方式 建议使用如下命名方式:smiley: 
    模块名：小写字母，单词间用_分割  about_data.py
    类名：首字母大写
    普通变量：小写字母，单词间用_分割 email_list;无下划线第二个单词大写开头（驼峰命名法）例：readConfig
    私有函数：以__双下划线开头小写字母，单词之间_用分割  外部访问，引用会报错
    普通函数：小写字母，单词之间用_分割 get_rangenemail
*注释*：

_单下划线开头：弱“内部使用”标识，如：”from M import *”，将不导入所有以下划线开头的对象，包括包、模块、成员 ；

__双下划线开头：模块内的成员，表示私有成员，外部无法直接调用 

包和模块：模块应该使用尽可能短的、全小写命名，可以在模块命名时使用下划线以增强可读性。同样包的命名也应该是这样的，虽然其并不鼓励下划线

***
## 模块方法及变量释义
### 模块:
***[location_of_walaopay_deposit.py :](https://github.com/Tyler96-QA/tylerhub/blob/main/demo/walaopay_deposit/location/location_of_walaopay_deposit.py)*** 

*方法*

    broswertype(broswername)                                        赋值对象driver
    get_url(self,environment,lang='CN')                             cp/bos登录页
    remove_login_topup()                                            判断ip去除cp登录页弹窗
    logincp(username,password)                                      登录cp
    logoutcp()                                                      登出cp
    login_bos(username,password)                                    登录bos  
    details_page(account)                                           账号详情页     
    where_is_tradeaccount_cp(tradeaccount)                          获取交易账号在cp账号列表位置
    get_tradeaccount_balance(tradeaccount)                          获取交易账号余额
    details_page(account)                                           进入账号详情页
    new_driver(environment,username,password,lang='CN')             新开浏览器进程登录bos
    get_live_country()                                              获取该账号居住国家
    is_have_walaopay(account)                                       进入账号详情页，获取账号国家，并判断该账号是否存在walaopay入金方式
    get_highestAndlowest(tradeaccount,excelpath,column,row)         获取WalaoPay MYR入金渠道最低最高入金金额
    get_mongodb_charge()                                            数据库查询入金汇率
    lowest_deposit(tradeaccount)                                    最低金额入金
    highest_deposit(tradeaccount)                                   最高金额入金
    upload_certificate()                                            上传入金凭证
    bos_verify(tradeaccount)                                        bos入金审核
    after_deposti(tradeaccount,excelpath,column,row)                获取入金成功后，交易账号余额
    closebrowser()                                                  关闭当前页面
    quitbrowser()                                                   退出浏览器进程

*变量*

    broswername                                                     浏览器驱动，默认谷歌
    environment                                                     测试环境，sit/uat
    username                                                        登录用户名，bos读取配置文件中用户，cp读取测试文档中用户
    password                                                        登录密码，bos读取配置文件中密码，cp读取测试文档中密码
    account                                                         主账号
    tradeaccount                                                    交易账号
    name                                                            截图名
    amount                                                          出金金额
    column                                                          列
    row                                                             行
***

### 模块:
***[test_walaopay_deposti.py:](https://github.com/Tyler96-QA/tylerhub/blob/main/demo/walaopay_deposit/action_bin/test_walaopay_deposti.py)*** 

*方法*

    setup_class()                                                   预置条件
    teardown()                                                      环境恢复
    test_walaopay(data)                                                 用例执行

*变量*

    testdata                                                        参数化用例