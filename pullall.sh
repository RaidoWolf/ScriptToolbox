#!/bin/bash
failtoenter="0"
for dir in `ls "$PWD"`; do
	if [ -d "$dir" ]; then
		cd $dir
		if [ "$?" != "0" ]; then
			echo "Could not enter $dir repository from $PWD. Check above for errors."
			failtoenter="1"
		else
			failtoenter="0"
		fi
		git pull
		if [ "$?" != "0" ]; then
			echo "Pull of $dir failed. Check above for errors."
		else
			echo "$dir updated."
		fi
		if [ "$failtoenter" != "1" ]; then
			cd ..
		fi
		if [ "$?" != "0" ]; then
			echo "Could not exit $dir repository. Check above for errors."
			exit
		fi
	fi
done
exit
