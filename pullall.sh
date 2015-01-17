#!/bin/bash
failtoenter="0"
for dir in `ls "$PWD"`; do
	if [ -d "$dir" ]; then

		# GIT REPOSITORIES
		if [ -d "$dir/.git" ]; then
			echo "$dir is git repository. pulling..."
			cd $dir
			if [ "$?" != "0" ]; then
				echo "Could not enter $dir repository from $PWD. Check above for errors."
				failtoenter="1"
			else
				failtoenter="0"
			fi
			git pull --no-edit
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

		# MERCURIAL REPOSITORIES
		elif [ -d "$dir/.hg" ]; then
			echo "$dir is mercurial repository. pulling..."
			cd $dir
			if [ "$?" != "0" ]; then
				echo "Could not enter $dir repository from $PWD. Check above for errors."
				failtoenter="1"
			else
				failtoenter="0"
			fi
			hg pull
			hg update
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

		# SUBVERSION REPOSITORIES
		elif [ -d "$dir/.svn" ]; then
			echo "$dir is subversion repository. pulling..."
			cd $dir
			if [ "$?" != "0" ]; then
				echo "Could not enter $dir repository from $PWD. Check above for errors."
				failtoenter="1"
			else
				failtoenter="0"
			fi
			svn update
			if [ "$?" != "0" ]; then
				echo "Update of $dir failed. Check above for errors."
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

	fi
done
exit
