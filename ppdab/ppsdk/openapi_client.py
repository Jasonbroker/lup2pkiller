#coding=utf-8
'''
Created on 2016年7月5日

@author: yanglei
'''

import datetime
import json

from .core.pphttpclient import http_client
from .core.rsa_client import rsa_client

'''
OpenAapi提交请求客户端
'''
class openapi_client:
    '''
    oauth2授权地址
    '''
    AUTHORIZE_URL = "https://ac.ppdai.com/oauth2/authorize"
    
    '''
       刷新Token地址
    '''
    REFRESHTOKEN_URL = "https://ac.ppdai.com/oauth2/refreshtoken"

    def __init__(self, private_key):
        self.http_client = http_client(privatekey=private_key)
        self.private_key = private_key
        '''
        Constructor
        '''
    
    '''
        获取授权
    AppId 应用ID
    code 授权码
    '''
    def authorize(self, appid, code):
        data = {
            'AppID': appid,
            'Code': code
        }
        data = "{\"AppID\":\"%s\",\"Code\":\"%s\"}" % (appid, code)
        data = data.encode("utf-8")
        print('authorize data: ', data)
        result = self.http_client.http_post(openapi_client.AUTHORIZE_URL, data=data)
        # result = gzip.GzipFile(fileobj=StringIO.StringIO(result),mode="r")
        # result = result.read().decode("gbk").encode("utf-8")
        print("authorize_data:%s" % (result))
        return result
        
    '''
        刷新AccessToken
    AppId 应用ID
    OpenId 用户唯一标识
    RefreshToken 刷新令牌Token
    '''

    def refresh_token(self, appid,openid,refreshtoken):
        data = "{\"AppID\":\"%s\",\"OpenId\":\"%s\",\"RefreshToken\":\"%s\"}" % (appid,openid,refreshtoken)
        result = self.http_client.http_post(openapi_client.REFRESHTOKEN_URL,data)
        print("refresh_token_data:%s" % (result))
        return result
    
    '''
        向拍拍贷网关发送请求
    Url 请求地址
    Data 请求报文
    AppId 应用编号
    Sign 签名信息
    AccessToken 访问令牌
    '''
    def send(self, url, data, appid, sign, accesstoken=''):
        utctime = datetime.datetime.utcnow()
        timestamp = utctime.strftime('%Y-%m-%d %H:%M:%S')
        headers = {
                    'Accept': 'application/json',
                    "X-PPD-APPID": appid,
                   "X-PPD-SIGN": sign,
                   "X-PPD-TIMESTAMP": timestamp,
                   "X-PPD-TIMESTAMP-SIGN": rsa_client.sign("%s%s" % (appid, timestamp), self.private_key)}

        data = json.dumps(data).lower()

        if accesstoken.strip():
            headers["X-PPD-ACCESSTOKEN"] = accesstoken
        # data = data.lower()
        result = self.http_client.http_post(url, data, headers=headers)
        return result
        
        