#!/usr/bin/python

import sqlite3, cgi, cgitb, datetime

from Crypto.PublicKey import RSA
from base64 import b64decode

fOpen = open('/srv/maze/private.pem', 'r')
privateKey = fOpen.read()

rsakey = RSA.importKey(privateKey)

def decrypt(decryptThis):
    raw_cipher_data = b64decode(decryptThis)
    return unicode(rsakey.decrypt(raw_cipher_data))

surveyForm = cgi.FieldStorage()

dbName = "gameData"

db = sqlite3.connect('/srv/sqlite/data/' + dbName)
cursor = db.cursor()

surveyID = decrypt(surveyForm.getvalue('surveyID'))
enjoy = decrypt(surveyForm.getvalue('enjoy'))
playmore = decrypt(surveyForm.getvalue('playmore'))
easy = decrypt(surveyForm.getvalue('easy'))
lost = decrypt(surveyForm.getvalue('lost'))
understandecho = decrypt(surveyForm.getvalue('understandecho'))
frustrating = decrypt(surveyForm.getvalue('frustrating'))
tutorial = decrypt(surveyForm.getvalue('tutorial'))
tutorialhelp = decrypt(surveyForm.getvalue('tutorialhelp'))
hints = decrypt(surveyForm.getvalue('hints'))
instructions = decrypt(surveyForm.getvalue('instructions'))
controls = decrypt(surveyForm.getvalue('controls'))
look = decrypt(surveyForm.getvalue('look'))
echonavigate = decrypt(surveyForm.getvalue('echonavigate'))
visuallyimpaired = decrypt(surveyForm.getvalue('visuallyimpaired'))
hearingimpaired = decrypt(surveyForm.getvalue('hearingimpaired'))

time = str(datetime.datetime.now())

cursor.execute('''INSERT INTO SurveyData(surveyID,
        enjoy, playmore, easy, lost, understandecho,
        frustrating, tutorial, tutorialhelp, hints,
        instructions, controls, look, echonavigate,
        visuallyimpaired, hearingimpaired, dateTimeStamp)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
        (surveyID, enjoy, playmore, easy, lost, understandecho,
        frustrating, tutorial, tutorialhelp, hints,
        instructions, controls, look, echonavigate,
        visuallyimpaired, hearingimpaired, time))

db.commit() #changes are committed to database
db.close()

print "Content-type:text/json\r\n\r\n"
print "{",
keys = surveyForm.keys()
for key in keys:
    print key, ":\"", surveyForm[key].value, "\"", ",",
print "}"