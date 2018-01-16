#!/bin/bash

if [ "$1" != "" ]; then
    input=$1
fi

if [ "$2" != "" ]; then
    output=$2
fi

if [ "$input" == "" ]; then
    echo "Input file?"
    read input;
    
    if [ "$output" == "" ]; then
        echo "Output file (optional)?"
        read output
    fi
fi

if [ "$input" == "" ]; then
    echo "I'm not a magic PDF conjurer. You need to give me an input file."
    exit
fi

if [ "$output" == "" ]; then
    output="$input.compressed.pdf"
fi

gs                                    \
  -q                                  \
  -dNOPAUSE                           \
  -dBATCH                             \
  -dSAFER                             \
  -dPDFA=2                            \
  -dPDFACompatibilityPolicy=1         \
  -dSimulateOverprint=true            \
  -sDEVICE=pdfwrite                   \
  -dCompatibilityLevel=1.3            \
  -dPDFSETTINGS=/screen               \
  -dEmbedAllFonts=true                \
  -dSubsetFonts=true                  \
  -dAutoRotatePages=/None             \
  -dColorImageDownsampleType=/Bicubic \
  -dColorImageResolution=150          \
  -dGrayImageDownsampleType=/Bicubic  \
  -dGrayImageResolution=150           \
  -dMonoImageDownsampleType=/Bicubic  \
  -dMonoImageResolution=150           \
  -sOutputFile="$output"              \
  "$input"
