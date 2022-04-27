'''
Author: tyler
Date: 2022-02-21 17:22:37
LastEditTime: 2022-04-21 10:22:03
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \tylerhub\demo\IB_deposit_withdrawal_list\actions\Test_IB_Deposit_Withdrawal.py
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
from Location_of_lower_Deposit_Withdrawal_List import Location_of_deposit_withdrawal


class Test_IB_deposit_withdrawal_list(object):
    
    global IBVerifyList,conFig,dealData,testdata,excelpath
    IBVerifyList=Location_of_deposit_withdrawal()
    conFig=ReadConfig()
    dealData=Aboutdata()

    #读取测试数据
    excelpath=os.path.join(path_project,r'test_data\IB_lowerData.xlsx')
    rows=dealData.openexcel(excelpath,'Sheet1')
    testdata=dealData.dict_data()

    def setup_class(self):
        #默认谷歌浏览器打开
        IBVerifyList.broswertype()
        #cp，bos登录
        IBVerifyList.get_url('sit',conFig.get_value('bos_login', 'username'),conFig.get_value('bos_login', 'password'))

    def teardown(self):
        if self.data_index==testdata.index(testdata[-1]):
            IBVerifyList.quitbrowser()
        else:
            IBVerifyList.closebrowser()
        try:
            os.remove(os.path.join(os.path.join(path_project,'test_data'),'copy_data.txt'))
            os.remove(os.path.join(os.path.join(path_project,'test_data'),'copy_data.xlsx'))
            os.remove(os.path.join(os.path.join(path_project,'test_data'),IBVerifyList.exportData_excel))
        except Exception as msg:
            print('用例跳过，未下载相应文件：{}'.format(msg))    
    
    
    @allure.feature('核对IB下级出入金记录，断言导出与复制功能')
    @allure.story('用例执行')
    @allure.description('读取测试文档数据，执行用例')
    @pytest.mark.parametrize('data',testdata)
    def test_IB_list(self,data):
        
        print('当前执行用例账号：{}'.format(int(data['IB账号'])))
                
        with allure.step('获取当前测试数据下标'):
            self.data_index=testdata.index(data)
        
        with allure.step('查询mysql，判断当前IB存在多少个下级'):
            IBVerifyList.search_ib_lower(int(data['IB账号']))
        
        with allure.step('登录会员中心判断当前IB是否存下级出入金记录'):
            if IBVerifyList.logincp(int(data['IB账号'])):

                with allure.step('IB账号{}存在下级出入金记录'.format(int(data['IB账号']))):
                    
                    for y in IBVerifyList.deduplication_lower_list:
                        with allure.step('查询下级账号{}出金记录'.format(y)):
                            if IBVerifyList.verify_withdrawal(int(y)):
                                with allure.step('存在出金记录,断言mongodb出金表与页面数据是否一致'):
                                    with allure.step('断言页面出金条数：{}，数据库出金条数：{}'.format(IBVerifyList.len_withdrawal,len(IBVerifyList.lower_withdrawalDatabase))):
                                        check.equal(len(IBVerifyList.lower_withdrawalDatabase),IBVerifyList.len_withdrawal,
                                        '页面出金条数{}，数据库出金条数：{}，账号{}出金记录总数断言失败'.format(IBVerifyList.len_withdrawal,len(IBVerifyList.lower_withdrawalDatabase),int(y)))
                                    
                                    #断言页面出金数据与数据库数据
                                    for i in range(0,len(IBVerifyList.lower_withdrawalDatabase)):
                                        for x in range(0,len(IBVerifyList.withdrawal_list)):
                                            if IBVerifyList.lower_withdrawalDatabase[i]['mtRefNo']==IBVerifyList.withdrawal_list[x]['mtRefNo']:
                                                
                                                with allure.step('断言订单号{}数据:'.format(IBVerifyList.lower_withdrawalDatabase[i]['mtRefNo'])):
                                                
                                                    with allure.step('断言页面主账号：{}，数据库主账号：{}'.format(IBVerifyList.lower_withdrawalDatabase[i]['accountNumber'],IBVerifyList.withdrawal_list[x]['accountNumber'])):
                                                        check.equal(IBVerifyList.lower_withdrawalDatabase[i]['accountNumber'],IBVerifyList.withdrawal_list[x]['accountNumber'],
                                                        '页面主账号{}；数据库主账号{}，第{}条数据断言失败'.format(IBVerifyList.withdrawal_list[x]['accountNumber'],IBVerifyList.lower_withdrawalDatabase[i]['accountNumber'],i+1)) 
                                                    
                                                    with allure.step('断言页面交易账号：{}，数据库交易账号：{}'.format(IBVerifyList.withdrawal_list[x]['tradeAccount'],int(IBVerifyList.lower_withdrawalDatabase[i]['tradeAccount']))):
                                                        check.equal(int(IBVerifyList.lower_withdrawalDatabase[i]['tradeAccount']),IBVerifyList.withdrawal_list[x]['tradeAccount'],
                                                        '页面交易账号：{}，数据库交易账号：{}，第{}条数据断言失败'.format(IBVerifyList.withdrawal_list[x]['tradeAccount'],int(IBVerifyList.lower_withdrawalDatabase[i]['tradeAccount']),i+1)) 
                                                    
                                                    with allure.step('断言页面姓名：{}，数据库姓名：{}'.format(IBVerifyList.withdrawal_list[x]['clnName'].replace(' ',''),IBVerifyList.lower_withdrawalDatabase[i]['clnName'].replace(' ',''))):
                                                        check.equal(IBVerifyList.lower_withdrawalDatabase[i]['clnName'].replace(' ',''),IBVerifyList.withdrawal_list[x]['clnName'].replace(' ',''),
                                                        '页面姓名：{}，数据库姓名：{}，第{}条数据断言失败'.format(IBVerifyList.withdrawal_list[x]['clnName'].replace(' ',''),IBVerifyList.lower_withdrawalDatabase[i]['clnName'].replace(' ',''),i+1)) 

                                                    with allure.step('断言页面时间：{}，数据库时间：{}'.format(IBVerifyList.withdrawal_list[x]['lastUpdateDate'].strftime('%Y-%m-%d %H:%M'),IBVerifyList.lower_withdrawalDatabase[i]['lastUpdateDate'].strftime('%Y-%m-%d %H:%M'))):
                                                        check.equal(IBVerifyList.lower_withdrawalDatabase[i]['lastUpdateDate'].strftime('%Y-%m-%d %H:%M'),IBVerifyList.withdrawal_list[x]['lastUpdateDate'].strftime('%Y-%m-%d %H:%M'),
                                                        '页面时间：{}，数据库时间：{}，第{}条数据断言失败'.format(IBVerifyList.withdrawal_list[x]['lastUpdateDate'].strftime('%Y-%m-%d %H:%M'),IBVerifyList.lower_withdrawalDatabase[i]['lastUpdateDate'].strftime('%Y-%m-%d %H:%M'),i+1)) 

                                                    with allure.step('断言页面交易金额：{}，数据库交易金额：{}'.format(IBVerifyList.withdrawal_list[x]['mtAmt'],float(IBVerifyList.lower_withdrawalDatabase[i]['mtAmt']))):
                                                        check.equal(float(IBVerifyList.lower_withdrawalDatabase[i]['mtAmt']),IBVerifyList.withdrawal_list[x]['mtAmt'],
                                                        '页面交易金额：{}，数据库交易金额：{}，第{}条数据断言失败'.format(IBVerifyList.withdrawal_list[x]['mtAmt'],float(IBVerifyList.lower_withdrawalDatabase[i]['mtAmt']),i+1)) #MT金额

                                                    break
                                            else:
                                                with allure.step('订单号{}在页面上无记录:'.format(IBVerifyList.lower_withdrawalDatabase[i]['mtRefNo'])):
                                                    pass
                            else:
                                with allure.step('下级账号{}不存在出金记录'.format(int(y))):
                                    print('数据库记录{}条'.format(len(IBVerifyList.lower_withdrawalDatabase)))
                                    
                        
                        with allure.step('查询下级账号{}入金记录'.format(y)):
                            if IBVerifyList.verify_deposit(int(y)):
                                with allure.step('存在入金记录,断言mongodb出金表与页面数据是否一致'):
                                    with allure.step('断言数据库入金条数：{}，页面入金条数：{}'.format(len(IBVerifyList.lower_depositDatabase),IBVerifyList.len_deposit)):
                                        check.equal(len(IBVerifyList.lower_depositDatabase),IBVerifyList.len_deposit,
                                        '数据库入金条数:{}，页面入金条数：{}，账号{}入金记录总数断言失败'.format(len(IBVerifyList.lower_depositDatabase),IBVerifyList.len_deposit,int(y)))
                                    
                                    for i in range(0,len(IBVerifyList.lower_depositDatabase)):
                                        for x in range(0,len(IBVerifyList.deposit_list)):
                                        
                                            if IBVerifyList.lower_depositDatabase[i]['mtRefNo'] == IBVerifyList.deposit_list[x]['mtRefNo']:
                                                with allure.step('断言订单号数据{}'.format(IBVerifyList.lower_depositDatabase[i]['mtRefNo'])):
                                                    
                                                    with allure.step('断言数据库主账号：{}，页面主账号：{}'.format(IBVerifyList.lower_depositDatabase[i]['accountNumber'],IBVerifyList.deposit_list[x]['accountNumber'])):
                                                        check.equal(IBVerifyList.lower_depositDatabase[i]['accountNumber'],IBVerifyList.deposit_list[x]['accountNumber'],
                                                        '数据库主账号：{}，页面主账号：{}，第{}条数据断言失败'.format(IBVerifyList.lower_depositDatabase[i]['accountNumber'],IBVerifyList.deposit_list[x]['accountNumber'],i+1)) 
                                                    
                                                    with allure.step('断言数据库交易账号：{}，页面交易账号：{}'.format(int(IBVerifyList.lower_depositDatabase[i]['tradeAccount']),IBVerifyList.deposit_list[x]['tradeAccount'])):
                                                        check.equal(int(IBVerifyList.lower_depositDatabase[i]['tradeAccount']),IBVerifyList.deposit_list[x]['tradeAccount'],
                                                        '数据库交易账号：{}，页面交易账号：{}，第{}条数据断言失败'.format(int(IBVerifyList.lower_depositDatabase[i]['tradeAccount']),IBVerifyList.deposit_list[x]['tradeAccount'],i+1))
                                                    
                                                    with allure.step('断言数据库姓名：{}，页面姓名：{}'.format(IBVerifyList.lower_depositDatabase[i]['clnName'].replace(' ',''),IBVerifyList.deposit_list[x]['clnName'].replace(' ',''))):
                                                        check.equal(IBVerifyList.lower_depositDatabase[i]['clnName'].replace(' ',''),IBVerifyList.deposit_list[x]['clnName'].replace(' ',''),
                                                        '数据库姓名：{}，页面姓名：{}，第{}条数据断言失败'.format(IBVerifyList.lower_depositDatabase[i]['clnName'].replace(' ',''),IBVerifyList.deposit_list[x]['clnName'].replace(' ',''),i+1)) #姓名
                                                    
                                                    with allure.step('断言数据库时间：{}，页面时间：{}'.format(IBVerifyList.lower_depositDatabase[i]['lastUpdateDate'].strftime('%Y-%m-%d %H:%M'),IBVerifyList.deposit_list[x]['lastUpdateDate'].strftime('%Y-%m-%d %H:%M'))):
                                                        check.equal(IBVerifyList.lower_depositDatabase[i]['lastUpdateDate'].strftime('%Y-%m-%d %H:%M'),IBVerifyList.deposit_list[x]['lastUpdateDate'].strftime('%Y-%m-%d %H:%M'),
                                                        '数据库时间：{}，页面时间:{},第{}条数据断言失败'.format(IBVerifyList.lower_depositDatabase[i]['lastUpdateDate'].strftime('%Y-%m-%d %H:%M'),IBVerifyList.deposit_list[x]['lastUpdateDate'].strftime('%Y-%m-%d %H:%M'),i+1)) #时间
                                                    
                                                    with allure.step('断言数据库金额：{}，页面金额：{}'.format(float(IBVerifyList.lower_depositDatabase[i]['mt4Amt']),IBVerifyList.deposit_list[x]['mt4Amt'])):
                                                        check.equal(float(IBVerifyList.lower_depositDatabase[i]['mt4Amt']),IBVerifyList.deposit_list[x]['mt4Amt'],
                                                        '数据库金额：{}，页面金额：{}，第{}条数据断言失败'.format(float(IBVerifyList.lower_depositDatabase[i]['mt4Amt']),IBVerifyList.deposit_list[x]['mt4Amt'],i+1)) #MT金额
                                                    
                                                    break
                                            else:
                                                with allure.step('订单号{}在页面无记录'.format(IBVerifyList.lower_depositDatabase[i]['mtRefNo'])):
                                                    pass
                            else:
                                with allure.step('下级账号{}不存在入金记录'.format(int(y))):
                                    print('数据库记录{}条'.format(len(IBVerifyList.lower_depositDatabase)))
                
                with allure.step('断言复制内容是否与页面一致'):
                    # 断言页面复制功能
                    IBVerifyList.verify_copy()

                    for i in range(0,IBVerifyList.pageDataLen):
                        
                        with allure.step('断言页面订单号：{}，复制订单号：{}'.format(IBVerifyList.pageDataList[i]['订单编号'],IBVerifyList.copyData[i]['订单编号'])):
                            check.equal(IBVerifyList.pageDataList[i]['订单编号'], IBVerifyList.copyData[i]['订单编号'],
                            '页面订单编号：{},复制订单编号：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['订单编号'],IBVerifyList.copyData[i]['订单编号'],i+1))

                        
                            with allure.step('断言页面会员账号：{}，复制会员账号：{}'.format(IBVerifyList.pageDataList[i]['会员账号'],IBVerifyList.copyData[i]['会员账号'])):
                                check.equal(IBVerifyList.pageDataList[i]['会员账号'], IBVerifyList.copyData[i]['会员账号'],
                                '页面会员账号：{}，复制会员账号：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['会员账号'], IBVerifyList.copyData[i]['会员账号'],i+1))
                        
                            with allure.step('断言页面交易账号：{}，复制交易账号：{}'.format(IBVerifyList.pageDataList[i]['交易账号'],IBVerifyList.copyData[i]['交易账号'])):
                                check.equal(IBVerifyList.pageDataList[i]['交易账号'], IBVerifyList.copyData[i]['交易账号'],
                                '页面交易账号：{}，复制交易账号：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['交易账号'], IBVerifyList.copyData[i]['交易账号'],i+1))
                            
                            with allure.step('断言页面姓名：{}，复制姓名：{}'.format(IBVerifyList.pageDataList[i]['姓名'],IBVerifyList.copyData[i]['姓名'])):
                                check.equal(IBVerifyList.pageDataList[i]['姓名'], IBVerifyList.copyData[i]['姓名'],
                                '页面姓名：{}，复制姓名：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['姓名'], IBVerifyList.copyData[i]['姓名'],i+1))
                            
                            with allure.step('断言页面上级会员中心账号：{}，复制上级会员中心账号：{}'.format(IBVerifyList.pageDataList[i]['上级会员中心账号'],IBVerifyList.copyData[i]['上级会员中心账号'])):
                                check.equal(IBVerifyList.pageDataList[i]['上级会员中心账号'], IBVerifyList.copyData[i]['上级会员中心账号'],
                                '页面上级会员中心账号：{}，复制上级会员中心账号：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['上级会员中心账号'], IBVerifyList.copyData[i]['上级会员中心账号'],i+1))
                            
                            with allure.step('断言页面上级返佣账号：{}，复制上级返佣账号：{}'.format(IBVerifyList.pageDataList[i]['上级返佣账号'],IBVerifyList.copyData[i]['上级返佣账号'])):
                                check.equal(IBVerifyList.pageDataList[i]['上级返佣账号'], IBVerifyList.copyData[i]['上级返佣账号'],
                                '页面上级返佣账号：{}，复制上级返佣账号：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['上级返佣账号'], IBVerifyList.copyData[i]['上级返佣账号'],i+1))
                            
                            with allure.step('断言页面上级名称：{}，复制上级名称：{}'.format(IBVerifyList.pageDataList[i]['上级名称'],IBVerifyList.copyData[i]['上级名称'])):
                                check.equal(IBVerifyList.pageDataList[i]['上级名称'], IBVerifyList.copyData[i]['上级名称'],
                                '页面上级名称：{}，复制上级名称：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['上级名称'], IBVerifyList.copyData[i]['上级名称'],i+1))
                            
                            with allure.step('断言页面时间：{}，复制时间：{}'.format(IBVerifyList.pageDataList[i]['时间'],IBVerifyList.copyData[i]['时间'])):
                                check.equal(IBVerifyList.pageDataList[i]['时间'], IBVerifyList.copyData[i]['时间'],
                                '页面时间：{}，复制时间：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['时间'], IBVerifyList.copyData[i]['时间'],i+1))
                    
                            with allure.step('断言页面备注：{}，复制备注：{}'.format(IBVerifyList.pageDataList[i]['备注'],IBVerifyList.copyData[i]['备注'])):
                                check.equal(IBVerifyList.pageDataList[i]['备注'], IBVerifyList.copyData[i]['备注'],
                                '页面备注：{}，复制备注：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['备注'], IBVerifyList.copyData[i]['备注'],i+1))
                            
                            with allure.step('断言页面MT金额：{}，复制MT金额：{}'.format(IBVerifyList.pageDataList[i]['MT金额'],IBVerifyList.copyData[i]['MT金额'])):
                                check.equal(IBVerifyList.pageDataList[i]['MT金额'], IBVerifyList.copyData[i]['MT金额'],
                                '页面MT金额：{}，复制MT金额：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['MT金额'], IBVerifyList.copyData[i]['MT金额'],i+1))
                    
                with allure.step('断言导出内容是否与页面一致'):
                    #断言页面导出功能
                    IBVerifyList.verify_export()

                    for i in range(0,IBVerifyList.pageDataLen):

                        with allure.step('断言页面订单号：{}，导出订单号：{}'.format(IBVerifyList.pageDataList[i]['订单编号'],IBVerifyList.exportDataList[i]['订单编号'])):
                            check.equal(int(IBVerifyList.pageDataList[i]['订单编号']), int(IBVerifyList.exportDataList[i]['订单编号']),
                            '页面订单编号：{}，导出订单编号：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['订单编号'], IBVerifyList.exportDataList[i]['订单编号'],i+1))
                        
                            with allure.step('断言页面会员账号：{}，导出会员账号：{}'.format(IBVerifyList.pageDataList[i]['会员账号'],IBVerifyList.exportDataList[i]['会员账号'])):
                                check.equal(IBVerifyList.pageDataList[i]['会员账号'], IBVerifyList.exportDataList[i]['会员账号'],
                                '页面会员账号：{}，导出会员账号：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['会员账号'], IBVerifyList.exportDataList[i]['会员账号'],i+1))
                            
                            with allure.step('断言页面交易账号：{}，导出交易账号：{}'.format(IBVerifyList.pageDataList[i]['交易账号'],IBVerifyList.exportDataList[i]['交易账号'])):
                                check.equal(IBVerifyList.pageDataList[i]['交易账号'], IBVerifyList.exportDataList[i]['交易账号'],
                                '页面交易账号：{}，导出交易账号：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['交易账号'], IBVerifyList.exportDataList[i]['交易账号'],i+1))
                            
                            with allure.step('断言页面姓名：{}，导出姓名：{}'.format(IBVerifyList.pageDataList[i]['姓名'],IBVerifyList.exportDataList[i]['姓名'])):
                                check.equal(IBVerifyList.pageDataList[i]['姓名'], IBVerifyList.exportDataList[i]['姓名'],
                                '页面姓名：{}，导出姓名：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['姓名'], IBVerifyList.exportDataList[i]['姓名'],i+1))
                            
                            with allure.step('断言页面上级会员中心账号：{}，导出上级会员中心账号：{}'.format(IBVerifyList.pageDataList[i]['上级会员中心账号'],IBVerifyList.exportDataList[i]['上级会员中心账号'])):
                                check.equal(IBVerifyList.pageDataList[i]['上级会员中心账号'], IBVerifyList.exportDataList[i]['上级会员中心账号'],
                                '页面上级会员中心账号：{}，导出上级会员中心账号：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['上级会员中心账号'], IBVerifyList.exportDataList[i]['上级会员中心账号'],i+1))
                            
                            with allure.step('断言页面上级返佣账号：{}，导出上级返佣账号：{}'.format(IBVerifyList.pageDataList[i]['上级返佣账号'],IBVerifyList.exportDataList[i]['上级返佣账号'])):
                                check.equal(IBVerifyList.pageDataList[i]['上级返佣账号'], IBVerifyList.exportDataList[i]['上级返佣账号'],
                                '页面上级返佣账号：{}，导出上级返佣账号：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['上级返佣账号'], IBVerifyList.exportDataList[i]['上级返佣账号'],i+1))
                            
                            with allure.step('断言页面上级名称：{}，导出上级名称：{}'.format(IBVerifyList.pageDataList[i]['上级名称'],IBVerifyList.exportDataList[i]['上级名称'])):
                                check.equal(IBVerifyList.pageDataList[i]['上级名称'], IBVerifyList.exportDataList[i]['上级名称'],
                                '页面上级名称：{}，导出上级名称：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['上级名称'], IBVerifyList.exportDataList[i]['上级名称'],i+1))
                            
                            with allure.step('断言页面时间：{}，导出时间：{}'.format(IBVerifyList.pageDataList[i]['时间'],IBVerifyList.exportDataList[i]['时间'])):
                                check.equal(IBVerifyList.pageDataList[i]['时间'], IBVerifyList.exportDataList[i]['时间'],
                                '页面时间：{}，导出时间：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['时间'], IBVerifyList.exportDataList[i]['时间'],i+1))
                            
                            with allure.step('断言页面备注：{}，导出备注：{}'.format(IBVerifyList.pageDataList[i]['备注'],IBVerifyList.exportDataList[i]['备注'])):
                                check.equal(IBVerifyList.pageDataList[i]['备注'], IBVerifyList.exportDataList[i]['备注'],
                                '页面备注：{}，导出备注：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['备注'], IBVerifyList.exportDataList[i]['备注'],i+1))
                            
                            with allure.step('断言页面MT金额：{}，导出MT金额：{}'.format(float(IBVerifyList.pageDataList[i]['MT金额']), IBVerifyList.exportDataList[i]['MT金额'])):
                                check.equal(float(IBVerifyList.pageDataList[i]['MT金额']), IBVerifyList.exportDataList[i]['MT金额'],
                                '页面MT金额：{}，导出MT金额：{}，第{}条数据断言失败'.format(IBVerifyList.pageDataList[i]['MT金额'], IBVerifyList.exportDataList[i]['MT金额'],i+1))
            else:
                with allure.step('IB账号{}不存在下级出入金记录'.format(int(data['IB账号']))):
                    print('当前账号不存在下级出入金记录')
                    pytest.skip()


                    


            
if __name__=='__main__':
    # pytest.main(['-s','-v',os.path.abspath(__file__)])
    pytest.main(['-s','-v',os.path.abspath(__file__),
    r'--alluredir={}\report\result'.format(path_project),'--disable-pytest-warnings'])
    os.system(r'allure generate {}\report\result -o {}\report\allure_report --clean'.format(path_project,path_project))
    os.system(r'allure serve {}\report\result'.format(path_project))