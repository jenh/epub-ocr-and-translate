#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Uses nltk to break a file into sentences
# Usage: nltk-sentences.py -s srcfile -o outputfile [-p] [-l n] 

import sys
import string
import re
import argparse

from nltk.tokenize import sent_tokenize

if (sys.version_info > (3, 0)):
    pass
else:
    reload(sys)
    sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser(description='nltk-sentences.py: Use nltk to break a file into individual sentences, optionally strip punctuation or remove short sentences')
parser.add_argument('-s','--source',help='Source File', required=True)
parser.add_argument('-o','--output',help='Output File', required=True)
parser.add_argument('-p','--strip_punc',help='Strip punctuation',action='store_true',required=False)
parser.add_argument('-l','--sentence_length',help='Remove sentences shorter than the specified amount',required=False)
args = parser.parse_args()

if (args.source):
    srcfile = args.source
else:
    exit
if (args.output):
    outfile = args.output
else:
    exit
if (args.strip_punc):
    strip_punc = True
else:
    strip_punc = False
if (args.sentence_length):
    long = True
    sentence_length = int(args.sentence_length)
else:
    long = False

filename = srcfile

file = open(filename, 'rt')
text = file.read()
file.close()
out = open(outfile,'w')
# split into sentences
sentences = sent_tokenize(text) 
for line in sentences:
    line = line.replace('\n\n','\n').replace('\n\n','\n')
    if strip_punc == True:
       translate_table = dict((ord(char), " ") for char in string.punctuation)
       line = line.translate(translate_table)
       line = re.sub(' +', ' ', line)
    else:
        pass
    if long == True:
        words = line.split() 
        word_count = len(words)
        if word_count > sentence_length:
            out.write(line)
            out.write("\n")
        else:
            pass
    else:
        out.write(line)
        out.write("\n")
