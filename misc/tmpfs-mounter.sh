#!/bin/bash
user="$(whoami)"
if [ "$user" != "root" ]; then
	echo "THIS SCRIPT MUST BE RUN AS ROOT!"
	exit
fi
echo "Where should the new tmpfs be mounted?"
	read mountpoint
echo "Size in MB?"
	read size
if [ "$mountpoint" == "" ]; then
	mountpoint="/mnt/tmpfs"
fi
if [ "$size" == "" ]; then
	size="256"
fi
if [ -f "$mountpoint" ]; then
	mpsize=$(stat -c%s "$mountpoint")
	if [ "$mpsize" > "0" ]; then
		echo "Mountpoint exists, not empty. Exiting."
		exit
	else
		rm -f "$mountpoint"
		if [ "$?" != "0" ]; then
			echo "Unable to remove existing mountpoint file. Exiting."
			exit
		fi
		mkdir "$mountpoint"
		if [ "$?" != "0" ]; then
			echo "Unable to create directory at mountpoint."
			exit
		fi
		mount -t tmpfs -o size="$size"m tmpfs "$mountpoint"
		if [ "$?" != "0" ]; then
			echo "Unable to mount tmpfs. Check above for errors."
			exit
		fi
		echo "Mounted $size MB on $mountpoint"
		exit
	fi
elif [ -d "$mountpoint" ]; then
	if [ "$(ls $mountpoint)" == "" ]; then
		mount -t tmpfs -o size="$size"m tmpfs "$mountpoint"
		if [ "$?" != "0" ]; then
			echo "Unable to mount tmpfs. Check above for errors."
			exit
		fi
		echo "Mounted $size MB on $mountpoint"
		exit
	else
		echo "Mountpoint exists, not empty. Exiting."
		exit
	fi
elif [ ! -e "$mountpoint" ]; then
	mkdir "$mountpoint"
	if [ "$?" != "0" ]; then
		echo "Unable to create directory at mountpoint."
		exit
	fi
	mount -t tmpfs -o size="$size"m tmpfs "$mountpoint"
	if [ "$?" != "0" ]; then
		echo "Unable to mount tmpfs. Check above for errors."
		exit
	fi
	echo "Mounted $size MB on $mountpoint"
	exit
else
	echo "Mountpoint exists, not file/dir. Exiting."
	exit
fi
exit

