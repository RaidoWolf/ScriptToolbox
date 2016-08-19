#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# listvacuum.py
#
# This script is meant to perform cleanup operations on lists, such as email
# lists. These cleanup operations include:
#  - Removing Duplicates
#  - Removing Bad Addresses
#  - Removing Blank Lines
#  - Removing Blacklist Matches
#  - Randomize List Order
#  - Split List into Even Parts
#
# Note that this program is currently only designed to handle single column
# lists. It can handle multi column lists, but keep in mind that things such as
# blacklist files will have to have the same columns in the same order with the
# same data to work correctly. There is, however, one feature that WILL NOT work
# with multi column lists, and that is the bad email remover. Since it matches
# the whole row as a string with strict regex, a multi column list will either
# throw an exception, or possibly output an empty list.
#
# Also note that this is not designed to handle column headers. Remove these
# from your lists before processing them with this file.
#
# This script is designed to work with Python 2.7, not because I am one of those
# people holding back progress with my fear of change, but rather because OSX
# still ships with Python 2.7 only for some reason. Nonetheless, I've taken care
# to ensure that this script will also run correctly on Python 3, so if you've
# got it, then use it. You can also change 'python' on line 1 to 'python3'.
#
# License: Public Domain (but credit would still be appreciated if you use it)
# Author:  Alex Barber

## -- IMPORTS -- ##
from __future__ import print_function, division #When will everyone come to their senses and start using Python 3?
import csv
import io
import itertools
import math
import random
import re
import sys
import time

tStart = time.time()

## -- ERROR PRINTING FUNCTION -- ##
def error(*msg):
    print(*msg, file=sys.stderr)

## -- VERBOSE PRINTING FUNCTION -- ##
def verbose(*msg):
    if outputToFile:
        print(*msg, file=sys.stdout)

## -- COLUMN ISOLATION FUNCTION -- ##
def column(matrix, index):
    if type(index) in [int, float, str]:
        index = int(index)
        return [(row[index] if len(row) > index else None) for row in matrix]

    elif type(index) == list:
        return [[row[i] for i in index] for row in matrix]
    else:
        error('ERROR: column() index argument must be number or list of numbers.')

## -- LIST LOWERCASING FUNCTION -- ##
def lowerForeach(matrix):
    tmp = []
    for row in matrix:
        if type(row) in [list, tuple]:
            tmp.append(lowerForeach(row))
        elif type(row) == str:
            tmp.append(row.lower())
        else:
            tmp.append(row)
    return tmp


#//TODO: When 0 or 1 arguments given, and no help flag, or if GUI flag is called, open a Python Tk GUI

## -- ARGUMENT COUNT VALIDATION -- ##
if len(sys.argv) < 3 and '--help' not in sys.argv and '-h' not in sys.argv: #if given fewer than 2 arguments...
    #three because, in case you don't know python, sys.argv[0] is the script name
    error('ERROR: Minimum of two arguments (first is filename, second is option(s)).')
    sys.exit()

## -- ARGUMENT VARIABLES -- ##
scriptName = sys.argv[0]
listFileName = sys.argv[1]
options = sys.argv[1:]

## -- OPERATIONAL FLAGS -- ##
actionCaseInsensitive       = False # treat all data as case insensitve
actionRandomizeList         = False # randomize the order of the list
actionRemoveBadEmails       = False # remove bad email addresses in the list
actionRemoveBlankLines      = False # remove blank lines in the list
actionRemoveBlacklist       = False # remove items that match a given blacklist
actionRemoveDuplicates      = False # remove duplicate items from the list
actionSplitList             = False # split list into evenly-sized parts
actionStripWhitespace       = False # strip whitespace from beginning and end of list items
outputToFile                = False # print the output to file instead of stdout

## -- OPERATIONAL VARIABLES -- ##
blacklistFileName           = ''    # filename for blacklist file
columnMainData              = 0     # column index of main data
columnBlacklist             = 0     # column index of blacklist data
outputFileName              = ''    # filename for output file(s)
splitCount                  = 1     # number of lists to split into

## -- STATISTICS VARIABLES -- ##
duplicatesRemoved           = 0     # number of duplicates removed
badEmailsRemoved            = 0     # number of bad emails removed
badEmailsFixed              = 0     # number of bad emails that were fixed
blacklistRemoved            = 0     # number of blacklist matches removed
blankLinesRemoved           = 0     # number of blank lines removed from the list
linesStripped               = 0     # number of lines that were stripped of whitespace

## -- COMMAND LINE FLAGS/OPTIONS PARSER -- ##
skipNext = False
for index, option in enumerate(options):
    if skipNext:
        skipNext = False
        continue
    optionLower = option.lower()
    # help flags
    if (optionLower == '--help') or (option == '-h'):
        print('Usage: ', scriptName, ' <input-csv-file-name> [options]')
        print('    [ --bad-emails | -e  ]        : remove items from the input list that are not valid email addresses')
        print('    [ --bcolumn    | -bc ] <n>    : when handling blacklist data, match against column n')
        print('    [ --blacklist  | -bl ] <file> : remove items from the input list that match items in the blacklist csv file')
        print('    [ --blanks     | -b  ]        : remove blank lines from the input list')
        print('    [ --column     | -c  ] <n>    : when handling data in list, use column n')
        print('    [ --duplicates | -d  ]        : remove duplicates from the input list')
        print('    [ --ignorecase | -i  ]        : treat data case-insensitively (usually more strict)')
        print('    [ --out        | -o  ] <file> : write the final list to a given file instead of stdout (also enables verbose info)')
        print('    [ --randomize  | -r  ]        : randomize items in the input list')
        print('    [ --split      | -s  ] <n>    : split the input list into a given number of subset lists')
        print('    [ --strip      | -w  ]        : strip whitespace from beginning and end of each list item')
        sys.exit()
    # remove-bad-emails flags
    elif (optionLower == '--bad-emails') or (option == '-e'):
        actionRemoveBadEmails = True
    # blacklist column flags
    elif (optionLower == '--bcolumn') or (option == '-bc'):
        columnBlacklist = int(options[index + 1]) #next option must be the index
        skipNext = True #therefore, next option cannot be a flag
    # blacklist flags
    elif (optionLower == '--blacklist') or (option == '-bl'):
        actionRemoveBlacklist = True
        blacklistFileName = str(options[index + 1]) #next option must be the file name
        skipNext = True #therefore, next option cannot be a flag
    # remove-blank-lines flags
    elif (optionLower == '--blanks') or (option == '-b'):
        actionRemoveBlankLines = True
    elif (optionLower == '--column') or (option == '-c'):
        columnMainData = int(options[index + 1]) #next option must be the index
        skipNext = True #therefore, next option cannot be a flag
    # remove-duplicates flags
    elif (optionLower == '--duplicates') or (option == '-d'):
        actionRemoveDuplicates = True
    # case insensitivity flags
    elif (optionLower == '--ignorecase') or (option == '-i'):
        actionCaseInsensitive = True
    # file output flags
    elif (optionLower == '--out') or (option == '-o'):
        outputToFile = True
        outputFileName = str(options[index + 1]) #next option must be the output file name
        skipNext = True
    # randomize flags
    elif (optionLower == '--randomize') or (option == '-r'):
        actionRandomizeList = True
    # split flags
    elif (optionLower == '--split') or (option == '-s'):
        actionSplitList = True
        splitCount = int(options[index + 1]) #next option must be the number of lists
        skipNext = True #thereofre, next option cannot be a flag
    elif (optionLower == '--strip') or (option == '-w'):
        actionStripWhitespace = True
    else:
        if not index == 0: #we can ignore argument #1 because it's supposed to be an arbitrary file name
            #but anything else should be caught
            #(other file names caught by skipNext if syntax is correct)
            error('ERROR: Unrecognized option "', option ,'".')
            sys.exit()

## -- INPUT FILE LOADER -- ##
try:
    listFile = open(listFileName, 'rU')
except IOError:
    error('ERROR: List file does not exist.')
    sys.exit()
listData = csv.reader(listFile)#, dialect=csv.excel_tab)

## -- WHITESPACE STRIPPER -- ##
if actionStripWhitespace:
    verbose('Stripping whitespace...')
    tmp = [] #create new temporary list
    for row in listData:
        if len(row) > columnMainData:
            if type(row[columnMainData]) == str:
                newRow = row
                newVal = row[columnMainData].strip()
                newRow[columnMainData] = newVal
                tmp.append(newRow)
                if newVal != row[columnMainData]:
                    linesStripped += 1
            else:
                tmp.append(row)
        else:
            tmp.append(row)
    listData = tmp

## -- DUPLICATE REMOVER -- ##
if actionRemoveDuplicates:
    verbose('Removing duplicates...')
    tmp = [] #create new temporary list
    for row in listData: #iterate over each item in the list
        if actionCaseInsensitive: #case insensitive
            if len(row) > columnMainData:
                if row[columnMainData].lower not in lowerForeach(column(tmp, columnMainData)): #if item has not already been included...
                    tmp.append(row) #add it
                else:
                    duplicatesRemoved += 1 #add to statistics
            else:
                tmp.append(row)
        else: #not case insensitive
            if len(row) > columnMainData:
                if row[columnMainData] not in column(tmp, columnMainData): #if item has not already been included...
                    tmp.append(row) #add it
                else:
                    duplicatesRemoved += 1 #add to statistics
            else:
                tmp.append(row)

    listData = tmp #write out the new list

## -- BAD EMAIL REMOVER -- ##
if actionRemoveBadEmails:
    verbose('Removing bad emails...')
    emailRegex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    tmp = [] #create new temporary list
    for item in listData: #iterate over each item in the list
        if type(item) in [list, tuple]:
            if len(item) > 0:
                against = item[0]
            else:
                against = None
        else:
            against = item

        if emailRegex.match(str(against)) or against == None: #if email matches regex above (or is empty)...
            tmp.append(item) #add it
        else:
            badEmailsRemoved += 1 #add to statistics
    listData = tmp #write out the new list

## -- BLANK LINE REMOVER -- ##
if actionRemoveBlankLines:
    verbose('Removing blank lines...')
    tmp = []
    for item in listData:
        if item not in [[], [''], '']:
            tmp.append(item)
        else:
            empty = True
            for element in item:
                if element not in [[], [''], '']:
                    empty = False
                    break
            if not empty:
                tmp.append(item)
            else:
                blankLinesRemoved += 1
    listData = tmp

## -- BLACKLIST MATCH REMOVER -- ##
if actionRemoveBlacklist:
    verbose('Removing blacklist matches...')
    try:
        blacklistFile = open(blacklistFileName, 'rU')
    except IOError:
        error('ERROR: Blacklist file does not exist.')
        sys.exit()
    blacklistReader = csv.reader(blacklistFile)#, dialect=csv.excel_tab)
    tmp = []
    for row in blacklistReader:
        tmp.append(row)
    i = 0
    blacklist = []
    for row in tmp:
        if len(row) > columnBlacklist:
            blacklist.append(row[columnBlacklist].lower())
        i += 1
    tmp = [] #create new temporary list
    i = 0
    for row in listData: #iterate over each item in the list
        if row[columnMainData].lower() not in blacklist:
            tmp.append(row)
        else:
            blacklistRemoved += 1
        i += 1
    listData = tmp #write out the new list

## -- LIST RANDOMIZER -- ##
if actionRandomizeList:
    verbose('Randomizing list...')
    random.shuffle(listData)

## -- LIST SPLITTER -- ##
if actionSplitList:
    verbose('Splitting list...')
    listLength = len(listData)

    #error handling
    if type(splitCount) != int or splitCount < 1:
        error('ERROR: Split count argument must be a positive integer.')
        sys.exit()
    if splitCount > listLength:
        error('ERROR: Split count argument must be less than the length of the list.')
        sys.exit()

    listAvgLength = listLength / splitCount
    listRanges = []
    lists = []
    splitModulo = listLength % splitCount

    #create list of lower and upper bounds of each list
    i = 0
    while i < splitCount:
        if i < splitModulo:
            listLength = int(math.ceil(listAvgLength))
        else:
            listLength = int(math.floor(listAvgLength))
        if i > 0:
            lowerBound = int(listRanges[i - 1][1])
        else:
            lowerBound = int(0)
        upperBound = int(lowerBound + listLength)
        listRanges.append([lowerBound, upperBound])
        i += 1

    #iterate over list ranges and actually create the lists
    for index, listRange in enumerate(listRanges):
        index = int(index)
        lists.append([])
        lists[index].extend(listData[listRange[0]:listRange[1]])

## -- OUTPUT HANDLER -- ##
if outputToFile:
    if actionSplitList:
        splitFileName = outputFileName.rsplit('.', 1)
        outputFiles = []
        for index, thisList in enumerate(lists):
            thisFile = open(splitFileName[0] + str(index) + '.' + splitFileName[1], 'w')
            writer = csv.writer(thisFile)
            for item in thisList:
                writer.writerow(item)
            thisFile.close()
    else:
        outputFile = open(outputFileName, 'w')
        writer = csv.writer(outputFile)
        for item in listData:
            writer.writerow(item)
        outputFile.close()
else:
    outputFile = io.BytesIO() #fake file that's actually almost a string so CSV functions will work
    writer = csv.writer(outputFile)
    if actionSplitList:
        emptyLine = []
        for index, thisList in enumerate(lists):
            if index != 0:
                i = 0
                while i < 5:
                    writer.writerow(emptyLine)
                    i += 1
            for item in thisList:
                writer.writerow(item)
    else:
        for item in listData:
            writer.writerow(item)
    print(outputFile.getvalue(), file=sys.stdout)

## -- STATISTICS PRINTER -- ##
if actionRemoveDuplicates:
    verbose('Duplicates Removed:            ', str(duplicatesRemoved))
if actionRemoveBadEmails:
    verbose('Bad Emails Removed:            ', str(badEmailsRemoved))
    verbose('Bad Emails Fixed:              ', str(badEmailsFixed))
if actionRemoveBlankLines:
    verbose('Blank Lines Removed:           ', str(blankLinesRemoved))
if actionRemoveBlacklist:
    verbose('Blacklist Matches Removed:     ', str(blacklistRemoved))
if actionStripWhitespace:
    verbose('Lines Stripped:                ', str(linesStripped))
if actionRemoveDuplicates or actionRemoveBadEmails or actionRemoveBlankLines or actionRemoveBlacklist or actionSplitList:
    verbose('-------------------------------------------')
    verbose('TOTAL REMOVED:                 ', str(duplicatesRemoved + badEmailsRemoved + blankLinesRemoved + blacklistRemoved))
    verbose('TOTAL ON FINAL LIST:           ', str(len(listData)))
if actionSplitList:
    verbose('EACH LIST:')
    for index, thisList in enumerate(lists):
        verbose('    ', splitFileName[0] + str(index) + '.' + splitFileName[1], ': ', str(len(thisList)))
verbose('Execution Time:', int(round((time.time() - tStart) * 1000)), 'ms')
