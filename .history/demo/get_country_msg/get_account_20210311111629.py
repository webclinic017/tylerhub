import time
import os
import sys
path=os.path.dirname(os.path.dirname(__file__))
path=os.path.join(path,'publick')
sys.path.append(path)
from browser_actions import Commonweb
from other_actions import public_method
from about_data import exceldata

pub_method=public_method()
exdata=exceldata()
class get_account(Commonweb):
    """爬取国家列表数据"""
    global driver

    def __init__(self,browsername='Chrome'):
        self.driver=self.open_browser(browsername)

    def login_bos(self,username,psword,lang='CN'):
        try:
            self.open_web('https://at-bos-frontend-sit.atfxdev.com/login')
            #选择页面语言
            self.bos_lang(lang)
            time.sleep(1)
            #输入bos用户名
            self.web_input('css,.ivu-input-default',username)
            time.sleep(1)
            #输入密码
            self.web_input('css,.ivu-input-default',psword,1)
            time.sleep(1)
            #点击登录
            self.web_click('css,.ivu-btn-large')
        except Exception as msg:
            pub_method.log_output('!!--!!login_bos').error(msg)

    #选择bos登录页语言
    def bos_lang(self,lang='CN'):
        try:
            if lang=='CN' or lang=='简中':
                self.web_click('css,.ivu-icon-ios-arrow-down')
                time.sleep(1)
                self.web_click('css,.ivu-select-item') #选择页面语言为中文
            else:
                pass
        except Exception as msg:
            pub_method.log_output('!!--!!lang').error('bos页面语言选择错误,参数CN/EN：{}'.format(msg)) 

    #爬取数据并保存到本地
    def save_msg(self):
        #系统设定
        self.display_click('css,.ivu-icon-md-settings')
        #国家列表
        self.display_click('xpath,//li[@class="ivu-menu-submenu ivu-menu-opened"]//span[.="国家列表"]')
        #选择每页显示条数
        self.display_click('css,div.ivu-page-options-sizer span')
        #每页显示100条数据
        self.display_click('css,ul.ivu-select-dropdown-list>li.ivu-select-item',7)
        time.sleep(1)
        #内嵌滚动条滚到底部
        self.js_scroll_inline('class','ivu-table-overflowY','down')
        self.country_list=[]
        self.page=0
        while self.page<3:
            self.list_len=self.get_lenofelement('css,tbody.ivu-table-tbody>tr')-3
            for i in range(1,self.list_len+1):
                self.CN_country=self.get_text('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/\
                    div/div[1]/div[2]/table/tbody/tr[{}]/td[4]'.format(i)) #中文国家名
                self.EN_country=self.get_text('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/\
                    div/div[1]/div[2]/table/tbody/tr[{}]/td[3]'.format(i)) #英文国家名
                self.ISO_name=self.get_text('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]\
                    /div/div[1]/div[2]/table/tbody/tr[{}]/td[12]'.format(i)) #ISO码
                self.PHONE_code=self.get_text('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]\
                    /div/div[1]/div[2]/table/tbody/tr[{}]/td[13]'.format(i)) #电话国码
                if self.page==0:
                    exdata.saveainfo(r'E:\test\all_country.xlsx',self.CN_country,'A',i+1) #保存中文国家名
                    exdata.saveainfo(r'E:\test\all_country.xlsx',self.EN_country,'B',i+1) #保存英文国家名
                    exdata.saveainfo(r'E:\test\all_country.xlsx',self.ISO_name,'C',i+1)   #保存ISO
                    exdata.saveainfo(r'E:\test\all_country.xlsx',self.PHONE_code,'D',i+1) #保存电话国码
                elif self.page==1:
                    exdata.saveainfo(r'E:\test\all_country.xlsx',self.CN_country,'A',i+1) 
                    exdata.saveainfo(r'E:\test\all_country.xlsx',self.EN_country,'B',i+1) 
                    exdata.saveainfo(r'E:\test\all_country.xlsx',self.ISO_name,'C',i+1)   
                    exdata.saveainfo(r'E:\test\all_country.xlsx',self.PHONE_code,'D',i+1)
                else:
                    exdata.saveainfo(r'E:\test\all_country.xlsx',self.CN_country,'A',i+1)
                    exdata.saveainfo(r'E:\test\all_country.xlsx',self.EN_country,'B',i+1)
                    exdata.saveainfo(r'E:\test\all_country.xlsx',self.ISO_name,'C',i+1)
                    exdata.saveainfo(r'E:\test\all_country.xlsx',self.PHONE_code,'D',i+1)

                dic_country={} 
                dic_country[self.CN_country]=self.EN_country
                self.country_list.append(dic_country)
                #获取最后一组数据后，翻页
                if i==self.list_len:
                    self.display_click('css,.ivu-icon-ios-arrow-forward')     
                    time.sleep(1)
                    self.page=self.page+1
                    continue
        return self.country_list

    #关闭浏览器
    def closer(self):
        self.quit_browser()


if __name__=='__main__':
    get=get_account()
    get.login_bos('tyler.tang','Tl123456')
    print(get.save_msg())
    get.closer()