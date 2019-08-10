# Builds an epub in language specified, called by 

#rm epub/by_$1.epub

sed -i "s/\_xx/\_$1/g" Makefile

cat Makefile

for i in `ls *.md |grep -v en |grep -v ru`; do python scripts/print-lang.py $i $1; done;

make pdf/by_$1.pdf
make epub/by_$1.epub

sed -i 's/_[[:alpha:]][[:alpha:]].md/_xx.md/' Makefile 
sed -i 's/_[[:alpha:]][[:alpha:]].epub/_xx.epub/' Makefile

ebook-viewer by_$1.epub
