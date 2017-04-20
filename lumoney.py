import requests
from bs4 import BeautifulSoup


def login():
    print('logging')


p2p_url = 'https://list.lu.com/list/transfer-p2p'


class LumoneyP2pTransfer:
    def __init__(self):
        self.session = requests.session()
        self.user = {}

    # return a list of suibable product id
    def check_suitable_productId(self):
        print('syncing')
        r = self.session.get(p2p_url)
        return r.content




    def sync_data(self):

        while True:
           product_list = self.check_suitable_productId()










if __name__ == '__main__':
    transfer = LumoneyP2pTransfer()
    transfer.sync_data()
