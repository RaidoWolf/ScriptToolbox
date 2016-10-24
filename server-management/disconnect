#!/bin/bash

if ["$1" != ""]; then
    tty="$1"
else
    echo "Which TTY do you want to disconnect?"
    read tty
fi

pkill -9 -t pts/"$tty"

exit
