#!/usr/bin/bash

# Uninstall tools from opt and unlink from /usr/bin

scriptname=`basename "$0"`

if [ $(id -u) -ne 0 ]; then
  echo "Must be root to run $scriptname."
  exit
fi


if [ ! -d "/opt/eoat-tools" ]; then
  echo "/opt/eoat-tools is missing. Try installing with eoat-install.sh, then try again"
  exit
fi

# Uninstall

for i in `ls /opt/eoat-tools/ | grep -E "eoat-"`
  do
    bin_name="${i%%.*}"
    echo "Removing /usr/bin/$bin_name"
    unlink /usr/bin/$bin_name
 done

echo "Removing files from /opt/eoat-tools"
rm -rf /opt/eoat-tools
