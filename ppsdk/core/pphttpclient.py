#coding=utf-8

__author__ = "yangl"
import requests

#网络请求操作类
class http_client:
    def __init__(self, privatekey):
        self.session = requests.session()
        self.privateKey = privatekey
    '''
        用于请求的Headers
    '''
    REQUEST_HEADER = {'Connection': 'keep-alive',
                  'Cache-Control': 'max-age=0',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
                  #'Accept-Encoding': 'gzip, deflate, sdch',
                  'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
                  'Content-Type':'application/json;charset=utf-8'
                  }


    #发送post请求
    def http_post(self, url, data, headers={}):

        custom_header = self.REQUEST_HEADER
        for head in headers:
            custom_header[head] = headers[head]
        r = self.session.post(url=url, data=data, headers=custom_header)
        return r.content
            

