#!/usr/bin/python

import sqlite3, cgi, cgitb

from Crypto.PublicKey import RSA
from base64 import b64decode

fOpen = open('/srv/maze/private.pem', 'r')
privateKey = fOpen.read()

rsakey = RSA.importKey(privateKey)

def decrypt(decryptThis):
    raw_cipher_data = b64decode(decryptThis)
    return unicode(rsakey.decrypt(raw_cipher_data))

dbName = "gameData"

db = sqlite3.connect('/srv/sqlite/data/' + dbName)
cursor = db.cursor()

# Create instance of FieldStorage
echoForm = cgi.FieldStorage()

userName = decrypt(echoForm.getvalue('userName'))
currentLevel = int(decrypt(echoForm.getvalue('currentLevel')))
trackCount = int(decrypt(echoForm.getvalue('trackCount')))
echoLocation = decrypt(echoForm.getvalue('echoLocation'))
locationType = decrypt(echoForm.getvalue('locationType'))
postEchoAction = decrypt(echoForm.getvalue('postEchoAction'))
correctAction = decrypt(echoForm.getvalue('correctAction'))
echoFile = decrypt(echoForm.getvalue('echoFile'))
dateTimeStamp = decrypt(echoForm.getvalue('dateTimeStamp'))

cursor.execute('''INSERT INTO EchoData(userName, currentLevel, trackCount, 
echoLocation, locationType, postEchoAction, correctAction, echoFile, dateTimeStamp)
VALUES(?,?,?,?,?,?,?,?,?)''', (userName, currentLevel, trackCount, 
  echoLocation, locationType, postEchoAction, correctAction, echoFile, dateTimeStamp))

db.commit() #changes are committed to database
db.close()

print "Content-type:text/json\r\n\r\n"
print "{",
keys = echoForm.keys()
for key in keys:
    print key, ":\"", echoForm[key].value, "\"", ",",
print "}"