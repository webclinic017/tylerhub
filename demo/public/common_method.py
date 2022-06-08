import time

from handlelog import MyLog


class Commonmethod():
    """
    此模块用于封装常用方法，例如登录会员中心/登录bos等
    """
    global log

    log=MyLog()

    #去除注册页弹窗
    def remove_register_topup(self,common):
        try:
            time.sleep(1)
            if 'none' not in common.get_attributes('css,.el-dialog__wrapper', 'style'):
                common.display_click('css,.blk-sure-btn')
                time.sleep(1)
            else:
                pass
        except Exception as msg:
            log.my_logger('!!--!!remove_register_topup').error(msg)

    #选择会员中心页面语言
    def choose_register_lang(self,common,lang):
        """
        lang值为简中、简体中文、EN
        """
        try:
            time.sleep(1)
            common.display_click('css,.el-icon-arrow-down')
            time.sleep(1)
            if lang=='简中' or lang=='CN':
                common.display_click('xpath,//li[contains(.,"简体中文")]')
            elif lang=='EN' or lang=='英语':
                common.display_click('xpath,//li[contains(.,"English")]')
            elif lang=='zh-hant' or lang=='繁中':
                common.display_click('xpath,//li[contains(.,"繁體中文")]')
            elif lang=='ar' or lang=='阿拉伯语':
                common.display_click("xpath,//li[contains(.,'العربية')]")
            elif lang=='ur' or lang=='乌尔都语':
                common.display_click('xpath,//li[contains(.,"اردو")]')
            elif lang=='id' or lang=='印尼':
                common.display_click('xpath,//li[contains(.,"Bahasa indonesia")]')
            elif lang=='ko' or lang=='韩语':
                common.display_click('xpath,//li[contains(.,"한국어")]')
            elif lang=='th' or lang=='泰语':
                common.display_click('xpath,//li[contains(.,"ไทย")]')
            elif lang=='vi' or lang=='越南语':
                common.display_click('xpath,//li[contains(.,"Tiếng Việt")]')
            else:
                print('请输入正确的页面语言')
        except Exception as msg:
            log.my_logger('!!--!!choose_register_lang').error(msg)

    #登录会员中心
    def login_cp(self,common,username,psword):
        try:
            #输入用户名
            common.web_clear('css,.el-input__inner',1)
            time.sleep(0.5)
            common.display_input('css,.el-input__inner',username,1)
            time.sleep(0.5)
            common.web_clear('css,.el-input__inner',-1)
            time.sleep(0.5)
            common.display_input('css,.el-input__inner',psword,-1)
            time.sleep(0.5)
            common.display_click('css,.login-btn')
        except Exception as msg:
            log.my_logger('!!--!!login_cp').error(msg)

    #登出会员中心
    def logout_cp(self,common):
        try:
            time.sleep(1)
            common.display_click('css,.el-icon--right')
            time.sleep(1)
            common.display_click('css,.drop-sub-title',-1)
            time.sleep(1)
            common.display_click('css,.logout-btn-confirm')
            time.sleep(1)
        except Exception as msg:
            log.my_logger('!!--!!lgoout_cp').error('登出会员中心失败：{}'.format(msg))

    #选择bos页面语言
    def choose_bos_lang(self,common,lang):
        """
        :param lang:CN/简中
        """
        try:
            if lang=='CN' or lang=='简中':
                common.display_click('css,.ivu-icon-ios-arrow-down')
                time.sleep(1)
                common.display_click('xpath,//li[@class="ivu-select-item"]')
            else:
                pass
        except Exception as msg:
            log.my_logger('!!--!!choose_bos_lang').error(msg)

    #登录bos
    def loginbos(self,common,username,psword):
        try:
            common.web_clear('css,.ivu-input-default')
            time.sleep(0.5)
            common.display_input('css,.ivu-input-default',username)
            time.sleep(0.5)
            common.web_clear('css,.ivu-input-default',1)
            time.sleep(0.5)
            common.display_input('css,.ivu-input-default',psword,1)
            time.sleep(0.5)
            common.display_click('css,.ivu-btn-large')
            while True:
                if common.ele_is_displayed('css,.ivu-spin-dot',1):
                    continue
                else:
                    break
        except Exception as msg:
            log.my_logger('!!--!!login_bos').error(msg)

    #进入账号详情页
    def enter_details_page(self,common,account):
        try:
            #输入主账号
            common.web_clear('css,.ivu-input-group-with-append > [placeholder]')
            time.sleep(0.5)
            common.display_input('css,.ivu-input-group-with-append > [placeholder]',account)
            time.sleep(1)
            #搜索
            common.display_click('css,.ivu-btn-icon-only > .ivu-icon')
            time.sleep(1)
            while True:
                if common.ele_is_displayed('css,.ivu-spin-dot',1):
                    continue
                else:
                    break

            #进入账号详情页
            common.display_click("xpath,//a[.='{}']".format(account))
        except Exception as msg:
            log.my_logger('!!--!!enter_details_page').error(msg)