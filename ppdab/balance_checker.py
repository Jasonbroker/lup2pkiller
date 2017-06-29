import ppsdk.openapi_client
from ppsdk.core import rsa_client
import os
import sched
import time
import hashlib
import requests
import json
import datetime

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
        self.runtime = time.time()
        self.noti_token = ''
        with open('balance', 'r') as f:
            self.balance = float(f.read())
            print('init balance %f' % self.balance)
        with open('accesstoken', 'r') as f:
            self.access_token = f.read()
        pass

    def get_authorize_code(self):
        authorize_url = 'https://ac.ppdai.com/oauth2/login?AppID=' + self.APPID + '&ReturnUrl=' + self.returnUrl
        print(authorize_url)
        authorize_url2 = 'https://ac.ppdai.com/oauth2/login?AppID=' + self.appid2 + '&ReturnUrl=' + self.returnUrl2
        print(authorize_url2)

    RefreshToken = "e3a0ca1e-b10c-448a-be46-0206b6ee870f"
    openID = '01a1a1337577473cb9c1650f79f31728'
    # authorize_data: {"OpenID": "01a1a1337577473cb9c1650f79f31728",
    #                  "AccessToken": "48f6ec50-2917-4ab0-8d97-6c0d76917af9",
    #                  "RefreshToken": "b8471d4e-3a5a-492c-b678-e638715ce536", "ExpiresIn": 604800}

    def authorize(self):
        code = 'cb5857ce8b674070a30503ba7feb816a'
        authorizeStr = self.client.authorize(appid=self.APPID, code=code)
        print(authorizeStr)

    def refreshToken(self):
        new_token_info = self.client.refresh_token(self.APPID, self.openID, self.RefreshToken)
        token = new_token_info.json()['AccessToken']
        print('got new token ', token)
        self.access_token = token
        with open('accesstoken', 'w') as f:
            f.write(str(self.access_token))


    def _checkBalance(self):
        url = 'http://gw.open.ppdai.com/balance/balanceService/QueryBalance'
        data = {}
        sort_data = rsa_client.rsa_client.sort(data)
        sign = rsa_client.rsa_client.sign(sort_data, self.APPSECRET)
        r = self.client.send(url, data, appid=self.APPID, sign=sign, accesstoken=self.access_token)
        dic = r.json()
        print(dic)
        if 'HttpStatus' in dic:
            self.refreshToken()
            self.checkBalance()
        if dic['Result'] == 0:
            balance = float(dic['Balance'][2]['Balance'])
            earn = balance - self.balance
            if self.balance >= 0:
                self.balance = balance
            with open('balance', 'w') as f:
                f.write(str(self.balance))
                utctime = datetime.datetime.utcnow()
                print('%s current balance %f' %(utctime.strftime('%Y-%m-%d %H:%M:%S'), self.balance))
        else:
            earn = 0
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
        if earn != 0:
            msg = '余额更新%f，现余额%f' % (earn, self.balance)
            os.system('terminal-notifier -title "拍拍贷" -message "%s"' % msg)
            transfer.send_notification(msg)

    def get_notification_token(self):
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
            token = ''
        return token

    def send_notification(self, notification):
        # 需要重新找token
        if self.noti_token == '' or time.time() - self.runtime > 24 * 3600:
            self.noti_token = self.get_notification_token()
            print('拍拍贷监控开始')
            self.runtime = time.time()
            self._send_notification('拍拍贷监控开始')

        if self.noti_token != '':
            self._send_notification(notification)

    def _send_notification(self, notification):
        noti_header = {
            'Content-Type': 'application/json',
            'authtoken': self.noti_token
        }
        noti_url = 'https://restapi.getui.com/v1/' + self.getuiappid + '/push_single'
        noti_data = {
            "message": {
                "appkey": self.getuiappkey,
                "is_offline": True,
                "offline_expire_time": 1,
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
                    'sound':'default',
                },
            },
            "alias": "zz",
            "requestid": str(time.time()*1000)
        }
        noti_r = self.session.post(noti_url, data=json.dumps(noti_data), headers=noti_header)
        dic = noti_r.json()
        print(dic)


if __name__ == '__main__':
    schedule = sched.scheduler(time.time, time.sleep)
    transfer = balance_checker()
    # transfer.get_authorize_code()
    # transfer.authorize()
    # transfer.refreshToken()
    transfer.checkBalance()
    while True:
        # 十分钟一检查
        schedule.enter(60*5, 0, transfer.checkBalance)
        schedule.run()



