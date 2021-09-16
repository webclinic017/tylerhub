<!--
 * @Author: tyler
 * @Date: 2021-09-07 16:59:11
 * @LastEditTime: 2021-09-16 10:14:29
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
location.location_of_neteller_withdrawal.py          |    页面操作   
action_bin.test_neteller_withdrawal.py   | 用例执行 
test_data       | *excel* 测试用例存放 
report    | 存放测试报告
log        |          存放日志         |

***

**脚本逻辑** 

    调用location_of_neteller_withdrawal.py模块中方法，执行测试用例：登录cp判断当前账号是否存在neteller出金方式，若不存在则新增一条neteller出金方式，截图；判断出金交易账号余额和可出金金额是否为0，若为0则跳过用例；若出金金额大于余额，默认出金余额的1/2；会员中心出金，并调用接口查询出金手续费，断言会员中心手续费与接口返回手续费是否一致；bos审核出金，保存cp，bos，mongodb数据库出金创建时间到本地

**用例预置条件** 

    用例数据必须是kyc通过，且能出金的账号


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
***[location_of_neteller_withdrawal.py :](https://github.com/Tyler96-QA/tylerhub/blob/main/demo/neteller_withdrawal/location/location_of_neteller_withdrawal.py)*** 

*方法*

    broswertype(broswername)                                        赋值对象driver
    get_url(self,environment,lang='CN')                             cp/bos登录页
    remove_login_topup()                                            判断ip去除cp登录页弹窗
    logincp(username,password)                                      登录cp
    logoutcp()                                                      登出cp
    login_bos()                                                     登录bos  
    details_page(account)                                           账号详情页     
    where_is_tradeaccount_cp(tradeaccount)                          获取交易账号在cp账号列表位置
    get_tradeaccount_balance(tradeaccount)                          获取交易账号余额
    details_page(account)                                           进入账号详情页
    is_balance_nil(tradeaccount)                                    判断交易账号余额是否为0
    is_exist_neteller()                                             判断当前账号是否存在neteller出金方式
    add_neteller(account)                                           添加neteller出金方式
    use_neteller_withdrawal(account,tradeaccount,username,amount,excelpath,column,row) 出金,并判断出金交易账号余额是否大于出金金额
    action_neteller(account,tradeaccount,username,amount,excelpath,column,row)   出金
    api_get_charge(account,tradeaccount,username,amount)            调用接口，获取当前出金手续费
    review_withdrawal(tradeaccount,excelpath,column,row)            bos审核出金
    check_cp(tradeaccount,excelpath,column1,column2,row)            会员中心查看
    screenshots_path(name,filename='picture')                       截图,返回截图路径
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
***[test_neteller_withdrawal.py:](https://github.com/Tyler96-QA/tylerhub/blob/main/demo/neteller_withdrawal/action_bin/test_neteller_withdrawal.py)*** 

*方法*

    setup_class()                                                   预置条件
    teardown()                                                      环境恢复
    test_neteller()                                                 用例执行

*变量*

    testdata                                                        参数化用例