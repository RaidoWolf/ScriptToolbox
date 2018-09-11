#!/usr/bin/env python

import os
import sys

def createOggDir (artistDirectory):
    oggdir = os.path.join(artistDirectory, 'ogg')
    if os.path.isdir(oggdir):
        return True
    else:
        if os.path.exists(oggdir):
            return False
        else:
            print("creating directory" + oggdir)
            os.makedirs(oggdir)

for artistDirectory in os.listdir('./'):
    for root, directories, filenames in os.walk(artistDirectory):
        for directory in directories:
            if directory == 'ogg':
                if createOggDir(artistDirectory):
                    sourceDirectory = os.path.join(os.path.abspath(root), directory)
                    targetOggDirectory = os.path.join(artistDirectory, 'ogg')
                    targetLinkName = os.path.basename(os.path.normpath(root))
                    targetLink = os.path.join(targetOggDirectory, targetLinkName)
                    if not os.path.islink(targetLink):
                        print("symlinking \"" + sourceDirectory + "\" >> \"" + targetLink + "\"")
                        os.symlink(sourceDirectory, targetLink)
