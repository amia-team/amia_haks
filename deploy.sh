#!/bin/bash
# Check if run as sudo
if [ "$EUID" -ne 0 ]
  then echo "Please run as sudo"
  exit
fi
# set var to user provided directory
dir=$1
# check if directory exists
if [ ! -d "$dir" ]; then
  echo "Directory $dir does not exist"
  exit
fi
# Pack all content
./linux-pack-all.sh
# copy *.hak to dir/hak
cp ./*.hak $dir/hak
# copy *.tlk to dir/tlk
cp ./*.tlk $dir/tlk
# Remove all tlk and hak files from current directory
rm ./*.tlk ./*.hak