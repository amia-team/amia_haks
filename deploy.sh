#!/bin/bash
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
sudo cp ./*.hak $dir/hak
# copy *.tlk to dir/tlk
sudo cp ./*.tlk $dir/tlk
# Remove all tlk and hak files from current directory
sudo rm ./*.tlk ./*.hak