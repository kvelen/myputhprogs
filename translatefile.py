#!/usr/bin/env python
from __future__ import print_function
from googletrans import Translator
import os, sys, fileinput, re
import urllib.request, urllib3.request
import json
from pymongo import MongoClient


#variables
path = 'C:\PythonPrograms\AnaliseSpeech'
finname = 'zespeechU.txt'
foutname = 'zespecehE.txt'
finame = path+'\\'+finname
foname = path+'\\'+foutname

def listdir(p):
    files = os. listdir(p)
    for name in files:
        print(name)

#t = translator.translate('если ребенок плачет но вы его не режете вы хорошая мать', dest='en', src='ru')
#print (t)

def translateFile():
    fin=open(finame, 'r')
    fout=open(foname,'w')
    translator = Translator()
    for i in fin:
        j=(translator.translate(i, dest='en', src='ru'))
        j=j.text
        fout.write(j)
    fin.close()
    fout.close()
    print(fout)

def translateFileSen():
    surprise = 0
    calm = 0
    fear = 0
    sadness = 0
    anger = 0
    disgust = 0

    number = 0

    fin=open(finame, 'r')
    text = fin.read()
#   print (text)
#   text = re.sub("\u2019","", text)
    sen = re.split("[.]|[…]|[!]|[?]+", text)
#    print(sen)
    fout=open(foname,'w')
    translator = Translator()
    collection = MongoClient('mongodb://188.166.83.105:27017').admin.sentences
    for i in sen:
        number +=1
        j=(translator.translate(i, dest='en', src='ru'))
        j=j.text
        j = re.sub("\u2019","",j)
        j = re.sub("\u201c","",j)
        j = re.sub("\n\xa0","",j)
        print(j)
        response = json.loads(
                 urllib.request.urlopen(
                     urllib.request.Request('https://qemotion.p.rapidapi.com/v1/emotional_analysis/get_emotions', headers={
                         "X-RapidAPI-Key": "4b77b0bfc8msha1e193906f5df01p149009jsn4171810ad2fd",
                         "Content-Type": "application/json; charset=UTF-8",
                         "Authorization": "Token token=\"bc55ca0a8f5c8c41556f499a93f7077a\"",
                         "lang": "en",
                         "text": j
                     })
                 ).read().decode('utf-8')
             )
        emotions = response['content']['emotions']

        surprise += emotions['surprise']
        calm += emotions['calm']
        fear += emotions['fear']
        sadness += emotions['sadness']
        anger += emotions['anger']
        disgust += emotions['disgust']

        collection.insert_one(
            {
                'number': number,
                'original_text': i,
                'translated_text': j,
                'surprise': surprise,
                'calm': calm,
                'fear': fear,
                'sadness': sadness,
                'anger': anger,
                'disgust': disgust
            }
        )

        print(emotions)
        fout.write(j)

    fin.close()
    fout.close()
    print(fout)
    sp = surprise/(surprise+calm+fear+sadness+anger+disgust)
    cp = calm/(surprise+calm+fear+sadness+anger+disgust)
    fp = fear/(surprise+calm+fear+sadness+anger+disgust)
    sdp = sadness/(surprise+calm+fear+sadness+anger+disgust)
    ap = anger/(surprise+calm+fear+sadness+anger+disgust)
    dp = disgust/(surprise+calm+fear+sadness+anger+disgust)

    print(f'surprise part:{sp}')
    print(f'calm part:{cp}')
    print(f'fear part:{fp}')
    print(f'sadness part:{sdp}')
    print(f'anger part:{ap}')
    print(f'disgust part:{dp}')


#MainLogic
listdir(path)
translateFileSen()


exit

