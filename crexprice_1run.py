#!/usr/bin/python

import urllib, urllib2, simplejson, threading, pymongo, datetime

def getPrice():
#    threading.Timer(30.0, getPrice).start()

### DB stuffs

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["qbot"]
    mycol = mydb["crexprice"]
    mypairs = mydb["crexpairs"]
    weathercol = mydb["weather"]

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

    coinpairs = []

    for x in mypairs.find():
        pair = x['pair']
        coinpairs.append(pair)

    curweath = []
    getweather = weathercol.find()
    for line in getweather:
        pair = line['pair']
        low = line['low']
        high = line['high']
        date = line['date']
        score = line['score']
        last = line['last']
        pct = line['percentchange']
        insweath = (pair, low, high, date, score, last, pct)
        curweath.append(insweath)

    for h in curweath:
        curpair = h[0]
        curlow = h[1]
        curhigh = h[2]
        curdate = h[3]
        curscore = h[4]
        curlast = h[5]
        curpct = [6]


    mypairs.drop()
    mycol.drop()

    pricelist = []

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

        priceins = (pair, low, high, last)
        pricelist.append(priceins)

        datains = { "pair": pair, "last": last, "percentchange": percentchange, "low": low, "high": high, "basevol": basevol, "quotevol": quotevol, "volbtc": volbtc, "volusd": volusd, "ask": ask, "bid": bid, "date": datetime.datetime.now() }
        mycol.insert_one(datains)
        pairins = {  "pair": pair }
        mypairs.insert_one(pairins)


        for h in curweath:
            curpair = h[0]
            curlow = h[1]
            curhigh = h[2]
            curdate = h[3]
            curscore = h[4]
            curlast = h[5]
            curpct = [6]

            if pair == curpair:

                if low < curlow:
                    print "LOW", pair, last, low, curpair, curlow
                    pairins = { "pair": pair }
                    weatherlow = { "$set": { "last": last, "high": curhigh, "date": datetime.datetime.now(), "score": curscore, "low": low, "percentchange": curpct, "pair": curpair }}
                    weathercol.update_many(pairins, weatherlow)

                if high > curhigh:
                    print "HIGH", pair, last, high, curpair, curhigh
                    pairins = { "pair": pair }
                    weatherhi = { "$set": { "pair": curpair, "last": last, "percentchange": curpct, "low": curlow, "high": high, "score": curscore, "date": datetime.datetime.now() }}
                    weathercol.update_many(pairins, weatherhi)
                else:
                    pairins = { "pair": pair }
                    weatherins = { "$set": { "last": last, "high": curhigh, "date": datetime.datetime.now(), "score": curscore, "low": curlow, "percentchange": curpct, "pair": curpair }}
                    weathercol.update_many(pairins, weatherins)

getPrice()
