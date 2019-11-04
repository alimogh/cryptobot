#!/usr/bin/python

import urllib, urllib2, simplejson, threading, pymongo, datetime

def getPrice():
#	threading.Timer(30.0, getPrice).start()

### DB stuffs

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["qbot"]
    mycol = mydb["crexprice"]

### time

    curtime = datetime.datetime.now()
    #print curtime

### URL data/fetch loop

    url = 'https://api.crex24.com/v2/public/tickers'

    class MyException(Exception):
        pass
    try:
        response = urllib2.urlopen(url, timeout = 5)
    except urllib2.URLError, e:
        raise MyException("There was an error: %r" % e)


    data = simplejson.load(response)

    #mycol.drop()

    for line in data:
	pair = line['instrument']
	last = line['last']
	percentchange = line['percentChange']
	low = line['low']
	high = line['high']
	basevol = line['baseVolume']
	quotevol = line['quoteVolume']
	volbtc = line['volumeInBtc']
	volusd = line['volumeInUsd']
	ask = line['ask']
	bid = line['bid']

        datains = { "pair": pair, "last": last, "percentchange": percentchange, "low": low, "high": high, "basevol": basevol, "quotevol": quotevol, "volbtc": volbtc, "volusd": volusd, "ask": ask, "bid": bid, "date": curtime}
        mycol.insert_one(datains)

getPrice()
