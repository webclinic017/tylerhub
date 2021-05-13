import datetime
import os
import sys
import time

path_demo=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_public=path_demo+r'\public'
sys.path.append(path_public)
from about_data import exceldata
from browser_actions import Commonweb
from other_actions import public_method

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
        try:
            #系统设定
            self.display_click('css,.ivu-icon-md-settings')
            #国家列表
            self.display_click('xpath,//li[@class="ivu-menu-submenu ivu-menu-opened"]//span[.="国家列表"]')
            #选择每页显示条数
            self.display_click('css,div.ivu-page-options-sizer span')
            #每页显示100条数据
            self.display_click('css,ul.ivu-select-dropdown-list>li.ivu-select-item',7)
            time.sleep(3)
            time.s
            #内嵌滚动条滚到底部
            self.js_scroll_inline('class','ivu-table-overflowY','down')
            self.country_list=[]
            self.page=0
            while self.page<3:
                self.list_len=self.get_lenofelement('css,tbody.ivu-table-tbody>tr')-3
                for i in range(1,self.list_len+1):
                    self.CHS=self.get_text('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/\
                        div/div[1]/div[2]/table/tbody/tr[{}]/td[4]'.format(i)) #CHS
                    self.CHT=self.get_text('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/\
                        div/div[1]/div[2]/table/tbody/tr[{}]/td[5]'.format(i)) #CHT
                    self.ENG=self.get_text('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/\
                        div/div[1]/div[2]/table/tbody/tr[{}]/td[3]'.format(i))#ENG
                    self.ARA=self.get_text('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/\
                        div/div[1]/div[2]/table/tbody/tr[{}]/td[9]'.format(i)) #ARA
                    self.IDN=self.get_text('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/\
                        div/div[1]/div[2]/table/tbody/tr[{}]/td[11]'.format(i)) #IDN
                    self.KOR=self.get_text('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/\
                        div/div[1]/div[2]/table/tbody/tr[{}]/td[6]'.format(i)) #KOR
                    self.MYS=self.get_text('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/\
                        div/div[1]/div[2]/table/tbody/tr[{}]/td[12]'.format(i)) #MYS
                    self.THA=self.get_text('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/\
                        div/div[1]/div[2]/table/tbody/tr[{}]/td[7]'.format(i)) #THA
                    self.UDR=self.get_text('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/\
                        div/div[1]/div[2]/table/tbody/tr[{}]/td[10]'.format(i)) #UDR
                    self.VIE=self.get_text('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/\
                        div/div[1]/div[2]/table/tbody/tr[{}]/td[8]'.format(i)) #VIE
                    self.ISO=self.get_text('xpath,//*[@id="app"]/div/div/div[4]/div/div[2]/\
                        div/div[1]/div[2]/table/tbody/tr[{}]/td[13]'.format(i)) #ISO
                    if self.page==0:
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.ISO,'A',i+1) 
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.CHS,'B',i+1) 
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.CHT,'C',i+1)  
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.ENG,'D',i+1)
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.ARA,'E',i+1)
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.IDN,'F',i+1)
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.KOR,'G',i+1)
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.MYS,'H',i+1)
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.THA,'I',i+1)
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.UDR,'J',i+1) 
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.VIE,'K',i+1)
                    elif self.page==1:
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.ISO,'A',i+101) 
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.CHS,'B',i+101) 
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.CHT,'C',i+101)  
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.ENG,'D',i+101)
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.ARA,'E',i+101)
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.IDN,'F',i+101)
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.KOR,'G',i+101)
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.MYS,'H',i+101)
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.THA,'I',i+101)
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.UDR,'J',i+101) 
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.VIE,'K',i+101)
                    else:
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.ISO,'A',i+201) 
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.CHS,'B',i+201) 
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.CHT,'C',i+201)  
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.ENG,'D',i+201)
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.ARA,'E',i+201)
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.IDN,'F',i+201)
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.KOR,'G',i+201)
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.MYS,'H',i+201)
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.THA,'I',i+201)
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.UDR,'J',i+201) 
                        exdata.saveainfo(os.path.dirname(os.path.abspath(__file__))+r'\all_country.xlsx',self.VIE,'K',i+201)

                    dic_country={} 
                    dic_country[self.CHS]=self.ENG
                    self.country_list.append(dic_country)
                    #获取最后一组数据后，翻页
                    if i==self.list_len:
                        self.display_click('css,.ivu-icon-ios-arrow-forward')     
                        time.sleep(1)
                        self.page=self.page+1
                        continue
            return self.country_list
        except Exception as msg:
            pub_method.log_output('!!--!!save_msg').error(msg)


    #关闭浏览器
    def closer(self):
        self.quit_browser()


if __name__=='__main__':
    # #开始时间
    start_time=datetime.datetime.now()
    get=get_account()
    get.login_bos('tyler.tang','Tl123456')
    print(get.save_msg())
    get.closer()
    #结束时间
    end_time=datetime.datetime.now()
    time_cost=time.gmtime((end_time-start_time).total_seconds())
    print('爬取数据总用时：{}'.format(time.strftime('%H:%M:%S',time_cost)))
