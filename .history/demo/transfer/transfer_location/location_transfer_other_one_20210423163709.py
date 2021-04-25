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

class locathion_of_transfer():

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
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!get_url').error(msg)

    #登录页弹窗
    def remove_topup(self):
        try:
            self.commethod.remove_register_topup()
        except Exception as msg:
            pub_method.log_output('!!--!!remove_topup').error(msg)

    #进入详情页
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
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!ender_detail_page').error(msg)

    #判断主账号转账控制是否开启
    def transfer_control_on(self):
        try:
            #主账户信息
            common.display_click('css,[href="#masterAccount"]')
            if common.get_attributes('css,label.switch>span.ivu-switch>input','value',4)=='false':
                time.sleep(1)
                #开启转账控制权限
                common.display_click('css,label.switch>span.ivu-switch',4)
                time.sleep(1)
                #确定
                common.display_click('css,.ivu-modal-confirm-footer > .ivu-btn-primary')
                time.sleep(8)
                print('开启主账号转账控制')
            else:
                print('主账号转账控制已开启')
                pass
        except Exception as msg:
            pub_method.log_output('!!--!!transfer_control_on').error(msg)


    #判断主账号转账给下级客户/代理控制是否开启
    def transfer_to_lower(self):
        try:
            time.sleep(1)
            for i in range(5,7):
                if common.get_attributes('css,label.switch>span.ivu-switch>input','value',i)=='false':#转账给下级客户控制
                    time.sleep(1)
                    common.display_click('css,label.switch>span.ivu-switch',i)
                    time.sleep(1)
                    common.display_click('css,.ivu-modal-confirm-footer > .ivu-btn-primary > span')
                    time.sleep(8)
                    print('开启转账给下级控制开关，上级返佣账号可给下级IB/CL转账')
                else:
                    print('转账给下级控制开关未关闭，上级返佣账号可给下级IB/CL转账')
        except Exception as msg:
            pub_method.log_output('!!--!!transfer_to_lower').error(msg)


    #判断转入转出账号状态是否满足转账条件
    def tdaccount_status_is_satisfy(self,site):
        try:
            self.tdaccount_status=common.display_get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/'
            'div[1]/div[2]/table/tbody/tr[{}]/td[5]/div/div/span'.format(site))
            time.sleep(2)
            if self.tdaccount_status in ('停用','Closed'):
                #状态为停用时，更改交易账号状态
                common.display_click('css,div.ivu-table-fixed-body>table>tbody>tr>td>div>div>div>div>a',2*site-1) #编辑
                time.sleep(1)
                common.display_click('css,form.ivu-form-label-right>div>div>div>div>div>div.ivu-select-selection',4)
                time.sleep(1)
                #选择暂停状态
                common.display_click('css,.ivu-select-visible .ivu-select-dropdown-list > li',1) #0:激活 1：暂停
                time.sleep(1)
                #提交表单
                common.display_click('css,button.ivu-btn-success>span',1)
                time.sleep(2)
                #判断交易账号激活+暂停个数是否超过五个
                if self.status_num>=5:
                    common.display_click('xpath,//div[@class="ivu-modal-wrap"]//span',1) #去除提醒弹窗
                    time.sleep(2)
                else:
                    self.numof_status=self.status_num
                print('修改交易账号为暂停状态')
                time.sleep(1)
            else:
                print('交易账号状态满足转账条件')
        except Exception as msg:
            pub_method.log_output('!!--!!tdaccount_status').error(msg)


    #判断交易账户转账按钮是否被勾选
    def transfer_is_selected(self,site):
        try:
            time.sleep(1)
            if not common.is_element_selected('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/div[1]'
            '/div[2]/table/tbody/tr[{}]/td[6]/div/div/div/label/span/input'.format(site),-1):#未被勾选时
                common.display_click('css,div.ivu-table-fixed-body>table>tbody>tr>td>div>div>div>div>a',2*site-1) #编辑
                time.sleep(1)
                #勾选转账权限
                common.display_click('xpath,//div[@class="checkbox ivu-form-item"]//input[@class="ivu-checkbox-input"]',-1)
                time.sleep(1)
                #提交
                common.display_click('css,button.ivu-btn-success>span',1)
                time.sleep(1)
                if self.status_num>=5:
                    common.display_click('xpath,//div[@class="ivu-modal-wrap"]//span',1)
                    time.sleep(2)
                else:
                    pass
                time.sleep(1)
                print('修改交易账户转账权限')
            else:
                print('交易账号转账权限已勾选')
        except Exception as msg:
            pub_method.log_output('!!--!!transfer_is_selected').error(msg)



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


    #判断主账号是IB/CL账号
    def type_is_ib(self,account):
        if int(float(str(account)[0:2]))==10:
            print('主账号为IB账号')
            return True
        else:
            print('主账号为CL账号')
            return False


    #判断交易账号是否为返佣账号
    def tdaccount_is_rebate(self,tdaccount):
        try:
            #获取IB账号下的返佣账号
            time.sleep(1)
            self.rebate_tdaccount=common.display_get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]'
            '/div[1]/div[2]/table/tbody/tr/td[1]/div/div/span',-2)
            time.sleep(1)
            print('该账号返佣账户为{}'.format(self.rebate_tdaccount))
            if str(tdaccount)==str(self.rebate_tdaccount):
                print('交易账号为返佣账号佣')
                return True
            else:
                print('交易账号非返佣账户')
                return False
        except Exception as msg:
            pub_method.log_output('!!--!!tdaccount_is_rebate').error(msg)


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



    #判断转账账户类型是否满足转账给下级逻辑
    def is_account_satisfy_logic(self,account_from,tdaccount_from,account_to,tdaccount_to):
        try:
            #判断转出主账户是否为IB
            if self.type_is_ib(account_from):
                print('转出主账户{}为IB，继续执行用例'.format(account_from))
                #详情页
                self.ender_detail_page(account_from)
                common.switch_windows(2)
                time.sleep(1)
                #真实账号信息
                common.display_click('css,[href="#tdAccount"]')
                time.sleep(8)
                #判断转出交易账号是否为返佣账号
                if self.tdaccount_is_rebate(tdaccount_from):
                    print('转出交易账号{}为返佣账号'.format(tdaccount_from))
                    #判断转入主账号是IB/CL
                    if self.type_is_ib(account_to):
                        print('转入主账号{}为IB'.format(account_to))
                        self.ender_detail_page(account_to) #转入主账号详情页
                        common.switch_windows(3)
                        time.sleep(1)
                        common.display_click('css,[href="#tdAccount"]') #真实账号信息
                        time.sleep(8)
                        #判断转入交易账号是否为返佣账号
                        if self.tdaccount_is_rebate(tdaccount_to):
                            print('转入交易账号{}为返佣账户，上级返佣转下级返佣'.format(tdaccount_to))
                            #判断转出主账号转账权限是否开启
                            common.switch_windows(2)
                            time.sleep(1)
                            self.transfer_control_on()
                            #判断主账号转账给下级控制是否开启
                            self.transfer_to_lower()
                            #获取转出交易账号在交易账户列表中的位置
                            self.tdaccount_from_site=self.where_is_tdaccount_bos(tdaccount_from)
                            #获取交易账号激活+暂停状态总数
                            self.is_status_five()
                            #判断转出交易账号状态
                            self.tdaccount_status_is_satisfy(self.tdaccount_from_site)
                            #再次判断交易账号激活+暂停状态是否超过5个
                            self.is_status_five()
                            #判断交易账户转账按钮是否被勾选
                            self.transfer_is_selected(self.tdaccount_from_site)
                            return False
                        else:
                            print('转入交易账号必须是返佣账号')
                            return True
                    else:#转入主账号为CL
                        print('转入主账号为CL，对转入交易账号不做返佣账户的判断')
                        return False
                else:
                    print('转出交易账号必须是返佣账号')
                    return True
            else:
                print('转出主账户{}为CL，跳过此条用例'.format(account_from))
                return True
        except Exception as msg:
            pub_method.log_output('!!--!!is_account_satisfy_logic').error(msg)


    