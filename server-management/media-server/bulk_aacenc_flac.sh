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
if [ -d "aac" ]; then
	echo "aac directory exists. Using it."
	cd "aac";
	if [ "$?" != "0" ]; then
		echo "Unable to enter aac directory. Exiting."
		exit
	fi
elif [ ! -e "aac" ]; then
	echo "Creating aac directory."
	mkdir aac
	if [ "$?" != "0" ]; then
		echo "Unable to create aac directory. Exiting"
		exit
	else
		echo "Aac directory created."
	fi
else
	echo "aac exists in directory. Please remove/relocate it. Exiting."
	exit
fi

for i in *.flac; do
	ffmpeg -i "$i" -c:a aac -b:a 320k "aac/${i/%.flac/.aac}"
	if [ "$?" != "0" ]; then
		echo "Failed to transcode \"$i\"."
	fi
done

cp *.jpg aac/
cp *.png aac/

exit
