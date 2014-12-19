#!/bin/bash

dir="$1"
if [ "$dir" == "" ]; then
	echo "Directory of FLAC album to convert?"
	read dir
	if [ "$dir" == "" ]; then
		dir="$PWD"
	fi
fi

cd "$dir"
if [ "$?" != "0" ]; then
	echo "Unable to enter directory. Exiting."
	exit
fi
if [ -d "ogg" ]; then
	echo "ogg directory exists. Using it."
	cd "ogg";
	if [ "$?" != "0" ]; then
		echo "Unable to enter ogg directory. Exiting."
		exit
	fi
elif [ ! -e "ogg" ]; then
	echo "Creating ogg directory."
	mkdir ogg
	if [ "$?" != "0" ]; then
		echo "Unable to create ogg directory. Exiting"
		exit
	else
		echo "Ogg directory created."
	fi
else
	echo "ogg exists in directory. Please remove/relocate it. Exiting."
	exit
fi

oggenc -q 7 *.flac
if [ "$?" != "0" ]; then
	echo "oggenc failed. exiting."
	exit
fi
mv *.ogg ogg/
if [ "$?" != "0" ]; then
	echo "unable to move ogg files into ogg directory. exiting."
	exit
fi
cp *.jpg ogg/
cp *.png ogg/

exit

