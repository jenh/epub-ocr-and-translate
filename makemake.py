import os
import fnmatch
import re

f = open('Makefile','w')

myfiles = fnmatch.filter(os.listdir('.'), '[0-9]*.md')


files = []

for line in myfiles:
    pattern = re.compile(r'\_[a-z][a-z]')
    if pattern.findall(line): 
        pass
    else: 
        files.append(line)

files = sorted(files)

f.write("view: book_xx_epub popopen\nFILES=\\\n")

for line in files:
    line = line.rsplit(".", 1)[ 0 ] + "_" + "xx.md"
    f.write("\t" + line + "\\\n")
f.write("\npdf/book_xx.pdf: $(FILES)\n\tcat variables.yaml titlepages.md $(FILES) | pandoc --latex-engine=xelatex --template=kindlebook.tex -o book_xx.pdf\n") 
f.write("\nepub/book_xx.epub: $(FILES)\n\tcat variables.yaml titlepages.md $(FILES) | pandoc  --toc --toc-depth=4 --epub-stylesheet=epub.css - -o book_xx.epub\npopopen: \n\tebook-viewer book_xx.epub\n")

f.close()

os.popen('cp templates/* .') 
