#!/bin/bash
echo "MAKE SURE YOU KNOW WHAT YOU'RE DOING! THIS SCRIPT CHANGES PERMISSIONS AND CAN BREAK THINGS!"
if [ "$1" != "" ]; then
   	dir="$1"
else
   	echo "directory for which to change permissions:"
        read dir
fi
echo "is this correct: (y/n)"
echo "$dir";
   	read correct
   	if [ "$correct" == "y" ]; then
        echo "chmod permissions for folders (eg 755):"
            read permdir
        echo "chmod permissions for files (eg 644):"
            read permfile
        echo "changing directory permissions..."
            find $dir -type d -print0 | xargs -0 chmod $permdir
        echo "changing file permissions..."
            find $dir -type f -print0 | xargs -0 chmod $permfile
   	elif [ "$correct" == "n" ]; then
        echo "Exiting..."
        exit
   	else
        echo "Invalid option (must be "y" or "n"). Exiting."
        exit
   	fi
exit
