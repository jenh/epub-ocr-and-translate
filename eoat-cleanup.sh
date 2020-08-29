#!/usr/bin/env bash

# Runs cleanup options from ocr.sh for one-off operations

if [ $# -ne 1 ]; then
  echo 1>&2 "Usage: $0 FILE_TO_CLEAN"
  exit 3
fi

filename=$1

# Fix linebreaks
echo "Fixing linebreaks in $filename"
sed -i -e ':a;N;$!ba;s/\(.\)\n/\1 /g' -e 's/\n/\n\n/' $filename

# Remove hyphenation
echo "Removing hyphenation from $filename"
sed -i 's/\-\ //g' $filename

# Remove page numbers and weird linefeeds

echo "Removing page numbers and line feeds from $filename"
sed -i 's/^[0-9].*\o14//g' $filename
sed -i 's/\o14//g' $filename

# Change dumbquotes to smartquotes

echo "Changing quotes to smartquotes for translate-shell. Unterminated quotes cause issues with line-by-line translation sent via shell; once translated, you may want to change back"
sed -i -zEe 's/\x27\x27/"/g; s/\x27([^\x27]*)\x27/‘\1’/g; s/"([^"]*)"/“\1”/g; ' $filename
# Find unmatched quotes and backticks
sed -i 's/`/‘/g' $filename
sed -i 's/"/”/g' $filename

