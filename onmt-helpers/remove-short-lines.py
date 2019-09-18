#!/usr/bin/env python
# -*- coding: utf-8 -*
from __future__ import print_function
import re
import sys
import string
import argparse

parser = argparse.ArgumentParser(description='remove-short-lines: Delete short lines') 
parser.add_argument('-s','--source', help='Source file that contains training data that needs scrubbing', required=True)
parser.add_argument('-t','--target',help='Target file that needs the corresponding lines removed', required=True)
parser.add_argument('-l','--length',help='Minimum number of words per sentence',required=False)
args = parser.parse_args()

if (args.source):
    source_file = args.source
    print('Found source file as ' + source_file)
else:
    exit

if (args.target):
    target_file = args.target
    print('Found target as ' + target_file)
else:
    exit

if (args.length):
    length = int(args.length)
else:
   print("No sentence length") 

num = 1
match_lines = {}

output_file_source_name = source_file + '_long'

output_file_source = open(output_file_source_name,'w')

output_file_target_name = target_file + '_long'

output_file_target = open(output_file_target_name,'w')

with open(source_file, 'r') as file:
    for line in file:
#       line = line.replace('\n\n','\n').replace('\n\n','\n')
       translate_table = dict((ord(char), " ") for char in string.punctuation)
       line = line.translate(translate_table)
       line = re.sub(' +', ' ', line)
       words = line.split()
       word_count = len(words)
       if word_count > length:
           match_lines[num] = 1
           output_file_source.write(line)
#           output_file_source.write("\n")
       else:
           pass
       num = num+1

output_file_source.close()

with open(target_file, 'r') as file:
    for i, line in enumerate(file):
        i = i+1
        if i in match_lines:
            output_file_target.write(line)
        else:
            pass
        #    output_file_target.flush()

output_file_target.close()
print('Found a total of ' + str(len(match_lines)) + ' matched lines')
