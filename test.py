import hashlib
import base64
import requests

username = 'florian-niedermeier@gmx.de'
password = '1R4ciNg_2.4?2'

def encode_pw(username, password):
    initialHash = hashlib.sha256((password + username.lower()).encode('utf-8')).digest()
    hashInBase64 = base64.b64encode(initialHash).decode('utf-8')
    return hashInBase64

pwValueToSubmit = encode_pw(username, password)

print(f'{username}\n{pwValueToSubmit}')

