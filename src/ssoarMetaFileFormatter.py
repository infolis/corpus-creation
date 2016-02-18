# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ElementTree
import sys
import os


class ssoarMetaFileFormatter:
    
    def __init__(self, rootDir, targetDir):
        self.rootDir = rootDir
        self.targetDir = targetDir
        self.counter = 0
        
    def formatMetadata(self):
        for filename in os.listdir(self.rootDir):
            for recordId, recordMetadata in self.parseMetadata(os.path.join(self.rootDir, filename)):
                self.writeToFile(recordId, recordMetadata)
    
    def getRootElements(self, root):
        return root
        
    def writeToFile(self, recordId, recordMetadata):
        towrite = ElementTree.ElementTree(recordMetadata)
        towrite.write(os.path.join(self.targetDir, recordId + ".xml"), "utf-8")
        self.counter += 1
        print "wrote %s (file no. %d)." %(os.path.join(self.targetDir, recordId + ".xml"), self.counter)
        
    def parseMetadata(self, filename):
        try:
            tree = ElementTree.parse(filename)
            root = tree.getroot()
            for element in root.getchildren():
                for attribute in element.getchildren():
                    if attribute.tag == "{http://www.openarchives.org/OAI/2.0/}record":
                        for part in attribute.getchildren():
                            if part.tag == "{http://www.openarchives.org/OAI/2.0/}metadata":
                                for dcElement in part.getchildren():
                                    for dcValue in dcElement.getchildren():
                                        if dcValue.get("qualifier") == "uri":
                                            recordId = dcValue.text.replace("http://www.ssoar.info/ssoar/handle/document/", "")
                                            yield recordId, attribute
        except:
            print "Caught error in filename %s." %filename

def usage():
    print "usage: ssoarMetaFileFormatter.py <inputDir> <outputDir>"
        
if __name__=="__main__":
    try:
        inputDir = sys.argv[1]
        outputDir = sys.argv[2]
        formatter = ssoarMetaFileFormatter(inputDir, outputDir)
        formatter.formatMetadata()
    except:
        usage()
    
