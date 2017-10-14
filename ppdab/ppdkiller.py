import ppsdk.openapi_client
from requests.utils import quote
from ppsdk.core import rsa_client
import xml.dom.minidom
# from ppdab.strategy import Strategy
from ppparser import PPParser
from auto_bitter import auto_bitter
import ppsdk.openapi_client
import rsa
# some consts for ppd
import os


class auto_bit_killer:
    APPID = '2f9f35c5c24e4968849d7bfa1fe9fbf3'
    appid2 = 'c2be1f8150b24544a373644cc4d65932'

    APPPUBLIC = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCRAmNaxDeRFF06gwClvn1K9JzvxeGYBFT8zdSi1YJW7FglB3xg4m3n' \
                'wADQ9PpZ6dNKdpj0HDq8PheaWbfNjiNHmG604+ov9Zx7N3sMaA1K9YyDTfQrZAyGZcCpLTSxgtPT+oLoM2OF3Q+g/gu' \
                'nd9m1S2wp0hAml89uA0ck8qx8LQIDAQAB'
    returnUrl = 'https://www.51talk.com'

    returnUrl2 = 'http://www.zhouzhengchang.com'
    script_path = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_path)

    def __init__(self):
        with open('%s/private.txt' % auto_bit_killer.script_dir, 'r') as f:
           self.APPSECRET = f.read()
        self.client = ppsdk.openapi_client.openapi_client(self.APPSECRET)
        with open('%s/accesstoken' % auto_bit_killer.script_dir, 'r') as f:
            self.access_token = f.read()

        with open('%s/balance' % auto_bit_killer.script_dir, 'r') as f:
            self.balance = float(f.read())
            print('init balance %f' % self.balance)

        self.auto_bitter = auto_bitter(self.APPSECRET, self.APPID, self.access_token)
        pass

    # 获取散标列表
    def bid_list(self, index):
        url = 'http://gw.open.ppdai.com/invest/LLoanInfoService/LoanList'
        data = {'PageIndex': index}
        sort_data = rsa_client.rsa_client.sort(data)
        sign = rsa_client.rsa_client.sign(sort_data, self.APPSECRET)
        client = ppsdk.openapi_client.openapi_client(self.APPSECRET)
        r = client.send(url=url, data=data, appid=self.APPID, sign=sign, accesstoken=self.access_token)
        return r.json()

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

    def getBalance(self):
        with open('%s/balance' % auto_bit_killer.script_dir, 'r') as f:
            self.balance = float(f.read())

if __name__ == '__main__':
    transfer = auto_bit_killer()
    # transfer.checkBalance()
    # transfer.get_authorize_code()
    # transfer.authorize()
    all_ids = set()
    index = 1
    flag = True
    last_id = 0
    amount = 500
    while flag:
        transfer.getBalance()
        # amount = min(amount, int(transfer.balance))

        json_list = transfer.bid_list(index)
        # print(json_list)
        level = 2
        highest_ids, high_ids, raw_filtered_Ids = PPParser.parse_AA_bid_list(json_list, level)

        if level == 1:
            if len(highest_ids) != 0:
                print('got highest bids', highest_ids)
                for id in highest_ids:
                    if id == last_id:
                        continue
                    transfer.auto_bitter.bid(id, amount)
                    last_id = id
        elif level == 2:
            if len(high_ids) != 0:
                print('got high bids', high_ids)
                for id in high_ids:
                    if id == last_id:
                        continue
                    transfer.auto_bitter.bid(id, amount)
                    last_id = id
        else:
            if len(raw_filtered_Ids) != 0:
                # all_ids
                print('got ids', raw_filtered_Ids)
                for id in raw_filtered_Ids:
                    if id == last_id:
                        continue
                    transfer.auto_bitter.bid(id, amount)
                    last_id = id
                # 投完标已经比较耗时了，就不用往后找了
                index = 1
                continue
        # if len(highest_ids) + len(high_ids) + len(raw_filtered_Ids) == 0:
            # print('没有，继续搞吧')
            # print('final got ', len(json_list["LoanInfos"]))
        # index += 1

        #if len(json_list["LoanInfos"]) == 0 or index > 2:
        #    index = 1

    # strategy = Strategy(Strategy.STRATEGY_SAFE_AA)

    # strategy = Strategy(Strategy.STRATEGY_BEST_GAIN_16)
    # raw_filtered_Ids = PPParser.parse_bid_list(xml_list, strategy)
    #
    # final_ids = []
    # tmp_ids = []
    # for raw_id in raw_filtered_Ids:
    #     tmp_ids.append(raw_id)
    #     if len(tmp_ids) == 10:
    #         detail_xml = transfer.batch_bid_detail(tmp_ids)
    #         filtered_final_ids = PPParser.parse_bid_detail_list(detail_xml, strategy, final_ids)
    #         tmp_ids.clear()
    # if len(tmp_ids) > 0:
    #     detail_xml = transfer.batch_bid_detail(tmp_ids)
    #     filtered_final_ids = PPParser.parse_bid_detail_list(detail_xml, strategy, final_ids)
    #     tmp_ids.clear()
    #
    # print('最终结果：\n')
    # print(final_ids)






