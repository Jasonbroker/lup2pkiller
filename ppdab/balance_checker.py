import ppdab.ppsdk.openapi_client
from requests.utils import quote
from ppdab.ppsdk.core import rsa_client
import xml.dom.minidom
import os
from ppdab.strategy import Strategy
from ppdab.ppparser import PPParser

import rsa
# some consts for ppd



class balance_checker:
    APPID = '2f9f35c5c24e4968849d7bfa1fe9fbf3'
    appid2 = 'c2be1f8150b24544a373644cc4d65932'

    APPPUBLIC = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCRAmNaxDeRFF06gwClvn1K9JzvxeGYBFT8zdSi1YJW7FglB3xg4m3n' \
                'wADQ9PpZ6dNKdpj0HDq8PheaWbfNjiNHmG604+ov9Zx7N3sMaA1K9YyDTfQrZAyGZcCpLTSxgtPT+oLoM2OF3Q+g/gu' \
                'nd9m1S2wp0hAml89uA0ck8qx8LQIDAQAB'
    returnUrl = 'https://www.51talk.com'

    returnUrl2 = 'http://www.zhouzhengchang.com'

    def __init__(self):
        with open('./private.txt', 'r') as f:
           self.APPSECRET = f.read()
        self.client = ppdab.ppsdk.openapi_client.openapi_client(self.APPSECRET)
        self.balance = 0
        pass

    def get_authorize_code(self):
        authorize_url = 'https://ac.ppdai.com/oauth2/login?AppID=' + self.APPID + '&ReturnUrl=' + self.returnUrl
        print(authorize_url)
        authorize_url2 = 'https://ac.ppdai.com/oauth2/login?AppID=' + self.appid2 + '&ReturnUrl=' + self.returnUrl2
        print(authorize_url2)

    def authorize(self):
        code = 'e3a5d899ffd04925a201c8d0823edff4'
        authorizeStr = self.client.authorize(appid=self.APPID, code=code)
        print(authorizeStr.decode())

    access_token = '2135b713-c892-4d2c-8f7b-1c37dbef97a2'
    RefreshToken = "e3a0ca1e-b10c-448a-be46-0206b6ee870f"

    def checkBalance(self):
        # "
        url = 'http://gw.open.ppdai.com/balance/balanceService/QueryBalance'
        data = {}
        sort_data = rsa_client.rsa_client.sort(data)
        sign = rsa_client.rsa_client.sign(sort_data, self.APPSECRET)
        print(sign)
        r = self.client.send(url, data, appid=self.APPID, sign=sign, accesstoken=self.access_token).decode()
        print(r)
        dom = xml.dom.minidom.parseString(r)
        root = dom.documentElement
        loan_infos = root.getElementsByTagName("d2p1:Balance")
        balance = float(loan_infos[1].childNodes[0].nodeValue)
        earn = balance - self.balance
        if earn > 0 and self.balance >= 0:
            self.balance = balance
        print(earn)
        return earn


    def checpayback(self, id):
        url = 'http://gw.open.ppdai.com/invest/RepaymentService/FetchLenderRepayment'
        data = {
            'ListingId': id
        }
        sort_data = rsa_client.rsa_client.sort(data)
        sign = rsa_client.rsa_client.sign(sort_data, self.APPSECRET)
        print(sign)
        r = self.client.send(url, data, appid=self.APPID, sign=sign, accesstoken=self.access_token).decode()
        return r



if __name__ == '__main__':
    transfer = balance_checker()
    # transfer.get_authorize_code()
    # transfer.authorize()
    earn = transfer.checkBalance()
    msg = 'earn %f' % earn
    os.system('terminal-notifier -title "拍拍贷" -message "%s"' % earn)






