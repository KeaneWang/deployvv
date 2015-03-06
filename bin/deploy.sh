#!/bin/sh

#get current dir
path=$(dirname $0)
#exec custom sh
files=`ls "$path"/../custom/*`

for file in $files
do
	$file
done

#start update listen server
python "$path"/updateserver.py
