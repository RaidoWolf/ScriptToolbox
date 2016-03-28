#!/bin/bash
failtoenter="0"
for dir in `ls "$PWD"`; do
	if [ -d "$dir" ]; then

		# GIT REPOSITORIES
		if [ -d "$dir/.git" ]; then
			echo "$dir is git repository. pruning..."
			cd $dir
			if [ "$?" != "0" ]; then
				echo "Could not enter $dir repository from $PWD. Check above for errors."
				failtoenter="1"
			else
				failtoenter="0"
			fi
			git gc --aggressive --prune=now
			git reflog expire --all --expire=now
			if [ "$?" != "0" ]; then
				echo "Prune of $dir failed. Check above for errors."
			else
				echo "$dir pruned."
			fi
			if [ "$failtoenter" != "1" ]; then
				cd ..
			fi
			if [ "$?" != "0" ]; then
				echo "Could not exit $dir repository. Check above for errors."
				exit
			fi
		fi

	fi
done
exit
