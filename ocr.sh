#!/bin/sh
# ocr.sh: Given a PDF, outputs an OCRed text file. 

# Usage: sh ocr.sh filename.pdf 3-letter-language-code

if [ $# -ne 2 ]; then
  echo 1>&2 "Usage: $0 PDF_FILE_NAME THREE_LETTER_SOURCE_LANGUAGE_CODE"
  exit 3
fi

filename=$1
lang=$2

trunc_file=`echo $filename |awk -F ".pdf$" '{print $1}'`

pages=`pdfinfo $filename |grep Pages |awk -F" " '{print $2}'`
echo "Found $pages pages to process in $filename."
mkdir singles

# Separate
echo "Separating PDF into individual files."
pdfseparate -f 1 -l $pages $filename singles/$trunc_file-%d.pdf

#convert pdf to tif
echo "Converting PDF files to Tiffs for OCR"
for i in `ls singles/*`; do trunc_tiff=`echo $i |awk -F ".pdf$" '{print $1}'`;echo "converting $i to tiff"; convert -density 300 $i -depth 8 -background white -alpha Off $trunc_tiff.tiff; done;

# ocr each file
echo "OCRing with tesseract"
for i in `ls singles/*.tiff`; do trunc_txt=`echo $i |awk -F ".tiff$" '{print $1}'`;tesseract -l $lang $i $trunc_txt; done;

#recombine file
echo "Recombining text files to $filename.txt"
for i in `ls singles/*.txt |sort -V`; do cat $i >> $filename.txt; done;

# Fix linebreaks
echo "Fixing linebreaks in $filename.txt"
sed -i -e ':a;N;$!ba;s/\(.\)\n/\1 /g' -e 's/\n/\n\n/' $filename.txt

# Remove hyphenation
echo "Removing hyphenation from $filename.txt"
sed -i 's/\-\ //g' $filename.txt

# Remove page numbers and weird linefeeds

echo "Removing hyphenation and line feeds from $filename.txt"
sed -i 's/^[0-9].*\o14//g' $filename.txt
sed -i 's/\o14//g' $filename.txt

# Change dumbquotes to smartquotes

echo "Changing quotes to smartquotes for translate-shell. Unterminated quotes cause issues with line-by-line translation sent via shell; once you\'re translated, you may want to change back"
sed -i -zEe 's/\x27\x27/"/g; s/\x27([^\x27]*)\x27/‘\1’/g; s/"([^"]*)"/“\1”/g; ' $filename.txt

echo "OCR process complete. Full OCRed text is available at $filename.txt. Individual PDF, TIFF and text files are located in the singles/ directory"


