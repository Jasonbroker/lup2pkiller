import ppdab.ppsdk.openapi_client
from requests.utils import quote
from ppdab.ppsdk.core import rsa_client
import json
import xml.dom.minidom
from  ppdab.strategy import Strategy
import rsa
# some consts for ppd



class auto_bit_killer:
    APPID = '2f9f35c5c24e4968849d7bfa1fe9fbf3'
    appid2 = 'c2be1f8150b24544a373644cc4d65932'

    # APPSECRET = b'-----BEGIN RSA PRIVATE KEY-----' \
    #             b'MIICXAIBAAKBgQCTiBIu4IvY/iT5zKy3v9NVTOCcomfVdib0l/LTq0xU2RW2W8nzfCfeG6ogeMOOYsVz+6vcSG6' \
    #             b'yGtoO/+bQpk51QG4RyTYPgPEEgUPfVz8YBCw6wbeY+BkkSn9Z59UOz9robAAeqtcsh89vCPbzQwTqnV+7wL8i5AAi' \
    #             b'5Gv6LVGuPQIDAQABAoGAQyvOE5fbNJYqIa4l6ZemUg0pq0dqfU9JV04jmmpA29TnRNsv7PNXd5Ii+Jvjdd3UxwUMb' \
    #             b'8Ru2hrNs8yhu9gsmhXOqh8p4y7go60mKa5gigD1Ne7AYCKN6USFJc2BXAesIRclqJVwbX1TsF1R8K4m8YfVmX+OZhW' \
    #             b'3XZz0wISoHqUCQQDbf4j3d99McloBWiMFz1bwDfpzcUiZq1i9K/BC56LKXfDlrUQrU5a5iGLGo20DcVxy8Q+RjREQ' \
    #             b'MaobxgLGJZf7AkEArBDGfUUy73Dfy+tKOZWADR2VO7tjmrug9dhFJosSbT7qD7CwPmwUC3kCHA9EUtlRJH6Icy3v/URM' \
    #             b'UpwwwKzlJwJBANUbnNKPmshxGbvIVMqWRNUq7SfaK9+uwahhGZMLrD0IOhP0RoQ+Us9tgGFVWEkIbfbW3wO0z4VGgt8' \
    #             b'WP6k75LMCQBfwZY08OW/yxlA6tiL41837Va3vzlXS0PwjUMuiAbhNTodMT9j/dHJ8LXz16s2UCqQHLrjHpWIZRH0h2e6' \
    #             b'Un3UCQD3nvYBGw2d3aN2KtjS2k1EhhXkIGeDqLL011NN905C1cvruocEGhq3OraZTmz/ixIwVUg26DURd+vYlkfOB1Rg=' \
    #             b'-----END RSA PRIVATE KEY-----'

    APPPUBLIC = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCRAmNaxDeRFF06gwClvn1K9JzvxeGYBFT8zdSi1YJW7FglB3xg4m3n' \
                'wADQ9PpZ6dNKdpj0HDq8PheaWbfNjiNHmG604+ov9Zx7N3sMaA1K9YyDTfQrZAyGZcCpLTSxgtPT+oLoM2OF3Q+g/gu' \
                'nd9m1S2wp0hAml89uA0ck8qx8LQIDAQAB'
    returnUrl = 'https://www.51talk.com'

    returnUrl2 = 'http://www.zhouzhengchang.com'

    def __init__(self):
        with open('./private.txt', 'r') as f:
           self.APPSECRET = f.read()
        self.client = ppdab.ppsdk.openapi_client.openapi_client(self.APPSECRET)
        pass

    def get_authorize_code(self):
        authorize_url = 'https://ac.ppdai.com/oauth2/login?AppID=' + self.APPID + '&ReturnUrl=' + self.returnUrl
        print(authorize_url)
        authorize_url2 = 'https://ac.ppdai.com/oauth2/login?AppID=' + self.appid2 + '&ReturnUrl=' + self.returnUrl2
        print(authorize_url2)

    def authorize(self):
        code = '39ee70dc20af4ea486bfcc54f02d553b'
        authorizeStr = self.client.authorize(appid=self.APPID, code=code)
        print(authorizeStr)

    access_token = '6a58ad4d-561c-4ad9-8ce5-648450e009c8'
    # 获取散标列表
    def bid_list(self):
        url = 'http://gw.open.ppdai.com/invest/LLoanInfoService/LoanList'
        data = {'PageIndex': 1}

        # data = {"timestamp":utctime.strftime('%Y-%m-%d %H:%M:%S')}#time.strftime('%Y-%m-%d %H:%M:%S',)
        # data = { "AccountName": "15200000001"}
        sort_data = rsa_client.rsa_client.sort(data)
        sign = rsa_client.rsa_client.sign(sort_data, self.APPSECRET)
        xmldata = self.client.send(url=url, data=data, appid=self.APPID, sign=sign, accesstoken=self.access_token).decode()
        print('xml data', xmldata)

    '''
    返回需要继续取得详情的列表
    '''
    def parse_bid_list(self, xml_string, strategy):

        dom = xml.dom.minidom.parseString(xml_string)
        root = dom.documentElement

        loan_infos = root.getElementsByTagName("LoanInfos")[0]

        filteredElements = []
        for element in loan_infos.childNodes:
            # 借款数
            amount = element.getElementsByTagName('Amount')[0].childNodes[0].nodeValue
            print('借款数：' + amount)
            amount = float(amount)
            if amount > strategy.max_amount or amount < strategy.min_amount:
                print('太贵')
                continue

            listingId = element.getElementsByTagName('ListingId')[0].childNodes[0].nodeValue
            filteredElements.append(listingId)
            if len(filteredElements) > 8:
                break
        return filteredElements

    '''detail bids'''
    def batch_bid_detail(self, listing_ids):
        # 新版散标详情批量接口（请求列表不大于10）
        url = "http://gw.open.ppdai.com/invest/LLoanInfoService/BatchListingInfos"

        data = {
            "ListingIds": listing_ids
        }

        print(data)
        sort_data = rsa_client.rsa_client.sort(data)
        sign = rsa_client.rsa_client.sign(sort_data, self.APPSECRET)
        list_result = self.client.send(url, data, appid=self.APPID, sign=sign, accesstoken=self.access_token).decode()
        print(list_result)

    def parse_bid_detail_list(self, xml_string, strategy):







            







if __name__ == '__main__':
    transfer = auto_bit_killer()

    # transfer.get_authorize_code()
    # transfer.authorize()
    # transfer.bid_list()

    with open('test_xml', 'r') as f:
        xml_file = f.read()

    strategy = Strategy(Strategy.STRATEGY_BEST_GAIN_16)
    listingIds = transfer.parse_bid_list(xml_file, strategy)
    # 符合初期预期的listId
    print(len(listingIds))
    data = {
        "ListingIds": [
            23886149,
            23886150
        ]
    }
    print(data)
    transfer.batch_bid_detail(listingIds)


