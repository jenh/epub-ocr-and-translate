# Builds an epub in language specified, called by 

#rm epub/book_$1.epub

if [ $# -eq 0 ]
  then
    echo "No arguments supplied, assuming no multi-language support, using all .md files in current directory. If this is not your intention, CTRL-C and rerun using 'sh extract.sh en' where en is the two-letter language you want to run."
  sleep 3;
  sed -i 's/_xx.md/.md/g' Makefile
  cat Makefile
  make pdf/book_xx.pdf
  make epub/book_xx.epub
  #ebook-viewer book_xx.epub
  sed -i 's/\.md/_xx.md/g' Makefile
else 
  sed -i "s/\_xx/\_$1/g" Makefile
  cat Makefile
  for i in `ls *.md |grep -v _[[:alpha:]][[:alpha:]].md`; do python scripts/print-lang.py $i $1; done;
  make pdf/book_$1.pdf
  make epub/book_$1.epub
  #ebook-viewer book_$1.epub
  sed -i 's/_[[:alpha:]][[:alpha:]]/_xx/' Makefile
fi

sed -i 's/_[[:alpha:]][[:alpha:]].md/_xx.md/' Makefile 
sed -i 's/_[[:alpha:]][[:alpha:]].epub/_xx.epub/' Makefile
sed -i 's/_[[:alpha:]][[:alpha:]].pdf/_xx.pdf/' Makefile
sed -i 's/_[[:alpha:]][[:alpha:]].tex/_xx.tex/' Makefile

#ebook-viewer book_$1.epub
