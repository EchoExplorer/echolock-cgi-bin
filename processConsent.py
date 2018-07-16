#!/usr/bin/python

import sqlite3, cgi, cgitb, pickle, random, datetime

from Crypto.PublicKey import RSA
from base64 import b64decode

fOpen = open('/srv/maze/private.pem', 'r')
privateKey = fOpen.read()

rsakey = RSA.importKey(privateKey)

def decrypt(decryptThis):
    raw_cipher_data = b64decode(decryptThis)
    return unicode(rsakey.decrypt(raw_cipher_data))

consentForm = cgi.FieldStorage()

username = decrypt(consentForm.getvalue('username'))
agecheck = decrypt(consentForm.getvalue('agecheck'))
understandcheck = decrypt(consentForm.getvalue('understandcheck'))
researchcheck = decrypt(consentForm.getvalue('researchcheck'))

if agecheck == "yes" and agecheck == understandcheck and understandcheck == researchcheck:
  code = findCode()
  storeConsent(code)
  print "Content-type:text/json\r\n\r\n"
  print "{",
  keys = consentForm.keys()
  for key in keys:
      print key, ":\"", consentForm[key].value, "\"", ",",
  print "}"

def findCode():
  with open('/srv/maze/consent.set', 'rb') as f: #set of already used ID #'s
    consentIDS = pickle.load(f)
  while (True):
    code = random.randint(100000, 999999)
    if code not in consentIDS:
      consentIDS.add(code)
      return code

def storeConsent(code):
  dbName = "gameData"

  db = sqlite3.connect('/srv/sqlite/data/' + dbName)
  cursor = db.cursor()

  time = str(datetime.datetime.now())

  cursor.execute('''INSERT INTO ConsentData(userName, surveyID, dateTimeStamp)
  VALUES(?,?,?)''', (userName, code, time))

  db.commit() #changes are committed to database
  db.close()
  