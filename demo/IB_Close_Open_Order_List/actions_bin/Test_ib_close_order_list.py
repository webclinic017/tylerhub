'''
Author: tyler
Date: 2022-04-21 10:21:22
LastEditTime: 2022-04-26 18:14:58
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \tylerhub\demo\IB_Close_Open_Order_List\actions_bin\Test_ib_close_order_list.py
'''


import pytest
import os
import allure
import sys
import pytest_check as check
path_public=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'public')
sys.path.append(path_public)
path_project=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(path_project)
sys.path.append(path_project+r'\location')
from about_data import Aboutdata
from read_dataconfig import ReadConfig
from Location_of_ib_close_order_list import Location_of_IB_Close_OrderList


class Test_IB_Open_OrderList(object):
    """
    查询下级已平仓订单并与数据库核对
    查询以下内容：
    指定IB账号下的会员账号的交易账号在查询时间内的已平仓订单数据，并与mysql数据核对；
    某个时间段内，交易类型为买/卖的已平仓订单数据，并与数据库核对；
    根据订单号码查询数据，并与数据库核对；
    复制导出内容与数据库核对
    """
        
    global VerifyOrderyList,conFig,dealData,testdata,excelpath
    VerifyOrderyList=Location_of_IB_Close_OrderList()
    conFig=ReadConfig()
    dealData=Aboutdata()

    #读取测试数据
    excelpath=os.path.join(path_project,r'test_data\search_closeOrder.xlsx')
    rows=dealData.openexcel(excelpath,'Sheet1')
    testdata=dealData.dict_data()

    def setup_class(self):
        #默认谷歌浏览器打开
        VerifyOrderyList.broswertype()
        #cp，bos登录
        VerifyOrderyList.get_url('sit',conFig.get_value('bos_login', 'username'),conFig.get_value('bos_login', 'password'))

    def teardown(self):
        if self.data_index==testdata.index(testdata[-1]):
            VerifyOrderyList.quitbrowser()
        else:
            VerifyOrderyList.closebrowser()

        try:
            os.remove(os.path.join(os.path.join(path_project,'test_data'),'copy_closeOrder.txt'))
            os.remove(os.path.join(os.path.join(path_project,'test_data'),'copy_closeOrder.xlsx'))
            os.remove(os.path.join(os.path.join(path_project,'test_data'),VerifyOrderyList.closeOrder_excel))
        except Exception as msg:
            print('用例跳过或脚本出错请检查代码，未下载相应文件：{}'.format(msg))

    
    @allure.feature('核对IB下级已平仓数据，断言导出与复制功能')
    @allure.story('用例执行')
    @allure.description('读取测试文档数据，执行用例')
    @allure.title('IB下级已平仓订单数据核对报告')
    @pytest.mark.parametrize('data',testdata)
    def test_IB_Order_List(self,data):

        print('当前执行用例账号：{}'.format(int(data['代理账号'])))
        
        with allure.step('获取当前测试数据下标'):
            self.data_index=testdata.index(data)

        with allure.step('查询当前代理账号存在多少个直属/非直属下级'): 
            VerifyOrderyList.search_ib_lower(int(data['代理账号']))
        
        with allure.step('根据代理账号通过BOS登录CP，进入下级已平仓页面'):
            VerifyOrderyList.logincp(int(data['代理账号']))
        
        with allure.step('查询当前代理是否存在下级已平仓订单'):
            
            if VerifyOrderyList.filter_lower_openOrder():
                with allure.step('当前代理存在已级已平仓订单'):

                    for i in VerifyOrderyList.tradeAccount_list2:
                        
                        with allure.step('查询下级主账号 {} 名下交易账号 {} 在 {} 00:00:00~{} 23:59:59 的已平仓订单数据'.format(VerifyOrderyList.
                        deduplication_lower_list[VerifyOrderyList.randomIndex],i,VerifyOrderyList.dateStart,VerifyOrderyList.dateEnd)):
                            
                            with allure.step('判断在该时间段内是否存在已平仓数据'):
                                if VerifyOrderyList.search_period_openOrder(i):
                                    
                                    with allure.step('在该时间段内存在{}条未平仓订单数据'.format(len(VerifyOrderyList.close_orderList))):
                                        
                                        with allure.step('核对页面交易账号：{} 在 {} 00:00:00~{} 23:59:59时间段内的总交易量，总佣金，总隔夜利息，总盈亏'.format(i,VerifyOrderyList.dateStart,VerifyOrderyList.dateEnd)):
                                            with allure.step('页面总交易量：{}，数据库总交易量：{}'.format(VerifyOrderyList.total_Volume,VerifyOrderyList.dataBase_total_Volume)):
                                                check.equal(VerifyOrderyList.total_Volume,VerifyOrderyList.dataBase_total_Volume,
                                                '断言失败：页面总交易量：{}，数据库总交易量：{}'.format(VerifyOrderyList.total_Volume,VerifyOrderyList.dataBase_total_Volume))

                                            with allure.step('页面总佣金：{}，数据库总佣金：{}'.format(VerifyOrderyList.total_Commission,VerifyOrderyList.dataBase_total_Commission)):
                                                check.equal(VerifyOrderyList.total_Commission,VerifyOrderyList.dataBase_total_Commission,
                                                '断言失败：页面总佣金：{}，数据库总佣金：{}'.format(VerifyOrderyList.total_Commission,VerifyOrderyList.dataBase_total_Commission))

                                            with allure.step('页面总利息：{}，数据库总利息：{}'.format('%.2f'%VerifyOrderyList.total_Swaps,'%.2f'%VerifyOrderyList.dataBase_total_Swaps)):
                                                check.equal('%.2f'%VerifyOrderyList.total_Swaps,'%.2f'%VerifyOrderyList.dataBase_total_Swaps,
                                                '断言失败：页面总利息：{}，数据库总利息：{}'.format('%.2f'%VerifyOrderyList.total_Swaps,'%.2f'%VerifyOrderyList.dataBase_total_Swaps))

                                            with allure.step('页面总盈亏：{}，数据库总盈亏：{}'.format('%.2f'%VerifyOrderyList.total_Profit,'%.2f'%VerifyOrderyList.dataBase_total_Profit)):
                                                check.equal('%.2f'%VerifyOrderyList.total_Profit,'%.2f'%VerifyOrderyList.dataBase_total_Profit,
                                                '断言失败：页面总盈亏：{}，数据库总盈亏：{}'.format('%.2f'%VerifyOrderyList.total_Profit,'%.2f'%VerifyOrderyList.dataBase_total_Profit))                                        
                                        
                                        for y in range(0,len(VerifyOrderyList.close_orderList)):
                                            
                                            with allure.step('断言页面订单号码{}与数据库订单号码{}：'.format(VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.mysql_closeOrder[y]['Ticket'])):
                                                check.equal(VerifyOrderyList.close_orderList[y]['Ticket'], VerifyOrderyList.mysql_closeOrder[y]['Ticket'],
                                                '第{}条数据断言失败：页面订单号码：{}，数据库订单号码：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.mysql_closeOrder[y]['Ticket']))
                                                
                                                with allure.step('断言页面交易账号：{}，数据库交易账号：{}'.format(VerifyOrderyList.close_orderList[y]['Login'], VerifyOrderyList.mysql_closeOrder[y]['Login'])):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Login'], VerifyOrderyList.mysql_closeOrder[y]['Login'],
                                                    '第{}条数据断言失败：页面订单号码：{},页面交易账号：{}，数据库交易账号：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Login'], VerifyOrderyList.mysql_closeOrder[y]['Login']))
                                                
                                                with allure.step('断言页面开仓时间：{}，数据库开仓时间：{}'.format(VerifyOrderyList.close_orderList[y]['Open_Time'], VerifyOrderyList.mysql_closeOrder[y]['Open_Time'])):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Open_Time'], VerifyOrderyList.mysql_closeOrder[y]['Open_Time'],
                                                    '第{}条数据断言失败：页面订单号码：{},页面开仓时间：{}，数据库开仓时间：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Open_Time'],VerifyOrderyList.mysql_closeOrder[y]['Open_Time']))    
                                                
                                                with allure.step('断言页面平仓时间：{}，数据库平仓时间：{}'.format(VerifyOrderyList.close_orderList[y]['Close_Time'], VerifyOrderyList.mysql_closeOrder[y]['Close_Time'])):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Close_Time'], VerifyOrderyList.mysql_closeOrder[y]['Close_Time'],
                                                    '第{}条数据断言失败：页面订单号码：{},页面平仓时间：{}，数据库平仓时间：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Close_Time'],VerifyOrderyList.mysql_closeOrder[y]['Close_Time'])) 
                                                
                                                with allure.step('断言页面交易量：{}，数据库交易量：{}'.format(VerifyOrderyList.close_orderList[y]['Volume'], float(VerifyOrderyList.mysql_closeOrder[y]['Volume']/100))):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Volume'], float(VerifyOrderyList.mysql_closeOrder[y]['Volume']/100),
                                                    '第{}条数据断言失败：页面订单号码：{},页面交易量：{}，数据库交易量：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Volume'],float(VerifyOrderyList.mysql_closeOrder[y]['Volume']/100))) 

                                                with allure.step('断言页面商品代码：{}，数据库商品代码：{}'.format(VerifyOrderyList.close_orderList[y]['Symbol'], VerifyOrderyList.mysql_closeOrder[y]['Symbol'])):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Symbol'], VerifyOrderyList.mysql_closeOrder[y]['Symbol'],
                                                    '第{}条数据断言失败：页面订单号码：{},页面商品代码：{}，数据库商品代码：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Symbol'],VerifyOrderyList.mysql_closeOrder[y]['Symbol'])) 

                                                with allure.step('断言页面开仓价：{}，数据库开仓价：{}'.format(VerifyOrderyList.close_orderList[y]['Open_Price'], VerifyOrderyList.mysql_closeOrder[y]['Open_Price'])):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Open_Price'], VerifyOrderyList.mysql_closeOrder[y]['Open_Price'],
                                                    '第{}条数据断言失败：页面订单号码：{},页面开仓价：{}，数据库开仓价：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Open_Price'],VerifyOrderyList.mysql_closeOrder[y]['Open_Price'])) 

                                                with allure.step('断言页面平仓价：{}，数据库平仓价：{}'.format(VerifyOrderyList.close_orderList[y]['Close_Price'], VerifyOrderyList.mysql_closeOrder[y]['Close_Price'])):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Close_Price'], VerifyOrderyList.mysql_closeOrder[y]['Close_Price'],
                                                    '第{}条数据断言失败：页面订单号码：{},页面平仓价：{}，数据库平仓价：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Close_Price'],VerifyOrderyList.mysql_closeOrder[y]['Close_Price']))                                                 
                                                
                                                with allure.step('断言页面佣金：{}，数据库佣金：{}'.format(VerifyOrderyList.close_orderList[y]['Commission'], VerifyOrderyList.mysql_closeOrder[y]['Commission'])):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Commission'], VerifyOrderyList.mysql_closeOrder[y]['Commission'],
                                                    '第{}条数据断言失败：页面订单号码：{},页面佣金：{}，数据库佣金：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Commission'],VerifyOrderyList.mysql_closeOrder[y]['Commission'])) 

                                                with allure.step('断言页面隔夜利息：{}，数据库隔夜利息：{}'.format(VerifyOrderyList.close_orderList[y]['Swaps'], VerifyOrderyList.mysql_closeOrder[y]['Swaps'])):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Swaps'], VerifyOrderyList.mysql_closeOrder[y]['Swaps'],
                                                    '第{}条数据断言失败：页面订单号码：{},页面隔夜利息：{}，数据库隔夜利息：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Swaps'],VerifyOrderyList.mysql_closeOrder[y]['Swaps']))                             

                                                with allure.step('断言页面盈亏：{}，数据库盈亏：{}'.format(VerifyOrderyList.close_orderList[y]['Profit'], VerifyOrderyList.mysql_closeOrder[y]['Profit'])):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Profit'], VerifyOrderyList.mysql_closeOrder[y]['Profit'],
                                                    '第{}条数据断言失败：页面订单号码：{},页面盈亏：{}，数据库盈亏：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Profit'],VerifyOrderyList.mysql_closeOrder[y]['Profit']))
                                
                                else:
                                    with allure.step('在该时间段内部存在已平仓订单，断言数据库查询数据是否为空'):
                                        check.equal(VerifyOrderyList.close_order_len, len(VerifyOrderyList.mysql_closeOrder),
                                        '断言失败，页面数据{}条，数据库数据{}条'.format(VerifyOrderyList.close_order_len,len(VerifyOrderyList.mysql_closeOrder)))
                        
                        
                        with allure.step('查询下级主账号 {} 名下交易账号 {} 在 {} 00:00:00~{} 23:59:59 类型为买/卖的已平仓订单数据'.format(VerifyOrderyList.
                        deduplication_lower_list[VerifyOrderyList.randomIndex],i,VerifyOrderyList.dateStart,VerifyOrderyList.dateEnd)):                           
                            
                            with allure.step('判断在该时间段内是否存在类型为买/卖的已平仓数据'):
                                
                                if VerifyOrderyList.search_buyOrSale_openOrder(i):

                                    with allure.step('在该时间段内存在{}条类型为{}的已平仓订单数据'.format(len(VerifyOrderyList.close_orderList),VerifyOrderyList.tradeType)):
                                        
                                        with allure.step('核对页面交易账号：{} 在 {} 00:00:00~{} 23:59:59时间段内的总交易量，总佣金，总隔夜利息，总盈亏'.format(i,VerifyOrderyList.dateStart,VerifyOrderyList.dateEnd)): 
                                            
                                            with allure.step('页面总交易量：{}，数据库总交易量：{}'.format(VerifyOrderyList.total_Volume,VerifyOrderyList.dataBase_total_Volume)):
                                                check.equal(VerifyOrderyList.total_Volume,VerifyOrderyList.dataBase_total_Volume,
                                                '断言失败：页面总交易量：{}，数据库总交易量：{}'.format(VerifyOrderyList.total_Volume,VerifyOrderyList.dataBase_total_Volume))

                                            with allure.step('页面总佣金：{}，数据库总佣金：{}'.format(VerifyOrderyList.total_Commission,VerifyOrderyList.dataBase_total_Commission)):
                                                check.equal(VerifyOrderyList.total_Commission,VerifyOrderyList.dataBase_total_Commission,
                                                '断言失败：页面总佣金：{}，数据库总佣金：{}'.format(VerifyOrderyList.total_Commission,VerifyOrderyList.dataBase_total_Commission))

                                            with allure.step('页面总利息：{}，数据库总利息：{}'.format('%.2f'%VerifyOrderyList.total_Swaps,'%.2f'%VerifyOrderyList.dataBase_total_Swaps)):
                                                check.equal('%.2f'%VerifyOrderyList.total_Swaps,'%.2f'%VerifyOrderyList.dataBase_total_Swaps,
                                                '断言失败：页面总利息：{}，数据库总利息：{}'.format('%.2f'%VerifyOrderyList.total_Swaps,'%.2f'%VerifyOrderyList.dataBase_total_Swaps))

                                            with allure.step('页面总盈亏：{}，数据库总盈亏：{}'.format('%.2f'%VerifyOrderyList.total_Profit,'%.2f'%VerifyOrderyList.dataBase_total_Profit)):
                                                check.equal('%.2f'%VerifyOrderyList.total_Profit,'%.2f'%VerifyOrderyList.dataBase_total_Profit,
                                                    '断言失败：页面总盈亏：{}，数据库总盈亏：{}'.format('%.2f'%VerifyOrderyList.total_Profit,'%.2f'%VerifyOrderyList.dataBase_total_Profit))
                                        
                                        for y in range(0,len(VerifyOrderyList.close_orderList)):
                                            
                                            with allure.step('断言页面订单号码{}与数据库订单号码{}：'.format(VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.mysql_closeOrder[y]['Ticket'])):
                                                check.equal(VerifyOrderyList.close_orderList[y]['Ticket'], VerifyOrderyList.mysql_closeOrder[y]['Ticket'],
                                                '第{}条数据断言失败：页面订单号码：{}，数据库订单号码：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.mysql_closeOrder[y]['Ticket']))
                                                
                                                with allure.step('断言页面交易账号：{}，数据库交易账号：{}'.format(VerifyOrderyList.close_orderList[y]['Login'], VerifyOrderyList.mysql_closeOrder[y]['Login'])):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Login'], VerifyOrderyList.mysql_closeOrder[y]['Login'],
                                                    '第{}条数据断言失败：页面订单号码：{},页面交易账号：{}，数据库交易账号：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Login'], VerifyOrderyList.mysql_closeOrder[y]['Login']))
                                                
                                                with allure.step('断言页面开仓时间：{}，数据库开仓时间：{}'.format(VerifyOrderyList.close_orderList[y]['Open_Time'], VerifyOrderyList.mysql_closeOrder[y]['Open_Time'])):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Open_Time'], VerifyOrderyList.mysql_closeOrder[y]['Open_Time'],
                                                    '第{}条数据断言失败：页面订单号码：{},页面开仓时间：{}，数据库开仓时间：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Open_Time'],VerifyOrderyList.mysql_closeOrder[y]['Open_Time']))    
                                                
                                                with allure.step('断言页面平仓时间：{}，数据库平仓时间：{}'.format(VerifyOrderyList.close_orderList[y]['Close_Time'], VerifyOrderyList.mysql_closeOrder[y]['Close_Time'])):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Close_Time'], VerifyOrderyList.mysql_closeOrder[y]['Close_Time'],
                                                    '第{}条数据断言失败：页面订单号码：{},页面平仓时间：{}，数据库平仓时间：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Close_Time'],VerifyOrderyList.mysql_closeOrder[y]['Close_Time'])) 
                                                
                                                with allure.step('断言页面交易量：{}，数据库交易量：{}'.format(VerifyOrderyList.close_orderList[y]['Volume'], float(VerifyOrderyList.mysql_closeOrder[y]['Volume']/100))):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Volume'], float(VerifyOrderyList.mysql_closeOrder[y]['Volume']/100),
                                                    '第{}条数据断言失败：页面订单号码：{},页面交易量：{}，数据库交易量：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Volume'],float(VerifyOrderyList.mysql_closeOrder[y]['Volume']/100))) 

                                                with allure.step('断言页面商品代码：{}，数据库商品代码：{}'.format(VerifyOrderyList.close_orderList[y]['Symbol'], VerifyOrderyList.mysql_closeOrder[y]['Symbol'])):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Symbol'], VerifyOrderyList.mysql_closeOrder[y]['Symbol'],
                                                    '第{}条数据断言失败：页面订单号码：{},页面商品代码：{}，数据库商品代码：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Symbol'],VerifyOrderyList.mysql_closeOrder[y]['Symbol'])) 

                                                with allure.step('断言页面开仓价：{}，数据库开仓价：{}'.format(VerifyOrderyList.close_orderList[y]['Open_Price'], VerifyOrderyList.mysql_closeOrder[y]['Open_Price'])):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Open_Price'], VerifyOrderyList.mysql_closeOrder[y]['Open_Price'],
                                                    '第{}条数据断言失败：页面订单号码：{},页面开仓价：{}，数据库开仓价：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Open_Price'],VerifyOrderyList.mysql_closeOrder[y]['Open_Price'])) 

                                                with allure.step('断言页面平仓价：{}，数据库平仓价：{}'.format(VerifyOrderyList.close_orderList[y]['Close_Price'], VerifyOrderyList.mysql_closeOrder[y]['Close_Price'])):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Close_Price'], VerifyOrderyList.mysql_closeOrder[y]['Close_Price'],
                                                    '第{}条数据断言失败：页面订单号码：{},页面平仓价：{}，数据库平仓价：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Close_Price'],VerifyOrderyList.mysql_closeOrder[y]['Close_Price']))                                                 
                                                
                                                with allure.step('断言页面佣金：{}，数据库佣金：{}'.format(VerifyOrderyList.close_orderList[y]['Commission'], VerifyOrderyList.mysql_closeOrder[y]['Commission'])):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Commission'], VerifyOrderyList.mysql_closeOrder[y]['Commission'],
                                                    '第{}条数据断言失败：页面订单号码：{},页面佣金：{}，数据库佣金：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Commission'],VerifyOrderyList.mysql_closeOrder[y]['Commission'])) 

                                                with allure.step('断言页面隔夜利息：{}，数据库隔夜利息：{}'.format(VerifyOrderyList.close_orderList[y]['Swaps'], VerifyOrderyList.mysql_closeOrder[y]['Swaps'])):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Swaps'], VerifyOrderyList.mysql_closeOrder[y]['Swaps'],
                                                    '第{}条数据断言失败：页面订单号码：{},页面隔夜利息：{}，数据库隔夜利息：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Swaps'],VerifyOrderyList.mysql_closeOrder[y]['Swaps']))                             

                                                with allure.step('断言页面盈亏：{}，数据库盈亏：{}'.format(VerifyOrderyList.close_orderList[y]['Profit'], VerifyOrderyList.mysql_closeOrder[y]['Profit'])):
                                                    check.equal(VerifyOrderyList.close_orderList[y]['Profit'], VerifyOrderyList.mysql_closeOrder[y]['Profit'],
                                                    '第{}条数据断言失败：页面订单号码：{},页面盈亏：{}，数据库盈亏：{}'.format(y+1,VerifyOrderyList.close_orderList[y]['Ticket'],VerifyOrderyList.close_orderList[y]['Profit'],VerifyOrderyList.mysql_closeOrder[y]['Profit']))                               
                                
                                else:
                                    with allure.step('在该时间段内不存在类型为{}的未平仓订单数据,断言数据库查询数据是否为空'.format(VerifyOrderyList.tradeType)):
                                        check.equal(VerifyOrderyList.close_order_len, len(VerifyOrderyList.mysql_closeOrder),
                                        '断言失败，页面数据{}条，数据库数据{}条'.format(VerifyOrderyList.close_order_len, len(VerifyOrderyList.mysql_closeOrder)))
                    
                with allure.step('根据订单号码查询已平仓订单，核对数据库数据'):  
                    VerifyOrderyList.search_ticket_openOrder(int(data['订单号码']))
                    
                    with allure.step('断言订单号码{}与数据库数据'.format(int(data['订单号码']))):
                        
                        with allure.step('断言页面交易账号：{}，数据库交易账号：{}'.format(VerifyOrderyList.close_orderDict['Login'], VerifyOrderyList.mysql_closeOrder[0]['Login'])):
                            check.equal(VerifyOrderyList.close_orderDict['Login'], VerifyOrderyList.mysql_closeOrder[0]['Login'],
                            '断言失败：页面交易账号：{}，数据库交易账号：{}'.format(VerifyOrderyList.close_orderDict['Login'],VerifyOrderyList.mysql_closeOrder[0]['Login']))

                        with allure.step('断言页面开仓时间：{}，数据库开仓时间：{}'.format(VerifyOrderyList.close_orderDict['Open_Time'], VerifyOrderyList.mysql_closeOrder[0]['Open_Time'])):
                            check.equal(VerifyOrderyList.close_orderDict['Open_Time'], VerifyOrderyList.mysql_closeOrder[0]['Open_Time'],
                            '断言失败：页面开仓时间：{}，数据库开仓时间：{}'.format(VerifyOrderyList.close_orderDict['Open_Time'],VerifyOrderyList.mysql_closeOrder[0]['Open_Time']))    
                                                
                        with allure.step('断言页面平仓时间：{}，数据库平仓时间：{}'.format(VerifyOrderyList.close_orderDict['Close_Time'], VerifyOrderyList.mysql_closeOrder[0]['Close_Time'])):
                            check.equal(VerifyOrderyList.close_orderDict['Close_Time'], VerifyOrderyList.mysql_closeOrder[0]['Close_Time'],
                            '断言失败：页面平仓时间：{}，数据库平仓时间：{}'.format(VerifyOrderyList.close_orderDict['Close_Time'],VerifyOrderyList.mysql_closeOrder[0]['Close_Time']))                          
                        
                        with allure.step('断言页面交易量：{}，数据库交易量：{}'.format(VerifyOrderyList.close_orderDict['Volume'], float(VerifyOrderyList.mysql_closeOrder[0]['Volume']/100))):
                            check.equal(VerifyOrderyList.close_orderDict['Volume'], float(VerifyOrderyList.mysql_closeOrder[0]['Volume']/100),
                            '断言失败：页面交易量：{}，数据库交易量：{}'.format(VerifyOrderyList.close_orderDict['Volume'],float(VerifyOrderyList.mysql_closeOrder[0]['Volume']/100))) 

                        with allure.step('断言页面商品代码：{}，数据库商品代码：{}'.format(VerifyOrderyList.close_orderDict['Symbol'], VerifyOrderyList.mysql_closeOrder[0]['Symbol'])):
                            check.equal(VerifyOrderyList.close_orderDict['Symbol'], VerifyOrderyList.mysql_closeOrder[0]['Symbol'],
                            '断言失败：页面商品代码：{}，数据库商品代码：{}'.format(VerifyOrderyList.close_orderDict['Symbol'],VerifyOrderyList.mysql_closeOrder[0]['Symbol'])) 

                        with allure.step('断言页面开仓价：{}，数据库开仓价：{}'.format(VerifyOrderyList.close_orderDict['Open_Price'], VerifyOrderyList.mysql_closeOrder[0]['Open_Price'])):
                            check.equal(VerifyOrderyList.close_orderDict['Open_Price'], VerifyOrderyList.mysql_closeOrder[0]['Open_Price'],
                            '断言失败：页面开仓价：{}，数据库开仓价：{}'.format(VerifyOrderyList.close_orderDict['Open_Price'],VerifyOrderyList.mysql_closeOrder[0]['Open_Price'])) 

                        with allure.step('断言页面平仓价：{}，数据库平仓价：{}'.format(VerifyOrderyList.close_orderDict['Close_Price'], VerifyOrderyList.mysql_closeOrder[0]['Close_Price'])):
                            check.equal(VerifyOrderyList.close_orderDict['Close_Price'], VerifyOrderyList.mysql_closeOrder[0]['Close_Price'],
                            '断言失败：页面平仓价：{}，数据库平仓价：{}'.format(VerifyOrderyList.close_orderDict['Close_Price'],VerifyOrderyList.mysql_closeOrder[0]['Close_Price']))                         
                        
                        with allure.step('断言页面佣金：{}，数据库佣金：{}'.format(VerifyOrderyList.close_orderDict['Commission'], VerifyOrderyList.mysql_closeOrder[0]['Commission'])):
                            check.equal(VerifyOrderyList.close_orderDict['Commission'], VerifyOrderyList.mysql_closeOrder[0]['Commission'],
                            '断言失败：页面佣金：{}，数据库佣金：{}'.format(VerifyOrderyList.close_orderDict['Commission'],VerifyOrderyList.mysql_closeOrder[0]['Commission'])) 

                        with allure.step('断言页面隔夜利息：{}，数据库隔夜利息：{}'.format(VerifyOrderyList.close_orderDict['Swaps'], VerifyOrderyList.mysql_closeOrder[0]['Swaps'])):
                            check.equal(VerifyOrderyList.close_orderDict['Swaps'], VerifyOrderyList.mysql_closeOrder[0]['Swaps'],
                            '断言失败：页面隔夜利息：{}，数据库隔夜利息：{}'.format(VerifyOrderyList.close_orderDict['Swaps'],VerifyOrderyList.mysql_closeOrder[0]['Swaps'])) 
                        
                        with allure.step('断言页面盈亏：{}，数据库盈亏：{}'.format(VerifyOrderyList.close_orderDict['Profit'], VerifyOrderyList.mysql_closeOrder[0]['Profit'])):
                            check.equal(VerifyOrderyList.close_orderDict['Profit'], VerifyOrderyList.mysql_closeOrder[0]['Profit'],
                            '断言失败：页面盈亏：{}，数据库盈亏：{}'.format(VerifyOrderyList.close_orderDict['Profit'],VerifyOrderyList.mysql_closeOrder[0]['Profit']))                         
                    
  
                with allure.step('断言页面导出与复制功能是否与数据库数据一致'):    
                    VerifyOrderyList.copy_close_export_OrderList(VerifyOrderyList.tradeAccount_list2[0])
                    
                    with allure.step('断言复制功能'):
                        for i in range(0,len(VerifyOrderyList.closeOrder_data)):
                            with allure.step('断言复制订单号：{}，数据库订单号：{}'.format(int(VerifyOrderyList.closeOrder_data[i]['订单号码']),VerifyOrderyList.mysql_closeOrder[i]['Ticket'])):
                                check.equal(int(VerifyOrderyList.closeOrder_data[i]['订单号码']),VerifyOrderyList.mysql_closeOrder[i]['Ticket'],
                                '第{}条数据断言失败：复制订单号码：{}，数据库订单号码：{}'.format(i+1,int(VerifyOrderyList.closeOrder_data[i]['订单号码']),VerifyOrderyList.mysql_closeOrder[i]['Ticket']))

                                with allure.step('断言复制交易账号：{}，数据库交易账号：{}'.format(int(VerifyOrderyList.closeOrder_data[i]['交易账号']),VerifyOrderyList.mysql_closeOrder[i]['Login'])):
                                    check.equal(int(VerifyOrderyList.closeOrder_data[i]['交易账号']),VerifyOrderyList.mysql_closeOrder[i]['Login'],
                                    '第{}条数据断言失败：订单号：{}，复制交易账号：{}，数据库交易账号：{}'.format(i+1,int(VerifyOrderyList.closeOrder_data[i]['订单号码']),int(VerifyOrderyList.closeOrder_data[i]['交易账号']),VerifyOrderyList.mysql_closeOrder[i]['Login']))

                                with allure.step('断言复制开仓时间：{}，数据库开仓时间：{}'.format(VerifyOrderyList.closeOrder_data[i]['开仓时间'],VerifyOrderyList.mysql_closeOrder[i]['Open_Time'].strftime('%Y-%m-%d %H:%M:%S'))):
                                    check.equal(VerifyOrderyList.closeOrder_data[i]['开仓时间'],VerifyOrderyList.mysql_closeOrder[i]['Open_Time'].strftime('%Y-%m-%d %H:%M:%S'),
                                    '第{}条数据断言失败：订单号：{}，复制开仓时间：{}，数据库开仓时间：{}'.format(i+1,int(VerifyOrderyList.closeOrder_data[i]['订单号码']),VerifyOrderyList.closeOrder_data[i]['开仓时间'],VerifyOrderyList.mysql_closeOrder[i]['Open_Time'].strftime('%Y-%m-%d %H:%M:%S')))

                                with allure.step('断言复制平仓时间：{}，数据库平仓时间：{}'.format(VerifyOrderyList.closeOrder_data[i]['平仓时间'],VerifyOrderyList.mysql_closeOrder[i]['Close_Time'].strftime('%Y-%m-%d %H:%M:%S'))):
                                    check.equal(VerifyOrderyList.closeOrder_data[i]['平仓时间'],VerifyOrderyList.mysql_closeOrder[i]['Close_Time'].strftime('%Y-%m-%d %H:%M:%S'),
                                    '第{}条数据断言失败：订单号：{}，复制平仓时间：{}，数据库平仓时间：{}'.format(i+1,int(VerifyOrderyList.closeOrder_data[i]['订单号码']),VerifyOrderyList.closeOrder_data[i]['开仓时间'],VerifyOrderyList.mysql_closeOrder[i]['Close_Time'].strftime('%Y-%m-%d %H:%M:%S')))                                
                                
                                with allure.step('断言复制交易量：{}，数据库交易量：{}'.format(float(VerifyOrderyList.closeOrder_data[i]['手数']),VerifyOrderyList.mysql_closeOrder[i]['Volume']/100)):
                                    check.equal(float(VerifyOrderyList.closeOrder_data[i]['手数']),VerifyOrderyList.mysql_closeOrder[i]['Volume']/100,
                                    '第{}条数据断言失败：订单号：{}，复制交易量：{}，数据库交易量：{}'.format(i+1,int(VerifyOrderyList.closeOrder_data[i]['订单号码']),float(VerifyOrderyList.closeOrder_data[i]['手数']),VerifyOrderyList.mysql_closeOrder[i]['Volume']/100))

                                with allure.step('断言复制商品代码：{}，数据库商品代码：{}'.format(VerifyOrderyList.closeOrder_data[i]['商品代码'],VerifyOrderyList.mysql_closeOrder[i]['Symbol'])):
                                    check.equal(VerifyOrderyList.closeOrder_data[i]['商品代码'],VerifyOrderyList.mysql_closeOrder[i]['Symbol'],
                                    '第{}条数据断言失败：订单号：{}，复制商品代码：{}，数据库商品代码：{}'.format(i+1,int(VerifyOrderyList.closeOrder_data[i]['订单号码']),VerifyOrderyList.closeOrder_data[i]['商品代码'],VerifyOrderyList.mysql_closeOrder[i]['Symbol']))

                                with allure.step('断言复制开仓价：{}，数据库开仓价：{}'.format(float(VerifyOrderyList.closeOrder_data[i]['开仓价']),VerifyOrderyList.mysql_closeOrder[i]['Open_Price'])):
                                    check.equal(float(VerifyOrderyList.closeOrder_data[i]['开仓价']),VerifyOrderyList.mysql_closeOrder[i]['Open_Price'],
                                    '第{}条数据断言失败：订单号：{}，复制开仓价：{}，数据库开仓价：{}'.format(i+1,int(VerifyOrderyList.closeOrder_data[i]['订单号码']),float(VerifyOrderyList.closeOrder_data[i]['开仓价']),VerifyOrderyList.mysql_closeOrder[i]['Open_Price']))

                                with allure.step('断言复制平仓价格：{}，数据库平仓价格：{}'.format(float(VerifyOrderyList.closeOrder_data[i]['平仓价格']),VerifyOrderyList.mysql_closeOrder[i]['Close_Price'])):
                                    check.equal(float(VerifyOrderyList.closeOrder_data[i]['平仓价格']),VerifyOrderyList.mysql_closeOrder[i]['Close_Price'],
                                    '第{}条数据断言失败：订单号：{}，复制平仓价格：{}，数据库平仓价格：{}'.format(i+1,int(VerifyOrderyList.closeOrder_data[i]['订单号码']),float(VerifyOrderyList.closeOrder_data[i]['平仓价格']),VerifyOrderyList.mysql_closeOrder[i]['Close_Price']))                                
                                
                                with allure.step('断言复制佣金：{}，数据库佣金：{}'.format(float(VerifyOrderyList.closeOrder_data[i]['佣金']),VerifyOrderyList.mysql_closeOrder[i]['Commission'])):
                                    check.equal(float(VerifyOrderyList.closeOrder_data[i]['佣金']),VerifyOrderyList.mysql_closeOrder[i]['Commission'],
                                    '第{}条数据断言失败：订单号：{}，复制佣金：{}，数据库佣金：{}'.format(i+1,int(VerifyOrderyList.closeOrder_data[i]['订单号码']),float(VerifyOrderyList.closeOrder_data[i]['佣金']),VerifyOrderyList.mysql_closeOrder[i]['Commission']))

                                with allure.step('断言复制隔夜利息：{}，数据库隔夜利息：{}'.format(float(VerifyOrderyList.closeOrder_data[i]['隔夜利息']),VerifyOrderyList.mysql_closeOrder[i]['Swaps'])):
                                    check.equal(float(VerifyOrderyList.closeOrder_data[i]['隔夜利息']),VerifyOrderyList.mysql_closeOrder[i]['Swaps'],
                                    '第{}条数据断言失败：订单号：{}，复制隔夜利息：{}，数据库隔夜利息：{}'.format(i+1,int(VerifyOrderyList.closeOrder_data[i]['订单号码']),float(VerifyOrderyList.closeOrder_data[i]['隔夜利息']),VerifyOrderyList.mysql_closeOrder[i]['Swaps']))

                                with allure.step('断言复制盈亏：{}，数据库盈亏：{}'.format(float(VerifyOrderyList.closeOrder_data[i]['盈亏']),VerifyOrderyList.mysql_closeOrder[i]['Profit'])):
                                    check.equal(float(VerifyOrderyList.closeOrder_data[i]['盈亏']),VerifyOrderyList.mysql_closeOrder[i]['Profit'],
                                    '第{}条数据断言失败：订单号：{}，复制盈亏：{}，数据库盈亏：{}'.format(i+1,int(VerifyOrderyList.closeOrder_data[i]['订单号码']),float(VerifyOrderyList.closeOrder_data[i]['盈亏']),VerifyOrderyList.mysql_closeOrder[i]['Profit']))

                    
                    with allure.step('断言导出功能'):
                        for i in range(0,len(VerifyOrderyList.closeOrderexcel_data)):                             
                            with allure.step('断言导出订单号：{}，数据库订单号：{}'.format(int(VerifyOrderyList.closeOrderexcel_data[i]['订单号码']),VerifyOrderyList.mysql_closeOrder[i]['Ticket'])):
                                check.equal(int(VerifyOrderyList.closeOrderexcel_data[i]['订单号码']),VerifyOrderyList.mysql_closeOrder[i]['Ticket'],
                                '第{}条数据断言失败：导出订单号码：{}，数据库订单号码：{}'.format(i+1,int(VerifyOrderyList.closeOrderexcel_data[i]['订单号码']),VerifyOrderyList.mysql_closeOrder[i]['Ticket']))

                                with allure.step('断言导出交易账号：{}，数据库交易账号：{}'.format(int(VerifyOrderyList.closeOrderexcel_data[i]['交易账号']),VerifyOrderyList.mysql_closeOrder[i]['Login'])):
                                    check.equal(int(VerifyOrderyList.closeOrderexcel_data[i]['交易账号']),VerifyOrderyList.mysql_closeOrder[i]['Login'],
                                    '第{}条数据断言失败：订单号：{}，导出交易账号：{}，数据库交易账号：{}'.format(i+1,int(VerifyOrderyList.closeOrderexcel_data[i]['订单号码']),int(VerifyOrderyList.closeOrder_data[i]['交易账号']),VerifyOrderyList.mysql_closeOrder[i]['Login']))

                                with allure.step('断言导出开仓时间：{}，数据库开仓时间：{}'.format(VerifyOrderyList.closeOrderexcel_data[i]['开仓时间'],VerifyOrderyList.mysql_closeOrder[i]['Open_Time'].strftime('%Y-%m-%d %H:%M:%S'))):
                                    check.equal(VerifyOrderyList.closeOrderexcel_data[i]['开仓时间'],VerifyOrderyList.mysql_closeOrder[i]['Open_Time'].strftime('%Y-%m-%d %H:%M:%S'),
                                    '第{}条数据断言失败：订单号：{}，导出开仓时间：{}，数据库开仓时间：{}'.format(i+1,int(VerifyOrderyList.closeOrderexcel_data[i]['订单号码']),VerifyOrderyList.closeOrder_data[i]['开仓时间'],VerifyOrderyList.mysql_closeOrder[i]['Open_Time'].strftime('%Y-%m-%d %H:%M:%S')))

                                with allure.step('断言导出平仓时间：{}，数据库平仓时间：{}'.format(VerifyOrderyList.closeOrderexcel_data[i]['平仓时间'],VerifyOrderyList.mysql_closeOrder[i]['Close_Time'].strftime('%Y-%m-%d %H:%M:%S'))):
                                    check.equal(VerifyOrderyList.closeOrderexcel_data[i]['平仓时间'],VerifyOrderyList.mysql_closeOrder[i]['Close_Time'].strftime('%Y-%m-%d %H:%M:%S'),
                                    '第{}条数据断言失败：订单号：{}，导出平仓时间：{}，数据库平仓时间：{}'.format(i+1,int(VerifyOrderyList.closeOrderexcel_data[i]['订单号码']),VerifyOrderyList.closeOrder_data[i]['开仓时间'],VerifyOrderyList.mysql_closeOrder[i]['Close_Time'].strftime('%Y-%m-%d %H:%M:%S')))                                
                                
                                with allure.step('断言导出交易量：{}，数据库交易量：{}'.format(float(VerifyOrderyList.closeOrderexcel_data[i]['手数']),VerifyOrderyList.mysql_closeOrder[i]['Volume']/100)):
                                    check.equal(float(VerifyOrderyList.closeOrderexcel_data[i]['手数']),VerifyOrderyList.mysql_closeOrder[i]['Volume']/100,
                                    '第{}条数据断言失败：订单号：{}，导出交易量：{}，数据库交易量：{}'.format(i+1,int(VerifyOrderyList.closeOrderexcel_data[i]['订单号码']),float(VerifyOrderyList.closeOrder_data[i]['手数']),VerifyOrderyList.mysql_closeOrder[i]['Volume']/100))

                                with allure.step('断言导出商品代码：{}，数据库商品代码：{}'.format(VerifyOrderyList.closeOrderexcel_data[i]['商品代码'],VerifyOrderyList.mysql_closeOrder[i]['Symbol'])):
                                    check.equal(VerifyOrderyList.closeOrderexcel_data[i]['商品代码'],VerifyOrderyList.mysql_closeOrder[i]['Symbol'],
                                    '第{}条数据断言失败：订单号：{}，导出商品代码：{}，数据库商品代码：{}'.format(i+1,int(VerifyOrderyList.closeOrderexcel_data[i]['订单号码']),VerifyOrderyList.closeOrder_data[i]['商品代码'],VerifyOrderyList.mysql_closeOrder[i]['Symbol']))

                                with allure.step('断言导出开仓价：{}，数据库开仓价：{}'.format(float(VerifyOrderyList.closeOrderexcel_data[i]['开仓价']),VerifyOrderyList.mysql_closeOrder[i]['Open_Price'])):
                                    check.equal(float(VerifyOrderyList.closeOrderexcel_data[i]['开仓价']),VerifyOrderyList.mysql_closeOrder[i]['Open_Price'],
                                    '第{}条数据断言失败：订单号：{}，导出开仓价：{}，数据库开仓价：{}'.format(i+1,int(VerifyOrderyList.closeOrderexcel_data[i]['订单号码']),float(VerifyOrderyList.closeOrder_data[i]['开仓价']),VerifyOrderyList.mysql_closeOrder[i]['Open_Price']))

                                with allure.step('断言导出平仓价格：{}，数据库平仓价格：{}'.format(float(VerifyOrderyList.closeOrderexcel_data[i]['平仓价格']),VerifyOrderyList.mysql_closeOrder[i]['Close_Price'])):
                                    check.equal(float(VerifyOrderyList.closeOrderexcel_data[i]['平仓价格']),VerifyOrderyList.mysql_closeOrder[i]['Close_Price'],
                                    '第{}条数据断言失败：订单号：{}，导出平仓价格：{}，数据库平仓价格：{}'.format(i+1,int(VerifyOrderyList.closeOrderexcel_data[i]['订单号码']),float(VerifyOrderyList.closeOrder_data[i]['平仓价格']),VerifyOrderyList.mysql_closeOrder[i]['Close_Price']))                                
                                
                                with allure.step('断言导出佣金：{}，数据库佣金：{}'.format(float(VerifyOrderyList.closeOrderexcel_data[i]['佣金']),VerifyOrderyList.mysql_closeOrder[i]['Commission'])):
                                    check.equal(float(VerifyOrderyList.closeOrderexcel_data[i]['佣金']),VerifyOrderyList.mysql_closeOrder[i]['Commission'],
                                    '第{}条数据断言失败：订单号：{}，导出佣金：{}，数据库佣金：{}'.format(i+1,int(VerifyOrderyList.closeOrderexcel_data[i]['订单号码']),float(VerifyOrderyList.closeOrder_data[i]['佣金']),VerifyOrderyList.mysql_closeOrder[i]['Commission']))

                                with allure.step('断言导出隔夜利息：{}，数据库隔夜利息：{}'.format(float(VerifyOrderyList.closeOrderexcel_data[i]['隔夜利息']),VerifyOrderyList.mysql_closeOrder[i]['Swaps'])):
                                    check.equal(float(VerifyOrderyList.closeOrderexcel_data[i]['隔夜利息']),VerifyOrderyList.mysql_closeOrder[i]['Swaps'],
                                    '第{}条数据断言失败：订单号：{}，导出隔夜利息：{}，数据库隔夜利息：{}'.format(i+1,int(VerifyOrderyList.closeOrderexcel_data[i]['订单号码']),float(VerifyOrderyList.closeOrder_data[i]['隔夜利息']),VerifyOrderyList.mysql_closeOrder[i]['Swaps']))

                                with allure.step('断言导出盈亏：{}，数据库盈亏：{}'.format(float(VerifyOrderyList.closeOrderexcel_data[i]['盈亏']),VerifyOrderyList.mysql_closeOrder[i]['Profit'])):
                                    check.equal(float(VerifyOrderyList.closeOrderexcel_data[i]['盈亏']),VerifyOrderyList.mysql_closeOrder[i]['Profit'],
                                    '第{}条数据断言失败：订单号：{}，导出盈亏：{}，数据库盈亏：{}'.format(i+1,int(VerifyOrderyList.closeOrderexcel_data[i]['订单号码']),float(VerifyOrderyList.closeOrder_data[i]['盈亏']),VerifyOrderyList.mysql_closeOrder[i]['Profit']))

            else:
                pytest.skip()

    

if __name__=='__main__':
    # pytest.main(['-s','-v',os.path.abspath(__file__)])
    pytest.main(['-s','-v',os.path.abspath(__file__),
    r'--alluredir={}\CloseOrder_report\result'.format(path_project),'--disable-pytest-warnings'])
    os.system(r'allure generate {}\CloseOrder_report\result -o {}\CloseOrder_report\allure_CloseOrder_report --clean'.format(path_project,path_project))
    os.system(r'allure serve {}\CloseOrder_report\result'.format(path_project))
