#!/bin/bash

if [ "$1" != "" ]; then
    OUTPUT="$1"
else
    echo "Output file?"
    read OUTPUT
fi

sudo adb logcat | tee /dev/tty | gzip --stdout > $OUTPUT

exit
