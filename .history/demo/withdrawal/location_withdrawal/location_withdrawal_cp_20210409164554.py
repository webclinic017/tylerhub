import os
import random
import sys
import time
import datetime
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



class location_withdrawal_incp():

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
        'div[3]/div[1]/div[2]/table/tbody/tr/td[1]/div/div/span')
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
        num=0
        for i in range(1,self.tdaccount_list_len+1):
            self.status=common.display_get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/'
            'div[1]/div[2]/table/tbody/tr[{}]/td[5]/div/div/span'.format(i))
            while self.status in ('暂停','激活','Suspended','Active'):
                num=num+1
        print(num)
        if num >=5:
            return True
        else:
            return False

    #判断交易账户状态
    def tdaccount_status(self,traccount,row):
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
                if self.is_status_five():
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
                if self.is_status_five():
                    common.display_click('xpath,//div[@class="ivu-modal-wrap"]//span',1)
                    time.sleep(1)
                else:
                    pass
                time.sleep(1)
                print('已修改交易账号{}出金权限为勾选状态'.format(traccount))
            else:
                print('交易账号{}出金权限已勾选'.format(traccount))
            #关闭页面
            #self.closebrowser()
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
                            print(i)
                            if common.is_element_selected('css,.bankInfo > div .ivu-switch',i):
                                print('出金渠道审核通过且能在会员中心使用')
                                break
                            else:
                                common.display_click('css,.bankInfo > div .ivu-switch',i) #开启会员中心权限
                                time.sleep(1)
                                common.display_click('css,.ivu-modal-confirm-footer > .ivu-btn-primary > span')
                                print('修改该出金渠道在会员中心使用权限')
                                break
                        else:
                            continue
                    else:
                        print('出金方式未审核通过')
                        self.creat_local_currency() #新增出金方式
                else:
                    if common.display_get_text('css,span.status') in ('审核通过','Approved'):
                        if common.is_element_selected('css,.bankInfo > div .ivu-switch'):
                            print('出金渠道审核通过')
                        else:
                            common.display_click('css,.bankInfo > div .ivu-switch')
                            time.sleep(1)
                            common.display_click('css,.ivu-modal-confirm-footer > .ivu-btn-primary > span')
                    else:
                        print('出金方式未审核通过')
                        self.creat_local_currency()
            else:
                print('该账号不存在本地银行支付及国际银行电汇出金方式')
                self.creat_local_currency()
        except Exception as msg:
            pub_method.log_output('!!--!!is_wayto_withdrawal').error(msg)


    #判断当地货币支付方式是否超过三条且都能在会员中心展示
    def islocal_surpass_three(self):
        try:
            self.local_len=common.get_lenofelement('xpath,//*[@id="paymentMethod"]/div[2]/div/div/div[1]/div[2]/div')
            cpsum=0
            if self.local_len>=3:
                for i in range(0,self.local_len):
                    if common.is_element_selected('xpath,//*[@id="paymentMethod"]/div[2]/div/div/div[1]/div[2]/div/div/div/span/span[2]',i):
                        cpsum=cpsum+1
                if cpsum>=3:
                    return True
                else:
                    return False
            else:
                print('本地货币支付方式未超过三条')
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
            if self.live_country in ('中国','China'):
                #新建本地银行出金方式
                common.display_click('xpath,//div[@id="paymentMethod"]//button//span')
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
                common.display_click('css,.ivu-select',-1)
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



    #判断主账号交易账号是否满足出金条件
    def is_satisfy_withdrawal(self,account,traccount):
        try:
            #判断主账号出金控制是否开启
            self.account_is_openwithdrawal(account)
            #获取交易账号在列表中所在位置
            self.rows=self.where_is_traccount_bos(traccount)
            print(self.rows)
            #判断交易账号状态
            self.tdaccount_status(traccount,self.rows)
            #判断交易账号出金按钮是否被勾选
            self.withdrawal_is_selected(traccount,self.rows)
            #判断是否存在可用的出金方式,不存在则新建
            self.is_wayto_withdrawal()
            self.closebrowser()
        except Exception as msg:
            pub_method.log_output('!!--!!is_satisfy_withdrawal').error(msg)


    #登录会员中心
    def logincp(self,username,psword):
        try:
            common.switch_windows(0)
            self.commethod.login_cp(username,psword)
        except Exception as msg:
            pub_method.log_output('!!--!!logincp').error(msg)


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
            self.balance=common.display_get_text('css,div.card-for-loop>div>div.el-card__body>div>p>span',4*self.cprows-4)
            return self.balance
        except Exception as msg:
            pub_method.log_output('!!--!!get_traccount_balance').error(msg)

    #出金
    # def withdrawal_action(self,traccount,amount):
    #     time.sleep(8)
    #     try:
    #         #获取当前交易账号的余额
    #         self.before_blance=float(self.get_traccount_balance(traccount))
    #         print('出金前交易账户余额为{}'.format(self.before_blance))
    #         #出金
    #         common.display_click('css,li.el-submenu>ul>li>ul>div>li>span',2)
    #         time.sleep(2)
    #         #选择交易账户
    #         common.display_click('xpath,//div[@class="el-select trade-account"]//input')
    #         time.sleep(1)
    #         common.display_click('xpath,//span[.="MT4 - {}"]'.format(traccount))
    #         time.sleep(1)
    #         #选择取款方式
    #     #     common.display_click('xpath,//input[@id="typeSelection"]')
    #     #     time.sleep(1)
    #     #     #满足如下居住国家选择本地货币银行出金
    #     #     if self.live_country in ('中国','中国台湾','中国香港','南韩','越南','日本','中国澳门','菲律宾','马来西亚','印尼','泰国','缅甸'):

    #     # except Exception as msg:
    #     #     pub_method.log_output('!!--!!withdrawal_action').error(msg)

            








    def closebrowser(self):
        common.close_browser()

    def quitbrowser(self):
        common.quit_browser()