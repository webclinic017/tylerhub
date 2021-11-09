'''
Author: tyler
Date: 2021-09-27 15:13:40
LastEditTime: 2021-11-09 11:13:45
LastEditors: Please set LastEditors
Description: Execute testcase
FilePath: \tylerhub\demo\deposit_withdrawal_list\action_bin\test_deposti_withdrawal.py
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
from location_of_deposti_withdrawal_List import Location_of_deposit_withdrawal

@allure.epic('查询出入金列表')
class Test_deposti_withdrawal_list(object):

    global verifyList,conFig,dealData,testdata,excelpath
    verifyList=Location_of_deposit_withdrawal()
    conFig=ReadConfig()
    dealData=Aboutdata()

    #读取测试数据
    excelpath=os.path.join(path_project,r'test_data\search_depositAndwithdrawal.xlsx')
    rows=dealData.openexcel(excelpath,'Sheet1')
    testdata=dealData.dict_data()

    def setup_class(self):
        #默认谷歌浏览器打开
        verifyList.broswertype()
        #cp，bos登录页
        verifyList.get_url('sit',conFig.get_value('bos_login', 'username'),conFig.get_value('bos_login', 'password'))
    
    
    def teardown(self):
        if self.data_index==testdata.index(testdata[-1]):
            verifyList.quitbrowser()
        else:
            verifyList.closebrowser()
    
    @allure.feature('随机选择时间，查询两次出入金列表数据并与数据库对应数据内数据核对')
    @allure.story('用例执行')
    @allure.description('读取测试文档数据，执行用例')
    @pytest.mark.parametrize('data',testdata)
    def test_verify_deposit_withdrawal_list(self,data):
        print('当前查询账号：{}'.format(int(data['主账号'])))
        
        with allure.step('获取当前测试数据下标'):
            self.data_index=testdata.index(data)

        with allure.step('bos登录cp，进入出入金记录页面'):
            verifyList.logincp(int(data['主账号']))

        for i in range(0,2):
            print('第{}次查询:'.format(i+1))
            with allure.step('判断当前时间段是否存在出入金转账记录'):
                if verifyList.serch_list(int(data['主账号'])):
                    with allure.step('当前时间段存在出入金转账记录'):
                        
                        with allure.step('判断当前时间段是否存在出金记录'):
                            if verifyList.search_withdrawal(int(data['主账号'])):

                                with allure.step('存在出金记录{}条，断言页面每条出金记录是否与数据库一致'.format(verifyList.withdrawal_len)):
                                    #出金类型
                                    self.withdrawal_type=['Cryptocurrency Wallet', 'Local Currency', 'AMP Account', 'Bankwire', 'Credit Card', 'Settlement Import', 'E-wallet']
                                        
                                    #断言页面出金条数是否与数据库一致
                                    check.equal(len(verifyList.mongodbWithdrawal),verifyList.withdrawal_len,
                                    '数据库出金记录{}条，页面出金记录{}条'.format(len(verifyList.mongodbWithdrawal),verifyList.withdrawal_len))
                                        
                                    for i in range(0,verifyList.withdrawal_len):
                                    #断言每条出金记录时间、交易金额、汇率、mt金额、状态、出金渠道是否与数据库一致
                                        with allure.step('断言时间：数据库出金时间 {}；页面出金时间 {}'.format(verifyList.mongodbWithdrawal[i]['createDate_mt'].strftime('%Y-%m-%d %H:%M'),
                                        verifyList.withdrawal_list[i]['createDate_mt'].strftime('%Y-%m-%d %H:%M'))):

                                            check.equal(verifyList.mongodbWithdrawal[i]['createDate_mt'].strftime('%Y-%m-%d %H:%M'),
                                            verifyList.withdrawal_list[i]['createDate_mt'].strftime('%Y-%m-%d %H:%M'),
                                            '数据库出金时间 {}，页面出金时间 {}'.format(verifyList.mongodbWithdrawal[i]['createDate_mt'].strftime('%Y-%m-%d %H:%M'),
                                            verifyList.withdrawal_list[i]['createDate_mt'].strftime('%Y-%m-%d %H:%M')))
                                            
                                        with allure.step('断言交易金额：数据库交易金额 {}；页面交易金额 {}'.format(verifyList.mongodbWithdrawal[i]['settleAmt'],
                                        verifyList.withdrawal_list[i]['settleAmt'])):

                                            check.equal(verifyList.mongodbWithdrawal[i]['settleAmt'],verifyList.withdrawal_list[i]['settleAmt'],
                                            '数据库交易金额：{};页面交易金额：{}'.format(verifyList.mongodbWithdrawal[i]['settleAmt'],verifyList.withdrawal_list[i]['settleAmt']))

                                        with allure.step('断言出金汇率：数据库出金汇率 {}；页面出金汇率 {}'.format(verifyList.mongodbWithdrawal[i]['realRate'],
                                        verifyList.withdrawal_list[i]['realRate'])):
                                            check.equal(verifyList.mongodbWithdrawal[i]['realRate'],verifyList.withdrawal_list[i]['realRate'],
                                            '数据库出金汇率：{};页面出金汇率：{}'.format(verifyList.mongodbWithdrawal[i]['realRate'],verifyList.withdrawal_list[i]['realRate']))

                                        with allure.step('断言出金mt金额：数据库出金mt金额 {}；页面出金mt金额 {}'.format(verifyList.mongodbWithdrawal[i]['mtAmt'],
                                        verifyList.withdrawal_list[i]['mtAmt'])):
                                            check.equal(verifyList.mongodbWithdrawal[i]['mtAmt'],verifyList.withdrawal_list[i]['mtAmt'],
                                            '数据库mt金额：{};页面mt金额：{}'.format(verifyList.mongodbWithdrawal[i]['mtAmt'],verifyList.withdrawal_list[i]['mtAmt']))

                                        with allure.step('断言出金状态：数据库出金状态 {}；页面出金状态 {}'.format(verifyList.mongodbWithdrawal[i]['currStatus'],
                                        verifyList.withdrawal_list[i]['currStatus'])):
                                            check.is_in(verifyList.mongodbWithdrawal[i]['currStatus'],'SU')
                                            check.is_in(verifyList.withdrawal_list[i]['currStatus'],'成功 待审核')
                                        
                                        with allure.step('断言出金渠道：数据库出金渠道 {}'.format(verifyList.mongodbWithdrawal[i]['channel'])):
                                            check.is_in(verifyList.mongodbWithdrawal[i]['channel'],self.withdrawal_type)
                            else:
                                with allure.step('不存在出金记录，断言当前时间段内数据库查询数据是否为空'):
                                    check.equal(verifyList.mongodbWithdrawal,[],'数据库查询不为空')
                                    print('当前时间段出金记录为空')

                        with allure.step('判断当前时间段是否存在入金记录'):    
                            if verifyList.search_deposit(int(data['主账号'])):

                                with allure.step('存在入金记录{}条，断言页面每条入金记录是否与数据库一致'.format(verifyList.deposit_len)):
                                    #入金类型
                                    self.deposit_type=['tapCard', 'jpayP2P', 'paymentInsideATM', 'walaopayIDR', 'paymentAsia', 'fxbitUSDTTRC20', 'help2IDR', 'pay88VND', 
                                    'nlpay', 'KHM_offline_P2P', 'dusupay', 'qubepay2', 'cardpayUganda', 'walaopayVND', 'qubepay', 'jpayUSDT', 'AT_USDT_ERC20', 
                                    'at_p2c', 'neteller', 'walaopayTHB', 'expayQR', 'dragonpay', 'bankwire', 'cashu', 'sticpay', 'p2cMMK', 'skrill', 'cardpay', 'rpnP2P', 
                                    'jpayAli', 'neteller2', 'walaopayMYR', 'payMeroUSDTTRC20']

                                    #断言页面入金金条数是否与数据库一致
                                    check.equal(len(verifyList.mongodbDeposit),verifyList.deposit_len,
                                    '数据库入金记录{}条，页面入金记录{}条'.format(len(verifyList.mongodbDeposit),verifyList.deposit_len))
                                    for i in range(0,verifyList.deposit_len):
                                        #断言每条入金记录时间、交易金额、汇率、mt金额、状态、入金渠道是否与数据库一致
                                        with allure.step('断言时间：数据库入金时间 {}；页面入金时间 {}'.format(verifyList.mongodbDeposit[i]['createDate_mt'].strftime('%Y-%m-%d %H:%M'),
                                        verifyList.deposti_list[i]['createDate_mt'].strftime('%Y-%m-%d %H:%M'))):

                                            check.equal(verifyList.mongodbDeposit[i]['createDate_mt'].strftime('%Y-%m-%d %H:%M'),
                                            verifyList.deposti_list[i]['createDate_mt'].strftime('%Y-%m-%d %H:%M'),
                                            '数据库出金时间 {}，页面出金时间 {}'.format(verifyList.mongodbDeposit[i]['createDate_mt'].strftime('%Y-%m-%d %H:%M'),
                                            verifyList.deposti_list[i]['createDate_mt'].strftime('%Y-%m-%d %H:%M')))

                                        with allure.step('断言入金交易金额：数据库入金交易金额 {}；页面交易金额 {}'.format(verifyList.mongodbDeposit[i]['fromAmt'],
                                        verifyList.deposti_list[i]['fromAmt'])):
                                            check.equal(verifyList.mongodbDeposit[i]['fromAmt'],verifyList.deposti_list[i]['fromAmt'],
                                            '数据库交易金额：{};页面交易金额：{}'.format(verifyList.mongodbDeposit[i]['fromAmt'],verifyList.deposti_list[i]['fromAmt']))

                                        with allure.step('断言入金汇率：数据库入金汇率 {}；页面入金汇率 {}'.format(verifyList.mongodbDeposit[i]['rate'],
                                        verifyList.deposti_list[i]['rate'])):
                                            check.equal(verifyList.mongodbDeposit[i]['rate'],verifyList.deposti_list[i]['rate'],
                                            '数据库交易汇率：{};页面交易汇率：{}'.format(verifyList.mongodbDeposit[i]['rate'],verifyList.deposti_list[i]['rate']))
                                        
                                        with allure.step('断言入金mt金额：数据库入金mt金额 {}；页面入金mt金额 {}'.format(verifyList.mongodbDeposit[i]['mt4Amt'],
                                        verifyList.deposti_list[i]['mt4Amt'])):
                                            check.equal(verifyList.mongodbDeposit[i]['mt4Amt'],verifyList.deposti_list[i]['mt4Amt'],
                                            '数据库交易mt金额：{};页面交易mt金额：{}'.format(verifyList.mongodbDeposit[i]['mt4Amt'],verifyList.deposti_list[i]['mt4Amt']))

                                        with allure.step('断言入金状态：数据库入金状态 {}；页面入金状态 {}'.format(verifyList.mongodbDeposit[i]['currStatus'],
                                        verifyList.deposti_list[i]['currStatus'])):
                                            check.is_in(verifyList.mongodbDeposit[i]['currStatus'],'SU')
                                            check.is_in(verifyList.deposti_list[i]['currStatus'],'成功 待审核')

                                        with allure.step('断言入金渠道：数据库入金渠道 {}'.format(verifyList.mongodbDeposit[i]['channel'])):
                                            check.is_in(verifyList.mongodbDeposit[i]['channel'],self.deposit_type)
                            else:
                                with allure.step('不存在入金记录，断言当前时间段内数据库查询数据是否为空'):
                                    check.equal(verifyList.mongodbDeposit,[],'数据库查询不为空')
                                    print('当前时间段入金记录为空')

                        with allure.step('判断当前时间段是否存在转账记录'): 
                            if verifyList.search_transfer(int(data['主账号'])):
                                with allure.step('存在转账记录，断言页面每条转账记录是否与数据库一致'):
                                    #断言页面转账记录是否与数据库一致
                                    check.equal(len(verifyList.mongodbTransfer),verifyList.transfer_len,
                                    '数据库转账记录{}条，页面转账记录{}条'.format(len(verifyList.mongodbTransfer),verifyList.transfer_len))
                                    for i in range(0,verifyList.transfer_len):
                                        #断言每条转账记录时间、mt金额、状态是否与数据库一致
                                        with allure.step('断言时间：数据库转账时间 {}；页面转账时间 {}'.format(verifyList.mongodbTransfer[i]['createDate_mt'].strftime('%Y-%m-%d %H:%M'),
                                        verifyList.transfer_list[i]['createDate_mt'].strftime('%Y-%m-%d %H:%M'))):
                                            check.equal(verifyList.mongodbTransfer[i]['createDate_mt'].strftime('%Y-%m-%d %H:%M'),
                                            verifyList.transfer_list[i]['createDate_mt'].strftime('%Y-%m-%d %H:%M'),
                                            '数据库出金时间 {}，页面出金时间 {}'.format(verifyList.mongodbTransfer[i]['createDate_mt'].strftime('%Y-%m-%d %H:%M'),
                                            verifyList.transfer_list[i]['createDate_mt'].strftime('%Y-%m-%d %H:%M')))

                                        with allure.step('断言转账mt金额：数据库转账mt金额 {}；页面转账mt金额 {}'.format(verifyList.mongodbTransfer[i]['toMtAmt'],
                                        verifyList.transfer_list[i]['toMtAmt'])):
                                            check.equal(verifyList.mongodbTransfer[i]['toMtAmt'],verifyList.transfer_list[i]['toMtAmt'],
                                            '数据库交易mt金额：{};页面交易mt金额：{}'.format(verifyList.mongodbTransfer[i]['toMtAmt'],verifyList.transfer_list[i]['toMtAmt']))
                                        
                                        with allure.step('断言转账状态：数据库转账状态 {}；页面转账状态 {}'.format(verifyList.mongodbTransfer[i]['currStatus'],
                                        verifyList.transfer_list[i]['currStatus'])):
                                            check.is_in(verifyList.mongodbTransfer[i]['currStatus'], 'SU')
                                            check.is_in(verifyList.transfer_list[i]['currStatus'],'成功 待审核')
                            else:
                                with allure.step('不存在转账记录，断言数据库数据库是否为空'):
                                    check.equal(verifyList.mongodbTransfer,[],'数据库查询不为空')
                                    print('当前时间段转账记录为空')
                else:
                    with allure.step('当前时间段不存在出入金转账记录,断言数据库查询是否为空'):
                        #断言数据库查询是否为空
                        check.equal(verifyList.mongodbWithdrawal,[],'数据库查询不为空')
                        check.equal(verifyList.mongodbDeposit,[],'数据库查询不为空')
                        check.equal(verifyList.mongodbTransfer,[],'数据库查询不为空')
                        print('当前时间段出入金记录为空')

if __name__=='__main__':
    # pytest.main(['-s','-v',os.path.abspath(__file__)])
    pytest.main(['-s','-v',os.path.abspath(__file__),
    r'--alluredir={}\report\result'.format(path_project),'--disable-pytest-warnings'])
    os.system(r'allure generate {}\report\result -o {}\report\allure_report --clean'.format(path_project,path_project))
    os.system(r'allure serve {}\report\result'.format(path_project))