import requests
import os
import platform
import time
from bs4 import BeautifulSoup
import pprint
import json
import pickle
import configs

def perfermance_checker(fn, *args, **kwargs):
    pretime = time.time()
    def wrapper(*args, **kwargs):
        fn(*args, **kwargs)
    print('耗时 %f' % (time.time() - pretime))
    return wrapper


class LumoneyP2pTransfer:
    def __init__(self):
        self.session = requests.session()
        self.is_login = True
        self.debug = True
        self.last_productId = ''
        self.product_id_cache = {}
        self.user_id = 30100743

        cookie_jar = self.get_cookies()
        # cookie_jar = None
        if cookie_jar:
            self.session.cookies = cookie_jar
        else:
            with open('cookies.json', 'rb') as f:
                cookies_str = f.read().decode()
                cookies = json.loads(cookies_str)
            for cookie in cookies:
                self.session.cookies.set(name=cookie['name'], value=cookie['value'])

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.session.cookies)

        # 在这个地方写出自己的账号密码
        path = '../p.av'
        with open(path, 'rb') as f:
            strr = f.read().decode()
            un_pwd = strr.split(',')
            self.username = un_pwd[0]
            self.pwd = un_pwd[1]
            self.pwd_encode = un_pwd[2]

    def login(self):
        print('logging…………')

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
            dic = r.json()
            if dic['resultId'] == '00':
                self.is_login = True
                self.save_cookies()
                print('Login succeed====\n username: %s\n phone: %s' % (dic['userName'], dic['maskMobileNo']))
                print(dic)
                self.user_id = dic['userId']
            else:
                return False

            redirect_path = dic['redirectPath']
            return redirect_path

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
        r = self.session.get(configs.p2p_url, headers=configs.HEADERS)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.content, "lxml")
        samples = soup.find_all("li", class_="product-list")
        return self.select_product(samples, 10000)

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

    def get_product_detail(self, product_id):
        url = 'https://trading.lu.com/trading/trade-info'
        dic = {'productId': product_id}
        r = self.session.get(url, params=dic)

        print('detail:\n')
        print(r.text)
        if self.debug:
            print('will buy product')
            self._safe_open(url)

    # check - trace?sid = 278159279 & productId = 145843105 & userId = 30100743 & curStep = TRADE_INFO & _ = 1493088790949
    # trade - info?productId = 145843105 & sid = 278159279
    def invest_check(self, product_id, amount=''):
        dic = {
            'productId': product_id,
            'investAmount': amount,
            'investSource': 0,
            'isCheckSQ': 1,
        }
        api = configs.buy_base_url + '/itrading/invest-check'
        r = self.session.post(api, data=dic)
        result = r.json()
        return result

    # 不需要请求其实
    def trade_info(self, product_id, sid):
        api = configs.trading_url + '/trading/trade-info'
        dic = {
            'productId': product_id,
            'sid': sid,
        }
        r = self.session.get(api, params=dic)
        return r.content

    '''{
    	"res_code": "66",
    	"res_msg": "投资申请已提交",
    	"data": {
    		"code": "66",
    		"apiCode": "400066",
    		"message": "购买验证通过，可开始交易",
    		"locked": false,
    		"sid": 278156788,
    		"balanceAmount": 0,
    		"riskLevelDesc": "稳健型",
    		"productRiskLevelDesc": "保守型",
    		"needWithholding": false,
    		"paymentMethod": "8",
    		"isRiskLevelMatch": true,
    		"isCanResetRiskVerify": false,
    		"riskVerifyLeftCount": 0,
    		"riskVerifyTotalCount": 0,
    		"isRiskVerifySysDefine": false,
    		"virutalPartialInavailProductNamesList": []
    	}
    }'''
    def sync_data(self):

        while True:
            print('syncing at %f' % time.time())
            url, cost = self.check_suitable_productId()
            # url 不存在说明没有数据，继续
            if not url:
                continue

            # 获取id
            product_id = url.split('=')[1]
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

    # https://trading.lu.com/trading/security-valid?productId = 145855546 & sid = 278205369
    def final_process(self, product_id, sid):
        # https: // user.lu.com / user / captcha / get - captcha?source = 1
        api = configs.trading_url + '/trading/security-valid'
        dic = {
            'productId': product_id,
            'sid': sid
        }
        if self.debug:
            self._safe_open(api)
        r = self.session.get(api, params=dic)
        print('final html:\n')
        print(r.content.decode())

    def check_trace(self, user_id, product_id, sid, curStep=configs.TRADE_INFO):
        url = configs.trading_url + '/trading/service/trade/check-trace'
        dic = {
            'sid': sid,
            'productId': product_id,
            'userId': user_id,
            'curStep': curStep,
            '_': int(time.time())
        }
        r = self.session.get(url, params=dic)
        result = r.content.decode()
        return result

    # contract - info?productId = 145855546 & sid = 278205369 & riskLevel = 1
    def contract_info(self, product_id, sid):
        api = configs.trading_url + '/trading/contract-info'
        dic = {
            'sid': sid,
            'productId': product_id,
            'riskLevel': 1,
        }
        r = self.session.get(api, params=dic)
        result = r.content.decode()
        return result


# helpers
    def save_cookies(self):
        cookies_jar = self.session.cookies
        with open(configs.cookie_file, 'wb') as f:
            pickle.dump(cookies_jar, f, pickle.HIGHEST_PROTOCOL)

    def get_cookies(self):
        with open(configs.cookie_file, 'rb') as f:
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
        r = self.session.get(url, params=param, headers=configs.HEADERS)
        if r.status_code == 200:
            print('success-----------\n')
            print(self.session.cookies.get_dict())
        print(r.content)

        check_url = 'https://user.lu.com/user/service/login/captcha-authorize'
        para = {
            'source': "PC",
            'username': self.username
        }
        check_r = self.session.post(check_url, params=para, headers=configs.HEADERS)
        print(check_r.text)

    def get_code(self):
        url = 'https://user.lu.com/user/captcha/captcha.jpg'
        param = {
            'source': 'login',
            '_': int(time.time()*1000)
        }
        r = self.session.get(url, params=param, headers=configs.HEADERS)
        print(self.session.cookies.get_dict())
        with open(configs.qr_code, 'wb') as f:
            f.write(r.content)
            self._safe_open(configs.qr_code)

    # 测试是否需要登录，如果需要登录则调用login
    def test_login(self):
        r = self.session.get('https://my.lu.com/my/account')
        if self.debug:
            print(r.history)
            print(r.url)
        return len(r.history) <= 0


if __name__ == '__main__':
    transfer = LumoneyP2pTransfer()

    redirect_url = transfer.login()

    transfer.sync_data()


