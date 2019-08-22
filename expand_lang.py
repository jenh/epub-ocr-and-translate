#!/usr/bin/env python
# -*- coding: utf-8 -*
import pycountry
import argparse

parser = argparse.ArgumentParser(description='expand_lang.py - splits a text files into multiple text files using a specified delimiter')
parser.add_argument('-l','--language', help='Two letter language code', required=True)
args = parser.parse_args()

if (args.language):
    lang = args.language.lower()
#    print "Found language as " + lang
    ccode = pycountry.languages.get(alpha_2=lang)
    if ccode is not None:
        print ccode.name.lower()
    else:
       print "None" 
else:
    print "Need two-letter language code. Usage: python expand_lang.py -l en"
    exit
