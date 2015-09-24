#!/bin/bash

#######CONFIG#######
DONOTRESET="0" #0|1 - this will prevent local changes from getting erased in the event of merge conflicts
####################

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
			git pull --recurse-submodules --no-edit
			return1="$?"
			if [ "$return1" == "0" ]; then
				git submodule update --recursive
				return2="$?"
			else
				git submodule update
				return3="$?"
				git submodule foreach git pull origin master
				return4="$?"
			fi
			if [ "$return1" == "0" -a "$return2" == "0" -o "$return3" == "0" -a "$return4" == "0" ]; then
				fail="0" #no-error
			else
				if [ "$DONOTRESET" == "0" ]; then
					git fetch origin
					return5="$?"
					git reset --hard origin/master
					return6="$?"
					if [ "$return5" == "0" && "$return6" == "0" ]; then
						fail="0"
					else
						fail="1" #error
					fi
				else
					fail="0"
				fi
			fi
			if [ "$fail" != "0" ]; then
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
			return1="$?"
			hg update
			return2="$?"
			if [ "$return1" == "0" && "$return2" == "0" ]; then
				fail="0" #no-error
			else
				fail="1" #error
			fi
			if [ "$fail" != "0" ]; then
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
			return1="$?"
			if [ "$return1" == "0" ]; then
				fail="0" #no-error
			else
				fail="1" #error
			fi
			if [ "$fail" != "0" ]; then
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
