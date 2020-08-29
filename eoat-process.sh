#!/usr/bin/env bash
# Usage is process.sh [engine] [infile] [outfile]

ENGINE=$1
SOURCE=$2
OUTPUT=$3

while read -r line; do
	echo "$line\n" >> $OUTPUT
	trans -b -e $ENGINE -s ru -t en "$line" >> $OUTPUT
	echo "\n" >> $OUTPUT
        sleep 5
done < $SOURCE 
