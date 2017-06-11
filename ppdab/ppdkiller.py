import ppdab.ppsdk.openapi_client
from requests.utils import quote
from ppdab.ppsdk.core import rsa_client
import xml.dom.minidom
from ppdab.strategy import Strategy
from ppdab.ppparser import PPParser

import rsa
# some consts for ppd



class auto_bit_killer:
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
        return xmldata

    '''detail bids'''
    def batch_bid_detail(self, listing_ids):
        # 新版散标详情批量接口（请求列表不大于10）
        url = "http://gw.open.ppdai.com/invest/LLoanInfoService/BatchListingInfos"
        data = {
            "ListingIds": listing_ids
        }
        sort_data = rsa_client.rsa_client.sort(data)
        sign = rsa_client.rsa_client.sign(sort_data, self.APPSECRET)
        list_result = self.client.send(url, data, appid=self.APPID, sign=sign, accesstoken=self.access_token).decode()
        return list_result



if __name__ == '__main__':
    transfer = auto_bit_killer()
    xml_list = transfer.bid_list()
    strategy = Strategy(Strategy.STRATEGY_BEST_GAIN_16)
    raw_filtered_Ids = PPParser.parse_bid_list(xml_list, strategy)

    final_ids = []
    tmp_ids = []
    for raw_id in raw_filtered_Ids:
        tmp_ids.append(raw_id)
        if len(tmp_ids) == 10:
            detail_xml = transfer.batch_bid_detail(tmp_ids)
            filtered_final_ids = PPParser.parse_bid_detail_list(detail_xml, strategy, final_ids)
            tmp_ids.clear()
    if len(tmp_ids) > 0:
        detail_xml = transfer.batch_bid_detail(tmp_ids)
        filtered_final_ids = PPParser.parse_bid_detail_list(detail_xml, strategy, final_ids)
        tmp_ids.clear()

    print('最终结果：\n')
    print(final_ids)





