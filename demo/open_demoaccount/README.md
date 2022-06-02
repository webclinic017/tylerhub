<!--
 * @Author: tyler
 * @Date: 2021-08-26 18:22:45
 * @LastEditTime: 2021-09-07 17:11:46
 * @LastEditors: Please set LastEditors
 * @Description: Module notes
 * @FilePath: \tylerhub\demo\cl_open_demoaccount\README.md
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
location.location_of_cl_opendome.py          |    页面操作   
action_bin.test_cl_opendemo.py   | 用例执行 
test_data       | *excel* 测试用例存放 
report    | 存放测试报告
log        |          存放日志         |

***

**脚本逻辑** 

    调用location_of_cl_opendome.py模块中方法，执行测试用例：登录cp，创建demo账号，查询数据库，bos获取新建demo账号组别点差加点等信息与数据库比对；CP修改
    杠杆后查询数据库该demo账号杠杆是否更新，是否与修改杠杆一致

**用例预置条件** 
    用例数据必须是kyc通过后的账号
    
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
***[location_of_cl_opendome.py :](https://github.com/Tyler96-QA/tylerhub/blob/main/demo/cl_open_demoaccount/action_bin/test_cl_opendemo.py)*** 

*方法*

    broswertype(broswername)                                        赋值对象driver
    get_url(self,environment,lang='CN')                             cp/bos登录页
    remove_login_topup()                                            判断ip去除cp登录页弹窗
    logincp(username,password)                                      登录cp
    logoutcp()                                                      登出cp
    login_bos()                                                     登录bos  
    details_page(account)                                           账号详情页     
    creat_demoaccount()                                             创建demo账号
    get_demoaccount(account)                                        数据库查询获取新开demo账号
    get_demo_group()                                                bos获取demo账号组别
    get_demo_lever()                                                bos获取demo账号杠杆
    get_demo_spreadtype()                                           bos获取demo账号点差类型
    get_demo_markup()                                               bos获取demo账号加点
    search_mongodb_demoinfo()                                       数据库查询demo账号信息
    where_demo_incp()                                               新开demo账号在cp位置
    revise_demolever()                                              cp修改demo账号杠杆
    revise_mongolever()                                             数据库查询修改后杠杆
    closebrowser()                                                  关闭当前页面
    quitbrowser()                                                   退出浏览器进程

*变量*

    broswername                                                     浏览器驱动，默认谷歌
    environment                                                     测试环境，sit/uat
    username                                                        登录用户名，bos读取配置文件中用户，cp读取测试文档中用户
    password                                                        登录密码，bos读取配置文件中密码，cp读取测试文档中密码
    account                                                         主账号
    tdAccount                                                       demo账号
***

### 模块:
***[test_cl_opendemo.py:](https://github.com/Tyler96-QA/tylerhub/blob/main/demo/cl_open_demoaccount/action_bin/test_cl_opendemo.py)*** 

*方法*

    setup_class()                                                   预置条件
    teardown()                                                      环境恢复
    test_execution_demo()                                           用例执行

*变量*

    testdata                                                        参数化用例