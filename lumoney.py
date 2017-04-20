import requests
import re
from bs4 import BeautifulSoup


def login():
    print('logging')


base_url = 'https://list.lu.com'

p2p_url = 'https://list.lu.com/list/transfer-p2p'


class LumoneyP2pTransfer:
    def __init__(self):
        self.session = requests.session()
        self.user = {}

    # return a list of suibable product id
    def check_suitable_productId(self):
        print('syncing')
        r = self.session.get(p2p_url)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.content, "lxml")
        samples = soup.find_all("li", class_="product-list")
        print(samples)
        return samples

    def test_data(self):
        with open('test.html', 'rt', encoding='utf-8') as f:
            data = f.read()

        soup = BeautifulSoup(data, 'lxml')
        samples = soup.find_all("li", class_="product-list")
        print(samples[0])
        url = self.select_product(samples, 20000)





    def select_product(self, product_list, max_price):
        selected_url = None
        for product in product_list:
            interest = product.find('p', class_='num-style').string
            time_remaining = product.find('li', class_='invest-period').find('p').string
            discount = product.find('b', class_='num-style').string
            if float(interest[:-1].strip()) < 8.4:
                print('low interest buy jb')
                continue
            price = product.find('em', class_='num-style').string
            if float(price.strip().replace(',', '')) > max_price:
                continue

            url = product.find('a', class_='ld-btn').get('href')
            selected_url = url
            print('已选择最优方案:', interest, price, discount, time_remaining, url)
            break
        return selected_url


    def sync_data(self):

        while True:
            # product_list = self.check_suitable_productId()
            self.test_data()
            break










if __name__ == '__main__':
    transfer = LumoneyP2pTransfer()
    transfer.sync_data()
