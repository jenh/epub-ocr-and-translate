#!/usr/bin/env python
# -*- coding: utf-8 -*
import re
import sys

file = sys.argv[1]
delimiter = sys.argv[2]

with open(file, 'r') as file:
    txt = file.read()

num = 0
output = re.split(delimiter, txt)

for line in output:
    chap = open(str(num).zfill(3) + ".md",'w')
    chap.write(delimiter + line + "\n")
    chap.close()
    num = num + 1
    print num 
 
