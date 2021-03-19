import sys
import os
import time
path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=path_demo+r'\public'
sys.path.append(path_public)
from browser_actions import Commonweb
from other_actions import public_method
from about_data import exceldata


ex=exceldata()
pub_method=public_method()

#创建继承基础类的注册页表单操作模块
class form_operations(Commonweb):
    """会员中心注册页表单方法封装，注册页表单填写，定位元素封装在此类中，若页面元素发生变化，维护此模块即可"""
    global driver
    
    #默认以谷歌浏览器执行测试用例
    def browsertype(self,browsername='Chrome'):
        self.driver=self.open_browser(browsername)

    #根据链接/邀请码/直客注册
    def get_url(self,url,code,column,row): #link:专属链接；code:邀请码；cloumn:列；row:行
        """判断是通过专属链接还是邀请码注册"""
        #获取当前项目路径
        path_process=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        try:
            if len(url)!=0:
                #通过ib专属链接注册
                self.open_web(url)
                ex.saveainfo(path_process+r'\test_excel_data\account_number.xlsx','专属链接', column, row) #
                time.sleep(2)
                self.register_topup()
                print('专属链接注册')
            elif len(code)!=0:
                #通过邀请码
                self.open_web('https://at-client-portal-uat.atfxdev.com/register')
                time.sleep(2)
                ex.saveainfo(path_process+r'\test_excel_data\account_number.xlsx','邀请码', column, row)#备注注册方式
                self.register_topup()
                time.sleep(1)
                #输入邀请码
                self.web_input('css,.el-textarea__inner',code)
                print('邀请码注册')
            else:
                #直客注册
                self.open_web('https://at-client-portal-uat.atfxdev.com/register')
                ex.saveainfo(path_process+r'\test_excel_data\account_number.xlsx','直客', column, row)#备注注册方式
                time.sleep(2)
                self.register_topup()
        except Exception as msg:
            pub_method.log_output('!!--!!get_url').error('访问注册页异常{}'.format(msg))

    #判断注册国家是否为UK国家
    def country_isuk(self,country):
        self.uk_list=['阿尔巴尼亚','Albania','安道尔','Andorra','奥地利','Austria','波斯尼亚和黑塞哥维那','Bosnia and Herzegovina',
        '保加利亚','Bulgaria','克罗地亚','塞浦路斯','Cyprus','捷克共和国','Czech Republic','丹麦','Denmark','爱沙尼亚','Estonia',
        '芬兰','Finland','佐治亚州','Georgia','德国','Germany','直布罗陀','Gibraltar','希腊','Greece','匈牙利','Hungary','冰岛','Iceland',
        '爱尔兰','Ireland','意大利','Italy','拉脱维亚','Latvia','列支敦士登','Liechtenstein','立陶宛','Lithuania','卢森堡','Luxembourg',
        '马其顿','North Macedonia','马耳他','摩纳哥','Monaco','黑山共和国','Montenegro','荷兰','Netherlands','挪威','Norway','葡萄牙','Portugal',
        '塞尔维亚共和国','罗马尼亚','Romania','圣马力诺','San Marino','斯洛伐克','Slovakia','斯洛文尼亚','Slovenia','西班牙','Spain',
        '瑞典','Sweden','瑞士','Switzerland','英国','United Kingdom']     
        if country in self.uk_list:
            print('AT Global Markets Limited 不接受居住在这个国家的个人申请。')
            return True
        else:
            return False

    #去除注册页弹窗
    def register_topup(self):
        try:
            self.display_click('css,.blk-sure-btn')
        except Exception as msg:
            self.get_screenpict('去除弹窗')
            pub_method.log_output('!!--!!topup').error('注册页弹窗去除失败：{}'.format(msg))

    #选择注册页弹窗语言
    def choose_lg(self,lang):
        """注册页弹窗语言目前只能选择简中和英语"""
        try:
            self.web_click('css,.el-icon-arrow-down')
            time.sleep(1)
            if lang=='简中' or lang=='简体中文':
                self.web_click('css,ul.el-dropdown-menu >li',1)
            elif lang=='EN' or lang=='英语':
                self.web_click('css,ul.el-dropdown-menu >li',0)
            else:
                print('选择语言为简中/英语')
        except Exception as msg:
            pub_method.log_output('!!--!!language_error').error('注册页语言选择错误：{}'.format(msg))

    #注册页表单填写
    def fill_inform(self,lang,fristname,lastname,emali,password,cn_country,en_country):
        #选择页面语言
        self.choose_lg(lang)
        try:
            #选择国家
            self.web_click('css,.el-input__inner')
            time.sleep(1)
            if lang=='简中' or lang=='简体中文':
                self.web_input('css,.el-input__inner',cn_country) #输入中文国家名
                time.sleep(1)
                self.web_click('xpath,//span[.="{}"]'.format(cn_country))
            else:
                self.web_input('css,.el-input__inner',en_country) #输入英文国家名
                time.sleep(1)
                self.web_click('xpath,//span[.="{}"]'.format(en_country))
            #输入名字
            self.web_input('css,.el-input__inner',fristname,1)
            time.sleep(1)
            #输入姓氏
            self.web_input('css,.el-input__inner',lastname,2)
            time.sleep(1)
            #输入随机手机号码
            self.web_input('css,.el-input__inner',pub_method.get_rangephone(),4)
            time.sleep(1)
            #输入电子邮箱
            self.web_input('css,.el-input__inner',emali,5)
            time.sleep(1)
            #输入登录密码
            self.web_input('css,.el-input__inner',password,6)
            time.sleep(1)
            #输入验证码,并判断验证码是否正确
            self._code_()
            time.sleep(1)
            #点击条款
            self.web_click('css,.el-checkbox__inner')
        except Exception as msg:
            #截图
            self.get_screenpict('表单注册页填写失败')
            pub_method.log_output('!!--!!language_error').error('表单页填写错误:{}'.format(msg))

    #识别验证码
    def _code_(self):
        try:
            while True:
                #清空输入框
                self.web_clear('css,.el-input__inner',-1)
                time.sleep(1)
                #输入验证码
                self.web_input('css,.el-input__inner',self.discern_code('tyler','123456','code','codeimg','css,div.code-cell>svg'),-1)
                time.sleep(1)
                #点击旁白
                self.web_click('css,.c-right')
                time.sleep(1)
                #判断验证码是否正确
                if self.is_element_isdisplayed('css,.el-form-item__error'):
                    #刷新验证码
                    self.web_click('css,.la-redo-alt')
                    print('11111111')
                    continue
                else:
                    print('2222222222')
                    break
        except Exception as msg:
            pub_method.log_output('!!--!!_code_').error(msg)




    #提交表单
    def submit(self):
        try:
            self.web_click('css,.b-confirm')
            time.sleep(1)
        except Exception as msg:
            pub_method.log_output('!!--!!submit').error('标题提交失败：{}'.format(msg))

    #登录成功后获取文本
    def register_success(self):
        try:
            return self.get_text('css,div.declar-dialog .el-dialog__title')
        except Exception as msg:
            pub_method.log_output('!!--!!register_success').error('获取登录成功后的文本失败{}'.format(msg))

    #关闭浏览器
    def closedriver(self):
        self.close_browser()

    #退出浏览器
    def quitdriver(self):
        self.quit_browser()

if __name__=='__main__':
    print(pub_method.get_rangephone()+'qq.com')