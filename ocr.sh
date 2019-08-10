# ocr.sh: Given a PDF, outputs an OCRed text file. 

# Usage: sh ocr.sh filename.pdf

filename=$1
echo $filename
pages=`pdfinfo $filename |grep Pages |awk -F" " '{print $2}'`
echo $pages
mkdir singles

# Separate
pdfseparate -f 1 -l $pages $filename singles/$filename-%d.pdf

#convert pdf to tif
for i in `ls singles/*`; do echo "converting $i to tiff"; convert -density 300 $i -depth 8 -background white -alpha Off $i.tiff; done;

# ocr each file
for i in `ls singles/*.tiff`; do tesseract -l eng $i $i.out; done;

#recombine file
for i in `ls singles/*.txt |sort -V`; do cat $i >> $filename.txt; done;

# Fix linebreaks
sed -i -e ':a;N;$!ba;s/\(.\)\n/\1 /g' -e 's/\n/\n\n/' $filename.txt

# Remove hyphenation
sed -i 's/\-\ //g' $filename.txt

# Remove page numbers and weird linefeeds
sed -i 's/^[0-9].*\o14//g' $filename.txt
sed -i 's/\o14//g' $filename.txt
