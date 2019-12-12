#!/usr/bin/python

from __future__ import division
import pymongo, threading, datetime, urllib, urllib2, simplejson, json
#from twilio.rest import TwilioRestClient

def getWeather():

#       threading.Timer(94.0, getWeather).start()

### DB stuffs

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["qbot"]
        mycol = mydb["crexprice"]
        crexpairs = mydb["crexpairs"]
        crexprice = mydb["crexprice"]
        weather = mydb["weather"]
        crexweatherhist = mydb["crexweatherhist"]



# datetime

        cur_time = datetime.datetime.now()


        for x in weather.find():
            pair = x['pair']
            #print pair
            last = x['last']
            low = x['low']
            high = x['high']
            date = x['date']
            pct = x['percentchange']

            pctlow = ((last - low) / low) * 100
            pcthi = ((high - last) / last) * 100

            if pcthi <= 10 and pcthi > 0.01:
                #print pair, pcthi, "selling"
                score = 100
                pairins = { "pair": pair }
                weatherins = { "$set": { "last": last, "high": high, "date": datetime.datetime.now(), "score": score, "low": low, "percentchange": pct, "pair": pair }}
                weather.update_many(pairins, weatherins)

            elif pcthi <= 0 and pcthi >= 0:
                #print pair, pcthi, "watching hi"
                score = 70
                pairins = { "pair": pair }
                weatherins = { "$set": { "last": last, "high": high, "date": datetime.datetime.now(), "score": score, "low": low, "percentchange": pct, "pair": pair }}
                weather.update_many(pairins, weatherins)
            elif pctlow <= 20 and pctlow > 0.01:
                #print pair, pctlow, "Buying"
                score = 0
                pairins = { "pair": pair }
                weatherins = { "$set": { "last": last, "high": high, "date": datetime.datetime.now(), "score": score, "low": low, "percentchange": pct, "pair": pair }}
                weather.update_many(pairins, weatherins)
            elif pctlow >= 0 and pctlow <= 0.01:
                #print pair, pctlow, last, low, "watching low"
                score = 30
                pairins = { "pair": pair }
                weatherins = { "$set": { "last": last, "high": high, "date": datetime.datetime.now(), "score": score, "low": low, "percentchange": pct, "pair": pair }}
                weather.update_many(pairins, weatherins)
            else:
                #print pair, "niets"
                score = 50
                pairins = { "pair": pair }
                weatherins = { "$set": { "last": last, "high": high, "date": datetime.datetime.now(), "score": score, "low": low, "percentchange": pct, "pair": pair }}
                weather.update_many(pairins, weatherins)

getWeather()
