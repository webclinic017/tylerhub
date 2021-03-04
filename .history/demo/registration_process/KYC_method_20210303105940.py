import time
import os
import sys
"""跨目录调用，需要将导入的包加入sys.path中"""
path=os.path.dirname(os.path.dirname(__file__))
path=os.path.join(path,'publick')
sys.path.append(path)
from browser_actions import Commonweb
from other_actions import public_method

#实例化对象
pub_method=public_method()

#继承基本类
class kyc_approve(Commonweb):
    global driver

    #默认以谷歌浏览器执行测试用例
    def browsertype(self,browsername='Chrome'):
        self.driver=self.open_browser(browsername)

    #去除登录页弹窗
    def login_topup(self):
        try:
            self.web_click('css,.blk-sure-btn')
        except Exception as msg:
            pub_method.log_output('!!--!!topup').error('页面弹窗去除失败：{}'.format(msg))

    #选择会员中心登录页语言
    def cp_lang(self,lang):
        try:
            self.web_click('css,.el-icon-arrow-down')
            time.sleep(1)
            if lang=='EN' or lang=='英语':
                self.web_click('css,.el-dropdown-menu__item')
            elif lang=='CN' or lang=='简中':
                self.web_click('css,.el-dropdown-menu__item',1)
        except Exception as msg:
            pub_method.log_output('!!--!!lang').error('cp页面语言选择错误,参数CN/EN：{}'.format(msg))

    #选择bos登录页语言
    def bos_lang(self,lang):
        try:
            if lang=='CN' or lang=='简中':
                self.web_click('css,.ivu-icon-ios-arrow-down')
                time.sleep(1)
                self.web_click('css,.ivu-select-item') #选择页面语言为中文
            else:
                pass
        except Exception as msg:
            pub_method.log_output('!!--!!lang').error('bos页面语言选择错误,参数CN/EN：{}'.format(msg)) 

    #访问会员中心及BOS登录页,选择页面语言
    def loginweb(self,lang):
        try:
            self.open_web('https://at-client-portal-sit.atfxdev.com/login')
            #点击弹窗
            self.login_topup()
            time.sleep(1)
            #选择页面语言
            self.cp_lang(lang)
            time.sleep(1)
            #新开窗口访问bos登录页
            self.js_openwindows('https://at-bos-frontend-sit.atfxdev.com/login')
            #切换窗口
            self.switch_windows(1)
            #选择页面语言
            self.bos_lang(lang)
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!loginweb').error('访问cp/bos登录页失败：{}'.format(msg))
   
    #登录会员中心
    def login_cp(self,username,psword):
        try:
            #切换窗口
            self.switch_windows(0)
            #输入用户名
            self.web_input('css,.el-input__inner',username,1)
            time.sleep(1)
            #输入密码
            self.web_input('css,.el-input__inner',psword,3)
            time.sleep(1)
            #点击登录
            self.web_click('css,.login-btn')
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!lgoin_cp').error('登录会员中心失败：{}'.format(msg))

    #登出会员中心
    def logout_cp(self):
        self.switch_windows(0)
        try:
            self.web_click('css,.el-icon--right')
            time.sleep(1)
            self.web_click('css,.drop-sub-title',12)
            time.sleep(1)
            self.web_click('css,.logout-btn-confirm')
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!lgoout_cp').error('登出会员中心失败：{}'.format(msg))

    #登录bos并打开客户名单页
    def login_bos(self,username,psword):
        try:
            #输入bos用户名
            self.web_input('css,.ivu-input-default',username)
            time.sleep(1)
            #输入密码
            self.web_input('css,.ivu-input-default',psword,1)
            time.sleep(1)
            #点击登录
            self.web_click('css,.ivu-btn-large')
            time.sleep(1)
            #点击客户管理
            self.web_click('css,.ivu-badge')
            time.sleep(1)
            #点击客户名单
            self.web_click('css,.ivu-menu-item',1)
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!lgoin-bos').error('登录bos失败：{}'.format(msg))

    #KYC认证操作
    def get_on_kyc(self,account):
        try:
            #认证联系方式
            time.sleep(1)
            self.web_click('css,.el-button--primary')
            time.sleep(1)
            #发送邮箱验证码
            self.web_click('css,.dialog-sendCode')
            time.sleep(1)
            #获取邮箱验证码
            self.get_emailcode_(account)
            #填写邮箱验证
            self.switch_windows(0)
            time.sleep(1)
            self.web_input('css,.el-input__inner',self.emailcode,1)
            time.sleep(1)
            #点击下一步
            self.web_click('css,.dialog-submit')
            time.sleep(1)
            #跳过手机验证码
            self.web_click('css,.doItLeTer-css',1)
            time.sleep(1)
            #点击完成
            self.web_click('css,.dialog-submit')
            time.sleep(1)
            #上传证件照
            self.web_click('css,.img-text-required')
            time.sleep(1)
            self.upload_img()
            time.sleep(1)



    #随机选择出生日期与性别
    def choose_data_gender(self):
        try:
            #出生日期
            self.web_click('css,.el-input__inner',4)
            time.sleep(1)
            self.web_click('css,.el-date-picker__header-label')
            time.sleep(1)
            #双击选择年份
            self.double_click('css,.el-picker-panel__icon-btn')
            time.sleep(1)
            self.web_click('css,table>tbody>tr>td.available',pub_method.random_int(31,40)) #年
            time.sleep(1)
            self.web_click('css,table.el-month-table>tbody>tr>td',pub_method.random_int(0,11))#月
            time.sleep(1)
            self.web_click('css,table.el-date-table>tbody>tr.el-date-table__row>td',pub_method.random_int(0,41))#日
            time.sleep(1)
            #随机性别
            self.web_click('css,.el-radio__inner',pub_method.random_int(0,1))
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!choose_data_gender').error(msg)



        
    #获取邮箱验证码
    def get_emailcode_(self,account):
        try:
            #切换bos窗口
            self.switch_windows(1)
            time.sleep(1)
            #根据主账号搜索
            self.web_input('css,.ivu-input-default',account) #输入主账户
            time.sleep(1)
            self.web_click('css,.ivu-icon-ios-search',1) #点击搜索按钮
            time.sleep(1)
            #点击主账号进入账号详情页
            self.web_click('css,div.ivu-table-overflowX>table>tbody.ivu-table-tbody>tr>td',1)
            #切换到主账号详情页窗口
            self.switch_windows(2)
            time.sleep(1)
            #点击邮件记录
            self.web_click('css,.ivu-anchor-link-title',7)
            time.sleep(1)
            #判断验证码邮件是否发送
            if self.is_element_isdisplayed('xpath,//span[.="emailCode"]'):
                #打开验证码邮件
                self.web_click('css,tbody.ivu-table-tbody>tr>td>div>div>div')
                time.sleep(1)
                #获取验证码文本
                acc_text=self.get_text('xpath,//div[@class="ivu-drawer-wrap"]//tr[2]//tr[4]/td[1]/span')
                #提取数字
                self.emailcode=pub_method.extract_numbers(acc_text)
                #关闭当前页面
                self.closedriver()
                return self.emailcode
            else:
                print('未发送邮箱验证码，请重新发送')
        except Exception as msg:
            pub_method.log_output('!!--!!get_emailcode_').error('获取邮箱验证失败{}'.format(msg))

    #清空主账号搜索条件
    def clearaccount(self):
        try:
            self.switch_windows(2)
            time.sleep(1)
            self.web_clear('css,.ivu-input-default') #清空主账户
        except Exception as msg:
            pub_method.log_output('!!--!!clearaccount').error('清空主账号证失败{}'.format(msg))

    #关闭页面             
    def closedriver(self):
        self.close_browser()

    #退出浏览器
    def quitdriver(self):
        self.quit_browser()
