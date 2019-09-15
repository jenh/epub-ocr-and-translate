#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Uses nltk to break a file into sentences
# Usage: nltk-sentences.py infile outfile

import sys
import string
import re
import argparse

if (sys.version_info > (3, 0)):
    pass
else:
    reload(sys)
    sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser(description='nltk-sentences.py: Use nltk to break a file into individual sentences')
parser.add_argument('-s','--source',help='Source File', required=True)
parser.add_argument('-o','--output',help='Output File', required=True)
parser.add_argument('-p','--strip_punc',help='Strip punctuation',action='store_true',required=False)
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

filename = srcfile

file = open(filename, 'rt')
text = file.read()
file.close()
out = open(outfile,'w')
# split into sentences
from nltk import sent_tokenize
sentences = sent_tokenize(text)
for line in sentences:
    if strip_punc == True:
       translate_table = dict((ord(char), " ") for char in string.punctuation)
       line = line.translate(translate_table)
       line = re.sub(' +', ' ', line)
    else:
        pass
    out.write(line)
    out.write("\n")
