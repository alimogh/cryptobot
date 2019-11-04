#!/usr/bin/python3

import datetime
import base64
import hmac
import simplejson
import pymongo
from hashlib import sha512
from urllib.request import urlopen, Request
from urllib.error import HTTPError

baseUrl = "https://api.crex24.com"
apiKey = "Put_Your_API_Key_HERE"
secret = "Put_Your_API_Secret_HERE"

## mongodb creds and location
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["qbot"]
mycol = mydb["crexbal"]

path = "/v2/account/balance"
nonce = round(datetime.datetime.now().timestamp() * 1000)

key = base64.b64decode(secret)
message = str.encode(path + str(nonce), "utf-8")
hmac = hmac.new(key, message, sha512)
signature = base64.b64encode(hmac.digest()).decode()

request = Request(baseUrl + path)
request.method = "GET"
request.add_header("X-CREX24-API-KEY", apiKey)
request.add_header("X-CREX24-API-NONCE", nonce)
request.add_header("X-CREX24-API-SIGN", signature)

try:
    response = urlopen(request)
except HTTPError as e:
    response = e

status = response.getcode()
data = simplejson.load(response)


mycol.drop()

for line in data:
    id = 1000
    coin = line['currency']
    availamount = line['available']
    orderamount = line['reserved']

    datains = { "id": id, "coin": coin, "avail": availamount, "order": orderamount }
    mycol.insert_one(datains)

