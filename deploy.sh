#!/bin/bash
# set var to user provided directory
dir=$1
# check if directory exists
if [ ! -d "$dir" ]; then
  echo "Directory $dir does not exist"
  exit 1
fi
# copy *.hak to dir/hak
cp ./*.hak "$dir/hak"
# copy *.tlk to dir/tlk
cp ./*.tlk "$dir/tlk"