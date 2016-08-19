#!/bin/bash

git filter-branch --env-filter '

echo "Git repository directory?"
	read dirRepo
echo "Old email address?"
	read emailOld
echo "Correct Name?"
	read name
echo "Correct email address?"
	read emailNew

cd $dirRepo

if [ "$GIT_COMMITTER_EMAIL" = "$emailOld" ]
then
	export GIT_COMMITTER_NAME = "$name"
	export GIT_COMMITTER_EMAIL = "$emailNew"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$emailOld" ]
then
	export GIT_AUTHOR_NAME = "$name"
	export GIT_AUTHOR_EMAIL = "$emailNew"
fi
' --tag-name-filter cat -- --branches --tags
