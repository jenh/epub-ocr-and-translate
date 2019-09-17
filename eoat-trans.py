#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import textwrap
import time
import subprocess
import argparse

if (sys.version_info > (3, 0)):
    pass
else:
    reload(sys)
    sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser(description='eoat-trans.py - translates text files from one language to another and combines them in a single file for later processing')
parser.add_argument('-i','--input', help='Input file', required=True)
parser.add_argument('-s','--source',help='Source language', required=True)
parser.add_argument('-t','--target',help='Target language', required=True)
parser.add_argument('-e','--trans',help='Translation engine. For translate-shell, options are google, deepl, bing, apertium, or yandex. Note that some of the commercial engines may not work. By default, we use translate-shell with the Google engine. If using the paid Google Cloud-based Translate API, set the engine to gcloud; if using with OpenNMT Simple Rest Server, set it to opennmt',required=False)
parser.add_argument('-w','--wait',help="Optional wait time to slow crawl free translation servers",required=False)
args = parser.parse_args()

if (args.input):
    input_file = args.input
    print("Found input file as " + input_file)
else:
    exit

if (args.source):
    source_lang = args.source
    print("Found source language code as " + source_lang)
else:
    exit

if (args.target):
    target_lang = args.target
    print("Found target language code as " + target_lang)
else:
    exit

engines = ['google','deepl','bing','apertium','yandex']

if (args.trans):
    trans = args.trans
    if trans in engines:
        engine = trans 
        trans_type = str("trans")
        print("Found engine as " + engine + " for translate-shell.")
    elif trans=='opennmt':
        engine = trans
        trans_type = str("opennmt")
        print("Found engine as " + engine + " for OpenNMT.")
    elif trans=='gcloud':
        from google.cloud import translate
        engine = "google"
        trans_type = str("gccloud")
        translate_client = translate.Client()
        print("Found engine as paid Google Translate API.")
    else:
        engine = "google"
        trans_type = str("trans")
        print("Engine not found, using translate-shell with Google.")
else:
    engine = "google"
    trans_type = str("trans")
    print("Engine not specified, using translate-shell with Google.")

if (args.wait):
    wait_secs = float(args.wait)
else:
    wait_secs = 2

doc = []
output_file_name = input_file + "-2lang.txt"

output_file = open(output_file_name,'a')

max_length = 4000
with open(input_file) as input:
    for line in input:
        lines = textwrap.wrap(line, max_length)
        for line in lines:
            doc.append(line)

if trans_type=='trans':
    for x in doc:
        try:
            output_file.write("\n" + x + "\n")
        except IOError as e:
    # one example is broken pipe
            if e.strerror.lower() == 'broken pipe':
                exit(0)
            raise       # other real IOError
        time.sleep(wait_secs)
        translated = "trans -b -e " + engine + " -s " + source_lang + " -t " +  target_lang + " \"" + x + "\""
        translation = subprocess.check_output(translated,shell=True)
        output_file.write("\n" + translation)
        sys.stdout.flush()
elif trans_type=='opennmt':
    for x in doc:
        try:
            output_file.write("\n")
        except IOError as e:
            if e.strerror.lower() == 'broken pipe':
                exit(0)
            raise
        time.sleep(wait_secs)
        translated = "eoat-onmtpost \"" + x + "\""
        translation = subprocess.check_output(translated,shell=True)
        output_file.write(translation.decode('utf-8'))
        sys.stdout.flush()
else:
    for x in doc:
        output_file.write("\n" + x + "\n")
        sys.stdout.flush()
        time.sleep(wait_secs)
        translation = translate_client.translate(
          x,
          target_language=target_lang,
          source_language=source_lang)
        output_file.write("\n" + translation['translatedText'].encode("utf-8") + "\n")
        sys.stdout.flush()
print("Translation output located in " + output_file_name)
