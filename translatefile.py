#!/usr/bin/env python
from __future__ import print_function
from googletrans import Translator
import os, sys, fileinput

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



#MainLogic
listdir(path)
translateFile()


exit

