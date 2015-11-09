# -*- coding: utf-8 -*-

import subprocess
import os

def createLinks(filenames, target):
    for filename in filenames:
        subprocess.Popen(getCommand(filename), cwd=target)
    return filenames
        
def getCommand(filename):
    return ["ln", "-s", filename]
    
def getAbsoluteFilenames(filenames, root, rejectNonexisting):
    if rejectNonexisting:
        return [os.path.join(root, filename) for filename in filenames if os.path.exists(os.path.join(root, filename))]
    else:
        return [os.path.join(root, filename) for filename in filenames]
    
def create(root, filenames, target, rejectNonexisting = True):
    """Create symbolic links to all files listed in filenames based at directory 
    root in directory target. If rejectNonexisting is set, create only links to 
    existing files. Return a list of files for which links were created."""
    return createLinks(getAbsoluteFilenames(filenames, root, rejectNonexisting), target)
