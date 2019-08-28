#!/usr/bin/env python2.7
# -*- coding: utf-8 -*
import pycountry
import argparse
import os

scriptname = os.path.basename(__file__)

parsearg = scriptname + ": splits a text file into multiple files using a specified delimiter"
parser = argparse.ArgumentParser(description=parsearg)
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
