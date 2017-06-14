import ppsdk.openapi_client
from ppsdk.core import rsa_client
import xml.dom.minidom
import os
import sched
import time
import hashlib
import requests
import json

class balance_checker:
    APPID = '2f9f35c5c24e4968849d7bfa1fe9fbf3'
    appid2 = 'c2be1f8150b24544a373644cc4d65932'

    APPPUBLIC = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCRAmNaxDeRFF06gwClvn1K9JzvxeGYBFT8zdSi1YJW7FglB3xg4m3n' \
                'wADQ9PpZ6dNKdpj0HDq8PheaWbfNjiNHmG604+ov9Zx7N3sMaA1K9YyDTfQrZAyGZcCpLTSxgtPT+oLoM2OF3Q+g/gu' \
                'nd9m1S2wp0hAml89uA0ck8qx8LQIDAQAB'
    returnUrl = 'https://www.51talk.com'

    returnUrl2 = 'http://www.zhouzhengchang.com'

    getuiappkey = 'jlsU5w2htZ7fRr3LCy0Mj8'
    getuiappid = 'M94TY2pmnn8g8VIPEWO808'
    mastersecret = 'BfWtyenXl86AwlL75kafJ'


    def __init__(self):
        with open('./private.txt', 'r') as f:
           self.APPSECRET = f.read()
        self.client = ppsdk.openapi_client.openapi_client(self.APPSECRET)
        self.session = requests.session()
        with open('balance', 'r') as f:
            self.balance = float(f.read())
            print('init balance %f' % self.balance)
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

    def _checkBalance(self):
        # "
        url = 'http://gw.open.ppdai.com/balance/balanceService/QueryBalance'
        data = {}
        sort_data = rsa_client.rsa_client.sort(data)
        sign = rsa_client.rsa_client.sign(sort_data, self.APPSECRET)
        r = self.client.send(url, data, appid=self.APPID, sign=sign, accesstoken=self.access_token).decode()
        dom = xml.dom.minidom.parseString(r)
        root = dom.documentElement
        loan_infos = root.getElementsByTagName("d2p1:Balance")
        balance = float(loan_infos[1].childNodes[0].nodeValue)
        earn = balance - self.balance
        if earn > 0 and self.balance >= 0:
            self.balance = balance
        with open('balance', 'w') as f:
            f.write(str(self.balance))
            print('current balance %f' % self.balance)
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

    def checkBalance(self):
        earn = transfer._checkBalance()
        if earn > 0:
            msg = '余额更新%f，先余额%f' % (earn, self.balance)
            os.system('terminal-notifier -title "拍拍贷" -message "%s"' % msg)
            transfer.send_notification(msg)

    def send_notification(self, notification):
        url = 'https://restapi.getui.com/v1/' + self.getuiappid + '/auth_sign'
        print(url)
        ts = int(time.time()*1000)
        sign = hashlib.sha256((self.getuiappkey + str(ts) + self.mastersecret).encode())
        sign = sign.hexdigest()
        print(sign)
        data = {
            'sign': sign,
            'timestamp': str(ts),
            'appkey': self.getuiappkey
        }
        header = {'Content-Type': 'application/json'}
        print(data)
        r = self.session.post(url, data=json.dumps(data), headers=header)
        dic = r.json()
        if dic['result'] == 'ok':
            token = dic['auth_token']
        else:
            return None

        noti_header = {
                        'Content-Type': 'application/json',
                        'authtoken': token
                       }
        noti_url = 'https://restapi.getui.com/v1/' + self.getuiappid + '/push_single'
        noti_data = {
            "message": {
                "appkey": self.getuiappkey,
                "is_offline": True,
                "offline_expire_time": 10000000,
                "msgtype": "transmission"
            },
            "transmission": {
                "transmission_type": False,
                "transmission_content": "this is the transmission_content",
                "duration_begin": "2017-03-22 11:40:00",
                "duration_end": "2017-03-29 11:40:00"
            },
            "push_info": {
                "aps": {
                    "alert": {
                        "title": "拍拍贷余额更新",
                        "body": notification
                    },
                    "content-available": 1
                },
            },
            "alias": "zz",
            "requestid": "12111111111111111111111"
        }
        noti_r = self.session.post(noti_url, data=json.dumps(noti_data), headers=noti_header)
        dic = noti_r.json()
        print(dic)




if __name__ == '__main__':
    schedule = sched.scheduler(time.time, time.sleep)

    # transfer.get_authorize_code()
    # transfer.authorize()


    transfer = balance_checker()
    # while True:
    #     schedule.enter(60*10, 0, transfer.checkBalance)
    #     schedule.run()







