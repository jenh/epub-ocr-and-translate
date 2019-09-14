#!/usr/bin/sh

# Quick way to sample individual lines in parallel corpora

# Usage: export srcfile='/path/to/srcfile' tgtfile='/path/to/tgtfile'
#        sh line_compare.sh 500
#        (where 500 is the line number you want to compare)

num=$1p

echo $num

sed -n $num $srcfile && sed -n $num $tgtfile 

