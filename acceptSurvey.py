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

dbName = "gameData"

db = sqlite3.connect('/srv/sqlite/data/' + dbName)
cursor = db.cursor()

# Create instance of FieldStorage
surveyForm = cgi.FieldStorage()

surveyID = decrypt(surveyForm.getvalue('surveyID'))
controls = decrypt(surveyForm.getvalue('controls'))
easy = decrypt(surveyForm.getvalue('easy'))
echonavigate = decrypt(surveyForm.getvalue('echonavigate'))
enjoy = decrypt(surveyForm.getvalue('enjoy'))
frustrating = decrypt(surveyForm.getvalue('frustrating'))
hearingimpaired = decrypt(surveyForm.getvalue('hearingimpaired'))
hints = decrypt(surveyForm.getvalue('hints'))
instructions = decrypt(surveyForm.getvalue('instructions'))
look = decrypt(surveyForm.getvalue('look'))
lost = decrypt(surveyForm.getvalue('lost'))
playmore = decrypt(surveyForm.getvalue('playmore'))
tutorial = decrypt(surveyForm.getvalue('tutorial'))
tutorialhelp = decrypt(surveyForm.getvalue('tutorialhelp'))
understandecho = decrypt(surveyForm.getvalue('understandecho'))
visuallyimpaired = decrypt(surveyForm.getvalue('visuallyimpaired'))
email = decrypt(surveyForm.getvalue('email'))
likes = decrypt(surveyForm.getvalue('likes'))
confusions = decrypt(surveyForm.getvalue('confusions'))
suggestions = decrypt(surveyForm.getvalue('suggestions'))

time = str(datetime.datetime.now())

cursor.execute('''INSERT INTO SurveyData(surveyID,
        controls, easy, echonavigate, enjoy,
        frustrating, hearingimpaired, hints,
        instructions, look, lost, playmore,
        tutorial, tutorialhelp, understandecho,
        visuallyimpaired, email, likes, confusions,
        suggestions, dateTimeStamp)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
        (surveyID, controls, easy, echonavigate, enjoy, frustrating,
            hearingimpaired, hints, instructions, look, lost, playmore,
            tutorial, tutorialhelp, understandecho, visuallyimpaired, email,
            likes, confusions, suggestions, time))

db.commit() #changes are committed to database
db.close()

print "Content-type:text/json\r\n\r\n"
print "{",
keys = surveyForm.keys()
for key in keys:
    print key, ":\"", surveyForm[key].value, "\"", ",",
print "}"
