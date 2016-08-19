#!/bin/bash
git diff --stat `git hash-object -t tree /dev/null` | tail -1
exit
