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
            common.open_web('https://at-bos-frontend-uat.atfxdev.com/login')
            time.sleep(1)
            self.commethod.choose_bos_lang(lang)
            time.sleep(1)
            self.commethod.loginbos(username,psword)
            #客户管理
            common.display_click('css,.ivu-badge>span')
            time.sleep(1)
            #客户名单
            common.display_click('css,[data-old-padding-top] > [href="/client/clientListNew/:type*"]')
        except Exception as msg:
            pub_method.log_output('!!--!!get_url').error(msg)

    #进入客户详情页
    def ender_detail_page(self,account):
        try:
            #清空输入框
            common.switch_windows(0)
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
            common.switch_windows(1)
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
            if common.get_attributes('css,label.switch>span.ivu-switch>input','value',-1)=='false':
                time.sleep(1)
                #开启转账控制权限
                common.display_click('css,label.switch>span.ivu-switch',-1)
                time.sleep(1)
                #确定
                common.display_click('css,.ivu-modal-confirm-footer > .ivu-btn-primary')
                print('开启主账号转账控制')
            else:
                print('主账号转账控制已开启')
                pass
            #真实账户信息
            common.display_click('css,[href="#tdAccount"]')
        except Exception as msg:
            pub_method.log_output('!!--!!transfer_control_on').error(msg)

    #判断转入转出账号状态是否满足转账条件
    def trdaccount_status(self):
        try:
            for i in [self.from_site,self.to_site]:
                self.traccount_status=common.display_get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/'
                'div[1]/div[2]/table/tbody/tr[{}]/td[5]/div/div/span'.format(i))
                if self.traccount_status in ('停用','Closed'):
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
                    else:
                        pass
                    print('修改交易账号为暂停状态')
                else:
                    print('交易账号状态满足转账条件')
        except Exception as msg:
            pub_method.log_output('!!--!!trdaccount_status').error(msg)


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
                    print('转入转出交易账号转账权限已勾选')
        except Exception as msg:
            pub_method.log_output('!!--!!transfer_is_selected').error(msg)
            
    #判断主账号交易账号是否满足转账条件
    def is_satisfy_transfer(self,account,traccount_from,traccount_to):
        try:
            #主账号转账权限
            self.transfer_control_on(account)
            #获取转入转出交易账号在交易账号列表中的位置
            self.from_site=self.where_is_traccount_bos(traccount_from)
            self.to_site=self.where_is_traccount_bos(traccount_to)
            #判断交易账号激活+暂停状态是否超过5个
            self.is_status_five()
            #交易账号状态
            self.trdaccount_status()
            #判断交易账号转账按钮是否被勾选
            self.transfer_is_selected()
        except Exception as msg:
            pub_method.log_output('!!--!!is_satisfy_transfer').error(msg)







