#!/bin/bash

# run gitk, displaying all existing branches
for b in "`git branch`"; do echo "$b"; done | tr -d "*" | xargs gitk
