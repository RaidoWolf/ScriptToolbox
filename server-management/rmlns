#!/bin/bash

if ["$1" != ""]; then
    wd="$1"
else
    echo "Remove symlinks from where?"
    read wd
fi

find "$wd" -maxdepth 1 -type l -exec rm -f {} \;

exit
