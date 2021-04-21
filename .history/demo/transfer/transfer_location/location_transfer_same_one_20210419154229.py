import os
import random
import sys
import time

path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=path_demo+r'\public'
sys.path.append(path_public)
from about_data import exceldata
from browser_actions import Commonweb
from common_method import commonmethod
from other_actions import public_method

common=Commonweb()
pub_method=public_method()
e=exceldata()



class location_of_transfer():

    def broswertype(self,broswername='Chrome'):
        self.driver=common.open_browser(broswername)
        self.commethod=commonmethod(self.driver)

    def get_url(self,username,psword,lang='CN'):
        try:
            common.open_web('https://at-client-portal-uat.atfxdev.com/login')
            time.sleep(1)
            #去除弹窗
            self.remove_topup()
            #选择页面语言
            self.commethod.choose_register_lang(lang)
            time.sleep(1)
            #新开窗口访问bos登录页
            common.js_openwindows('https://at-bos-frontend-uat.atfxdev.com/login')
            time.sleep(1)
            common.switch_windows(1)
            #选择页面语言
            self.commethod.choose_bos_lang(lang)
            #登录bos
            self.commethod.loginbos(username,psword)
            time.sleep(1)
            #客户管理
            common.display_click('css,.ivu-badge>span')
            #客户名单
            common.display_click('css,[data-old-padding-top] > [href="/client/clientListNew/:type*"]')
        except Exception as msg:
            pub_method.log_output('!!--!!get_url').error(msg)

    #登录页弹窗
    def remove_topup(self):
        try:
            self.commethod.remove_register_topup()
        except Exception as msg:
            pub_method.log_output('!!--!!remove_topup').error(msg)

    #进入客户详情页
    def ender_detail_page(self,account):
        try:
            #清空输入框
            common.switch_windows(1)
            common.web_clear('css,.ivu-input-group-with-append > [placeholder]')
            time.sleep(1)
            #输入主账号搜索
            common.display_input('css,.ivu-input-group-with-append > [placeholder]',account)
            time.sleep(1)
            common.display_click('css,.ivu-btn-icon-only > .ivu-icon')
            time.sleep(1)
            #进入客户详情页
            common.display_click('css,div.ivu-table-overflowX>table>tbody.ivu-table-tbody>tr>td',1)
            #切换窗口
            common.switch_windows(2)
            time.sleep(1)
            #主账户信息
            common.display_click('css,[href="#masterAccount"]')
            time.sleep(7)
        except Exception as msg:
            pub_method.log_output('!!--!!ender_detail_page').error(msg)

    #遍历BOS交易账号列表，获取入金账号所在行数
    def where_is_tdaccount_bos(self,tdaccount):
        #获取交易账号列表的总行数
        self.tdaccount_list_len=common.get_lenofelement('xpath,//*[@id="tdAccount"]/div[2]/div/div/'
        'div[3]/div[1]/div[2]/table/tbody/tr/td[2]/div/span')
        time.sleep(1)
        for i in range(0,self.tdaccount_list_len):
            if str(common.get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/div[1]/div[2]/'
            'table/tbody/tr/td[1]/div/div/span',i))==str(tdaccount):
                return i+1
                break
    

    #遍历会员中心首页的交易账户列表，找到入金交易账户所处位置
    def where_is_tdaccount_cp(self,tdaccount):
        #获取首页交易账号列表长度
        self.len_incp=common.get_lenofelement('css,.account-number-cla')
        time.sleep(1)
        new_str=str(4)+str(tdaccount)
        for i in range(0,self.len_incp):
            if pub_method.extract_numbers(common.get_text('css,.account-number-cla',i)) == new_str:
                return i+1
                break


    #获取交易账号余额
    def get_tdaccount_balance(self,tdaccount):
        try:
            self.cprows=self.where_is_tdaccount_cp(tdaccount)
            time.sleep(1)
            self.balance_text=common.display_get_text('css,div.card-for-loop>div>div.el-card__body>div>p>span',4*self.cprows-4)
            time.sleep(1)
            self.balance=float(self.balance_text.replace(',',''))
            return self.balance
        except Exception as msg:
            pub_method.log_output('!!--!!get_tdaccount_balance')


    #判断交易账号激活+暂停状态是否超过或等于5个
    def is_status_five(self):
        self.status_num=0
        for i in range(1,self.tdaccount_list_len+1):
            self.status=common.display_get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/'
            'div[1]/div[2]/table/tbody/tr[{}]/td[5]/div/div/span'.format(i))
            time.sleep(1)
            while self.status in ('暂停','激活','Suspended','Active'):
                self.status_num=self.status_num+1
                break
        print('交易账号激活+暂停状态总数为：{}'.format(self.status_num))
        return self.status_num


    #判断主账号转账控制是否开启
    def transfer_control_on(self,account):
        try:
            #账户详情页
            self.ender_detail_page(account)
            if common.get_attributes('css,label.switch>span.ivu-switch>input','value',4)=='false':
                time.sleep(1)
                #开启转账控制权限
                common.display_click('css,label.switch>span.ivu-switch',4)
                time.sleep(1)
                #确定
                common.display_click('css,.ivu-modal-confirm-footer > .ivu-btn-primary')
                print('开启主账号转账控制')
                time.sleep(3)
            else:
                print('主账号转账控制已开启')
                pass
            #真实账户信息
            common.display_click('css,[href="#tdAccount"]')
        except Exception as msg:
            pub_method.log_output('!!--!!transfer_control_on').error(msg)

    #判断主账号转账给下级客户/代理控制是否开启
    def transfer_to_lower(self):
        try:
            common.display_click('css,[href="#masterAccount"]') #主账户信息
            time.sleep(1)
            for i in range(5,7):
                if common.get_attributes('css,label.switch>span.ivu-switch>input','value',i)=='true':#转账给下级客户控制
                    time.sleep(1)
                    common.display_click('css,label.switch>span.ivu-switch',i)
                    time.sleep(1)
                    common.display_click('css,.ivu-modal-confirm-footer > .ivu-btn-primary > span')
                    time.sleep(5)
                    print('关闭转账给下级控制开关，可进行非返佣账号转返佣账户转账方式')
                else:
                    print('转账给下级控制开关未开启，可进行非返佣账号转返佣账户转账方式')
        except Exception as msg:
            pub_method.log_output('!!--!!transfer_to_lower').error(msg)




    #判断主账号是IB/CL账号
    def type_is_ib(self,account):
        if int(float(str(account)[0:2]))==10:
            print('主账号为IB账号')
            return True
        else:
            print('主账号为CL账号')
            return False

    #判断转出交易账号是否为返佣账号
    def tdaccount_to_is_rebate(self,tdaccount_to):
        try:
            #获取IB账号下的返佣账号
            self.rebate_tdaccount=common.display_get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]'
            '/div[1]/div[2]/table/tbody/tr/td[1]/div/div/span',-2)
            print('该账号返佣账户为{}'.format(self.rebate_tdaccount))
            if str(tdaccount_to)==str(self.rebate_tdaccount):
                print('转入交易账号为返佣账号，转账类型为非返佣转返佣')
                return True
            else:
                print('转入交易账号为非返佣账户')
                return False
        except Exception as msg:
            pub_method.log_output('!!--!!tdaccount_to_is_rebate').error(msg)
    
    #判断转入转出账号状态是否满足转账条件
    def tdaccount_status(self):
        try:
            for i in [self.from_site,self.to_site]:
                self.tdaccount_status=common.display_get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/'
                'div[1]/div[2]/table/tbody/tr[{}]/td[5]/div/div/span'.format(i))
                if self.tdaccount_status in ('停用','Closed'):
                    #状态为停用时，更改交易账号状态
                    common.display_click('css,div.ivu-table-fixed-body>table>tbody>tr>td>div>div>div>div>a',2*i-1) #编辑
                    time.sleep(1)
                    common.display_click('css,form.ivu-form-label-right>div>div>div>div>div>div.ivu-select-selection',4)
                    time.sleep(1)
                    #选择暂停状态
                    common.display_click('css,.ivu-select-visible .ivu-select-dropdown-list > li',1) #0:激活 1：暂停
                    time.sleep(1)
                    #提交表单
                    common.display_click('css,button.ivu-btn-success>span',1)
                    time.sleep(1)
                    #判断交易账号激活+暂停个数是否超过五个
                    if self.status_num>=5:
                        common.display_click('xpath,//div[@class="ivu-modal-wrap"]//span',1) #去除提醒弹窗
                        time.sleep(1)
                    else:
                        pass
                    print('修改交易账号为暂停状态')
                    time.sleep(1)
                else:
                    print('交易账号状态满足转账条件')
        except Exception as msg:
            pub_method.log_output('!!--!!tdaccount_status').error(msg)


    #判断交易账户转账按钮是否被勾选
    def transfer_is_selected(self):
        try:
            for i in [self.from_site,self.to_site]:
                if not common.is_element_selected('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/div[1]'
                '/div[2]/table/tbody/tr[{}]/td[6]/div/div/div/label/span/input'.format(i),-1):#未被勾选时
                    common.display_click('css,div.ivu-table-fixed-body>table>tbody>tr>td>div>div>div>div>a',2*i-1) #编辑
                    time.sleep(1)
                    #勾选转账权限
                    common.display_click('xpath,//div[@class="checkbox ivu-form-item"]//input[@class="ivu-checkbox-input"]',-1)
                    time.sleep(1)
                    #提交
                    common.display_click('css,button.ivu-btn-success>span',1)
                    time.sleep(1)
                    if self.status_num>=5:
                        common.display_click('xpath,//div[@class="ivu-modal-wrap"]//span',1)
                        time.sleep(1)
                    else:
                        pass
                    time.sleep(1)
                    print('修改交易账户转账权限')
                else:
                    print('交易账号转账权限已勾选')
        except Exception as msg:
            pub_method.log_output('!!--!!transfer_is_selected').error(msg)
            
    
    #判断主账号交易账号是否满足转账条件
    def is_satisfy_transfer(self,account,tdaccount_from,tdaccount_to):
        try:
            #主账号转账权限
            self.transfer_control_on(account)
            #获取转入转出交易账号在交易账号列表中的位置
            self.from_site=self.where_is_tdaccount_bos(tdaccount_from)
            self.to_site=self.where_is_tdaccount_bos(tdaccount_to)
            #判断交易账号激活+暂停状态是否超过5个
            self.is_status_five()
            #交易账号状态
            self.tdaccount_status()
            #判断交易账号转账按钮是否被勾选
            self.transfer_is_selected()
            #判断主账号是否为IB
            if self.type_is_ib(account):
                if self.tdaccount_to_is_rebate(tdaccount_to):#判断转入交易账号是否为返佣账号
                    self.transfer_to_lower() #判断转账给下级控制是否开启
                else:
                    pass
            else:
                pass
            #self.closebrowser()
        except Exception as msg:
            pub_method.log_output('!!--!!is_satisfy_transfer').error(msg)

    #登录会员中心
    def logincp(self,username,psword):
        try:
            common.switch_windows(0)
            self.commethod.login_cp(username,psword)
        except Exception as msg:
            pub_method.log_output('!!--!!logincp').error(msg)

    #登出会员中心
    def logoutcp(self):
        try:
            common.switch_windows(0)
            time.sleep(1)
            self.commethod.logout_cp()
        except Exception as msg:
            pub_method.log_output('!!--!!logoutcp').error(msg)


    def transfer_action(self,tdaccount_from,tdaccount_to,amount,excelpath,row):
        try:
            time.sleep(2)
            #获取转出交易账号余额
            self.tdaccount_from_before_blance=self.get_tdaccount_balance(tdaccount_from)
            print('转出交易账号{}转账前余额为{}'.format(tdaccount_from,self.tdaccount_from_before_blance))
            e.saveainfo(excelpath,self.tdaccount_from_before_blance,'G',row)
            time.sleep(1)
            #内部转账
            common.display_click('css,li .menu-font',4)
            time.sleep(4)
            #转出账户
            common.display_click('xpath,//input[@class="el-input__inner"]',1)
            time.sleep(1)
            #选择转出交易账户
            common.display_click('xpath,//span[contains(.,"MT4 - {} (USD)")]'.format(tdaccount_from),1)
            time.sleep(3)
            #获取当前交易账号可转金额
            self.transfer_balance=float(pub_method.extract_numbers(common.display_get_text('xpath,//div[@class="balance"]')))/100
            time.sleep(1)
            if self.transfer_balance >= int(amount):#可转金额大于转账金额
                common.display_input('xpath,//input[@class="el-input__inner"]',int(amount),2)#输入转账金额
                time.sleep(1)
            else:#可转金额小于转账金额时，自动转账可转金额的1/2
                common.display_input('xpath,//input[@class="el-input__inner"]',int(self.transfer_balance/2),2)
                time.sleep(1)
                print('转账金额大于可转金额，更改转账金额为可转金额的1/2：{}'.format(int(self.transfer_balance/2)))
            #转入账号
            common.display_click('xpath,//input[@class="el-input__inner"]',5)
            time.sleep(1)
            common.display_click('xpath,//span[contains(.,"MT4 - {} (USD)")]'.format(tdaccount_to),1)
            time.sleep(1)
            #验证码
            common.display_input('xpath,//input[@class="el-input__inner"]','gvls',-1)
            time.sleep(1)
            #提交
            common.display_click('css,.submit .el-button')
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!transfer_action').error(msg)

    #判断转账是否完成或在处理中状态
    def is_successful_transfer(self):
        try:
            time.sleep(2)
            self.transfer_text=common.display_get_text('css,.icon > span')
            if self.transfer_text not in ('转账待处理','Request Pending'):
                print('转账成功')
                common.switch_windows(2)
                self.closebrowser()
                return True
            else:
                print('转账处理中需要审核')
                return False
        except Exception as msg:
            pub_method.log_output('!!--!!is_successful_transfer').error(msg)

    def review_transfer(self,account):
        try:
            common.switch_windows(2)
            #资金管理
            common.display_click('css,.ivu-badge>span',3)
            time.sleep(1)
            #资金转户
            common.display_click('css,.ivu-badge>span',7)
            time.sleep(2)
            #根据转出主账号搜索
            common.display_click('css,.ivu-select-default .ivu-icon',4)
            time.sleep(1)
            common.display_click('css,.ivu-select-visible li',2)
            time.sleep(1)
            #输入转出主账号
            common.display_input('css,.ivu-input-group > [placeholder]',account)
            time.sleep(1)
            #搜索
            common.display_click('css,.ivu-btn-icon-only > .ivu-icon')
            time.sleep(2)
            #勾选该转账记录
            common.display_click('css,td .ivu-checkbox-input')
            time.sleep(1)
            #完成
            common.display_click('css,.ivu-btn-success > span')
            time.sleep(3)
            try:
                if common.display_get_text('css,div.ivu-message-success span')=='success':
                    print('转账审核通过')
                    self.closebrowser()
                    return 'success'
            except:
                print('转账审核未通过')
                self.closebrowser()
                return 'failed'
        except Exception as msg:
            pub_method.log_output('!!--!!review_transfer').error(msg)



    def transfer_in_cp(self,username,psword,account,tdaccount_from,tdaccount_to,amount,excelpath,row):
        try:
            self.logincp(username,psword)
            time.sleep(10)
            self.transfer_action(tdaccount_from,tdaccount_to,amount,excelpath,row)
            if self.is_successful_transfer():
                print(self.transfer_text)
            else:
                self.review_transfer(account)
            time.sleep(1)
            #获取转账后账户余额
            common.switch_windows(0)
            time.sleep(1)
            #首页
            common.display_click('css,.el-menu-item > .menu-font')
            time.sleep(8)
            #获取转账成功后余额
            self.after_transfer_balance=self.get_tdaccount_balance(tdaccount_from)
            #保存
            e.saveainfo(excelpath,self.after_transfer_balance,'H',row)
        except Exception as msg:
            pub_method.log_output('!!--!!transfer_in_cp').error(msg)


    def closebrowser(self):
        common.close_browser()
    
    def quitbrowser(self):
        common.quit_browser()

