#!/bin/bash

if [[ "$1" != "" ]]; then
    INPUT_FILE=$1
else
    echo "Input path?"
    read INPUT_FILE
fi

if [[ "$2" != "" ]]; then
    OUTPUT_FILE=$2
else
    echo "Output path?"
    read OUTPUT_FILE
fi

if [[ "$3" != "" ]]; then
    FRAMERATE=$3
else
    echo "Output framerate?"
    read FRAMERATE
fi

if [[ "$4" != "" ]]; then
    CODEC=$4
else
    echo "Output codec?"
    read CODEC
fi

if [[ "$5" != "" ]]; then
    RATIO=$5
else
    echo "Slowdown ratio?"
    read RATIO
fi

ffmpeg -i "$INPUT_FILE" -vcodec "$CODEC" -an -vf "fps=$FRAMERATE, setpts=(1/$RATIO)*PTS" "$OUTPUT_FILE"

exit
