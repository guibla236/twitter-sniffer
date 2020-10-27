#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tweepy as tw
import os
import requests
import time

from lib.TwitterDB import TwitterDataBase
from lib.Listener import StListener
from datetime import date
from urllib3.exceptions import ReadTimeoutError
from lib.utils import keyScanner

db_directory=os.getcwd() #This is the path where the database file will be saved.
os.chdir(db_directory)

cols_names=["user","text","timestamp","answer_to","hashtags","mentions_to","location_name","json"]

DB=TwitterDataBase(date.today().strftime("%m_%d_%Y"),cols_names)
c=DB.getCursor()
conn=DB.getConector()

auth_keys_path="./auth.key" #The auth file is in the working directory by default. If you want to take this from another location, change this line.
keys=keyScanner(auth_keys_path)

auth=tw.OAuthHandler(keys[0],
                     keys[1])

auth.set_access_token(keys[2],
                      keys[3])
api=tw.API(auth,wait_on_rate_limit=True)

country_location=[-58.491052, -34.9801634, -53.071505, -30.0856928] #READ BELOW!!!
"""This is the Uruguay location. You can change this selecting two coordinates in a polygon done from https://geojson.io/.
   That page gives a five element polygon. You should select only the different points. Use this default location as an example

   To extract specific geographical places from the Twitter's API, use tweepi.api.geo_search(query="Uruguay",granularity="country"),
   changing Uruguay to the desired country.

   ALWAYS REMEBER: the geo polygon can include some neighboring areas. To filter that areas,
   you need to modify the "country_code" parameter of the Listener definition.
"""


listener=StListener(DB,"America/Montevideo","UY",debug=True) #Change if need another location.
stream=tw.Stream(auth=api.auth,listener=listener)


while True:
    try:
        stream.filter(locations=country_location)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")

    except ReadTimeoutError:
        print("Timeout Error. Retrying conection...")
        continue

    except requests.ConnectionError:
        print("Can't establish connection. Retrying in 5 seconds")
        time.sleep(5)
        continue

    #except Exception as ex: print(ex)

conn.close()
