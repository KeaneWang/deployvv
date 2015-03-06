#!/bin/sh

chmod +x /opt/deployvv/bin/*
chmod +x /opt/deployvv/custom/*
#get current dir
path=$(dirname $0)
#exec custom sh
files=`ls "$path"/custom/*`

for file in $files
do
	$file
done


