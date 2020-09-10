#!/usr/bin/env python3
# -*- coding: utf-8 -*-


version="0.0.1.0"

import tweepy as tw
import os
os.chdir("WORKING DIRECTORY PATH") #Change by the path of key file and where the database will be saved

from lib.TwitterDB import TwitterDataBase
from lib.Listener import StListener

from datetime import date
from urllib3.exceptions import ReadTimeoutError
import requests
import time
def keyScanner(path):
    """Reads a file with Twitter keys used to access to a Twitter stream (remember
    you need a developer account to get this).
    The file must contain four lines:
        -Consumer Key
        -Consumer Secret
        -Access token
        -Access secret.

    The keys should be separated into lines and don't need any quotes.
    If there is a space in any part of the file, Twitter would reject the
    connection due to incorrect keyword.
    """

    handler=open(path)
    lines=handler.readlines()
    for i in range(0,len(lines)):
        #The file comes with "\n" between lines. This for erase that.
        lines[i]=lines[i][:-1]

    return(lines)


DB=TwitterDataBase(version,date.today().strftime("_%d_%m_%Y"))
DB.baseCreator("usuario,texto,tiempo,responde_a,hashtags,menciona_a,nombre_lugar,json")
c=DB.getCursor()
conn=DB.getConector()
path="./auth.key"

auth=tw.OAuthHandler(keyScanner(path)[0],
                     keyScanner(path)[1])

auth.set_access_token(keyScanner(path)[2],
                      keyScanner(path)[3])
api=tw.API(auth,wait_on_rate_limit=True)

listener=StListener(DB)
stream=tw.Stream(auth=api.auth,listener=listener)


def searchByLocation(loc):
    stream.filter(locations=loc)


country_location=[-58.491052, -34.9801634, -53.071505, -30.0856928] #READ BELOW
#This is the Uruguay location. You can change this selecting two coordinates in a polygon done with https://geojson.io/.
#ALWAYS REMEBER: the geo polygon can include some neighboring areas. To filter that areas, you need to modify the "country_code" line of lib/Listener.py.
while True:
    try:
        searchByLocation(country_location)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    
    except ReadTimeoutError:
        print("Timeout Error. Retrying conection...")
        continue
    except requests.ConnectionError:
        print("Can't establish connection. Retrying in 5 seconds")
        time.sleep(5)
        continue
    except: #In next version this should print the unknown exception in a log file.
        continue
conn.close()
