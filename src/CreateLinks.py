# -*- coding: utf-8 -*-

import subprocess
import os

def createLinks(filenames, target):
    for filename in filenames:
        subprocess.Popen(getCommand(filename), cwd=target)
        
def getCommand(filename):
    return ["ln", "-s", filename]
    
def getAbsoluteFilenames(filenames, root):
    return [os.path.join(root, filename) for filename in filenames]
    
def create(root, filenames, target):
    createLinks(getAbsoluteFilenames(filenames, root), target)
