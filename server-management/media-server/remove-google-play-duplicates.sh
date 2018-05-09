#!/bin/bash
find . -type f -regextype posix-extended -regex ".*\([1-9]\)\.mp3$" -print0 | xargs -0 rm
