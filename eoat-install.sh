#!/usr/bin/bash

# Install tools into opt 

scriptname=`basename "$0"`

basedir=$(dirname "$0")

if [ "$EUID" -ne 0 ]; then
  echo "Must be root to run $scriptname."
  exit
fi

if [ -d "/opt/eoat-tools" ]; then
  echo "/opt/eoat-tools already exists. Try uninstalling with eoat-uninstall.sh, then try again"
  exit
fi
mkdir /opt/eoat-tools
cp -r $basedir/* /opt/eoat-tools

for i in `ls $basedir |grep -E "*sh|*py"` 
  do
    bin_name="${i%%.*}"
    echo $filename
    echo "Linking /opt/eoat-tools/$i to /usr/local/bin/$bin_name"
    ln -s /opt/eoat-tools/$i /usr/local/bin/$bin_name
    chmod 755 /usr/local/bin/$bin_name
  done

  printf "\neoat-tools installed to /opt/eoat-tools and linked at /usr/local/bin.\n\n"
