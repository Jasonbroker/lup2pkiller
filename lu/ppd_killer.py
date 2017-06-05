import requests

access_url = "http://gw.open.ppdai.com/invest/LLoanInfoService/BatchListingInfos"
data = {
  "ListingIds": [
    23886149,
    23886150
  ]
}

session = requests.session()

r = session.get(access_url, params=data)
print(r.json())
