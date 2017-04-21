from os import read

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
        self.driver = webdriver.Firefox(executable_path='/Users/jason/logs/geckodriver')
        self.username = str

    def login(self):
        driver = self.driver
        driver.get('https://user.lu.com/user/login')
        cookie = driver.get_cookies()
        print(cookie)
        input_userName = driver.find_element_by_id('userNameLogin')
        input_userName.send_keys(self.username)

        input_password = driver.find_element_by_id('pwd')
        input_password.send_keys(self.pwd)

        login = driver.find_element_by_id('loginBtn')
        login.send_keys(Keys.ENTER)
        login_cookie = driver.get_cookies()
        print(login_cookie)




if __name__ == '__main__':

    transfer = Lumoney()
    # transfer.login()
