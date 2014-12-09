#!/bin/bash
echo "Directory of Nikon Raw files to convert:"
read dir
echo "Is this correct? (y/n): $dir"
read correct
if [ "$correct" = "y" ]
then
	if [ -d "$dir/jpg" ]; then
		echo "jpg directory already exists, using it"
	else
		mkdir $dir/jpg
	fi
	ufraw-batch --out-type=jpeg --out-path=$dir/jpg $dir/*.NEF
elif [ "$correct" = "n" ]; then
	echo "Exiting."
	exit
else
	echo "Invalid option (must be 'y' or 'n')"
	exit
fi
