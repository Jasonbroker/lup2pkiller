import requests
import os
import platform
import time
from bs4 import BeautifulSoup
import pprint
import json
import pickle

HEADERS = {'ContentType': 'application/json; charset=UTF-8',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

qr_code = 'qr_code.jpg'

cookie_file = 'cookies.log'

base_url = 'https://list.lu.com'

p2p_url = 'https://list.lu.com/list/transfer-p2p'

test_login_url = 'https://my.lu.com/my/account'


class LumoneyP2pTransfer:
    def __init__(self):
        self.session = requests.session()
        self.is_login = False
        self.debug = True

        cookie_jar = self.get_cookies()
        if cookie_jar:
            self.session.cookies = cookie_jar
        else:
            with open('cookies.json', 'rb') as f:
                cookis_str = f.read().decode()
                cookies = json.loads(cookis_str)
            for cookie in cookies:
                self.session.cookies.set(name=cookie['name'], value=cookie['value'])

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.session.cookies)

        path = '../p.av'
        with open(path, 'rb') as f:
            strr = f.read().decode()
            un_pwd = strr.split(',')
            self.username = un_pwd[0]
            self.pwd = un_pwd[1]
            self.pwd_encode = un_pwd[2]

        print(self.username, self.pwd)

    def login(self):
        print('logging')

        def try_login():
            url = 'https://user.lu.com/user/login'
            data = {
                'isTrust': "Y",
                'password':	self.pwd_encode,
                'openlbo':	"0",
                'deviceKey': "4BA03AE1A3E3A5B7B09C606C1C1F6104B87E6D6AF489E02C22D5A0856827C61B50ADDE6C55CDF3EE3D1C9CE2A40684468117EF64214574F69ABCE0B8A38CFD168E63175E062CED5A627F97D1DBC8692BAAC09E974DAC48BE51ADD2C66F7169ED2EE1DF07CFB48B7A66F753F00DB97645D74F4B024E8AB872B186543C9AE81828",
                'deviceInfo': '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',
                'loginFlag': "2",
                'userName': self.username,
                # 'pwd': self.pwd,
                'validNum':	"",
                'agreeLbo':	"on",
                'loginagree': "on"
            }
            r = self.session.post(url, data=data)
            print(r.cookies)
            dic = r.json()
            if dic['resultId'] == '00':
                self.is_login = True
                self.save_cookies()
                print('Login succeed====\n username: %s\n phone: %s' % (dic['userName'], dic['maskMobileNo']))
                print(dic)
            else:
                return False

            redirect_url = dic['redirectPath']
            return redirect_url

        # get_code()
        #
        # ver_code = input('输入验证码')
        #
        # check_code()

        session_verified = self.test_login()
        if not session_verified:
            redirect_url = try_login()
            return redirect_url
        else:
            return None


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

    def buy_with_url(self, url):
        buy_url = base_url + url
        if self.debug:
            print('will buy product')
            self._safe_open(buy_url)
        if not self.is_login:
            self.login()
        r = self.session.get(buy_url, headers=HEADERS)
        print(r.content.decode('utf-8'))


    def select_product(self, product_list, max_price):
        selected_url = None
        for product in product_list:
            interest = product.find('p', class_='num-style').string
            time_remaining = product.find('li', class_='invest-period').find('p').string
            discount = product.find('b', class_='num-style').string
            if float(interest[:-1].strip()) < 8.4:
                print('low interest %s buy jb' % interest)
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
                time.sleep(0.5)
                continue
            result = self.buy_with_url(url)
            if result:
                break
            # self.test_data()
            break


# helpers
    def save_cookies(self):
        cookiesJar = self.session.cookies
        # if self.debug:
            # print(cookiesJar)
        dic = requests.utils.dict_from_cookiejar(cookiesJar)
        print(dic)
        with open(cookie_file, 'wb') as f:
            pickle.dump(cookiesJar, f, pickle.HIGHEST_PROTOCOL)

    def get_cookies(self):
        with open(cookie_file, 'rb') as f:
            cookie = pickle.load(f)
            print(cookie)
        return cookie


    def _safe_open(self, path):
        if platform.system() == "Linux":
            os.system("xdg-open %s &" % path)
        else:
            os.system('open %s &' % path)

    def check_code(self, capcha):
        url = 'https://user.lu.com/user/captcha/pre-check'
        param = {
            'inputValue': capcha,
            'source': 'login',
            '_': int(time.time()*1000)
        }
        r = self.session.get(url, params=param, headers=HEADERS)
        if r.status_code == 200:
            print('success-----------\n')
            print(self.session.cookies.get_dict())
        print(r.content)

        check_url = 'https://user.lu.com/user/service/login/captcha-authorize'
        para = {
            'source': "PC",
            'username': self.username
        }
        check_r = self.session.post(check_url, params=para, headers=HEADERS)
        print(check_r.text)

    def get_code(self):
        url = 'https://user.lu.com/user/captcha/captcha.jpg'
        param = {
            'source': 'login',
            '_': int(time.time()*1000)
        }
        r = self.session.get(url, params=param, headers=HEADERS)
        print(self.session.cookies.get_dict())
        with open(qr_code, 'wb') as f:
            f.write(r.content)
            self._safe_open(qr_code)

    def test_login(self):
        r = self.session.get('https://my.lu.com/my/account')
        if self.debug:
            print(r.history)
            print(r.url)
        return len(r.history) <= 1


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


if __name__ == '__main__':
    transfer = LumoneyP2pTransfer()

    redirect_url = transfer.login()
    # if transfer.debug:
        # r = transfer.session.get('https://my.lu.com/my/user-ms')
        # print(r.content.decode())


    # transfer.sync_data()


