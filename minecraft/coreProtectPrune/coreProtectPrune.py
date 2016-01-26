#!/usr/bin/env python3

import __future__ #you really should be using python 3 by now.
import sqlite3
from os.path import isfile
from sys import argv, exit, stderr
from yaml import load as loadYaml

config = {
    'defaultBlockEntryLimit':   64,         #default maximum number of entries for each block coordinate
    'defaultBlockTimeLimit':    0,          #default maximum age (in hours) of each block coordinate entry (0 means no limit)
    'defaultTablePrefix':       'co_'       #default prefix for tables in CoreProtect database
}

stats = {}

def error (*msg):
    print('ERROR: ', *msg, file=stderr)
    exit()

SCRIPT_NAME = argv[0]
SCRIPT_ARGS = argv[1:]

#parse command-line arguments
DATABASE_FILENAME = False
CP_CONF_FILENAME =  False
BLOCK_ENTRY_LIMIT = False
BLOCK_TIME_LIMIT =  False
skipNext =          False
for index, arg in enumerate(SCRIPT_ARGS):
    if not skipNext:
        lowerArg = arg.lower()
        #help argument
        if lowerArg == '--help' or lowerArg == '-h':
            print('Usage: ' + SCRIPT_NAME + ' database-file [options]')
            print('    # OPTIONS #')
            print('    --help, -h                       - Display this help information.')
            print('    --block-entries <n>, -be <n>     - Limit entries-per-block to n entries')
            print('    --block-time <n>, -bt <n>        - Limit age of block entries to n hours')
            print('    --cpconfig <file>, -cc <file>    - include CoreProtect config file for auto-detecting things')
            print('    --config <file>, -c <file>       - include CoreProtectPrune config file (does not supersede args)')
        #block entry limit argument
        elif lowerArg == '--block-entries' or arg == '-be':
            BLOCK_ENTRY_LIMIT = SCRIPT_ARGS[index + 1]
            skipNext = True
        #block time limit argument
        elif lowerArg == '--block-time' or arg == '-bt':
            BLOCK_TIME_LIMIT = SCRIPT_ARGS[index + 1]
            skipNext = True
        elif lowerArg == '--cpconfig' or arg == '-cc':
            CP_CONF_FILENAME = SCRIPT_ARGS[index + 1]
            skipNext = True
        elif lowerArg == '--config' or arg == '-c':
            CONF_FILENAME = SCRIPT_ARGS[index + 1]
            skipNext = True
        #unmatched arugment (possibly error, probably database filename)
        else:
            if not DATABASE_FILENAME and isfile(arg):
                DATABASE_FILENAME = arg
            else:
                if DATABASE_FILENAME:
                    error('Caught unrecognized or out-of-place argument: ' + arg)
                else:
                    error('File "' + arg + '" does not exist.')
    else:
        continue
if not DATABASE_FILENAME:
    error('No database file argument detected.')

#connect to the database
db  = sqlite3.connect(DATABASE_FILENAME)
dbc = db.cursor()

def tableExists (table):
    dbc.execute('SELECT name FROM sqlite_master WHERE type='table' AND name='?';', (table,))
    if (dbc.fetchone()):
        return true
    else:
        return false

#get block data from database
if not tableExists(DATABASE_TABLE_PREFIX + 'blocks'):
    error('Table "' + DATABASE_TABLE_PREFIX + 'blocks" does not exist.')
dbc.execute('SELECT * FROM \'' + DATABASE_TABLE_PREFIX + 'block\';')
blocks = dbc.fetchAll()
blockEntryCount = len(blocks)

#find and remove entries past the limited entry count #TODO: This probably uses some serious memory. Optimize this.
blockTree = {}
for block in blocks:
    x = block[3]
    y = block[4]
    z = block[5]
    if x in blockTree:
        if y in blockTree[x]:
            if z not in blockTree[x][y]:
                blockTree[x][y][z] = []
        else:
            blockTree[x][y] = {}
    else:
        blockTree[x] = {}
    blockTree[x][y][z] = block

deleteList = []
for xchunk in blockTree:
    for ychunk in xchunk:
        for zchunk in ychunk:
            length = len(zchunk)
            if length > BLOCK_ENTRY_LIMIT:
                deleteList.append((zchunk[3], zchunk[4], zchunk[5], BLOCK_ENTRY_LIMIT))
dbc.executemany('DELETE FROM \'' + DATABASE_TABLE_PREFIX + 'block\' WHERE (\'x\' = ? AND \'y\' = ? AND \'z\' = ?) OFFSET ?', deleteList)
db.commit()

#close the database connection
db.close()
