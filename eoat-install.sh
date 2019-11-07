#!/usr/bin/bash

# Install tools into opt 

scriptname=`basename "$0"`

basedir=$(dirname "$0")


if [ $(id -u) -ne 0 ]; then
  echo "Must be root to run $scriptname."
  exit
fi

if [ -d "/opt/eoat-tools" ]; then
  echo "/opt/eoat-tools already exists. Try uninstalling with eoat-uninstall.sh, then try again"
  exit
fi
mkdir /opt/eoat-tools
cp -r $basedir/eoat-* /opt/eoat-tools/
cp -r $basedir/onmt-helpers/eoat-* /opt/eoat-tools/
cp -r $basedir/templates /opt/eoat-tools/templates/

for i in `ls -R /opt/eoat-tools/ |grep -E "eoat-*" |grep -v :` 
  do
    bin_name="${i%%.*}"
    echo $filename
    echo "Linking /opt/eoat-tools/$i to /usr/bin/$bin_name"
    ln -s /opt/eoat-tools/$i /usr/bin/$bin_name
    chmod 755 /usr/bin/$bin_name
  done

  printf "\neoat-tools installed to /opt/eoat-tools and linked at /usr/bin.\n\n"
