#!/bin/bash
# set var to user provided directory
dir=$1
# check if directory exists
if [ ! -d "$dir" ]; then
  echo "Directory $dir does not exist"
  exit
fi
# copy *.hak to dir/hak
sudo cp ./*.hak $dir/hak
# copy *.tlk to dir/tlk
sudo cp ./*.tlk $dir/tlk