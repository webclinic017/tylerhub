'''
Author: your name
Date: 2022-02-14 10:37:15
LastEditTime: 2022-02-15 17:55:59
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \tylerhub\demo\public\check_chromeDriver.py
'''
from browser_actions import Commonweb
import re
import time
import os
import zipfile

class CheckDriverExe(object):

    global common,common2

    common=Commonweb()
    common2=Commonweb()

    #尝试打开谷歌浏览器，驱动过期则返回False
    def open_chrome(self):
        self.massage=str(common.open_browser())
        if 'Message' in self.massage:#默认打开谷歌浏览器
            return True
        else:
            return False


    def check_action(self):
        if self.open_chrome():
            #获取谷歌浏览器最新版本号
            self.pattern=r'Current browser version is \S*'
            self.pattern2=r'[\d*.]'
            self.chromeVersions=''.join(re.findall(self.pattern2,''.join(re.findall(self.pattern,self.massage))))
            print('chrome浏览器最新版本号：{}'.format(self.chromeVersions))
            #Firefox下载压缩包放在本地python目录下
            common.open_browser(download_path=common.pythonPath[:-11],browsername='Firefox')
            #访问谷歌驱动下载地址
            common.open_web('http://chromedriver.storage.googleapis.com/index.html')
            time.sleep(2)
            try:
                #选择最新驱动下载
                common.display_click("xpath,//a[contains(.,'{}')]".format(self.chromeVersions[:-1]))
                time.sleep(2)
                common.display_click("xpath,//a[.='chromedriver_win32.zip']")
                print('chrome浏览器最新驱动版本号：{}'.format(self.chromeVersions[:-1]))
                #删除过期谷歌驱动
                os.remove(os.path.join(common.pythonPath[:-11],'chromedriver.exe'))
                #解压下载的驱动包
                self.zip=zipfile.ZipFile(os.path.join(common.pythonPath[:-11],'chromedriver_win32.zip'))
                self.zip_list = self.zip.namelist()
                for f in self.zip_list:
                    self.zip.extract(f, common.pythonPath[:-11])

                self.zip.close()

                #删除下载文件
                os.remove(os.path.join(common.pythonPath[:-11],'chromedriver_win32.zip'))
                common.close_browser()
                
                #测试驱动是否生效
                if 'Message' in str(common2.open_browser()):#默认打开谷歌浏览器
                    print('驱动仍未生效请重新下载驱动')
                    common2.close_browser()
                else:
                    print('驱动更新成功')

            except:
                print('请检查谷歌浏览器最新驱动版本是否与页面一致')

        else:
            print('当前谷歌浏览器驱动未过期')



#测试
if __name__=='__main__':
    check=CheckDriverExe()
    check.check_action()