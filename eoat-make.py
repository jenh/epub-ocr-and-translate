#!/usr/bin/env python2.7

import os
import fnmatch
import re

book_path = os.getcwd()

scripts_path = os.path.dirname(os.path.realpath(__file__))

f = open('Makefile','w')

myfiles = fnmatch.filter(os.listdir('.'), '[0-9]*.md')

files = []

for line in myfiles:
    files.append(line)

files = sorted(files)

f.write("view: book_xx_epub popopen\nFILES=\\\n")

"""

  Some notes on pandoc options we're setting here, as
  a lot of it can break if you're on an older version
  of pandoc (or may become obsolete in a future version.
  We're using 2.8 here. Most linux distros
  provide 1.x.

  -f gfm (Github-flavored Markdown) is to keep pandoc 
  from crashing by using all available memory on cloud 
  servers. More investigation should be done to see if 
  there's a better parsing option with more features 
  and still doesn't eat up all the memory. +smart gives
  us emdashes and smartquotes.

  --metadata-file specifies the yaml metadata file. pandoc 
  used your yaml as long as the file was compiled, but 
  this no longer works in 2.8.

  --top-level-division is also needed in 2.8, older 
  versions would interpret # in markdown as a chapter 
  division, but no longer.

"""

for line in files:
    line = line.rsplit(".", 1)[ 0 ] + "_" + "xx.md"
    f.write("\t" + line + "\\\n")
f.write("\npdf/book_xx.pdf: $(FILES)\n\tcat $(FILES) | pandoc --metadata-file=variables.yaml --top-level-division=chapter -f gfm+smart --pdf-engine=xelatex --template=paperback.tex -o book_xx.pdf\n") 
f.write("\nepub/book_xx.epub: $(FILES)\n\tcat $(FILES) | pandoc --metadata-file=variables.yaml --top-level-division=chapter -f gfm+smart --toc --toc-depth=4 --css=epub.css - -o book_xx.epub\npopopen: \n\tebook-viewer book_xx.epub\n")

f.close()

copy_templates = "cp " + scripts_path + "/templates/* " + book_path + "/"
os.popen(copy_templates)

print "\nAdded makefile and templates to current directory.\n\nEdit **variables.yaml** with project-specific metadata values and then run:\n\n   " + scripts_path + "/eoat-extract.sh [2-letter language code]\n   (if running from a directory)\n\nor\n\n   eoat-extract [2-letter language code]\n   (if running from an install)\n\nto build PDF and EPUB files.\n"
