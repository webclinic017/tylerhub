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

path_withdrawal=path_demo+r'\withdrawal'
common=Commonweb()
pub_method=public_method()
e=exceldata()

class location_withdrawal_incp():
    """
    判断逻辑：主账号出金权限是否开启；交易账号暂停+激活状态是否超过5个；出金交易账号状态判断；
    出金渠道判断：是否审核通过，审核通过后是否能在会员中心展示；出金方式是否超过三条，超过三条后是否都能在会员中心显示

    """

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

    #去除登录页弹窗
    def remove_topup(self):
        try:
            common.switch_windows(0)
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
    def where_is_traccount_bos(self,traccount):
        #获取交易账号列表的总行数
        self.tdaccount_list_len=common.get_lenofelement('xpath,//*[@id="tdAccount"]/div[2]/div/div/'
        'div[3]/div[1]/div[2]/table/tbody/tr/td[2]/div/span')
        time.sleep(1)
        for i in range(0,self.tdaccount_list_len):
            if str(common.get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/div[1]/div[2]/'
            'table/tbody/tr/td[1]/div/div/span',i))==str(traccount):
                return i+1
                break

    #判断主账号出金权限是否开启
    def account_is_openwithdrawal(self,account):
        try:
            #账户详情页
            self.ender_detail_page(account)
            #判断出金控制按钮是否开启
            if common.get_attributes('css,label.switch>span.ivu-switch>input','value',3)=='false':#获取input标签下value的属性值
                time.sleep(1)
                #开启主账号入金权限
                common.display_click('css,label.switch>span.ivu-switch',3)
                time.sleep(1)
                #确认
                common.display_click('css,.ivu-modal-confirm-footer > .ivu-btn-primary')
                time.sleep(3)
                print('开启主账号出金控制')
            else:
                print('主账号出金控制已开启')
            #真实账户信息
            common.display_click('css,[href="#tdAccount"]')
        except Exception as msg:
            pub_method.log_output('!!--!!account_is_openwithdrawal').error(msg)

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
            


    #判断交易账户状态
    def tdaccount_status(self,traccount,row):
        """"
        注：暂未对处理中账号做判断
        """"
        try:
            self.account_status=common.get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/'
            'div[1]/div[2]/table/tbody/tr[{}]/td[5]/div/div/span'.format(row))
            time.sleep(1)
            if self.account_status in ('停用','Closed'):
                time.sleep(1)
                #状态为停用时，更改交易账号状态
                common.display_click('css,div.ivu-table-fixed-body>table>tbody>tr>td>div>div>div>div>a',2*row-1) #编辑
                #更改交易账号状态，改为激活或者是暂停
                time.sleep(1)
                common.display_click('css,form.ivu-form-label-right>div>div>div>div>div>div.ivu-select-selection',4)
                time.sleep(1)
                #选择暂停状态
                common.display_click('css,.ivu-select-visible .ivu-select-dropdown-list > li',1) #0:激活 1：暂停
                time.sleep(1)
                #提交表单
                common.display_click('css,button.ivu-btn-success>span',1)
                time.sleep(1)
                #判断交易账户激活+暂停状态是否超过五个
                if self.status_num>=5:
                    common.display_click('xpath,//div[@class="ivu-modal-wrap"]//span',1) #去除提醒弹窗
                else:
                    pass                   
                print('修改交易账号{}为暂停状态'.format(traccount))
                time.sleep(1)
            else:
                print('交易账号{}状态为:{}'.format(traccount,self.account_status))
        except Exception as msg:
            pub_method.log_output('!!--!!tdaccount_status').error(msg)    

    #判断交易账号出金按钮是否被勾选
    def withdrawal_is_selected(self,traccount,row):
        try:
            # 判断出金按钮是否被勾选
            time.sleep(1)
            #未勾选时
            if not common.is_element_selected('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/div[1]/div[2]/'
            'table/tbody/tr[{}]/td[6]/div/div/div/label/span/input'.format(row),1):
                time.sleep(1)
                common.display_click('css,div.ivu-table-fixed-body>table>tbody>tr>td>div>div>div>div>a',2*row-1) #编辑
                time.sleep(1)
                #勾选出金权限
                common.display_click('xpath,//div[@class="checkbox ivu-form-item"]//input[@class="ivu-checkbox-input"]',1)
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
                print('已修改交易账号{}出金权限为勾选状态'.format(traccount))
            else:
                print('交易账号{}出金权限已勾选'.format(traccount))
        except Exception as msg:
            pub_method.log_output('!!--!!withdrawal_is_selected').error(msg)


    #判断是否存在出金方式且审核通过
    def is_wayto_withdrawal(self):
        try:
            #客户收款银行信息
            common.display_click('css,[href="#paymentMethod"]')
            time.sleep(1)
            if common.ele_is_displayed('css,div.bankItem>div.info',2):#存在支付渠道
                if common.get_lenofelement('css,div.bankItem>div.info')>1:#存在多个取款方式
                    for i in range(0,common.get_lenofelement('css,div.bankItem>div.info')):
                        if common.display_get_text('css,span.status',i) in ('审核通过','Approved'):
                            if common.get_attributes('css,.bankInfo > div .ivu-switch input','value',i)=='true':#会员中心按钮开启
                                print('出金渠道审核通过且能在会员中心使用')
                                break
                            else:
                                common.display_click('css,.bankInfo > div .ivu-switch',i) #开启会员中心权限
                                time.sleep(1)
                                common.display_click('css,.ivu-modal-confirm-footer > .ivu-btn-primary > span')
                                print('修改该出金渠道在会员中心使用权限')
                                break
                        else:
                            if i==common.get_lenofelement('css,div.bankItem>div.info')-1:
                                print('存在多个取款方式但都未审核')
                                self.creat_local_currency() #新建取款方式
                            else:
                                continue
                else:#单个取款方式
                    if common.display_get_text('css,span.status') in ('审核通过','Approved'):
                        if common.get_attributes('css,.bankInfo > div .ivu-switch input','value')=='true':
                            print('出金渠道审核通过')
                        else:
                            common.display_click('css,.bankInfo > div .ivu-switch')
                            time.sleep(1)
                            common.display_click('css,.ivu-modal-confirm-footer > .ivu-btn-primary > span')
                    else:
                        print('出金方式未审核通过')
                        self.creat_local_currency()
            else:#不存在出金方式
                print('该账号不存在本地银行支付及国际银行电汇出金方式')
                self.creat_local_currency()
        except Exception as msg:
            pub_method.log_output('!!--!!is_wayto_withdrawal').error(msg)


    #判断当地货币支付方式是否超过三条且都能在会员中心展示
    def islocal_surpass_three(self):
        try:
            self.cpsum=0
            if common.ele_is_displayed('css,div.bankItem>div.info',2): #存在出金渠道
                self.local_len=common.get_lenofelement('xpath,//*[@id="paymentMethod"]/div[2]/div/div/div[1]/div[2]/div')
                if self.local_len>=3:
                    for i in range(0,self.local_len):
                        while common.get_attributes('xpath,//*[@id="paymentMethod"]/div[2]'
                        '/div/div/div[1]/div[2]/div/div/div/span/span[2]/input','value',i)=='true':
                            self.cpsum=self.cpsum+1
                            break
                    return self.cpsum
                else:
                    print('本地货币支付方式未超过三条')
                    return self.cpsum
            else:
                return self.cpsum
        except Exception as msg:
            pub_method.log_output('!!--!!is_wayto_withdrawal').error(msg)



    #根据居住国家新建支付方式
    def creat_local_currency(self):
        """
        居住国为：区分中国与其他地区，中国地区新增本地银行出金方式，其他地区新增电子钱包出金方式
        """
        try:
            #基本资料
            common.display_click('css,[href="#clientInfo"]')
            time.sleep(1)
            self.live_country=common.display_get_text('xpath,//div[@class="page"]//div[7]//span')
            time.sleep(1)
            #客户收款银行信息
            common.display_click('css,[href="#paymentMethod"]')
            if self.live_country in ('中国','China'):
                #判断当地货币支付方式是否超过三条且都能在会员中心展示
                self.islocal_surpass_three()
                #新建本地银行出金方式
                common.display_click('xpath,//div[@id="paymentMethod"]//button//span')
                if self.cpsum>=3:
                    #去除提示
                    common.display_click('css,.ivu-modal-confirm-footer > .ivu-btn-primary')
                    time.sleep(1)
                else:
                    pass
                time.sleep(1)
                #收款人姓名
                common.display_input('xpath,//div[@class="ivu-drawer-wrap"]//input','uitest')
                time.sleep(1)
                #银行名称
                common.display_click('css,.ivu-form div:nth-of-type(8) div:nth-of-type(2) i:nth-of-type(1)')
                time.sleep(1)
                common.display_click('css,.ivu-select-dropdown-transfer li',3)#招商银行
                #分行名称
                common.display_input('xpath,//div[@class="ivu-drawer-wrap"]//input','testbank',4)
                time.sleep(1)
                #分行省份
                common.display_input('xpath,//div[@class="ivu-drawer-wrap"]//input','testprovince',5)
                time.sleep(1)
                #分行城市
                common.display_input('xpath,//div[@class="ivu-drawer-wrap"]//input','testcity',6)
                time.sleep(1)
                #银行卡号
                common.display_input('xpath,//div[@class="ivu-drawer-wrap"]//input',pub_method.get_purerange(14,'number'),7)
                time.sleep(1)
                #上传银行图片
                common.display_click('xpath,//div[@class="ivu-drawer-wrap"]//span',3)
                time.sleep(1)
                common.upload_img(path_withdrawal+r'\test_data\bank_card.exe')
                time.sleep(3)
                #新增
                common.display_click('xpath,//div[@class="ivu-drawer-wrap"]//span',-1)
                time.sleep(1)
                print('新增本地银行出金方式')
            else:
                #电子钱包
                common.display_click('xpath,//div[@id="paymentMethod"]//button//span',-2)
                time.sleep(1)
                #选择skrill渠道
                common.display_click('xpath,/html/body/div/div/div/div/div/div/form/div/div[1]/div/div/div/div/div[1]/div/i')
                time.sleep(1)
                common.display_click('css,.ivu-select-visible .ivu-select-dropdown-list > li')
                time.sleep(1)
                #输入随机邮箱
                common.display_input('xpath,//div[@class="ivu-drawer-wrap"]//input',pub_method.get_rangenemail(9),-1)
                time.sleep(1)
                #新增
                common.display_click('xpath,//div[@class="ivu-drawer-wrap"]//span',-1)
                time.sleep(2)
                print('新增E-wallet出金方式')
        except Exception as msg:
            pub_method.log_output('!!--!!creat_local_currency').error(msg)


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
            self.commethod.logout_cp()
        except Exception as msg:
            pub_method.log_output('!!--!!logoutcp').error(msg)


    #遍历会员中心首页的交易账户列表，找到入金交易账户所处位置
    def where_is_traccount_cp(self,traccount):
        #获取首页交易账号列表长度
        self.len_incp=common.get_lenofelement('css,.account-number-cla')
        time.sleep(1)
        new_str=str(4)+str(traccount)
        for i in range(0,self.len_incp):
            if pub_method.extract_numbers(common.get_text('css,.account-number-cla',i)) == new_str:
                return i+1
                break

    #获取入金交易账号余额
    def get_traccount_balance(self,traccount):
        try:
            self.cprows=self.where_is_traccount_cp(traccount)
            time.sleep(1)
            self.balance_text=common.display_get_text('css,div.card-for-loop>div>div.el-card__body>div>p>span',4*self.cprows-4)
            time.sleep(1)
            self.balance=float(self.balance_text.replace(',',''))
            print(type(self.balance_text.replace(',','')))
            return self.balance
        except Exception as msg:
            pub_method.log_output('!!--!!get_traccount_balance').error(msg)

    #判断该账号存在哪种可出金方式
    def usable_withdrawal(self):
        try:
            #账户设定页面
            common.display_click('xpath,//i[@class="el-icon-arrow-down el-icon--right"]')
            time.sleep(1)
            common.display_click('css,.el-client-menu > li > .drop-sub-title') #设置
            time.sleep(5)
            for i in ['localCurrency-card','bank-card','e-wallet-card']:
                if common.ele_is_displayed('css,.{} .isApprove'.format(i),2):
                    if i=='localCurrency-card':
                        self.withdrawal_type='当地货币银行转账'
                        print('当前账号可用出金方式为：{}'.format(self.withdrawal_type))
                        return self.withdrawal_type
                        break
                    elif i=='bank-card':
                        self.withdrawal_type='国际银行电汇'
                        print('当前账号可用出金方式为：{}'.format(self.withdrawal_type))
                        return self.withdrawal_type
                        break
                    else:
                        self.withdrawal_type='电子钱包'
                        print('当前账号可用出金方式为：{}'.format(self.withdrawal_type))
                        return self.withdrawal_type
                        break
                else:
                    print('该账号{}出金渠道不可用'.format(i))
        except Exception as msg:
            pub_method.log_output('!!--!!usable_withdrawal').error(msg)


    #出金
    def withdrawal_action(self,traccount,amount,excelpath,row):
        try:
            #获取当前交易账号的余额
            self.before_blance=self.get_traccount_balance(traccount)
            e.saveainfo(excelpath,self.before_blance,'F',row)
            print('出金前交易账户余额为{}'.format(self.before_blance))
            #判断当前账号存在哪种可用出金方式
            self.usable_withdrawal()
            #出金
            common.display_click('css,li.el-submenu>ul>li>ul>div>li>span',3)
            time.sleep(2)
            #选择交易账户
            common.display_click('xpath,//div[@class="el-select trade-account"]//input')
            time.sleep(2)
            common.display_click('xpath,//span[.="MT4 - {}"]'.format(traccount))
            time.sleep(1)
            #选择取款方式
            common.display_click('xpath,//input[@id="typeSelection"]')
            time.sleep(1)
            common.display_click('xpath,//span[.="{}"]'.format(self.withdrawal_type))
            time.sleep(1)
            #选择渠道
            common.display_click('css,.form > .left-row > div .el-select__caret',-1)
            time.sleep(1)
            if self.withdrawal_type=='电子钱包':
                #渠道选择skill时
                common.display_click('xpath,//span[.="Skrill"]')
                time.sleep(1)
                #电邮
                common.display_click('css,.form > .left-row > div .el-select__caret',-1)
                time.sleep(1)
                common.display_click('css,[x-placement="bottom-start"] li > span')
                time.sleep(1)
            else:#非skill渠道时
                common.display_click('css,[x-placement="bottom-start"] .el-select-dropdown__item')
                time.sleep(1)
            #获取当前交易账号可取款金额
            self.withdrawal_amount=float(pub_method.extract_numbers(common.display_get_text('xpath,//div[@class="balance"]')))/100
            print('当前交易账号可取款金额为：{}'.format(self.withdrawal_amount))
            if int(amount)>=self.withdrawal_amount:
                print('取款金额大于可取款金额，更改出金金额为可取款金额的1/2：{}'.format(int(self.withdrawal_amount/2)))
                common.display_input('xpath,//div[@class="left-row-content el-row"]'
                '//input[@class="el-input__inner"]',int(self.withdrawal_amount/2))
            else:
                common.display_input('xpath,//div[@class="left-row-content el-row"]'
                '//input[@class="el-input__inner"]',int(amount))
            time.sleep(1)
            #输入验证码
            common.display_input('css,.el-input__inner','gvls',-1)
            time.sleep(1)
            #勾选条款
            common.display_click('css,.el-checkbox__inner')
            time.sleep(1)
            #提交
            common.display_click('css,.allow_color')
            time.sleep(1)
            #确认提交
            common.display_click('css,.allow_color')
            time.sleep(1)
            try:
                common.display_click('css,.btn-confirm')
                time.sleep(1)
            except:
                print('无手续费')
        except Exception as msg:
            pub_method.log_output('!!--!!withdrawal_action').error(msg)

            
    #BOS审核出金
    def review_withdrawal(self,traccount):
        try:
            common.switch_windows(2)
            #资金管理
            common.display_click('css,.ivu-badge>span',3)
            time.sleep(1)
            #出金管理
            common.display_click('css,.ivu-badge>span',5)
            time.sleep(2)
            #筛选搜索条件为交易账号
            common.display_click('css,.ivu-select-single .ivu-icon',2)
            time.sleep(1)
            common.display_click('css,.ivu-select-visible li',7)
            time.sleep(1)
            #输入交易账号
            common.display_input('css,.ivu-input-group > [placeholder]',traccount)
            time.sleep(1)
            #搜索
            common.display_click('css,.ivu-btn-icon-only > .ivu-icon')
            time.sleep(3)
            #勾选该条出金记录
            common.display_click('css,td .ivu-checkbox-input')
            time.sleep(1)
            #转完成
            common.display_click('css,.ivu-btn-success > span')
            time.sleep(1)
            self.closebrowser()
        except Exception as msg:
            pub_method.log_output('!!--!!review_withdrawal').error(msg)

    #判断主账号交易账号是否满足出金条件
    def is_satisfy_withdrawal(self,account,traccount):
        try:
            #判断主账号出金控制是否开启
            self.account_is_openwithdrawal(account)
            #获取交易账号在列表中所在位置
            self.rows=self.where_is_traccount_bos(traccount)
            #判断交易账号激活+暂停状态是否超过或等于5个
            self.is_status_five()
            #判断交易账号状态
            self.tdaccount_status(traccount,self.rows)
            #判断交易账号出金按钮是否被勾选
            self.withdrawal_is_selected(traccount,self.rows)
            #判断是否存在可用的出金方式,不存在则新建
            self.is_wayto_withdrawal()
        except Exception as msg:
            pub_method.log_output('!!--!!is_satisfy_withdrawal').error(msg)

    #登录会员中心出金，bos审核
    def withdrawal_cp(self,username,psword,traccount,amount,excelpath,row):
        try:
            #登录会员中心
            self.logincp(username,psword)
            time.sleep(10)
            #出金
            self.withdrawal_action(traccount,amount,excelpath,row)
            #bos审核出金
            self.review_withdrawal(traccount)
            #获取出金后交易账号余额
            common.switch_windows(0)
            common.display_click('css, .el-menu-item > .menu-font')
            time.sleep(5)
            self.after_balance=self.get_traccount_balance(traccount)
            e.saveainfo(excelpath,self.after_balance,'G',row)
            print('出金后交易账号余额为：{}'.format(self.after_balance))
        except Exception as msg:
            pub_method.log_output('!!--!!withdrawal_cp').error(msg)
            

    def closebrowser(self):
        common.close_browser()

    def quitbrowser(self):
        common.quit_browser()