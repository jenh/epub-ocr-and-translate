#!/usr/bin/env python3
# -*- coding: utf-8 -*
import re
import sys
import argparse

parser = argparse.ArgumentParser(description='eoat-split - splits a text files into multiple text files using a specified delimiter')
parser.add_argument('-i','--input', help='Input file', required=True)
parser.add_argument('-d','--delimiter',help='Chapter or section delimiter, for example, CHAPTER', required=True)
args = parser.parse_args()

if (args.input):
    input_file = args.input
    print("Found input file as " + input_file)
else:
    exit

if (args.delimiter):
    delimiter = args.delimiter
    print("Found chapter delimiter as " + delimiter) 
else:
    exit

with open(input_file, 'r',encoding='utf-8') as file:
    txt = file.read()

num = 0
output = re.split(delimiter, txt)

for line in output:
    chap = open(str(num).zfill(3) + ".md",'w',encoding='utf-8')
    chap.write("# " + delimiter + line + "\n")
    chap.close()
    num = num + 1
    print(num)
 
