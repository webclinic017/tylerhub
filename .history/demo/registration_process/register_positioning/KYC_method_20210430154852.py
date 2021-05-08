import os
import sys
import time

path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=path_demo+r'\public'
sys.path.append(path_public)
from browser_actions import Commonweb
from other_actions import public_method
from common_method import commonmethod

path_process=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#实例化对象
pub_method=public_method()
common=Commonweb()

#继承基本类
class kyc_approve():
    global driver

    #默认以谷歌浏览器执行测试用例
    def browsertype(self,browsername='Chrome'):
        self.driver=common.open_browser(browsername)
        self.commethod=commonmethod(self.driver)

    #去除登录页弹窗
    def login_topup(self):
        common.switch_windows(0)
        self.commethod.remove_register_topup()

    #选择会员中心登录页语言
    def cp_lang(self,lang):
        self.commethod.choose_register_lang(lang)

    #访问会员中心及BOS登录页,选择页面语言
    def loginweb(self,lang):
        try:
            common.open_web('https://at-client-portal-uat.atfxdev.com/login')
            #点击弹窗
            common.switch_windows(0)
            self.commethod.remove_register_topup()
            time.sleep(1)
            #选择页面语言
            self.cp_lang(lang)
            time.sleep(1)
            #新开窗口访问bos登录页
            common.js_openwindows('https://at-bos-frontend-uat.atfxdev.com/login')
            #切换窗口
            common.switch_windows(1)
            #选择页面语言
            self.commethod.choose_bos_lang(lang)
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!loginweb').error('访问cp/bos登录页失败：{}'.format(msg))
   
    #登录会员中心
    def login_cp(self,username,psword):
        common.switch_windows(0)
        self.commethod.login_cp(username,psword)
        time.sleep(3)

    #去除首次登录会员中心的弹窗
    def fisrtcp_top(self):
        try:
            time.sleep(3)
            common.display_click('css,.el-checkbox__inner')
            time.sleep(1)
            common.web_click('css,.confirm-btn')
        except Exception as msg:
            pub_method.log_output('!!--!!topup').error('首次登录弹窗点击失败{}'.format(msg))

    #获取登录成功后的主账号
    def get_account_(self):
        try:
            time.sleep(5)
            #获取主账号文本
            acc=common.display_get_text('css,.user-name-font')
            #提取数字
            self.account=pub_method.extract_numbers(acc)
            return self.account
        except Exception as msg:
            pub_method.log_output('!!--!!topup').error('获取主账号失败{}'.format(msg))

    #判断是否为返佣账号，如是，点击返佣申请表格
    def is_rebate_type(self):
        if self.account[0:2]=='10':
            #点击代理申请
            time.sleep(2)
            common.display_click('css,.el-button--primary')
            time.sleep(2)
            #同意IB协议
            common.web_click('css,div.ps-agree-bot .el-checkbox__inner')
            time.sleep(1)
            #提交
            common.web_click('css,.agree-btn')
            time.sleep(1)
        else:
            #点击验证联系方式
            common.web_click('css,.el-button--primary')

    #登出会员中心
    def logout_cp(self):
        common.switch_windows(0)
        try:
            common.web_click('css,.el-icon--right')
            time.sleep(1)
            common.web_click('css,.drop-sub-title',12)
            time.sleep(1)
            common.web_click('css,.logout-btn-confirm')
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!lgoout_cp').error('登出会员中心失败：{}'.format(msg))

    #登录bos并打开客户名单页
    def login_bos(self,username,psword):
        try:
            #登录bos
            self.commethod.loginbos(username,psword)
            time.sleep(1)
            #点击客户管理
            common.web_click('css,.ivu-badge')
            time.sleep(1)
            #点击客户名单
            common.web_click('css,.ivu-menu-item',1)
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!lgoin-bos').error('登录bos失败：{}'.format(msg))

    #验证邮箱
    def verification_emali(self):
        try:
            self.is_rebate_type()
            time.sleep(1)
            #发送邮箱验证码
            common.web_click('css,.dialog-sendCode')
            time.sleep(1)
            #获取邮箱验证码
            self.get_emailcode_()
            #填写邮箱验证
            common.switch_windows(0)
            time.sleep(1)
            common.web_input('css,.el-input__inner',self.emailcode,1)
            time.sleep(1)
            #点击下一步
            common.web_click('css,.dialog-submit')
            time.sleep(1)
            #跳过手机验证码
            common.web_click('css,.doItLeTer-css')
            time.sleep(1)
            #点击完成
            common.web_click('css,.dialog-submit')
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!verification_emali').error(msg)

    #上传证件照
    def upload_ID_photo(self,path):
        try:
            common.web_click('css,.img-text-required')
            time.sleep(1)
            #调用基础类中的上传图片方法
            common.upload_img(path)
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!upload_ID_photo').error(msg)

    #随机选择出生日期与性别
    def choose_data_gender(self):
        try:
            #出生日期
            common.web_click('css,.el-input__inner',4)
            time.sleep(1)
            common.web_click('css,.el-date-picker__header-label')
            time.sleep(1)
            common.web_click('css,.el-picker-panel__icon-btn')
            time.sleep(1)
            #双击选择年份
            common.doubleclick('css,.el-picker-panel__icon-btn')
            time.sleep(2)
            common.web_click('css,table>tbody>tr>td.available',pub_method.random_int(31,40)) #年
            time.sleep(1)
            common.web_click('css,table.el-month-table>tbody>tr>td',pub_method.random_int(0,11))#月
            time.sleep(1)
            common.web_click('css,table.el-date-table>tbody>tr.el-date-table__row>td',pub_method.random_int(0,41))#日
            time.sleep(1)
            #随机性别
            common.web_click('css,.el-radio__inner',pub_method.random_int(0,1))
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!choose_data_gender').error(msg)

    #输入地址，勾选协议并提交表单
    def submit(self):
        try:
            #输入证件号码
            common.web_input('css,.el-input__inner',pub_method.get_purerange(12,'number'),5)
            time.sleep(1)
            #输入居住地址
            common.web_input('css,.el-input__inner',pub_method.get_purerange(12,'letter'),8)
            time.sleep(1)
            #勾选协议
            common.web_click('css,.el-checkbox__inner',1)
            time.sleep(1)
            #点击提交
            common.web_click('css,.submit-btn')
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!submit').error(msg)
     
    #获取邮箱验证码
    def get_emailcode_(self):
        try:
            #切换bos窗口
            common.switch_windows(1)
            time.sleep(1)
            #根据主账号搜索
            common.web_input('css,.ivu-input-default',self.account) #输入主账户
            time.sleep(1)
            common.web_click('css,.ivu-icon-ios-search',1) #点击搜索按钮
            time.sleep(1)
            #点击主账号进入账号详情页
            common.web_click('css,div.ivu-table-overflowX>table>tbody.ivu-table-tbody>tr>td',1)
            #切换到主账号详情页窗口
            common.switch_windows(2)
            time.sleep(1)
            #点击邮件记录
            common.web_click('css,.ivu-anchor-link-title',-2)
            time.sleep(2)
            #打开验证码邮件
            common.web_click('css,.tips',1)
            time.sleep(1)
            #获取验证码文本
            acc_text=common.get_text('xpath,//div[@class="ivu-drawer-wrap"]//tr[2]//tr[4]/td[1]/span')
            #提取数字
            self.emailcode=pub_method.extract_numbers(acc_text)
            #关闭当前页面
            self.closedriver()
            return self.emailcode
        except Exception as msg:
            pub_method.log_output('!!--!!get_emailcode_').error('获取邮箱验证失败{}'.format(msg))

    #中国区账号操作
    def china_kyc(self):
        #点击完善个人资料
        common.web_click('css,.el-button--primary')
        time.sleep(1)
        #上传正反面证件照
        common.display_click('css,.img-text-required')
        time.sleep(1)
        common.upload_img(path_process+r'\test_excel_data\card_front.exe')
        time.sleep(4)
        common.web_click('css,.img-text-required',1)
        time.sleep(1)
        common.upload_img(path_process+r'\test_excel_data\card_behind.exe')
        time.sleep(4)
        common.js_scroll('down')
        time.sleep(1)
        #点击下一步
        common.web_click('css,.submit-btn')
        time.sleep(3)
        #上传银行卡照片
        common.display_click('css,.img-text-required')
        time.sleep(1)
        common.upload_img(path_process+r'\test_excel_data\bank_card.exe')
        time.sleep(4)
        #重新输入银行卡号
        common.web_clear('css,.el-input__inner')
        time.sleep(1)
        common.display_input('css,.el-input__inner',pub_method.get_purerange(14,number))
        #一键填充
        common.web_click('css,.el-button--text')
        time.sleep(1)
        #下一步
        common.web_click('css,.submit-btn')
        time.sleep(2)
        #选择地址认证
        common.display_click('css,.btns')
        #上传地址证明
        common.display_click('css,.img-text-required')
        time.sleep(1)
        common.upload_img(path_process+r'\test_excel_data\address.exe')
        time.sleep(3)
        #点击提交
        common.web_click('css,.submit-btn')   


    #KYC认证表单操作
    def get_on_kyc(self,region):
        try:
            if region=='中国':
                self.china_kyc()
            else:
                #验证邮箱
                self.verification_emali()
                #上传证件照
                self.upload_ID_photo(path_process+r'\test_excel_data\kyc_img.exe')
                #选择出生日期及性别
                self.choose_data_gender()
                #输入证件号码，地址，勾选协议并提交表单
                self.submit()
                time.sleep(1)
                #去除公司声明弹窗
                self.fisrtcp_top()
        except Exception as msg:
            pub_method.log_output('!!--!!get_on_kyc').error('kyc表单填写失败：{}'.format(msg))

    #清空主账号搜索条件
    def clearaccount(self):
        try:
            common.switch_windows(1)
            time.sleep(1)
            common.web_clear('css,.ivu-input-default') #清空主账户
        except Exception as msg:
            pub_method.log_output('!!--!!clearaccount').error('清空主账号证失败{}'.format(msg))

    #获取KYC成功后的文本
    def get_kyc_success(self):
        try:
            time.sleep(4)
            self.text= common.get_text('css,.title',-1)
            return self.text
        except Exception as msg:
            pub_method.log_output('!!--!!get_kyc_success').error(msg)

    #关闭页面             
    def closedriver(self):
        common.close_browser()

    #退出浏览器
    def quitdriver(self):
        common.quit_browser()

    #失败截图保存
    def get_fail_img(self,name,filename):
        try:
            common.get_screenpict(name,filename)
        except Exception as msg:
            pub_method.log_output('!!--!!get_fail_img').error(msg)