'''
Author: tyler
Date: 2021-09-14 10:54:12
LastEditTime: 2021-10-12 16:10:30
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \tylerhub\demo\public\jiami.py
'''

  
from Crypto.Cipher import AES
import base64
import json
class aescrypt():
    def __init__(self,key):
        self.bs=AES.block_size
        if isinstance(key,str):
            self.key=key.encode('utf8')
    


    def encrypt(self,data):
        cipher=AES.new(self.key,AES.MODE_CBC)
        #data=json.dumps(data,ensure_ascii=False)
        data=json.dumps(data)
        count=len(data.encode('utf8'))
        if (count%self.bs !=0):
            add=self.bs-(count%self.bs)
        else:
            add=0
        text=data+(chr(add)*add)
        self.ciphertext=cipher.encrypt(text.encode('utf8'))
        cryptedstr=str(base64.b64encode(self.ciphertext),encoding='utf-8')
        return cryptedstr

if __name__ == '__main__':
    key='254e5504778ccbf9a3c19127643faa9a'
    a=aescrypt(key)
    print(a.encrypt('atfxqapeter222@gmail.com'))
 



  # AES解密
#   def decrypt(self,encrData):
#     #encrData = base64.b64decode(encrData)
#     #unpad = lambda s: s[0:-s[len(s)-1]]
#     unpad = lambda s: s[0:-s[-1]]
#     cipher = AES.new(self.__key, AES.MODE_ECB)
#     decrData = unpad(cipher.decrypt(encrData))
#     return decrData.decode('utf-8')


# if __name__=='__main__':
    # a=AEScoder()
    # print(a.encrypt('Tl123456'))