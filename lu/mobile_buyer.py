import requests


class MobileBuyer:
    def __init__(self):
        self.cookie = '_g=e98761b9-4a39-4486-bd56-44e7f89dc4c6;' \
                      ' _lufaxSID="6b0210ad-accd-4a7f-9e67-e1d357023a3c,' \
                      'PuCtmsgIlggo2n7dL2EB7ZIALePCvZ1xl4GvAAjmDu5+ukHqLkBdejKvSswGiMxgnXNY671jN5p+F++W86I0kA==";' \
                      ' _token=Mzc1YjkxNDNiMThlZTkwOWYyZDk5YjEwNjI1NGJmZjVjN2NiNjNkYzozMDEwMDc0MzoxNDkyNzcwMjc1NzQ4'
        self.Header = {}
        self.session = requests.session()

    def show_buy(self):
        pass


