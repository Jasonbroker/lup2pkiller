from ppdab.ppsdk.core import rsa_client
import ppdab

class auto_bitter:
    def __init__(self, appsecret, appid, access_token):
        self.APPSECRET = appsecret
        self.APPID = appid
        self.access_token = access_token

    def bid(self, listid, amount):
        url = 'http://gw.open.ppdai.com/invest/BidService/Bidding'
        data = {'ListingId': listid,
                'Amount': amount}
        sort_data = rsa_client.rsa_client.sort(data)
        sign = rsa_client.rsa_client.sign(sort_data, self.APPSECRET)
        client = ppdab.ppsdk.openapi_client.openapi_client(self.APPSECRET)
        r = client.send(url=url, data=data, appid=self.APPID, sign=sign, accesstoken=self.access_token)
        print(r)
        return r.json()