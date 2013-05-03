#!/bin/sh
# $Id: prejob.sh 9640 2005-12-17 03:20:21Z minh $

STARTTIME=`date +"%F %T"`

for dir in *.BQ
do
	cd $dir
	#	
	cd ..
done

echo ----------------------------------------
echo "Start running: $STARTTIME"
echo "Stop  running: `date +"%F %T"`"
echo ----------------------------------------
