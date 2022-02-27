
# Builds an epub and PDF in language specified from source md files that contain multiple languages

#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
scriptname=`basename "$0"`

if [ ! -f "/usr/bin/$scriptname" ]; then
  eoat_type="local"
  printf "\nFound local directory as $BASEDIR\n"
else
  printf "\nFound system installation\n"
  eoat_type="system"
fi

if [ $# -eq 0 ]
  then
    echo "No arguments supplied, assuming no multi-language support, using all .md files in current directory. If this is not your intention, CTRL-C and rerun using 'sh eoat-build en' where en is the two-letter language you want to run."
  sleep 3;
  sed -i 's/_xx.md/.md/g' Makefile
  cat Makefile
  make pdf/book_xx.pdf
  make epub/book_xx.epub
  #ebook-viewer book_xx.epub
  sed -i 's/\.md/_xx.md/g' Makefile
else
  if [ "$eoat_type" = local ]; then	
    lang=`python $BASEDIR/eoat-expandlang.py -l $1`
  else  
    lang=`eoat-expandlang -l $1`
  fi
  if [ "$lang" = None ]
  then
      echo "Could not determine language. Try again with a two-letter language code or run without one to use all files."
  else
      echo "Preparing to build for $lang"
      sed -i "s/\[english\]/\[$lang\]/g" paperback.tex
      if [ "$lang" != english ]
      then
       sed -i 's@\\usepackage{bookman}@%\\usepackage{bookman}@g' paperback.tex 
      fi  
      sed -i "s/\_xx/\_$1/g" Makefile
      cat Makefile
      for i in `ls *.md |grep -v _[[:alpha:]][[:alpha:]].md`; do 
        if [ "$eoat_type" = local ]; then 
          python $BASEDIR/eoat-printlang.py $i $1; 
	else
	  eoat-printlang $i $1;
	fi
      done
      sed -i 's/_xx.tex/_$1.tex/g' Makefile
      make pdf/book_$1.pdf
      make epub/book_$1.epub
      #ebook-viewer book_$1.epub
      sed -i 's/_[[:alpha:]][[:alpha:]]/_xx/' Makefile
      sed -i "s/\[$lang\]/\[english\]/g" paperback.tex
      sed -i 's@%\\usepackage{bookman}@\\usepackage{bookman}@g' paperback.tex
 fi
fi

sed -i 's/_[[:alpha:]][[:alpha:]].md/_xx.md/g' Makefile 
sed -i 's/_[[:alpha:]][[:alpha:]].epub/_xx.epub/g' Makefile
sed -i 's/_[[:alpha:]][[:alpha:]].pdf/_xx.pdf/g' Makefile
sed -i 's/_[[:alpha:]][[:alpha:]].tex/_xx.tex/g' Makefile

#ebook-viewer book_$1.epub
