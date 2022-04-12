import os
import sys
import time

path_public=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'public')
sys.path.append(path_public)
from browser_actions import Commonweb
from common_method import Commonmethod
from handlelog import MyLog
from randomdata import Random_data
from read_dataconfig import ReadConfig

path_process=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#实例化对象
randomData=Random_data()
common=Commonweb()
log=MyLog()
conFig=ReadConfig()

#继承基本类
class Kyc_approve():
    global driver

    #默认以谷歌浏览器执行测试用例
    def browsertype(self,browsername='Chrome'):
        self.driver=common.open_browser(browsername)
        self.commethod=Commonmethod(self.driver)

    #去除登录页弹窗
    def login_topup(self):
        common.switch_windows(0)
        self.commethod.remove_register_topup()

    #选择会员中心登录页语言
    def cp_lang(self,lang):
        self.commethod.choose_register_lang(lang)

    #访问会员中心及BOS登录页,选择页面语言
    def loginweb(self,environment,lang):
        try:
            common.open_web(conFig.get_value('cp_login', '{}'.format(environment)))
            #点击弹窗
            common.switch_windows(0)
            self.commethod.remove_register_topup()
            time.sleep(1)
            #选择页面语言
            self.cp_lang(lang)
            time.sleep(1)
            #新开窗口访问bos登录页
            common.js_openwindows(conFig.get_value('bos_login', '{}'.format(environment)))
            #切换窗口
            common.switch_windows(1)
            #选择页面语言
            self.commethod.choose_bos_lang(lang)
            time.sleep(1)
        except Exception as msg:
            log.my_logger('!!--!!loginweb').error('访问cp/bos登录页失败：{}'.format(msg))
   
    #登录会员中心
    def login_cp(self,username,psword):
        common.switch_windows(0)
        self.commethod.login_cp(username,psword)
        time.sleep(3)

    #去除弹窗，公司声明
    def fisrtcp_top(self):
        try:
            common.display_click('css,.el-checkbox__inner')
            time.sleep(1)
            common.web_click('css,.confirm-btn')
        except Exception as msg:
            log.my_logger('!!--!!fisrtcp_top').error('首次登录弹窗点击失败{}'.format(msg))

    #获取登录成功后的主账号
    def get_account_(self):
        try:
            time.sleep(5)
            #获取主账号文本
            acc=common.display_get_text('css,.user-name-font')
            #提取数字
            self.account=randomData.extract_numbers(acc)
            return self.account
        except Exception as msg:
            log.my_logger('!!--!!get_account_').error('获取主账号失败{}'.format(msg))

    #判断是否为返佣账号，如是，点击返佣申请表格
    def is_rebate_type(self):
        if self.account[0:2]=='10':
            #点击代理申请
            # time.sleep(1)
            # common.display_click('css,.el-button--primary')
            time.sleep(2)
            #同意IB协议
            common.web_click('css,div.ps-agree-bot .el-checkbox__inner')
            time.sleep(1)
            #提交
            common.web_click('css,.agree-btn')
            time.sleep(2)
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
            log.my_logger('!!--!!lgoout_cp').error('登出会员中心失败：{}'.format(msg))

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
            log.my_logger('!!--!!lgoin-bos').error('登录bos失败：{}'.format(msg))

    #验证邮箱
    def verification_emali(self):
        try:
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
            log.my_logger('!!--!!verification_emali').error(msg)

    #上传证件照
    def upload_ID_photo(self,exe_path,pic_path):
        try:
            common.web_click('css,.img-text-required')
            time.sleep(1)
            #调用基础类中的上传图片方法
            common.upload_img(exe_path,pic_path)
            time.sleep(1)
        except Exception as msg:
            log.my_logger('!!--!!upload_ID_photo').error(msg)

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
            time.sleep(1)
            common.web_click('css,table>tbody>tr>td.available',randomData.random_int(30,39)) #年
            time.sleep(1)
            common.web_click('css,table.el-month-table>tbody>tr>td',randomData.random_int(0,11))#月
            time.sleep(1)
            common.web_click('css,table.el-date-table>tbody>tr.el-date-table__row>td',randomData.random_int(0,41))#日
            time.sleep(1)
            #随机性别
            common.web_click('css,.el-radio__inner',randomData.random_int(0,1))
            time.sleep(1)
            # #中间名
            # common.web_input('css,.el-input__inner', 'test',3)
            # time.sleep(0.5)
        except Exception as msg:
            log.my_logger('!!--!!choose_data_gender').error(msg)

    #输入地址，勾选协议并提交表单
    def submit(self):
        try:
            #输入证件号码
            common.web_input('css,.el-input__inner',randomData.get_purerange(12,'number'),5)
            time.sleep(1)
            #输入居住地址
            common.web_input('css,.el-input__inner',randomData.get_purerange(12,'letter'),8)
            time.sleep(1)
            #勾选协议
            common.web_click('css,.el-checkbox__inner',1)
            time.sleep(1)
            #点击提交
            common.web_click('css,.submit-btn')
            time.sleep(4)
        except Exception as msg:
            log.my_logger('!!--!!submit').error(msg)
     
    #获取邮箱验证码
    def get_emailcode_(self):
        try:
            #切换bos窗口
            common.switch_windows(1)
            time.sleep(1)
            #根据主账号搜索
            common.web_clear('css,.ivu-input-default')
            time.sleep(0.5)
            common.web_input('css,.ivu-input-default',self.account) #输入主账户
            time.sleep(1)
            common.web_click('css,.ivu-icon-ios-search',1) #点击搜索按钮
            time.sleep(3)
            #点击主账号进入账号详情页
            common.web_click('css,div.ivu-table-overflowX>table>tbody.ivu-table-tbody>tr>td',1)
            time.sleep(0.5)
            #切换到主账号详情页窗口
            common.switch_windows(2)
            time.sleep(2)
            #点击邮件记录
            common.web_click("xpath,//a[.='邮件记录']")
            time.sleep(1)
 
            while True:
                emailtext=common.get_text('css,.emailRecod-table .ivu-table-tip span')
                if not emailtext=='暂无数据':
                    break
                else:
                    continue
            time.sleep(2)
            common.web_click('css,.tips',1)            
            time.sleep(1)
            #获取验证码文本
            acc_text=common.get_text('xpath,//div[@class="ivu-drawer-wrap"]//tr[2]//tr[4]/td[1]/span')
            #提取数字
            self.emailcode=randomData.extract_numbers(acc_text)
            #关闭当前页面
            self.closedriver()
            return self.emailcode
        except Exception as msg:
            log.my_logger('!!--!!get_emailcode_').error('获取邮箱验证失败{}'.format(msg))

    #中国区账号操作
    def china_kyc(self):
        #上传正反面证件照
        common.display_click('css,.img-text-required')
        time.sleep(1)
        common.upload_img(path_process+r'\test_excel_data\upimg.exe',path_process+r'\test_excel_data\front.jpg')
        time.sleep(4)
        common.web_click('css,.img-text-required',1)
        time.sleep(1)
        common.upload_img(path_process+r'\test_excel_data\upimg.exe',path_process+r'\test_excel_data\behind.jpg')
        time.sleep(4)
        common.js_scroll('down')
        #一键填充
        #common.display_click('css,div.el-col-8 > button > span',1)
        time.sleep(1)
        #点击下一步
        common.web_click('css,.submit-btn')
        time.sleep(6)
        #页面是否响应
        while True:
            if common.ele_is_displayed('css,.el-loading-text', 1):
                continue
            else:
                break
        #上传银行卡照片
        common.display_click('css,.img-text-required')
        time.sleep(1)
        common.upload_img(path_process+r'\test_excel_data\upimg.exe',path_process+r'\test_excel_data\bank_card.jpg')
        time.sleep(4)
        #重新输入银行卡号
        common.web_clear('css,.el-input__inner')
        time.sleep(1)
        common.display_input('css,.el-input__inner',randomData.get_purerange(14,'number'))
        time.sleep(1)
        #银行名称
        common.web_clear('css,.el-input__inner',2)
        time.sleep(0.5)
        common.display_input('css,.el-input__inner', 'bankname',2)
        time.sleep(0.5)
        #分行名称
        common.display_input('css,.el-input__inner', 'bankbranch',3)
        time.sleep(0.5)
        #分行省份
        common.display_input('css,.el-input__inner', 'bankprovince',4)
        time.sleep(0.5)
        #分行城市
        common.display_input('css,.el-input__inner', 'bankcity',5)
        time.sleep(0.5)
        #勾选协议
        common.display_click('css,.el-checkbox__inner')
        time.sleep(0.5)
        #下一步
        common.web_click('css,.submit-btn')
        time.sleep(5)
        while True:
            if common.ele_is_displayed('css,.el-loading-text', 1):
                continue
            else:
                break
        #选择地址认证
        common.display_click('css,.la-file-alt')
        time.sleep(1)
        #上传地址证明
        common.display_click('css,.img-text-required')
        time.sleep(1)
        common.upload_img(path_process+r'\test_excel_data\upimg.exe',path_process+r'\test_excel_data\address.jpg')
        time.sleep(4)
        #点击提交
        common.web_click('css,.submit-btn')   


    #KYC认证表单操作
    def get_on_kyc(self,region):
        try:
            self.is_rebate_type()
            if region=='中国':
                self.china_kyc()
            else:
                #验证邮箱
                self.verification_emali()
                time.sleep(1)
                common.display_click('css,.img-text')
                time.sleep(1)
                #上传证件照
                common.upload_img(path_process+r'\test_excel_data\upimg.exe',path_process+r'\test_excel_data\creataccount.jpg')
                time.sleep(3)
                #选择出生日期及性别
                self.choose_data_gender()
                #输入证件号码，地址，勾选协议并提交表单
                self.submit()
                time.sleep(1)
        except Exception as msg:
            log.my_logger('!!--!!get_on_kyc').error('kyc表单填写失败：{}'.format(msg))

    #清空主账号搜索条件
    def clearaccount(self):
        try:
            common.switch_windows(1)
            time.sleep(1)
            common.web_clear('css,.ivu-input-default') #清空主账户
        except Exception as msg:
            log.my_logger('!!--!!clearaccount').error('清空主账号证失败{}'.format(msg))

    #获取KYC成功后的文本
    def get_kyc_success(self):
        try:
            time.sleep(2)
            #刷新页面
            common.general_refresh_()
            time.sleep(3)
            #去除公司声明弹窗
            self.fisrtcp_top()
            time.sleep(2)
            common.general_refresh_()
            #资料审核弹出
            time.sleep(2)
            common.display_click('css,.el-button--primary > span')
            time.sleep(2)
            self.text= common.get_text('css,.alert-text')
            return self.text
        except Exception as msg:
            log.my_logger('!!--!!get_kyc_success').error(msg)

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
            log.my_logger('!!--!!get_fail_img').error(msg)
