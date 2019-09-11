#!/usr/bin/env python3

from guess_language import guessLanguage

import sys
import sqlite3 as lite
import re
import argparse

parser = argparse.ArgumentParser(description='EOAT post-process: After translating using OpenNMT, locate untranslated pieces and translate them using literal dictionary terms')
parser.add_argument('-s','--sentence',help='Sentence to translate',required=True)
parser.add_argument('-l','--language',help='Source language (two-letter-code)',required=True)
parser.add_argument('-t','--targetlanguage',help='Target language, defaults to en',required=False)
parser.add_argument('-d','--database',help='SQLite3 dictionary database',required=True)
parser.add_argument('-T','--table',help='dictionary table name',required=True)
parser.add_argument('-u','--showunknowns',action='store_true',help='Surround post-processed words with brackets',required=False)
args = parser.parse_args()

if (args.sentence):
    sentence = args.sentence
else:
  print("Must specify a sentence to translate using -s or --sentence")
  sys.exit(0)

if (args.language):
    language = args.language
else:
    print("Must specify a two-letter language code using -l or --language")
    sys.exit(0)

if (args.targetlanguage):
    tl = args.targetlanguage
else:
    tl = 'en'

if (args.database):
    db = args.database
else:
    print("Must specify dictionary database name using -d or --database")
    sys.exit(0)

if (args.table):
    tablename = args.table
else:
    print("Must specify table name")
    sys.exit(0)

if (args.showunknowns):
    unk = True
else:
    unk = False

conn = lite.connect(db)
conn.text_factory = str

words = []
recombine = []

for i,word in enumerate(sentence.split()):
    words.append(word)

for word in words:
    if word.istitle() == True:
        title = True
        word = word.lower()
    else:
        title = False
    splitword = re.findall(r"[\w']+|[.,!?;—]", word)
    word = splitword[0]
    if len(splitword) >= 2:
        p = True
        punc = splitword[1]
    else:
        p = False
    if guessLanguage(word) == language:
        # Worst way to find a match ever...
        translation = conn.cursor().execute('select ' + tl + ' from \'' + tablename + '\' where ' + language + '  = ? limit 1',(word,)).fetchone()
        if translation == None:
            translation = conn.cursor().execute('select ' + tl + ' from \'' + tablename + '\' where ' + language + '  like ? limit 1',('%'+word+'%',)).fetchone()
            if translation == None:
                translation = conn.cursor().execute('select ' + tl + ' from \'' + tablename + '\' where ' + language + '  like ? limit 1',('%'+word[:-2]+'%',)).fetchone()
                if translation == None:
                    translation = conn.cursor().execute('select ' + tl + ' from \'' + tablename + '\' where ' + language + '  like ? limit 1',('%'+word[:-3]+'%',)).fetchone()
                    if translation == None:
                        translation = conn.cursor().execute('select ' + tl + ' from \'' + tablename + '\' where ' + language + '  like ? limit 1',('%'+word[:-4]+'%',)).fetchone()
                        if translation == None:
                            translation = conn.cursor().execute('select ' + tl + ' from \'' + tablename + '\' where ' + language + '  like ? limit 1',('%'+word[2:]+'%',)).fetchone()
                            if translation == None:
                                translation = conn.cursor().execute('select ' + tl + ' from \'' + tablename + '\' where ' + language + '  like ? limit 1',('%'+word[3:]+'%',)).fetchone()
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
             pass
        if translation:
            translation = translation[0]
        else:
            translation = word 
        if title == True:
            translation = translation.title()
        else:
           pass 
        if p == True:
            if unk == True:
                recombine.append('['+translation+punc+']')
            else:
                recombine.append(translation+punc)
        else:
            if unk == True:
                recombine.append('['+translation+']')
            else:
                recombine.append(translation)
    else:
        if p == True:
            recombine.append(word+punc)
        else:
            recombine.append(word)

recombine = ' '.join(recombine)

print(recombine)
conn.close()
