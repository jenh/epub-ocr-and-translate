#!/usr/bin/env python
# -*- coding: utf-8 -*

import sys
import os
import textwrap
#import time
from subprocess import call
import argparse

# Check for system vs local install
install = os.path.isfile('/usr/bin/eoat-tool')

# Get script and working directories
dir_path = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()

arglength = len(sys.argv)

if arglength == 1:
    mode = "help"
else:
    mode = sys.argv[1]
    args = " ".join(sys.argv[2:arglength])
    args = [a.strip() for a in args.split("--")]
    argstopass = "\n".join(args)
modes = ['ocr','trans','split','make','build']
if mode in modes: 
    if install == True:
        mycommand = "eoat-" + mode + " " + argstopass
    else:
        myexec = os.popen('ls ' + dir_path + '|grep ' + mode).read().strip()
        mycommand = dir_path + "/" + myexec + " " + argstopass 
    print("\nRunning in mode " + mode + " using " + mycommand + " \n")
    exit
    call(mycommand,shell=True)
else:
    ocr_help = "ocr:   Given a PDF and a three-letter source language, OCRs and cleans up output."
    ocr_usage = "Usage: eoat-tool ocr PDF_FILE_NAME THREE_LETTER_SOURCE_LANGUAGE_CODE"
    ocr_example = "Example: eoat-tool ocr my_file.pdf eng"
    trans_help = "trans: Translate text files. Input file name and source/destination languages are required. Wait seconds (default 2 seconds) between translation server requests and translation engine (default free Google search using translate-shell) are optional. Engine options include google, bing, yandex, and gcloud. gcloud requires gcloud, google-cloud-translate Python modules and your credentials exported to GOOGLE_APPLICATION_CREDENTIALS."
    trans_usage = "Usage: eoat-tool trans -i source_text_file -s two-letter-source_lang -t two-letter-target_lang [-e trans|gcloud] [-w wait_seconds]" 
    trans_example = "Example: eoat-tool trans -i input.txt -s ru -t en -e google -w 20"
    split_help = "split: Splits a given file into individual files for each chapter. UTF-8 is accepted, so you should be able to use any language. For example, if your source text is Russian, you could use \"Глава\""
    split_usage = "Usage: oeat-tool split -i filename.txt -d CHAPTER"
    make_help = "make:  Creates a Makefile and copies templates to the current directory for use with the eoat build command."
    make_usage = "Usage: eoat-tool make"
    build_help = "build: For a specified language and input file, create PDF and epub files"
    build_usage = "Usage: eoat-tool build two_letter_language"
    build_example = "Example: eoat-tool build es"
    wrapper = textwrap.TextWrapper(width=72)
    wrapper.initial_indent = "\n* "
    wrapper.subsequent_indent ="\t "
    subwrapper = textwrap.TextWrapper(width=72)
    subwrapper.initial_indent = "\n\t "
    subwrapper.subsequent_indent = "\t"
    ocr_help = wrapper.fill(text=ocr_help)
    print(ocr_help)
    ocr_usage = subwrapper.fill(text=ocr_usage)
    print(ocr_usage)
    ocr_example = subwrapper.fill(text=ocr_example)
    print(ocr_example)
    trans_help = wrapper.fill(text=trans_help)
    print(trans_help)
    trans_usage = subwrapper.fill(text=trans_usage)
    print(trans_usage)
    trans_example = subwrapper.fill(text=trans_example)
    print(trans_example)
    split_help = wrapper.fill(text=split_help)
    print(split_help)
    split_usage = subwrapper.fill(text=split_usage)
    print(split_usage)
    make_help = wrapper.fill(text=make_help)
    print(make_help)
    make_usage = subwrapper.fill(text=make_usage)
    print(make_usage)
    build_help = wrapper.fill(text=build_help)
    print(build_help)
    build_usage = subwrapper.fill(text=build_usage)
    print(build_usage)
    build_example = subwrapper.fill(text=build_example)
    print(build_example)
    print("\n")

