from os import read

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
import time
from bs4 import BeautifulSoup
import requests
from requests.cookies import RequestsCookieJar
from http.cookiejar import Cookie

HEADERS = {'ContentType': 'application/json; charset=UTF-8',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3)'
                         ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

qr_code = 'qr_code.jpg'

cookie_file = 'cookies.log'

base_url = 'https://list.lu.com'

p2p_url = 'https://list.lu.com/list/transfer-p2p'

test_login_url = 'https://my.lu.com/my/account'

class Lumoney:
    def __init__(self):
        path = '../p.av'
        with open(path, 'rb') as f:
            str = f.read().decode()
            un_pwd = str.split(',')
            self.username = un_pwd[0]
            self.pwd = un_pwd[1]
            print(self.username, self.pwd)
        # self.driver = webdriver.PhantomJS(executable_path='/Users/jason/logs/phantomjs')
        # self.driver = webdriver.Firefox(executable_path='/Users/jason/logs/geckodriver')
        self.driver = webdriver.Chrome(executable_path='/Users/jason/logs/chromedriver')

        def get_cookies():
            with open(cookie_file, 'rb') as f:
                cookie = pickle.load(f)
                # print(cookie)
            return cookie

        self.session = requests.session()
        self.is_login = False
        self.veri = False
        # cookie_jar = get_cookies()
        # dic = requests.utils.dict_from_cookiejar(cookie_jar)
        # for cookie in dic.items():
            # self.driver.add_cookie(cookie)
        # self.driver.get_cookies()

    def login(self):
        driver = self.driver
        driver.get('https://user.lu.com/user/login')
        cookie = driver.get_cookies()
        print(cookie)
        input_userName = driver.find_element_by_id('userNameLogin')
        input_userName.send_keys(self.username)

        input_password = driver.find_element_by_id('pwd')
        input_password.send_keys(self.pwd)

        vericode = input('input code:')
        input_capcha = driver.find_element_by_id('validNum')
        if not input_capcha.text:
            input_capcha.send_keys(vericode)
        login = driver.find_element_by_id('loginBtn')
        login.send_keys(Keys.ENTER)
        self.is_login = True

        login_cookies = driver.get_cookies()
        print(login_cookies)



        # self.driver.get('https://my.lu.com/my/account')
        # total = self.driver.find_element_by_class_name('total-asset-number')
        # print('共有资产 %s' % total.text)

    def sync_data(self):

        while True:
            url = self.check_suitable_productId()
            # url 不存在说明没有数据，继续
            if not url:
                time.sleep(0.1)
                continue
            result = self.buy_with_url(url)
            if result:
                break
            # self.test_data()
            break

    def buy_with_url(self, url):
        buy_url = base_url + url
        product_id = url.split('=')[1]

        # if self.debug:
        #     print('will buy product')
        #     self._safe_open(buy_url)
        if not self.is_login:
            self.login()
        # r = self.session.get(buy_url, headers=HEADERS)
        self.driver.get(buy_url)
        investBtn = None
        try:
            investBtn = self.driver.find_element_by_class_name('investBtn')
            investBtn.click()
        except Exception:
            print('nonono button')
            self.sync_data()

        # print(detail.content)
        # print(r.content.decode('utf-8'))

    def check_suitable_productId(self):
        print('syncing')
        r = self.session.get(p2p_url, headers=HEADERS, verify=self.veri)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.content, "lxml")
        samples = soup.find_all("li", class_="product-list")
        url = self.select_product(samples, 10000)
        return url

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



if __name__ == '__main__':

    transfer = Lumoney()
    transfer.login()

    transfer.sync_data()
