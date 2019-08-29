#!/usr/bin/env python2.7
# -*- coding: utf-8 -*
import re
import sys
import argparse

parser = argparse.ArgumentParser(description='eoat-corpusclean - If specified characters exist in a source training file, removes the entire line, then removes the corresponding lines from the target file. By default, latin characters are removed. Optionally, you can use a regex (for example, use default mode to remove mixed English/Russian lines from a Russian file and corresponding English file, then run with -r regex (-r 'А-ЯЁ', for example) with the English file as source and Russian as target to remove Cyrillic from the English and coresponding lines from the Russian. A helper script for OpenNMT corpus cleanup') 
parser.add_argument('-s','--source', help='Source file that contains training data that needs scrubbing', required=True)
parser.add_argument('-t','--target',help='Target file that needs the corresponding lines removed', required=True)
parser.add_argument('-r','--regex',help='Any lines that contain matches will be removed',required=False)
args = parser.parse_args()

if (args.source):
    source_file = args.source
    print "Found source file as " + source_file
else:
    exit

if (args.target):
    target_file = args.target
    print "Found target as " + target_file
else:
    exit

if (args.regex):
    regex = args.regex
    print "Found regex as " + regex

else:
    regex = "a-zA-Z" 

with open(source_file, 'r') as file:
    txt = file.readlines()

num = 1
deleted_lines = []

output_file_source_name = source_file + "_clean"

output_file_source = open(output_file_source_name,'w',0)

output_file_target_name = target_file + "_clean"

output_file_target = open(output_file_target_name,'w',0)

for line in txt:
    myregex = r'[{}]'.format(regex)
    mymatch = bool(re.findall(myregex,line))
    if mymatch:
        #print "Found latin characters in line " + str(num) + ":" + line
        deleted_lines.append(num)
    else:
        output_file_source.write(line) 
        output_file_source.flush()
    num = num + 1

output_file_source.close()

with open(target_file, 'r') as file:
    txt = file.readlines()

for i, line in enumerate(txt):
    i = i+1
    if i in deleted_lines:
        pass
    else:
        output_file_target.write(line)
        output_file_target.flush()
output_file_target.close()
print "found a total of " + str(len(deleted_lines)) + " mixed lines"
