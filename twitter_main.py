#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 18:35:08 2020

@author: guillermo

Para extraer lugares geográficos específicos de la api de twitter se recomienda hacer tweepi.api.geo_search(query="Uruguay",granularity="country"), cambiando Uruguay por el país que sea.
"""

version="0.0.1.0"

import tweepy as tw
import os
os.chdir("/home/guillermo/Documentos/Programación/Twitter/")

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
ruta="./auth.key"

auth=tw.OAuthHandler(keyScanner(ruta)[0],
                     keyScanner(ruta)[1])

auth.set_access_token(keyScanner(ruta)[2],
                      keyScanner(ruta)[3])
api=tw.API(auth,wait_on_rate_limit=True)

listener=StListener(DB)
stream=tw.Stream(auth=api.auth,listener=listener)


def busquedaPorFiltro(filtro):
    stream.filter(track=filtro)
def busquedaPorLocation(loc):
    stream.filter(locations=loc)
    
#filtro=['Lacalle Pou',"lacalle pou","Lacalle pou","Montevideo","damiani","Damiani","peñarol","Peñarol"]
#filtro=['Trump',"trump"]
loc_mvd=[-56.432647705078125,-34.9484279063708,-56.02134704589844,-34.696461172723474]
loc_uy=[-58.491052, -34.9801634, -53.071505, -30.0856928]
while True:
    try:
        busquedaPorLocation(loc_uy)
        #busquedaPorFiltro(filtro)

    except KeyboardInterrupt:
        print("SE INTERRUMPE LA EJECUCIÓN")
    
    except ReadTimeoutError:
        print("SE CORTÓ LA CONEXIÓN, REINTENTANDO")
        continue
    except requests.ConnectionError:
        print("Imposible establecer conexión. Reintentando en 5 segundos")
        time.sleep(5)
        continue
    except:
        continue
conn.close()

#Hay que ver cómo maneja la excepción ReadTimeoutError
    

#conn=sqlite3.connect("Base_twitter.db")
#df=pd.read_sql_query("SELECT * FROM twitter",conn)


