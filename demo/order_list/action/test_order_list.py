'''
Author: tyler
Date: 2021-10-20 10:30:09
LastEditTime: 2021-11-18 18:36:24
LastEditors: Please set LastEditors
Description: Execute testcase
FilePath: \tylerhub\demo\order_list\action\test_order_list.py
'''
import pytest
import os
import allure
import sys
import pytest_check as check
path_public=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'public')
sys.path.append(path_public)
path_project=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_project+r'\location')
from about_data import Aboutdata
from read_dataconfig import ReadConfig
from location_of_order_list import Location_of_order_list


class Test_verify_order_list(object):

    global verifyOrder,conFig,dealData,testdata,excelpath
    verifyOrder=Location_of_order_list()
    conFig=ReadConfig()
    dealData=Aboutdata()

    #读取测试数据
    excelpath=os.path.join(path_project,r'test_data\search_condition.xlsx')
    rows=dealData.openexcel(excelpath,'Sheet1')
    testdata=dealData.dict_data()

    def setup_class(self):
        #默认谷歌浏览器打开
        verifyOrder.broswertype()
        #cp，bos登录页
        verifyOrder.get_url('sit',conFig.get_value('bos_login', 'username'),conFig.get_value('bos_login', 'password'))

    def teardown(self):
        if self.data_index==testdata.index(testdata[-1]):
            verifyOrder.quitbrowser()
        else:
            verifyOrder.closebrowser()
        #删除下载的文件
        os.remove(os.path.join(os.path.join(path_project,'test_data'),verifyOrder.openOrder_excel))
        os.remove(os.path.join(os.path.join(path_project,'test_data'),verifyOrder.closeOrder_excel))
        os.remove(os.path.join(os.path.join(path_project,'test_data'),'copy_openOrder.txt'))
        os.remove(os.path.join(os.path.join(path_project,'test_data'),'copy_openOrder.xlsx'))
        os.remove(os.path.join(os.path.join(path_project,'test_data'),'copy_closeOrder.txt'))
        os.remove(os.path.join(os.path.join(path_project,'test_data'),'copy_closeOrder.xlsx'))




    @allure.feature('查询已平仓未平仓订单列表')
    @allure.story('用例执行')
    @allure.description('读取测试文档数据，执行用例')
    @pytest.mark.parametrize('data',testdata)
    def test_orderList(self,data):

        print('当前查询账号：{}'.format(int(data['主账号'])))
        
        with allure.step('获取当前测试数据下标'):
            self.data_index=testdata.index(data)
        
        with allure.step('bos登录cp'):
            verifyOrder.logincp(int(data['主账号']))

        with allure.step('查询交易账号所有平仓未平仓订单'):
            verifyOrder.search_order_len(int(data['交易账号']))
        
        #判断交易账号是否存在未平仓订单
        with allure.step('判断交易账号是否存在未平仓订单'):
            if verifyOrder.open_order_len!=0:
                with allure.step('交易账号存在未平仓订单{}条'.format(verifyOrder.open_order_len)):
                    with allure.step('断言导出数据是否与页面一致'):
                        for i in range(0,verifyOrder.open_order_len):
                            with allure.step('断言第{}条数据,订单号 {}：'.format(i+1,int(verifyOrder.openOrderexcel_data[i]['订单号码']))):
                                with allure.step('断言下载文件订单号：{}，页面订单号：{}'.format(int(verifyOrder.openOrderexcel_data[i]['订单号码']),verifyOrder.open_orderList[i]['订单号码'])):
                                    check.equal(int(verifyOrder.openOrderexcel_data[i]['订单号码']),verifyOrder.open_orderList[i]['订单号码'],'第{}条数据断言失败：'
                                    '下载文件订单号：{}，页面订单号：{}'.format(i+1,verifyOrder.openOrderexcel_data[i]['订单号码'],verifyOrder.open_orderList[i]['订单号码']))
                                
                                with allure.step('断言下载文件交易账号：{}，页面交易账号：{}'.format(verifyOrder.openOrderexcel_data[i]['交易账号'],verifyOrder.open_orderList[i]['交易账户'])):
                                    check.equal(int(verifyOrder.openOrderexcel_data[i]['交易账号']),verifyOrder.open_orderList[i]['交易账户'],'第{}条数据断言失败：'
                                    '下载文件交易账号：{}，页面交易账号：{}'.format(i+1,verifyOrder.openOrderexcel_data[i]['交易账号'],verifyOrder.open_orderList[i]['交易账户']))

                                with allure.step('断言下载文件开仓时间：{}，页面开仓时间：{}'.format(verifyOrder.openOrderexcel_data[i]['开仓时间'],verifyOrder.open_orderList[i]['开仓时间'])):
                                    check.equal(verifyOrder.openOrderexcel_data[i]['开仓时间'],verifyOrder.open_orderList[i]['开仓时间'],'第{}条数据断言失败：'
                                    '下载文件开仓时间：{}，页面开仓时间：{}'.format(i+1,verifyOrder.openOrderexcel_data[i]['开仓时间'],verifyOrder.open_orderList[i]['开仓时间']))
                                
                                with allure.step('断言下载文件类型：{}，页面类型：{}'.format(verifyOrder.openOrderexcel_data[i]['类型'],verifyOrder.open_orderList[i]['类型'])):
                                    check.equal(verifyOrder.openOrderexcel_data[i]['类型'],verifyOrder.open_orderList[i]['类型'],'第{}条数据断言失败：'
                                    '下载文件类型：{}，页面类型：{}'.format(i+1,verifyOrder.openOrderexcel_data[i]['类型'],verifyOrder.open_orderList[i]['类型']))
                                
                                with allure.step('断言下载文件手数：{}，页面交易量：{}'.format(float(verifyOrder.openOrderexcel_data[i]['手数']),verifyOrder.open_orderList[i]['交易量'])):
                                    check.equal(float(verifyOrder.openOrderexcel_data[i]['手数']),verifyOrder.open_orderList[i]['交易量'],'第{}条数据断言失败：'
                                    '下载文件手数：{}，页面交易量：{}'.format(i+1,float(verifyOrder.openOrderexcel_data[i]['手数']),verifyOrder.open_orderList[i]['交易量']))

                                with allure.step('断言下载文件商品代码：{}，页面商品代码：{}'.format(verifyOrder.openOrderexcel_data[i]['商品代码'],verifyOrder.open_orderList[i]['商品代码'])):
                                    check.equal(verifyOrder.openOrderexcel_data[i]['商品代码'],verifyOrder.open_orderList[i]['商品代码'],'第{}条数据断言失败：'
                                    '下载文件商品代码：{}，页面商品代码：{}'.format(i+1,verifyOrder.openOrderexcel_data[i]['商品代码'],verifyOrder.open_orderList[i]['商品代码']))
                                
                                with allure.step('断言下载文件开仓价：{}，页面开仓价：{}'.format(verifyOrder.openOrderexcel_data[i]['开仓价'],verifyOrder.open_orderList[i]['开仓价'])):
                                    check.equal(float(verifyOrder.openOrderexcel_data[i]['开仓价']),verifyOrder.open_orderList[i]['开仓价'],'第{}条数据断言失败：'
                                    '下载文件开仓价：{}，页面开仓价：{}'.format(i+1,verifyOrder.openOrderexcel_data[i]['开仓价'],verifyOrder.open_orderList[i]['开仓价']))

                                with allure.step('断言下载文件S/L：{}，页面S/L：{}'.format(verifyOrder.openOrderexcel_data[i]['S/L'],verifyOrder.open_orderList[i]['S/L'])):
                                    check.equal(float(verifyOrder.openOrderexcel_data[i]['S/L']),verifyOrder.open_orderList[i]['S/L'],'第{}条数据断言失败：'
                                    '下载文件S/L：{}，页面S/L：{}'.format(i+1,verifyOrder.openOrderexcel_data[i]['S/L'],verifyOrder.open_orderList[i]['S/L']))
                                
                                with allure.step('断言下载文件T/P：{}，页面T/P：{}'.format(verifyOrder.openOrderexcel_data[i]['T/P'],verifyOrder.open_orderList[i]['T/P'])):
                                    check.equal(float(verifyOrder.openOrderexcel_data[i]['T/P']),verifyOrder.open_orderList[i]['T/P'],'第{}条数据断言失败：'
                                    '下载文件T/P：{}，页面T/P：{}'.format(i+1,verifyOrder.openOrderexcel_data[i]['T/P'],verifyOrder.open_orderList[i]['T/P']))

                                with allure.step('断言下载文件佣金：{}，页面佣金：{}'.format(verifyOrder.openOrderexcel_data[i]['佣金'],verifyOrder.open_orderList[i]['佣金'])):
                                    check.equal(float(verifyOrder.openOrderexcel_data[i]['佣金']),verifyOrder.open_orderList[i]['佣金'],'第{}条数据断言失败：'
                                    '下载文件佣金：{}，页面佣金：{}'.format(i+1,verifyOrder.openOrderexcel_data[i]['佣金'],verifyOrder.open_orderList[i]['佣金']))

                                with allure.step('断言下载文件隔夜利息：{}，页面隔夜利息：{}'.format(float(verifyOrder.openOrderexcel_data[i]['隔夜利息']),verifyOrder.open_orderList[i]['隔夜利息'])):
                                    check.equal(float(verifyOrder.openOrderexcel_data[i]['隔夜利息']),verifyOrder.open_orderList[i]['隔夜利息'],'第{}条数据断言失败：'
                                    '下载文件隔夜利息：{}，页面隔夜利息：{}'.format(i+1,verifyOrder.openOrderexcel_data[i]['隔夜利息'],verifyOrder.open_orderList[i]['隔夜利息']))
                                
                                # check.equal(float(verifyOrder.openOrderexcel_data[i]['盈亏']),verifyOrder.open_orderList[i]['盈亏'],'第{}条数据断言失败：'
                                # '下载文件盈亏：{}，页面盈亏：{}'.format(i+1,verifyOrder.openOrderexcel_data[i]['盈亏'],verifyOrder.open_orderList[i]['盈亏']))
                    
                    with allure.step('断言复制数据是否与页面一致'):   
                        for i in range(0,verifyOrder.open_order_len):
                            with allure.step('断言第{}条数据，订单号 {}：'.format(i+1,int(verifyOrder.openOrder_data[i]['订单号码']))):
                                #断言未平仓订单复制数据是否与页面一致
                                with allure.step('断言复制内容订单号码：{}，页面订单号码：{}'.format(int(verifyOrder.openOrder_data[i]['订单号码']),verifyOrder.open_orderList[i]['订单号码'])):
                                    check.equal(int(verifyOrder.openOrder_data[i]['订单号码']),verifyOrder.open_orderList[i]['订单号码'],'第{}条数据断言失败：'
                                    '复制内容订单号码：{}，页面订单号码：{}'.format(i+1,verifyOrder.openOrder_data[i]['订单号码'],verifyOrder.open_orderList[i]['订单号码']))

                                with allure.step('断言复制内容交易账号：{}，页面交易账号：{}'.format(int(verifyOrder.openOrder_data[i]['交易账号']),verifyOrder.open_orderList[i]['交易账户'])):
                                    check.equal(int(verifyOrder.openOrder_data[i]['交易账号']),verifyOrder.open_orderList[i]['交易账户'],'第{}条数据断言失败：'
                                    '复制内容交易账号：{}，页面交易账号：{}'.format(i+1,verifyOrder.openOrder_data[i]['交易账号'],verifyOrder.open_orderList[i]['交易账户']))
                                
                                with allure.step('断言复制内容开仓时间：{}，页面开仓时间：{}'.format(verifyOrder.openOrder_data[i]['开仓时间'],verifyOrder.open_orderList[i]['开仓时间'])):
                                    check.equal(verifyOrder.openOrder_data[i]['开仓时间'],verifyOrder.open_orderList[i]['开仓时间'],'第{}条数据断言失败：'
                                    '复制内容开仓时间：{}，页面开仓时间：{}'.format(i+1,verifyOrder.openOrder_data[i]['开仓时间'],verifyOrder.open_orderList[i]['开仓时间']))

                                with allure.step('断言复制内容类型：{}，页面类型：{}'.format(verifyOrder.openOrder_data[i]['类型'],verifyOrder.open_orderList[i]['类型'])):
                                    check.equal(verifyOrder.openOrder_data[i]['类型'],verifyOrder.open_orderList[i]['类型'],'第{}条数据断言失败：'
                                    '复制内容类型：{}，页面类型：{}'.format(i+1,verifyOrder.openOrder_data[i]['类型'],verifyOrder.open_orderList[i]['类型']))
                                
                                with allure.step('断言复制内容手数：{}，页面交易量：{}'.format(float(verifyOrder.openOrder_data[i]['手数']),verifyOrder.open_orderList[i]['交易量'])):
                                    check.equal(float(verifyOrder.openOrder_data[i]['手数']),verifyOrder.open_orderList[i]['交易量'],'第{}条数据断言失败：'
                                    '复制内容手数：{}，页面交易量：{}'.format(i+1,float(verifyOrder.openOrder_data[i]['手数']),verifyOrder.open_orderList[i]['交易量']))

                                with allure.step('断言复制内容商品代码：{}，页面商品代码：{}'.format(verifyOrder.openOrder_data[i]['商品代码'],verifyOrder.open_orderList[i]['商品代码'])):
                                    check.equal(verifyOrder.openOrder_data[i]['商品代码'],verifyOrder.open_orderList[i]['商品代码'],'第{}条数据断言失败：'
                                    '复制内容商品代码：{}，页面商品代码：{}'.format(i+1,verifyOrder.openOrder_data[i]['商品代码'],verifyOrder.open_orderList[i]['商品代码']))

                                with allure.step('断言复制内容开仓价：{}，页面开仓价：{}'.format(verifyOrder.openOrder_data[i]['开仓价'],verifyOrder.open_orderList[i]['开仓价'])):
                                    check.equal(float(verifyOrder.openOrder_data[i]['开仓价']),verifyOrder.open_orderList[i]['开仓价'],'第{}条数据断言失败：'
                                    '复制内容开仓价：{}，页面开仓价：{}'.format(i+1,verifyOrder.openOrder_data[i]['开仓价'],verifyOrder.open_orderList[i]['开仓价']))

                                with allure.step('断言复制内容S/L：{}，页面S/L：{}'.format(verifyOrder.openOrder_data[i]['S/L'],verifyOrder.open_orderList[i]['S/L'])):
                                    check.equal(float(verifyOrder.openOrder_data[i]['S/L']),verifyOrder.open_orderList[i]['S/L'],'第{}条数据断言失败：'
                                    '复制内容S/L：{}，页面S/L：{}'.format(i+1,verifyOrder.openOrder_data[i]['S/L'],verifyOrder.open_orderList[i]['S/L']))
                                
                                with allure.step('断言复制内容T/P：{}，页面T/P：{}'.format(verifyOrder.openOrder_data[i]['T/P'],verifyOrder.open_orderList[i]['T/P'])):
                                    check.equal(float(verifyOrder.openOrder_data[i]['T/P']),verifyOrder.open_orderList[i]['T/P'],'第{}条数据断言失败：'
                                    '复制内容T/P：{}，页面T/P：{}'.format(i+1,verifyOrder.openOrder_data[i]['T/P'],verifyOrder.open_orderList[i]['T/P']))

                                with allure.step('断言复制内容佣金：{}，页面佣金：{}'.format(float(verifyOrder.openOrder_data[i]['佣金']),verifyOrder.open_orderList[i]['佣金'])):
                                    check.equal(float(verifyOrder.openOrder_data[i]['佣金']),verifyOrder.open_orderList[i]['佣金'],'第{}条数据断言失败：'
                                    '复制内容佣金：{}，页面佣金：{}'.format(i+1,verifyOrder.openOrder_data[i]['佣金'],verifyOrder.open_orderList[i]['佣金']))

                                with allure.step('断言复制内容隔夜利息：{}，页面隔夜利息：{}'.format(float(verifyOrder.openOrder_data[i]['隔夜利息']),verifyOrder.open_orderList[i]['隔夜利息'])):
                                    check.equal(float(verifyOrder.openOrder_data[i]['隔夜利息']),verifyOrder.open_orderList[i]['隔夜利息'],'第{}条数据断言失败：'
                                    '复制内容隔夜利息：{}，页面隔夜利息：{}'.format(i+1,verifyOrder.openOrder_data[i]['隔夜利息'],verifyOrder.open_orderList[i]['隔夜利息']))
                                
                                # check.equal(float(verifyOrder.openOrder_data[i]['盈亏']),verifyOrder.open_orderList[i]['盈亏'],'第{}条数据断言失败：'
                                # '复制内容盈亏：{}，页面盈亏：{}'.format(i+1,verifyOrder.openOrder_data[i]['盈亏'],verifyOrder.open_orderList[i]['盈亏']))   
            else:
                with allure.step('交易账号不存在未平仓订单'):
                    check.equal(verifyOrder.open_order_len,0)


        with allure.step('判断交易账号是否存在已平仓订单'):
            if verifyOrder.close_order_len!=0:
                with allure.step('交易账号存在已平仓订单{}条'.format(verifyOrder.close_order_len)):
                    with allure.step('断言导出数据是否与页面一致'):
                        for i in range(0,verifyOrder.close_order_len):
                            with allure.step('断言第{}条数据，订单号 {}：'.format(i+1,int(verifyOrder.closeOrderexcel_data[i]['订单号码']))):
                                with allure.step('断言下载文件订单号码：{}，页面订单号码：{}'.format(int(verifyOrder.closeOrderexcel_data[i]['订单号码']),verifyOrder.close_orderList[i]['订单号码'])):
                                    check.equal(int(verifyOrder.closeOrderexcel_data[i]['订单号码']),verifyOrder.close_orderList[i]['订单号码'],'第{}条数据断言失败：'
                                    '下载文件订单号码：{}，页面订单号码：{}'.format(i+1,verifyOrder.closeOrderexcel_data[i]['订单号码'],verifyOrder.close_orderList[i]['订单号码']))
                                
                                with allure.step('断言下载文件交易账号：{}，页面交易账号：{}'.format(int(verifyOrder.closeOrderexcel_data[i]['交易账号']),verifyOrder.close_orderList[i]['交易账户'])):
                                    check.equal(int(verifyOrder.closeOrderexcel_data[i]['交易账号']),verifyOrder.close_orderList[i]['交易账户'],'第{}条数据断言失败：'
                                    '下载文件交易账号：{}，页面交易账号：{}'.format(i+1,verifyOrder.closeOrderexcel_data[i]['交易账号'],verifyOrder.close_orderList[i]['交易账户']))
                                
                                with allure.step('断言下载文件开仓时间：{}，页面交易账号：{}'.format(verifyOrder.closeOrderexcel_data[i]['开仓时间'],verifyOrder.close_orderList[i]['开仓时间'])):
                                    check.equal(verifyOrder.closeOrderexcel_data[i]['开仓时间'],verifyOrder.close_orderList[i]['开仓时间'],'第{}条数据断言失败：'
                                    '下载文件开仓时间：{}，页面开仓时间：{}'.format(i+1,verifyOrder.closeOrderexcel_data[i]['开仓时间'],verifyOrder.close_orderList[i]['开仓时间']))

                                with allure.step('断言下载文件平仓时间：{}，页面平仓时间：{}'.format(verifyOrder.closeOrderexcel_data[i]['平仓时间'],verifyOrder.close_orderList[i]['平仓时间'])):
                                    check.equal(verifyOrder.closeOrderexcel_data[i]['平仓时间'],verifyOrder.close_orderList[i]['平仓时间'],'第{}条数据断言失败：'
                                    '下载文件平仓时间：{}，页面平仓时间：{}'.format(i+1,verifyOrder.closeOrderexcel_data[i]['平仓时间'],verifyOrder.close_orderList[i]['平仓时间']))

                                with allure.step('断言下载文件类型：{}，页面类型：{}'.format(verifyOrder.closeOrderexcel_data[i]['类型'],verifyOrder.close_orderList[i]['类型'])):
                                    check.equal(verifyOrder.closeOrderexcel_data[i]['类型'],verifyOrder.close_orderList[i]['类型'],'第{}条数据断言失败：'
                                    '下载文件类型：{}，页面类型：{}'.format(i+1,verifyOrder.closeOrderexcel_data[i]['类型'],verifyOrder.close_orderList[i]['类型']))

                                with allure.step('断言下载文件手数：{}，页面交易量：{}'.format(float(verifyOrder.closeOrderexcel_data[i]['手数']),verifyOrder.close_orderList[i]['交易量'])):
                                    check.equal(float(verifyOrder.closeOrderexcel_data[i]['手数']),verifyOrder.close_orderList[i]['交易量'],'第{}条数据断言失败：'
                                    '下载文件手数：{}，页面交易量：{}'.format(i+1,float(verifyOrder.closeOrderexcel_data[i]['手数']),verifyOrder.close_orderList[i]['交易量']))

                                with allure.step('断言下载文件商品代码：{}，页面商品代码：{}'.format(verifyOrder.closeOrderexcel_data[i]['商品代码'],verifyOrder.close_orderList[i]['商品代码'])):
                                    check.equal(verifyOrder.closeOrderexcel_data[i]['商品代码'],verifyOrder.close_orderList[i]['商品代码'],'第{}条数据断言失败：'
                                    '下载文件商品代码：{}，页面商品代码：{}'.format(i+1,verifyOrder.closeOrderexcel_data[i]['商品代码'],verifyOrder.close_orderList[i]['商品代码']))

                                with allure.step('断言下载文件开仓价：{}，页面开仓价：{}'.format(float(verifyOrder.closeOrderexcel_data[i]['开仓价']),verifyOrder.close_orderList[i]['开仓价'])):
                                    check.equal(float(verifyOrder.closeOrderexcel_data[i]['开仓价']),verifyOrder.close_orderList[i]['开仓价'],'第{}条数据断言失败：'
                                    '下载文件开仓价：{}，页面开仓价：{}'.format(i+1,verifyOrder.closeOrderexcel_data[i]['开仓价'],verifyOrder.close_orderList[i]['开仓价']))

                                with allure.step('断言下载文件平仓价格：{}，页面平仓价格：{}'.format(float(verifyOrder.closeOrderexcel_data[i]['平仓价格']),verifyOrder.close_orderList[i]['平仓价格'])):
                                    check.equal(float(verifyOrder.closeOrderexcel_data[i]['平仓价格']),verifyOrder.close_orderList[i]['平仓价格'],'第{}条数据断言失败：'
                                    '下载文件平仓价格：{}，页面平仓价格：{}'.format(i+1,verifyOrder.closeOrderexcel_data[i]['平仓价格'],verifyOrder.close_orderList[i]['平仓价格']))
                                
                                with allure.step('断言下载文件S/L：{}，页面S/L：{}'.format(float(verifyOrder.closeOrderexcel_data[i]['S/L']),verifyOrder.close_orderList[i]['S/L'])):
                                    check.equal(float(verifyOrder.closeOrderexcel_data[i]['S/L']),verifyOrder.close_orderList[i]['S/L'],'第{}条数据断言失败：'
                                    '下载文件S/L：{}，页面S/L：{}'.format(i+1,verifyOrder.closeOrderexcel_data[i]['S/L'],verifyOrder.close_orderList[i]['S/L']))

                                with allure.step('断言下载文件T/P：{}，页面T/P：{}'.format(float(verifyOrder.closeOrderexcel_data[i]['T/P']),verifyOrder.close_orderList[i]['T/P'])):
                                    check.equal(float(verifyOrder.closeOrderexcel_data[i]['T/P']),verifyOrder.close_orderList[i]['T/P'],'第{}条数据断言失败：'
                                    '下载文件T/P：{}，页面T/P：{}'.format(i+1,verifyOrder.closeOrderexcel_data[i]['T/P'],verifyOrder.close_orderList[i]['T/P']))

                                with allure.step('断言下载文件佣金：{}，页面佣金：{}'.format(float(verifyOrder.closeOrderexcel_data[i]['佣金']),verifyOrder.close_orderList[i]['佣金'])):
                                    check.equal(float(verifyOrder.closeOrderexcel_data[i]['佣金']),verifyOrder.close_orderList[i]['佣金'],'第{}条数据断言失败：'
                                    '下载文件佣金：{}，页面佣金：{}'.format(i+1,verifyOrder.closeOrderexcel_data[i]['佣金'],verifyOrder.close_orderList[i]['佣金']))

                                with allure.step('断言下载文件隔夜利息：{}，页面隔夜利息：{}'.format(float(verifyOrder.closeOrderexcel_data[i]['隔夜利息']),verifyOrder.close_orderList[i]['隔夜利息'])):
                                    check.equal(float(verifyOrder.closeOrderexcel_data[i]['隔夜利息']),verifyOrder.close_orderList[i]['隔夜利息'],'第{}条数据断言失败：'
                                    '下载文件隔夜利息：{}，页面隔夜利息：{}'.format(i+1,verifyOrder.closeOrderexcel_data[i]['隔夜利息'],verifyOrder.close_orderList[i]['隔夜利息']))

                                with allure.step('断言下载文件盈亏：{}，页面盈亏：{}'.format(float(verifyOrder.closeOrderexcel_data[i]['盈亏']),verifyOrder.close_orderList[i]['盈亏'])):
                                    check.equal(float(verifyOrder.closeOrderexcel_data[i]['盈亏']),verifyOrder.close_orderList[i]['盈亏'],'第{}条数据断言失败：'
                                    '下载文件盈亏：{}，页面盈亏：{}'.format(i+1,verifyOrder.closeOrderexcel_data[i]['盈亏'],verifyOrder.close_orderList[i]['盈亏']))
                    
                    with allure.step('断言复制内容是否与页面一致'):
                        for i in range(0,verifyOrder.close_order_len):
                            with allure.step('断言第{}条数据，订单号 {}：'.format(i+1,int(verifyOrder.closeOrder_data[i]['订单号码']))):
                                with allure.step('断言复制内容订单号码：{}，页面订单号码：{}'.format(int(verifyOrder.closeOrder_data[i]['订单号码']),verifyOrder.close_orderList[i]['订单号码'])):
                                    check.equal(int(verifyOrder.closeOrder_data[i]['订单号码']),verifyOrder.close_orderList[i]['订单号码'],'第{}条数据断言失败：'
                                    '复制内容订单号码：{}，页面订单号码：{}'.format(i+1,verifyOrder.closeOrder_data[i]['订单号码'],verifyOrder.close_orderList[i]['订单号码']))
                                
                                with allure.step('断言复制内容交易账号：{}，页面交易账号：{}'.format(int(verifyOrder.closeOrder_data[i]['交易账号']),verifyOrder.close_orderList[i]['交易账户'])):
                                    check.equal(int(verifyOrder.closeOrder_data[i]['交易账号']),verifyOrder.close_orderList[i]['交易账户'],'第{}条数据断言失败：'
                                    '复制内容交易账号：{}，页面交易账号：{}'.format(i+1,verifyOrder.closeOrder_data[i]['交易账号'],verifyOrder.close_orderList[i]['交易账户']))

                                with allure.step('断言复制内容开仓时间：{}，页面开仓时间：{}'.format(verifyOrder.closeOrder_data[i]['开仓时间'],verifyOrder.close_orderList[i]['开仓时间'])):
                                    check.equal(verifyOrder.closeOrder_data[i]['开仓时间'],verifyOrder.close_orderList[i]['开仓时间'],'第{}条数据断言失败：'
                                    '复制内容开仓时间：{}，页面开仓时间：{}'.format(i+1,verifyOrder.closeOrder_data[i]['开仓时间'],verifyOrder.close_orderList[i]['开仓时间']))
                                
                                with allure.step('断言复制内容平仓时间：{}，页面平仓时间：{}'.format(verifyOrder.closeOrder_data[i]['平仓时间'],verifyOrder.close_orderList[i]['平仓时间'])):
                                    check.equal(verifyOrder.closeOrder_data[i]['平仓时间'],verifyOrder.close_orderList[i]['平仓时间'],'第{}条数据断言失败：'
                                    '复制内容平仓时间：{}，页面平仓时间：{}'.format(i+1,verifyOrder.closeOrder_data[i]['平仓时间'],verifyOrder.close_orderList[i]['平仓时间']))
                                
                                with allure.step('断言复制内容类型：{}，页面类型：{}'.format(verifyOrder.closeOrder_data[i]['类型'],verifyOrder.close_orderList[i]['类型'])):
                                    check.equal(verifyOrder.closeOrder_data[i]['类型'],verifyOrder.close_orderList[i]['类型'],'第{}条数据断言失败：'
                                    '复制内容类型：{}，页面类型：{}'.format(i+1,verifyOrder.closeOrder_data[i]['类型'],verifyOrder.close_orderList[i]['类型']))
                                
                                with allure.step('断言复制内容手数：{}，页面交易量：{}'.format(float(verifyOrder.closeOrder_data[i]['手数']),verifyOrder.close_orderList[i]['交易量'])):
                                    check.equal(float(verifyOrder.closeOrder_data[i]['手数']),verifyOrder.close_orderList[i]['交易量'],'第{}条数据断言失败：'
                                    '复制内容手数：{}，页面交易量：{}'.format(i+1,float(verifyOrder.closeOrder_data[i]['手数']),verifyOrder.close_orderList[i]['交易量']))

                                with allure.step('断言复制内容商品代码：{}，页面商品代码：{}'.format(verifyOrder.closeOrder_data[i]['商品代码'],verifyOrder.close_orderList[i]['商品代码'])):
                                    check.equal(verifyOrder.closeOrder_data[i]['商品代码'],verifyOrder.close_orderList[i]['商品代码'],'第{}条数据断言失败：'
                                    '复制内容商品代码：{}，页面商品代码：{}'.format(i+1,verifyOrder.closeOrder_data[i]['商品代码'],verifyOrder.close_orderList[i]['商品代码']))

                                with allure.step('断言复制内容开仓价：{}，页面开仓价：{}'.format(float(verifyOrder.closeOrder_data[i]['开仓价']),verifyOrder.close_orderList[i]['开仓价'])):
                                    check.equal(float(verifyOrder.closeOrder_data[i]['开仓价']),verifyOrder.close_orderList[i]['开仓价'],'第{}条数据断言失败：'
                                    '复制内容开仓价：{}，页面开仓价：{}'.format(i+1,verifyOrder.closeOrder_data[i]['开仓价'],verifyOrder.close_orderList[i]['开仓价']))

                                with allure.step('断言复制内容开仓价：{}，页面开仓价：{}'.format(float(verifyOrder.closeOrder_data[i]['平仓价格']),verifyOrder.close_orderList[i]['平仓价格'])):
                                    check.equal(float(verifyOrder.closeOrder_data[i]['平仓价格']),verifyOrder.close_orderList[i]['平仓价格'],'第{}条数据断言失败：'
                                    '复制内容平仓价格：{}，页面平仓价格：{}'.format(i+1,verifyOrder.closeOrder_data[i]['平仓价格'],verifyOrder.close_orderList[i]['平仓价格']))

                                with allure.step('断言复制内容S/L：{}，页面S/L：{}'.format(float(verifyOrder.closeOrder_data[i]['S/L']),verifyOrder.close_orderList[i]['S/L'])):
                                    check.equal(float(verifyOrder.closeOrder_data[i]['S/L']),verifyOrder.close_orderList[i]['S/L'],'第{}条数据断言失败：'
                                    '复制内容S/L：{}，页面S/L：{}'.format(i+1,verifyOrder.closeOrder_data[i]['S/L'],verifyOrder.close_orderList[i]['S/L']))
                                
                                with allure.step('断言复制内容T/P：{}，页面T/P：{}'.format(float(verifyOrder.closeOrder_data[i]['T/P']),verifyOrder.close_orderList[i]['T/P'])):
                                    check.equal(float(verifyOrder.closeOrder_data[i]['T/P']),verifyOrder.close_orderList[i]['T/P'],'第{}条数据断言失败：'
                                    '复制内容T/P：{}，页面T/P：{}'.format(i+1,verifyOrder.closeOrder_data[i]['T/P'],verifyOrder.close_orderList[i]['T/P']))

                                with allure.step('断言复制内容佣金：{}，页面佣金：{}'.format(float(verifyOrder.closeOrder_data[i]['佣金']),verifyOrder.close_orderList[i]['佣金'])):
                                    check.equal(float(verifyOrder.closeOrder_data[i]['佣金']),verifyOrder.close_orderList[i]['佣金'],'第{}条数据断言失败：'
                                    '复制内容佣金：{}，页面佣金：{}'.format(i+1,verifyOrder.closeOrder_data[i]['佣金'],verifyOrder.close_orderList[i]['佣金']))
                                
                                with allure.step('断言复制内容隔夜利息：{}，页面隔夜利息：{}'.format(float(verifyOrder.closeOrder_data[i]['隔夜利息']),verifyOrder.close_orderList[i]['隔夜利息'])):
                                    check.equal(float(verifyOrder.closeOrder_data[i]['隔夜利息']),verifyOrder.close_orderList[i]['隔夜利息'],'第{}条数据断言失败：'
                                    '复制内容隔夜利息：{}，页面隔夜利息：{}'.format(i+1,verifyOrder.closeOrder_data[i]['隔夜利息'],verifyOrder.close_orderList[i]['隔夜利息']))
                                
                                with allure.step('断言复制内容盈亏：{}，页面盈亏：{}'.format(float(verifyOrder.closeOrder_data[i]['盈亏']),verifyOrder.close_orderList[i]['盈亏'])):
                                    check.equal(float(verifyOrder.closeOrder_data[i]['盈亏']),verifyOrder.close_orderList[i]['盈亏'],'第{}条数据断言失败：'
                                    '复制内容盈亏：{}，页面盈亏：{}'.format(i+1,verifyOrder.closeOrder_data[i]['盈亏'],verifyOrder.close_orderList[i]['盈亏']))
            else:
                with allure.step('交易账号不存在已平仓订单'):
                    check.equal(verifyOrder.close_order_len,0)
        
        
        # 断言交易账号某个时间段内未平仓订单
        with allure.step('判断交易账号某个时间段内是否存在未平仓订单'):
            if verifyOrder.search_period_openOrder(int(data['交易账号'])):
                with allure.step('交易账号某个时间段内存在未平仓订单{}条'.format(verifyOrder.open_order_len)):
                    with allure.step('断言数据库查询数据是否与页面一致'):
                        for i in range(0,verifyOrder.open_order_len):
                            with allure.step('断言第{}条数据，订单号 {}：'.format(i+1,verifyOrder.open_orderList[i]['Ticket'])):

                                with allure.step('断言页面订单号码：{}，数据库ticket：{}'.format(verifyOrder.open_orderList[i]['Ticket'],verifyOrder.mysql_openOrder[i][0])):
                                    check.equal(verifyOrder.open_orderList[i]['Ticket'],verifyOrder.mysql_openOrder[i][0],'第{}条数据断言失败：'
                                    '页面订单号码：{}，数据库ticket：{}'.format(i+1,verifyOrder.open_orderList[i]['Ticket'],verifyOrder.mysql_openOrder[i][0]))

                                with allure.step('断言页面开仓时间：{}，数据库开仓时间：{}'.format(verifyOrder.open_orderList[i]['Open_Time'],verifyOrder.mysql_openOrder[i][6])):    
                                    check.equal(verifyOrder.open_orderList[i]['Open_Time'],verifyOrder.mysql_openOrder[i][6],'第{}条数据断言失败：'
                                    '页面订单开仓时间：{}，数据库开仓时间：{}'.format(i+1,verifyOrder.open_orderList[i]['Open_Time'],verifyOrder.mysql_openOrder[i][6]))
                                
                                with allure.step('断言页面交易量：{}，数据库交易量：{}'.format(verifyOrder.open_orderList[i]['Volume'],float(verifyOrder.mysql_openOrder[i][5]/100))): 
                                    check.equal(verifyOrder.open_orderList[i]['Volume'],float(verifyOrder.mysql_openOrder[i][5]/100),'第{}条数据断言失败：'
                                    '页面订单交易量：{}，数据库交易量：{}'.format(i+1,verifyOrder.open_orderList[i]['Volume'],float(verifyOrder.mysql_openOrder[i][5]/100)))

                                with allure.step('断言页面商品代码：{}，数据库商品代码：{}'.format(verifyOrder.open_orderList[i]['Symbol'],verifyOrder.mysql_openOrder[i][2])):  
                                    check.equal(verifyOrder.open_orderList[i]['Symbol'],verifyOrder.mysql_openOrder[i][2],'第{}条数据断言失败：'
                                    '页面订单商品代码：{}，数据库商品代码：{}'.format(i+1,verifyOrder.open_orderList[i]['Symbol'],verifyOrder.mysql_openOrder[i][2]))

                                with allure.step('断言页面开仓价：{}，数据库开仓价：{}'.format(verifyOrder.open_orderList[i]['Open_Price'],verifyOrder.mysql_openOrder[i][7])):
                                    check.equal(verifyOrder.open_orderList[i]['Open_Price'],verifyOrder.mysql_openOrder[i][7],'第{}条数据断言失败：'
                                    '页面订单开仓价：{}，数据库开仓价：{}'.format(i+1,verifyOrder.open_orderList[i]['Open_Price'],verifyOrder.mysql_openOrder[i][7]))

                                with allure.step('断言页面订单佣金：{}，数据库佣金：{}'.format(verifyOrder.open_orderList[i]['Commission'],verifyOrder.mysql_openOrder[i][11])):
                                    check.equal(verifyOrder.open_orderList[i]['Commission'],verifyOrder.mysql_openOrder[i][11],'第{}条数据断言失败：'
                                    '页面订单佣金：{}，数据库佣金：{}'.format(i+1,verifyOrder.open_orderList[i]['Commission'],verifyOrder.mysql_openOrder[i][11]))
                                
                                with allure.step('断言页面隔夜利息：{}，数据库隔夜利息：{}'.format(verifyOrder.open_orderList[i]['Swaps'],verifyOrder.mysql_openOrder[i][13])):
                                    check.equal(verifyOrder.open_orderList[i]['Swaps'],verifyOrder.mysql_openOrder[i][13],'第{}条数据断言失败：'
                                    '页面订单隔夜利息：{}，数据库隔夜利息：{}'.format(i+1,verifyOrder.open_orderList[i]['Swaps'],verifyOrder.mysql_openOrder[i][13]))

            else:
                with allure.step('交易账号某个时间段内不存在未平仓订单'):
                    check.equal(verifyOrder.open_order_len,len(verifyOrder.mysql_openOrder))
        
        # 查询交易账号某个时间段内已平仓订单
        with allure.step('判断交易账号某个时间段内是否存在已平仓订单'):
            if verifyOrder.search_period_closeOrder(int(data['交易账号'])):
                with allure.step('交易账号某个时间段内存在已平仓订单{}条'.format(verifyOrder.close_order_len)):
                    with allure.step('断言数据库查询数据是否与页面一致'):
                        for i in range(0,verifyOrder.close_order_len):
                            with allure.step('断言第{}条数据，订单号 {}：'.format(i+1,verifyOrder.close_orderList[i]['Ticket'])):

                                with allure.step('断言页面订单号码：{}，数据库订单号码：{}'.format(verifyOrder.close_orderList[i]['Ticket'],verifyOrder.mysql_closeOrder[i][0])):
                                    check.equal(verifyOrder.close_orderList[i]['Ticket'],verifyOrder.mysql_closeOrder[i][0],'第{}条数据断言失败：'
                                    '页面订单号码：{}，数据库订单号码：{}'.format(i+1,verifyOrder.close_orderList[i]['Ticket'],verifyOrder.mysql_closeOrder[i][0]))
                                
                                with allure.step('断言页面开仓时间：{}，数据库开仓时间：{}'.format(verifyOrder.close_orderList[i]['Open_Time'],verifyOrder.mysql_closeOrder[i][6])):
                                    check.equal(verifyOrder.close_orderList[i]['Open_Time'],verifyOrder.mysql_closeOrder[i][6],'第{}条数据断言失败：'
                                    '页面订单开仓时间：{}，数据库订单开仓时间：{}'.format(i+1,verifyOrder.close_orderList[i]['Open_Time'],verifyOrder.mysql_closeOrder[i][6]))

                                with allure.step('断言页面平仓时间：{}，数据库平仓时间：{}'.format(verifyOrder.close_orderList[i]['Close_Time'],verifyOrder.mysql_closeOrder[i][10])):
                                    check.equal(verifyOrder.close_orderList[i]['Close_Time'], verifyOrder.mysql_closeOrder[i][10],'第{}条数据断言失败：'
                                    '页面订单平仓时间：{}，数据库订单平仓时间：{}'.format(i+1,verifyOrder.close_orderList[i]['Close_Time'],verifyOrder.mysql_closeOrder[i][10]))
                                
                                with allure.step('断言页面交易量：{}，数据库交易量：{}'.format(verifyOrder.close_orderList[i]['Volume'],float(verifyOrder.mysql_closeOrder[i][5]/100))):
                                    check.equal(verifyOrder.close_orderList[i]['Volume'],float(verifyOrder.mysql_closeOrder[i][5]/100),'第{}条数据断言失败：'
                                    '页面订单交易量：{}，数据库订单交易量：{}'.format(i+1,verifyOrder.close_orderList[i]['Volume'],float(verifyOrder.mysql_closeOrder[i][5]/100)))

                                with allure.step('断言页面商品代码：{}，数据库商品代码：{}'.format(verifyOrder.close_orderList[i]['Symbol'],verifyOrder.mysql_closeOrder[i][2])):
                                    check.equal(verifyOrder.close_orderList[i]['Symbol'],verifyOrder.mysql_closeOrder[i][2],'第{}条数据断言失败：'
                                    '页面订单商品代码：{}，数据库订单商品代码：{}'.format(i+1,verifyOrder.close_orderList[i]['Symbol'],verifyOrder.mysql_closeOrder[i][2]))
                                
                                with allure.step('断言页面开仓价：{}，数据库开仓价：{}'.format(verifyOrder.close_orderList[i]['Open_Price'],verifyOrder.mysql_closeOrder[i][7])):
                                    check.equal(verifyOrder.close_orderList[i]['Open_Price'],verifyOrder.mysql_closeOrder[i][7],'第{}条数据断言失败：'
                                    '页面订单开仓价：{}，数据库订单开仓价：{}'.format(i+1,verifyOrder.close_orderList[i]['Open_Price'],verifyOrder.mysql_closeOrder[i][7]))

                                with allure.step('断言页面平仓价：{}，数据库平仓价：{}'.format(verifyOrder.close_orderList[i]['Close_Price'],verifyOrder.mysql_closeOrder[i][14])):
                                    check.equal(verifyOrder.close_orderList[i]['Close_Price'],verifyOrder.mysql_closeOrder[i][14],'第{}条数据断言失败：'
                                    '页面订单平仓价：{}，数据库订单平仓价：{}'.format(i+1,verifyOrder.close_orderList[i]['Close_Price'],verifyOrder.mysql_closeOrder[i][14]))
                                
                                with allure.step('断言页面佣金：{}，数据库佣金：{}'.format(verifyOrder.close_orderList[i]['Commission'],verifyOrder.mysql_closeOrder[i][11])):
                                    check.equal(verifyOrder.close_orderList[i]['Commission'],verifyOrder.mysql_closeOrder[i][11],'第{}条数据断言失败：'
                                    '页面订单佣金：{}，数据库订单佣金：{}'.format(i+1,verifyOrder.close_orderList[i]['Commission'],verifyOrder.mysql_closeOrder[i][11]))

                                with allure.step('断言页面隔夜利息：{}，数据库隔夜利息：{}'.format(verifyOrder.close_orderList[i]['Swaps'],verifyOrder.mysql_closeOrder[i][13])):
                                    check.equal(verifyOrder.close_orderList[i]['Swaps'],verifyOrder.mysql_closeOrder[i][13],'第{}条数据断言失败：'
                                    '页面订单隔夜利息：{}，数据库订单隔夜利息：{}'.format(i+1,verifyOrder.close_orderList[i]['Swaps'],verifyOrder.mysql_closeOrder[i][13]))
                                
                                with allure.step('断言页面盈亏：{}，数据库盈亏：{}'.format(verifyOrder.close_orderList[i]['Profit'],verifyOrder.mysql_closeOrder[i][15])):
                                    check.equal(verifyOrder.close_orderList[i]['Profit'],verifyOrder.mysql_closeOrder[i][15],'第{}条数据断言失败：'
                                    '页面订单盈亏：{}，数据库订单盈亏：{}'.format(i+1,verifyOrder.close_orderList[i]['Profit'],verifyOrder.mysql_closeOrder[i][15]))
            else:
                with allure.step('交易账号某个时间段内不存在已平仓订单'):
                    check.equal(verifyOrder.close_order_len,len(verifyOrder.mysql_closeOrder))   

        
        with allure.step('判断当前主账号是否存在某个商品代码的未平仓订单'):
            if verifyOrder.search_symbol_openOrder(data['商品代码']):
                with allure.step('当前主账号存在 {} 商品代码的未平仓订单{}条'.format(data['商品代码'],len(verifyOrder.symbol_openLsit))):
                    with allure.step('断言数据库查询数据是否与页面一致'):
                        for i in range(0,len(verifyOrder.symbol_openLsit)):
                            for y in range(0,len(verifyOrder.mysql_symbol_openOrder)):
                                if verifyOrder.symbol_openLsit[i]['Ticket']==verifyOrder.mysql_symbol_openOrder[y][0]:
                                    with allure.step('断言第{}条数据，订单号 {}：'.format(i+1,verifyOrder.symbol_openLsit[i]['Ticket'])):

                                        with allure.step('断言页面交易账户：{}，数据库交易账户：{}'.format(verifyOrder.symbol_openLsit[i]['Login'],verifyOrder.mysql_symbol_openOrder[y][1])):
                                            check.equal(verifyOrder.symbol_openLsit[i]['Login'],verifyOrder.mysql_symbol_openOrder[y][1],'第{}条数据断言失败：'
                                            '页面订单交易账户：{}，数据库订单交易账户：{}'.format(i+1,verifyOrder.symbol_openLsit[i]['Login'],verifyOrder.mysql_symbol_openOrder[y][1]))
                                        
                                        with allure.step('断言页面开仓时间：{}，数据库开仓时间：{}'.format(verifyOrder.symbol_openLsit[i]['Open_time'],verifyOrder.mysql_symbol_openOrder[y][6])):
                                            check.equal(verifyOrder.symbol_openLsit[i]['Open_time'],verifyOrder.mysql_symbol_openOrder[y][6],'第{}条数据断言失败：'
                                            '页面订单开仓时间：{}，数据库订单开仓时间：{}'.format(i+1,verifyOrder.symbol_openLsit[i]['Open_time'],verifyOrder.mysql_symbol_openOrder[y][6]))

                                        with allure.step('断言页面交易量：{}，数据库交易量：{}'.format(verifyOrder.symbol_openLsit[i]['Volume'],float(verifyOrder.mysql_symbol_openOrder[y][5]/100))):
                                            check.equal(verifyOrder.symbol_openLsit[i]['Volume'],float(verifyOrder.mysql_symbol_openOrder[y][5]/100),'第{}条数据断言失败：'
                                            '页面订单交易量：{}，数据库订单交易量：{}'.format(i+1,verifyOrder.symbol_openLsit[i]['Volume'],float(verifyOrder.mysql_symbol_openOrder[y][5]/100)))

                                        with allure.step('断言页面商品代码：{}，数据库商品代码：{}'.format(verifyOrder.symbol_openLsit[i]['Symbol'],verifyOrder.mysql_symbol_openOrder[y][2])):
                                            check.equal(verifyOrder.symbol_openLsit[i]['Symbol'],verifyOrder.mysql_symbol_openOrder[y][2],'第{}条数据断言失败：'
                                            '页面订单商品代码：{}，数据库订单商品代码：{}'.format(i+1,verifyOrder.symbol_openLsit[i]['Symbol'],verifyOrder.mysql_symbol_openOrder[y][2]))

                                        with allure.step('断言页面开仓价：{}，数据库开仓价：{}'.format(verifyOrder.symbol_openLsit[i]['Open_price'],verifyOrder.mysql_symbol_openOrder[y][7])):
                                            check.equal(verifyOrder.symbol_openLsit[i]['Open_price'],verifyOrder.mysql_symbol_openOrder[y][7],'第{}条数据断言失败：'
                                            '页面订单开仓价：{}，数据库订单开仓价：{}'.format(i+1,verifyOrder.symbol_openLsit[i]['Open_price'],verifyOrder.mysql_symbol_openOrder[y][7]))

                                        with allure.step('断言页面佣金：{}，数据库佣金：{}'.format(verifyOrder.symbol_openLsit[i]['Commission'],verifyOrder.mysql_symbol_openOrder[y][11])):
                                            check.equal(verifyOrder.symbol_openLsit[i]['Commission'],verifyOrder.mysql_symbol_openOrder[y][11],'第{}条数据断言失败：'
                                            '页面订单佣金：{}，数据库订单佣金：{}'.format(i+1,verifyOrder.symbol_openLsit[i]['Commission'],verifyOrder.mysql_symbol_openOrder[y][11]))

                                        with allure.step('断言页面佣金：{}，数据库佣金：{}'.format(verifyOrder.symbol_openLsit[i]['Swaps'],verifyOrder.mysql_symbol_openOrder[y][13])):
                                            check.equal(verifyOrder.symbol_openLsit[i]['Swaps'],verifyOrder.mysql_symbol_openOrder[y][13],'第{}条数据断言失败：'
                                            '页面订单隔夜利息：{}，数据库隔夜利息：{}'.format(i+1,verifyOrder.symbol_openLsit[i]['Swaps'],verifyOrder.mysql_symbol_openOrder[y][13]))

                                        break
                                else:
                                    pass
            else:
                with allure.step('当前主账号不存在该商品类型的未平仓订单'):
                    check.equal(verifyOrder.symbol_openLen,0)
        
        
        with allure.step('判断当前主账号是否存在某个商品代码的已平仓订单'):
            if verifyOrder.search_symbol_closeOrder(data['商品代码']):
                with allure.step('当前主账号存在 {} 商品代码的未平仓订单{}条'.format(data['商品代码'],len(verifyOrder.symbol_closeLsit))):
                    with allure.step('断言数据库查询数据是否与页面一致'):
                        for i in range(0,len(verifyOrder.symbol_closeLsit)):
                            for y in range(0,len(verifyOrder.mysql_symbol_closeOrder)):
                                if verifyOrder.symbol_closeLsit[i]['Ticket']==verifyOrder.mysql_symbol_closeOrder[y][0]:
                                    with allure.step('断言第{}条数据，订单号 {}：'.format(i+1,verifyOrder.symbol_closeLsit[i]['Ticket'])):

                                        with allure.step('断言页面交易账户：{}，数据库交易账户：{}'.format(verifyOrder.symbol_closeLsit[i]['Login'],verifyOrder.mysql_symbol_closeOrder[y][1])):
                                            check.equal(verifyOrder.symbol_closeLsit[i]['Login'],verifyOrder.mysql_symbol_closeOrder[y][1],'第{}条数据断言失败：'
                                            '页面交易账户：{}，数据库交易账户：{}'.format(i+1,verifyOrder.symbol_closeLsit[i]['Login'],verifyOrder.mysql_symbol_closeOrder[y][1]))
                                        
                                        with allure.step('断言页面开仓时间：{}，数据库开仓时间：{}'.format(verifyOrder.symbol_closeLsit[i]['Open_time'],verifyOrder.mysql_symbol_closeOrder[y][6])):
                                            check.equal(verifyOrder.symbol_closeLsit[i]['Open_time'],verifyOrder.mysql_symbol_closeOrder[y][6],'第{}条数据断言失败：'
                                            '页面订单开仓时间：{}，数据库开仓时间：{}'.format(i+1,verifyOrder.symbol_closeLsit[i]['Open_time'],verifyOrder.mysql_symbol_closeOrder[y][6]))

                                        with allure.step('断言页面平仓时间：{}，数据库平仓时间：{}'.format(verifyOrder.symbol_closeLsit[i]['Close_time'],verifyOrder.mysql_symbol_closeOrder[y][10])):
                                            check.equal(verifyOrder.symbol_closeLsit[i]['Close_time'],verifyOrder.mysql_symbol_closeOrder[y][10],'第{}条数据断言失败：'
                                            '页面订单平仓时间：{}，数据库平仓时间：{}'.format(i+1,verifyOrder.symbol_closeLsit[i]['Close_time'],verifyOrder.mysql_symbol_closeOrder[y][10]))

                                        with allure.step('断言页面交易量：{}，数据库交易量：{}'.format(verifyOrder.symbol_closeLsit[i]['Volume'],float(verifyOrder.mysql_symbol_closeOrder[y][5]/100))):
                                            check.equal(verifyOrder.symbol_closeLsit[i]['Volume'],float(verifyOrder.mysql_symbol_closeOrder[y][5]/100),'第{}条数据断言失败：'
                                            '页面订单手数：{}，数据库交易量：{}'.format(i+1,verifyOrder.symbol_closeLsit[i]['Volume'],float(verifyOrder.mysql_symbol_closeOrder[y][5]/100)))
                                        
                                        with allure.step('断言页面商品代码：{}，数据库商品代码：{}'.format(verifyOrder.symbol_closeLsit[i]['Symbol'],verifyOrder.mysql_symbol_closeOrder[y][2])):
                                            check.equal(verifyOrder.symbol_closeLsit[i]['Symbol'],verifyOrder.mysql_symbol_closeOrder[y][2],'第{}条数据断言失败：'
                                            '页面订单商品代码：{}，数据库商品代码：{}'.format(i+1,verifyOrder.symbol_closeLsit[i]['Symbol'],verifyOrder.mysql_symbol_closeOrder[y][2]))
                                        
                                        with allure.step('断言页面开仓价：{}，数据库开仓价：{}'.format(verifyOrder.symbol_closeLsit[i]['Open_price'],verifyOrder.mysql_symbol_closeOrder[y][7])):
                                            check.equal(verifyOrder.symbol_closeLsit[i]['Open_price'],verifyOrder.mysql_symbol_closeOrder[y][7],'第{}条数据断言失败：'
                                            '页面订单开仓价：{}，数据库开仓价：{}'.format(i+1,verifyOrder.symbol_closeLsit[i]['Open_price'],verifyOrder.mysql_symbol_closeOrder[y][7]))

                                        with allure.step('断言页面开仓价：{}，数据库开仓价：{}'.format(verifyOrder.symbol_closeLsit[i]['Close_price'],verifyOrder.mysql_symbol_closeOrder[y][14])):
                                            check.equal(verifyOrder.symbol_closeLsit[i]['Close_price'],verifyOrder.mysql_symbol_closeOrder[y][14],'第{}条数据断言失败：'
                                            '页面订单平仓价：{}，数据库平仓价：{}'.format(i+1,verifyOrder.symbol_closeLsit[i]['Close_price'],verifyOrder.mysql_symbol_closeOrder[y][14]))
                                        
                                        with allure.step('断言页面佣金：{}，数据库佣金：{}'.format(verifyOrder.symbol_closeLsit[i]['Commission'],verifyOrder.mysql_symbol_closeOrder[y][11])):
                                            check.equal(verifyOrder.symbol_closeLsit[i]['Commission'],verifyOrder.mysql_symbol_closeOrder[y][11],'第{}条数据断言失败：'
                                            '页面订单佣金：{}，数据库佣金：{}'.format(i+1,verifyOrder.symbol_closeLsit[i]['Commission'],verifyOrder.mysql_symbol_closeOrder[y][11]))

                                        with allure.step('断言页面隔夜利息：{}，数据库隔夜利息：{}'.format(verifyOrder.symbol_closeLsit[i]['Swaps'],verifyOrder.mysql_symbol_closeOrder[y][13])):
                                            check.equal(verifyOrder.symbol_closeLsit[i]['Swaps'],verifyOrder.mysql_symbol_closeOrder[y][13],'第{}条数据断言失败：'
                                            '页面订单隔夜利息：{}，数据库隔夜利息：{}'.format(i+1,verifyOrder.symbol_closeLsit[i]['Swaps'],verifyOrder.mysql_symbol_closeOrder[y][13]))

                                        with allure.step('断言页面盈亏：{}，数据库盈亏：{}'.format(verifyOrder.symbol_closeLsit[i]['Profit'],verifyOrder.mysql_symbol_closeOrder[y][15])):
                                            check.equal(verifyOrder.symbol_closeLsit[i]['Profit'],verifyOrder.mysql_symbol_closeOrder[y][15],'第{}条数据断言失败：'
                                            '页面订单盈亏：{}，数据库盈亏：{}'.format(i+1,verifyOrder.symbol_closeLsit[i]['Profit'],verifyOrder.mysql_symbol_closeOrder[y][15]))

                                        break
                                else:
                                    pass
            else:
                with allure.step('当前主账号不存在该商品类型的已平仓订单'):
                    check.equal(verifyOrder.symbol_closeLen,0)
                    


if __name__=='__main__':
    # pytest.main(['-s','-v',os.path.abspath(__file__)])
    pytest.main(['-s','-v',os.path.abspath(__file__),
    r'--alluredir={}\report\result'.format(path_project),'--disable-pytest-warnings'])
    os.system(r'allure generate {}\report\result -o {}\report\allure_report --clean'.format(path_project,path_project))
    os.system(r'allure serve {}\report\result'.format(path_project))