import hashlib
import base64
import json
import os
from http.cookiejar import CookieJar, LWPCookieJar

import requests

username = 'florian-niedermeier@gmx.de'
password = '1R4ciNg_2.4?2'


def encode_pw(username, password):
    initialHash = hashlib.sha256((password + username.lower()).encode('utf-8')).digest()
    hashInBase64 = base64.b64encode(initialHash).decode('utf-8')
    return hashInBase64


def authenticate(pwValueToSubmit):
    loginAdress = "https://members-ng.iracing.com/auth"
    loginHeaders = {"Content-Type": "application/json"}
    authBody = {"email": username, "password": pwValueToSubmit}

    session = requests.Session()
    cookie_File = "cookie-jar.txt"
    session.cookies = LWPCookieJar(cookie_File)

    if os.path.exists(cookie_File):
        session.cookies.load(cookie_File)

    response = session.get('https://members-ng.iracing.com/data/car/get')

    if response.status_code == 401:
        print('setting cookies')
        session.cookies.save()
        loginNow = session.post(loginAdress, json=authBody, headers=loginHeaders)
        response_Data = loginNow.json()

        if loginNow.status_code == 200 and response_Data['authcode']:
            if cookie_File:
                session.cookies.save(ignore_discard=True)
            authenticated = True
        else:
            raise RuntimeError("Error from iRacing: ", response_Data)
    else:
        print('loading saved cookies')
        session.cookies.load(cookie_File)

    return session


###############################

pwValueToSubmit = encode_pw(username, password)
session = authenticate(pwValueToSubmit)

responseJson = session.get('https://members-ng.iracing.com/data/car/get')
responseDict = responseJson.json()
finalJson = requests.get(responseDict["link"])
finalList = finalJson.json()

print(finalList[0]["car_name"])
