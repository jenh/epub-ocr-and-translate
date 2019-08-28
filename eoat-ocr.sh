#!/bin/bash
# ocr.sh: Given a PDF, outputs an OCRed text file. 

# Usage: sh ocr.sh filename.pdf 3-letter-language-code

if [ ! -f "/usr/bin/$scriptname" ]; then
  eoat_type="local"
  myexec=$0
else
  eoat_type="system"
  myexec="eoat-ocr"
fi

if [ $# -ne 2 ]; then
  printf "\nUsage: $myexec PDF_FILE_NAME THREE_LETTER_SOURCE_LANGUAGE_CODE\n\n"
  exit 3
fi

filename=$1
lang=$2

trunc_file=`echo $filename |awk -F ".pdf$" '{print $1}'`

pages=`pdfinfo $filename |grep Pages |awk -F" " '{print $2}'`
echo "Found $pages pages to process in $filename."
mkdir $trunc_file

# Separate
echo "Separating PDF into individual files."
pdfseparate -f 1 -l $pages $filename $trunc_file/$trunc_file-%d.pdf

#convert pdf to tif
echo "Converting PDF files to Tiffs for OCR"
for i in `ls $trunc_file/*`; do trunc_tiff=`echo $i |awk -F ".pdf$" '{print $1}'`;echo "converting $i to tiff"; convert -density 300 $i -depth 8 -background white -alpha Off $trunc_tiff.tiff; done;

# ocr each file
echo "OCRing with tesseract"
for i in `ls $trunc_file/*.tiff`; do trunc_txt=`echo $i |awk -F ".tiff$" '{print $1}'`;tesseract -l $lang $i $trunc_txt; done;

# remove the tiff files post-OCR 
rm -rf $trunc_file/$trunc_tiff.tiff

#recombine file
echo "Recombining text files to $trunc_file.txt"
for i in `ls $trunc_file/*.txt |sort -V`; do cat $i >> $trunc_file.txt; done;

# Fix linebreaks
echo "Fixing linebreaks in $trunc_file.txt"
sed -i -e ':a;N;$!ba;s/\(.\)\n/\1 /g' -e 's/\n/\n\n/' $trunc_file.txt

# Remove hyphenation
echo "Removing hyphenation from $trunc_file.txt"
sed -i 's/\-\ //g' $trunc_file.txt

# Remove page numbers and weird linefeeds

echo "Removing page numbers and line feeds from $trunc_file.txt"
sed -i 's/^[0-9].*\o14//g' $trunc_file.txt
sed -i 's/\o14//g' $trunc_file.txt

# Change dumbquotes to smartquotes

echo "Changing quotes to smartquotes for translate-shell. Unterminated quotes cause issues with line-by-line translation sent via shell; once translated, you may want to change back"
sed -i -zEe 's/\x27\x27/"/g; s/\x27([^\x27]*)\x27/‘\1’/g; s/"([^"]*)"/“\1”/g; ' $trunc_file.txt
# Find unmatched quotes and backticks
sed -i 's/`/‘/g' $trunc_file.txt
sed -i 's/"/”/g' $trunc_file.txt
echo "OCR process complete. Full OCRed text is available at $trunc_file.txt. Individual PDF, TIFF and text files are located in the $trunc_file/ directory"


