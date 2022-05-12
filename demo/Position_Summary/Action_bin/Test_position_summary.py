'''
Author: tyler
Date: 2022-04-28 16:17:56
LastEditTime: 2022-05-12 16:56:34
LastEditors: Tyler96-QA 1718459369@qq.com
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \tylerhub\demo\Position_Summary\Action_bin\Test_position_summary.py
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
from Location_of_position_summary import Location_position_summary



class Test_position_summary(object):
    """
    IB仓位总结:
    根据交易账号查询入金表，出金表，转账表，统计数据库数据并与页面核对
    查询交易账号交易数据，与页面核对
    """



    global Verifyposition,conFig,dealData,testdata,excelpath
    Verifyposition=Location_position_summary()
    conFig=ReadConfig()
    dealData=Aboutdata()

    #读取测试数据
    excelpath=os.path.join(path_project,r'test_data\Position_summary.xlsx')
    rows=dealData.openexcel(excelpath,'Sheet1')
    testdata=dealData.dict_data()


    def setup_class(self):
        #默认谷歌浏览器打开
        Verifyposition.broswertype()
        #cp，bos登录
        Verifyposition.get_url('sit',conFig.get_value('bos_login', 'username'),conFig.get_value('bos_login', 'password'))

    
    
    def teardown(self):
        if self.data_index==testdata.index(testdata[-1]):
            Verifyposition.quitbrowser()
        else:
            Verifyposition.closebrowser()

     
    @allure.feature('核对IB仓位总结数据，断言页面数据是否与数据库一致')
    @allure.story('用例执行')
    @allure.description('读取测试文档数据，执行用例')
    @allure.title('IB仓位总结数据核对报告')
    @pytest.mark.parametrize('data',testdata)
    def test_verify_position_summary(self,data):
        
        print('当前执行用例账号：{}'.format(int(data['IB主账号'])))
        
        if Verifyposition.logincp(int(data['IB主账号'])):
            pytest.skip()
        else:
            with allure.step('获取当前测试数据下标'):
                self.data_index=testdata.index(data)
            #根据交易账号统计
            with allure.step('根据交易账号查询仓位总结数据'):
                Verifyposition.serch_basetraccount(int(data['交易账号']))

                with allure.step('断言交易账号{}在{} 00:00:00~{} 23:59:59时间段内数据库总入金：{}与页面总入金：{}'.format(int(data['交易账号']),Verifyposition.dateStart,Verifyposition.dateEnd,
                Verifyposition.totalDeposit,Verifyposition.totalPage_deposit)):
                    check.equal(Verifyposition.totalDeposit,Verifyposition.totalPage_deposit,'交易账号{}总入金断言失败：数据库总入金：{}；页面总入金：{}'.
                    format(int(data['交易账号']),Verifyposition.totalDeposit,Verifyposition.totalPage_deposit))
                
                with allure.step('断言交易账号{}在{} 00:00:00~{} 23:59:59时间段内数据库总出金：{}与页面总出金：{}'.format(int(data['交易账号']),Verifyposition.dateStart,Verifyposition.dateEnd,
                -Verifyposition.totalWithdrawal,Verifyposition.totalPage_withdrawal)):
                    check.equal(-Verifyposition.totalWithdrawal,Verifyposition.totalPage_withdrawal,'交易账号{}总出金断言失败：数据库总出金：{}；页面总出金：{}'.
                    format(int(data['交易账号']),-Verifyposition.totalWithdrawal,Verifyposition.totalPage_withdrawal))

                with allure.step('断言交易账号{}在{} 00:00:00~{} 23:59:59时间段内数据库净入金：{}与页面净入金：{}'.format(int(data['交易账号']),Verifyposition.dateStart,Verifyposition.dateEnd,
                Verifyposition.totalDeposit+(-Verifyposition.totalWithdrawal),Verifyposition.netPage_deposit)):
                    check.equal(Verifyposition.totalDeposit+(-Verifyposition.totalWithdrawal),Verifyposition.netPage_deposit,'交易账号{}净入金断言失败：数据库净入金：{}；页面净入金：{}'.
                    format(int(data['交易账号']),Verifyposition.totalDeposit+(-Verifyposition.totalWithdrawal),Verifyposition.netPage_deposit))

                with allure.step('断言交易账号{}在{} 00:00:00~{} 23:59:59时间段内数据库总资金转入：{}与页面总资金转入：{}'.format(int(data['交易账号']),Verifyposition.dateStart,Verifyposition.dateEnd,
                Verifyposition.totalTransfer,Verifyposition.totalPage_transfer)):
                    check.equal(Verifyposition.totalTransfer,Verifyposition.totalPage_transfer,'交易账号{}总资金转入断言失败：数据库总资金转入：{}；页面总资金转入：{}'.
                    format(int(data['交易账号']),Verifyposition.totalTransfer,Verifyposition.totalPage_transfer))                   
                
                with allure.step('断言交易账号{}在{} 00:00:00~{} 23:59:59时间段内数据库总交易量：{}与页面总交易量：{}'.format(int(data['交易账号']),Verifyposition.dateStart,Verifyposition.dateEnd,
                Verifyposition.mysqlVolume,Verifyposition.totalPage_volume)):
                    check.equal(Verifyposition.mysqlVolume,Verifyposition.totalPage_volume,'交易账号{}总交易量断言失败：数据库总交易量：{}；页面总交易量：{}'.
                    format(int(data['交易账号']),Verifyposition.mysqlVolume,Verifyposition.totalPage_volume)) 

                with allure.step('断言交易账号{}在{} 00:00:00~{} 23:59:59时间段内数据库总佣金：{}与页面总佣金：{}'.format(int(data['交易账号']),Verifyposition.dateStart,Verifyposition.dateEnd,
                Verifyposition.mysqlCommission,Verifyposition.totalPage_commission)):
                    check.equal(Verifyposition.mysqlCommission,Verifyposition.totalPage_commission,'交易账号{}总佣金断言失败：数据库总佣金：{}；页面总佣金：{}'.
                    format(int(data['交易账号']),Verifyposition.mysqlCommission,Verifyposition.totalPage_commission))

                with allure.step('断言交易账号{}在{} 00:00:00~{} 23:59:59时间段内数据库总隔夜利息：{}与页面总隔夜利息：{}'.format(int(data['交易账号']),Verifyposition.dateStart,Verifyposition.dateEnd,
                Verifyposition.mysqlSwaps,Verifyposition.totalPage_swaps)):
                    check.equal(Verifyposition.mysqlSwaps,Verifyposition.totalPage_swaps,'交易账号{}总隔夜利息断言失败：数据库总隔夜利息：{}；页面总隔夜利息：{}'.
                    format(int(data['交易账号']),Verifyposition.mysqlSwaps,Verifyposition.totalPage_swaps))

                with allure.step('断言交易账号{}在{} 00:00:00~{} 23:59:59时间段内数据库总盈亏：{}与页面总盈亏：{}'.format(int(data['交易账号']),Verifyposition.dateStart,Verifyposition.dateEnd,
                Verifyposition.mysqlProfit,Verifyposition.totalPage_profit)):
                    check.equal(Verifyposition.mysqlProfit,Verifyposition.totalPage_profit,'交易账号{}总盈亏断言失败：数据库盈亏：{}；页面总盈亏：{}'.
                    format(int(data['交易账号']),Verifyposition.mysqlProfit,Verifyposition.totalPage_profit))

            # Verifyposition.search_allTradeaccount()



if __name__=='__main__':
    # pytest.main(['-s','-v',os.path.abspath(__file__)])
    pytest.main(['-s','-v',os.path.abspath(__file__),
    r'--alluredir={}\report\result'.format(path_project),'--disable-pytest-warnings'])
    os.system(r'allure generate {}\report\result -o {}\report\allure_report --clean'.format(path_project,path_project))
    os.system(r'allure serve {}\report\result'.format(path_project))





















