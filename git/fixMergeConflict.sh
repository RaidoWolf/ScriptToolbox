#!/bin/bash

if [ "$1" == "" ]; then
    echo "Path to repository to fix?"
    read $path
else
    path="$1"
fi

cd $path
if [ "$?" != "0" ]; then
    echo "Failed to enter given path. Exiting..."
    exit 1
fi

git fetch origin
git reset --hard origin/master
