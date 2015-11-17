# -*- coding: utf-8 -*-

import subprocess
import os

def createLinks(filenameTuples, target):
    for filenameTuple in filenameTuples:
        subprocess.Popen(getCommand(filenameTuple[0], filenameTuple[1]), cwd=target)
    return filenameTuples
        
def getCommand(name, linktarget):
    return ["ln", "-s", linktarget, name]
    
def getFilenameTuples(filenames, root, extensionToAdd, rejectNonexisting):
    if rejectNonexisting:
        return [(filename + extensionToAdd, os.path.abspath(os.path.join(root, filename + extensionToAdd))) for filename in filenames if os.path.exists(os.path.join(root, filename + extensionToAdd))]
    else:
        return [(filename + extensionToAdd, os.path.abspath(os.path.join(root, filename + extensionToAdd))) for filename in filenames]
    
def create(root, filenames, target, extensionToAdd = ".pdf", rejectNonexisting = True):
    """Create symbolic links to all files listed in filenames based at directory 
    root in directory target. Extension extensionToAdd is added to all filenames. 
    If rejectNonexisting is set, create only links to 
    existing files. Return a list of files for which links were created."""
    return createLinks(getFilenameTuples(filenames, root, extensionToAdd, rejectNonexisting), target)
