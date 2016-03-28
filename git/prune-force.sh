#!/bin/bash
if [ "$1" != "" ]; then
	dir="$1"
else
	echo "Path to repository to prune:"
	read dir
fi
if [ -d "$dir" ]; then

	# GIT REPOSITORIES
	if [ -d "$dir/.git" ]; then
		echo "$dir is git repository. pruning..."
		cd $dir
		if [ "$?" != "0" ]; then
			echo "Failed to enter directory."
			failtoenter="1"
		fi
		git gc
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
exit
