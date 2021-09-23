'''
Author: your name
Date: 2021-09-18 18:04:52
LastEditTime: 2021-09-22 11:01:18
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \tylerhub\demo\bos_creataccount\api_creat_account.py
'''
import os
import sys
import random

path_demo=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_public=os.path.join(path_demo,'public')
sys.path.append(path_public)

from randomdata import Random_data
from read_dataconfig import ReadConfig
from api import Api


request=Api()
conFig=ReadConfig()
ranData=Random_data()

def loginbos():
    headers_login={
        'accept':'application/json, text/plain, */*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh,zh-CN;q=0.9,en;q=0.8',
        'content-type':'application/json;charset=UTF-8',
        'sec-ch-ua':'"Google Chrome";v="93","Not;A Brand";v="99", "Chromium";v="93"',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-site',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        }

    data_login={
	    "account": conFig.get_value('api_login_bos', 'username'), 
	    "passwd": conFig.get_value('api_login_bos', 'password')
        }
    
    lgoinData=request.api_post(conFig.get_value('api_login_bos', 'host'),conFig.get_value('api_login_bos', 'path'),
    headers=headers_login,json=data_login)
    return lgoinData.json()['data']['token']

def creataccount(parend_code,type):
    if type=='IB':
        level='12'
        ib_code=ranData.get_rangenum(9)
    else:
        level='99'
        ib_code=''
    conFig.modify('api_login_bos', 'authentication', loginbos())


    headers_creat={
        'accept':'application/json, text/plain, */*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh,zh-CN;q=0.9,en;q=0.8',
        'content-type':'application/json;charset=UTF-8',
        'sec-ch-ua':'"Google Chrome";v="93","Not;A Brand";v="99", "Chromium";v="93"',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-site',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'authentication':conFig.get_value('api_login_bos', 'authentication')
        }

    data_creat={
        "entity":"GM",
        "accountInfo":{
            "accType":type,
            "city":"",
            "comment":"",
            "copyTrade":"",
            "createTd":True,
            "enabled":True,
            "ibCode":ib_code,
            "ibLink":["A01","A005"],
            "level":level,
            "masterAccountFundAuthority":{
                "depositInd":True,
                "fundTransferInd":True,
                "withdrawalInd":True},
            "mtGroup":"demoforex",
            "mtName":"mt4_s02",
            "mtRegion":"SEA",
            "parentAccountNumber":"",
            "parentCode":parend_code,
            "region":"7",
            "riskLevel":"Undetermined",
            "state":"",
            "td_type":"IBC",
            "tradeAccountFundAuthority":{
                "depositInd":True,
                "fundTransferInd":True,
                "withdrawalInd":True
                },
            "tradeAccountType":"mt4",
            "zipCode":ranData.get_purerange(8,'number')
        },
        "bankInfo":{
            "ampAccount":[],
            "bankAccount":[],
            "bankWire":[],
            "cryptoWallet":[],
            "eChannel":[]
            },
        "clientInfo":{
            "accountTag":"",
            "addr":"addr",
            "ageRiskConfirm":"",
            "birthDate":ranData.random_date(),
            "country":"VNM",
            "dbaName":"",
            "docBackImg":{
                "addr":"",
                "name":""
                },
            "docFrontImg":{
                "addr":"1631957741983930.jpeg",
                "imgDeg":0,
                "name":"code.jpg"
                },
            "docIssuingCountry":"POL",
            "docNo":ranData.get_purerange(18,'number'),
            "docType":"IDC",
            "email":ranData.get_rangenemail(9),
            "firstName":"tyler",
            "fullName":"tyler testapi",
            "gender":"M",
            "lang":"ENG",
            "lastName":"testapi",
            "middleName":"",
            "mobilePhone":ranData.get_rangephone(),
            "otherFiles":[],
            "phoneAreaCode":"84",
            "proofOfAddress":{
                "addr":"",
                "name":""
                }
            }
    }
    creatData=request.api_post(conFig.get_value('api_login_bos', 'host'),conFig.get_value('api_login_bos', 'path_creat'),
    headers=headers_creat,json=data_creat)
    return creatData.json()



if __name__=='__main__':
    iblist=["G0088A", "G0088AM1", "G0088AS1", "G0088AS2", "G0088AS3", "G0088AS4", "G0088AS5", "G0088AM2", "G0088AS6", 
    "G0088AS7", "G0088AS8", "G0088AS14", "G0088AS15", "G0088AS17", "G0088AM3", "G0088AS9", "G0088AS10", "G0088AS12", 
    "G0088AS13", "G0088AS16", "G0088AR1", "G0088AR2"]

    print(creataccount('G0088A','CL')['data']['accountNumber'])