import pickle

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from lu import configs

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
        self.product_id_cache = {}
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
            url, cost = self.check_suitable_productId()
            # url 不存在说明没有数据，继续
            if not url:
                # time.sleep(0.1)
                continue
                # 获取id

            '''product_id = url.split('=')[1]
            content_json = self.invest_check(product_id, cost)
            can_buy = (content_json['res_code'] == '66')
            print(content_json)
            if can_buy:
                print('go a head')
                sid = content_json['data']['sid']
                # check = self.check_trace(self.user_id, product_id, sid)
                # print(check)
                # contract = self.contract_info(product_id, sid)
                # print(contract)
                self.final_process(product_id, sid)
                break
            '''
            self.buy_with_url(url)


    def final_process(self, product_id, sid):
        # https: // user.lu.com / user / captcha / get - captcha?source = 1
        api = configs.trading_url + '/trading/security-valid'
        dic = {
            'productId': product_id,
            'sid': sid
        }
        url = api + '?productId=%s&sid=%s' % (product_id, sid)
        self.driver.get(url)

        # r = self.session.get(api, params=dic)
        # print('final html:\n')
        # print(r.content.decode())

    def invest_check(self, product_id, amount=''):
        dic = {
            'productId': product_id,
            'investAmount': amount,
            'investSource': 0,
            'isCheckSQ': 1,
        }
        api = configs.buy_base_url + '/itrading/invest-check'
        r = self.session.post(api, data=dic)
        print(r.content.decode())
        if r.content:
            result = r.json()
        return result

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

            # confirmBtn = self.driver.find_element_by_class_name('confirmBtn')
            # print(confirmBtn.text)
            # if confirmBtn:
            #     if confirmBtn.text == '浏览其他投资项目':
            #         print('浏览其他投资项目')
            #         # self.driver.close()
            #         self.sync_data()

            print('current url: %s' % self.driver.current_url)
            nextButton = self.driver.find_element_by_class_name('infoNextBtn')
            print('next button:')
            print(nextButton)
            if nextButton:
                print('gogo next button')
                print(self.driver.current_url)
                nextButton.click()

        except Exception:
            print('nonono button')
            self.do_again()

        # print(detail.content)
        # print(r.content.decode('utf-8'))

    def check_suitable_productId(self):
        print('syncing')
        r = self.session.get(p2p_url, headers=HEADERS, verify=self.veri)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.content, "lxml")
        samples = soup.find_all("li", class_="product-list")
        url, cost = self.select_product(samples, 10000)
        return url, cost

    def select_product(self, product_list, max_price):
        selected_url = None
        fprice = 0
        for product in product_list[:-1]:
            url = product.find('a', class_='ld-btn').get('href')
            if self.product_id_cache.get(url):
                print('same url')
                if len(self.product_id_cache) > 20:
                    self.product_id_cache.clear()
                continue
            else:
                self.product_id_cache[url] = url

            interest = product.find('p', class_='num-style').string
            time_remaining = product.find('li', class_='invest-period').find('p').string
            discount = product.find('b', class_='num-style').string
            if float(interest[:-1].strip()) < 8.4:
                print('low interest %s buy jb' % interest)
                continue
            price = product.find('em', class_='num-style').string
            fprice = float(price.strip().replace(',', ''))
            if fprice > max_price:
                continue

            selected_url = url
            print('已选择最优方案:', interest, fprice, discount, time_remaining, url)
            break
        return selected_url, fprice

    def do_again(self):
        # self.driver.close()
        self.sync_data()


if __name__ == '__main__':

    transfer = Lumoney()
    transfer.login()

    transfer.sync_data()
