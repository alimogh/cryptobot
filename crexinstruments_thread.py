#!/usr/bin/python

import urllib, urllib2, simplejson, threading, pymongo, datetime

def getPrice():
	threading.Timer(30.0, getPrice).start()

### DB stuffs

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["qbot"]
    mycol = mydb["crexinstruments"]

### time

    curtime = datetime.datetime.now()
    #print curtime

### URL data/fetch loop

    url = 'https://api.crex24.com/v2/public/instruments'

    class MyException(Exception):
        pass
    try:
        response = urllib2.urlopen(url, timeout = 5)
    except urllib2.URLError, e:
        raise MyException("There was an error: %r" % e)


    data = simplejson.load(response)

    mycol.drop()

    for line in data:
	pair = line['symbol']
	base = line['baseCurrency']
	quote = line['quoteCurrency']
	fee = line['feeCurrency']
	ticksize = line['tickSize']
	minprice = line['minPrice']
	maxprice = line['maxPrice']
	volumeinc = line['volumeIncrement']
	minvolume = line['minVolume']
	maxvolume = line['maxVolume']
	minquotevol = line['minQuoteVolume']
	maxquotevol = line['maxQuoteVolume']
	supporttype = line['supportedOrderTypes']
	state = line['state']

        datains = { "pair": pair, "base": base, "quote": quote, "fee": fee, "ticksize": ticksize, "minprice": minprice, "maxprice": maxprice, "volumeinc": volumeinc, "minvolume": minvolume, "maxvolume": maxvolume, "minquotevol": minquotevol, "maxquotevol": maxquotevol, "supporttype": supporttype, "state": state, "date": curtime}
        mycol.insert_one(datains)

getPrice()
