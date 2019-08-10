import os
import fnmatch

f = open('Makefile','w')

myfiles = fnmatch.filter(os.listdir('.'), '*.md')

files = []

for line in myfiles:
    files.append(line)

files = sorted(files)

f.write("view: by_xx_epub popopen\nBY_FILES=\\\n")

for line in files:
    line = line.rsplit(".", 1)[ 0 ] + "_" + "xx.md"
    f.write("\t" + line + "\\\n")
f.write("\npdf/by_xx.pdf: $(BY_FILES)\n\tcat $(BY_FILES) | pandoc --latex-engine=xelatex -o by_xx.pdf\n") 
f.write("\nepub/by_xx.epub: $(BY_FILES)\n\tcat $(BY_FILES) | pandoc  --toc --toc-depth=4 - -o by_xx.epub\npopopen: \n\tebook-viewer by_xx.epub\n")

f.close()
