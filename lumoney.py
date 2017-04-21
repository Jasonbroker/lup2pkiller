import requests
import os
import platform
import time
from bs4 import BeautifulSoup

HEADERS = {'ContentType': 'application/json; charset=UTF-8',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0'}

qr_code = 'qr_code.jpg'

def login():
    print('logging')

base_url = 'https://list.lu.com'

p2p_url = 'https://list.lu.com/list/transfer-p2p'


class LumoneyP2pTransfer:
    def __init__(self):
        self.session = requests.session()
        self.user = {}
        self.debug = True

    def login(self):
        print('logging')
        # https: // user.lu.com / user / captcha / captcha.jpg?source = login & _ = 1492757276691

        def get_code():
            url = 'https://user.lu.com/user/captcha/captcha.jpg'
            param = {
                'source': 'login',
                '_': int(time.time())
            }
            r = self.session.get(url, params=param, headers=HEADERS)
            with open(qr_code, 'wb') as f:
                f.write(r.content)
                self._safe_open(qr_code)
        get_code()

        ver_code = input('输入验证码')

        def try_login():
            url = 'https://user.lu.com/user/login'
            '''isTrust	"Y"
            password	"26931FD9B7C390CE8B4519A6476AB…6C1D5D7F8171D961D8E5CB89793A"
            openlbo	"0"
            deviceKey	"25A72D1F9E8C27F40830AAFA390C2…33973B486ABDD01D5723C3609B1F"
            deviceInfo	"IzsS30vNklZc7mS4kaoJLVdOIE009…i9muo6u7LtEpY1HMXRIOH/CTsrY="
            loginFlag	"2"
            userName	"13752012220"
            pwd	"************"
            validNum	""
            agreeLbo	"on"
            loginagree	"on"'''



    # return a list of suibable product id
    def check_suitable_productId(self):
        print('syncing')
        r = self.session.get(p2p_url, headers=HEADERS)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.content, "lxml")
        samples = soup.find_all("li", class_="product-list")
        url = self.select_product(samples, 20000)
        return url

    def test_data(self):
        with open('test.html', 'rt', encoding='utf-8') as f:
            data = f.read()

        soup = BeautifulSoup(data, 'lxml')
        samples = soup.find_all("li", class_="product-list")
        print(samples[0])
        url = self.select_product(samples, 20000)

        # url 不存在说明没有数据，继续
        if not url:
            return
        self.buy_with_url(url)

    def buy_with_url(self, url):
        buy_url = base_url + url
        if self.debug:
            self._safe_open(buy_url)
            return True
        r = self.session.get(buy_url, headers=HEADERS)
        print(r.content.decode('utf-8'))



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
            url = self.check_suitable_productId()
            # url 不存在说明没有数据，继续
            if not url:
                continue
            result = self.buy_with_url(url)
            if result:
                break
            # self.test_data()
            break





# helpers
    def _get(self, **kwargs):
        return self.session.get(**kwargs)

    def _safe_open(self, path):
        if platform.system() == "Linux":
            os.system("xdg-open %s &" % path)
        else:
            os.system('open %s &' % path)


if __name__ == '__main__':
    transfer = LumoneyP2pTransfer()
    # transfer.login()

    transfer.sync_data()
