# -*- coding: utf-8 -*-

import shutil
import os
import xml.etree.ElementTree as ElementTree
import cPickle as pickle
import sys

class MetaHandler():
    """Class for parsing econStor metadata and saving it to 7 indices storing 
    association between documents and: 
    1. subject tags
    2. type tags
    3. ppn and other id tags
    4. language tags
    5. date tags
    6. relation tags
    7. other tags
    Indicies can be loaded and queried using econCorpusCreator class"""
    
    def __init__(self, logFile):
        self.subjectTag = "{http://purl.org/dc/elements/1.1/}subject"
        self.typeTag = "{http://purl.org/dc/elements/1.1/}type"
        self.ppnIdTag = "{http://purl.org/dc/elements/1.1/}identifier"
        self.langTag = "{http://purl.org/dc/elements/1.1/}language"
        self.dateTag = "{http://purl.org/dc/elements/1.1/}date"
        self.relationTag = "{http://purl.org/dc/elements/1.1/}relation"

        self.subjectDict = {}
        self.typeDict = {}
        self.ppnIdDict = {}
        self.langDict = {}
        self.dateDict = {}
        self.relationDict = {}
        self.miscDict = {}
        
        self.log = logFile

    def getId(self, part):
        for attribute in part.getchildren():
            if attribute.tag == "identifier": 
                return attribute.text.replace("oai:econstor.eu:", "")\
                .replace("/", "-")

    def getDcInfo(self, metadata):
        for dc in metadata.getchildren():
            yield {dc.tag : dc.text}
        
    def parse(self, filename):
        recordData = {}
        try:
            tree = ElementTree.parse(filename)
            record = tree.getroot()
            for part in record.getchildren():
                if part.tag == "header": 
                    recordId = self.getId(part)
                    print recordId
                if part.tag == "metadata":
                    for metadata in part.getchildren():
                        return recordId, self.getDcInfo(metadata)
        except ElementTree.ParseError as e:
            msg = "{0} - ParseError({1}): {2}".format(filename, e.code, e.position)
            sys.stderr.write(msg)
            with open(self.log, "a") as f:
                f.write(msg)
            return "", []
                
    def createMetaDicts(self, path):
        for filename in os.listdir(path):
            self.updateMetaDicts(self.parse(os.path.join(path, filename)))
 
    def addToValues(self, value, dictionary, key):
        try:
            key = key.encode('utf-8')
        # empty tag
        except AttributeError:
            key = u"None"
        value = value.encode('utf-8')
        values = dictionary.get(key, [])
        values.append(value)
        dictionary[key] = values
        return dictionary
            
    def updateMetaDicts(self, data):
        recordId, metadata = data
        for info in metadata:
            if self.subjectTag in info:
                self.subjectDict = self.addToValues(recordId, self.subjectDict,\
                info.get(self.subjectTag))
            elif self.typeTag in info:
                self.typeDict = self.addToValues(recordId, self.typeDict,\
                info.get(self.typeTag))
            elif self.ppnIdTag in info:
                self.ppnIdDict = self.addToValues(recordId, self.ppnIdDict,\
                info.get(self.ppnIdTag))
            elif self.langTag in info:
                self.langDict = self.addToValues(recordId, self.langDict,\
                info.get(self.langTag))
            elif self.dateTag in info:
                self.dateDict = self.addToValues(recordId, self.dateDict,\
                info.get(self.dateTag))
            elif self.relationTag in info:
                self.relationDict = self.addToValues(recordId,\
                self.relationDict, info.get(self.relationTag))
            else:
                self.miscDict = self.addToValues(recordId, self.miscDict,\
                info.get(info.keys()[0]))

    def exportMetaDicts(self, target):
        pFile = open(target, 'w+')
        pickle.dump([self.subjectDict, self.typeDict, self.ppnIdDict,\
        self.langDict, self.dateDict, self.relationDict], pFile)
        pFile.close()
        self.writeToFile(self.subjectDict.keys(), \
        os.path.join(os.path.dirname(target), "subjectTags.csv"))
        self.writeToFile(self.typeDict.keys(), \
        os.path.join(os.path.dirname(target), "typeTags.csv"))
        self.writeToFile(self.ppnIdDict.keys(), \
        os.path.join(os.path.dirname(target), "ppnIdTags.csv"))
        self.writeToFile(self.langDict.keys(), \
        os.path.join(os.path.dirname(target), "langTags.csv"))
        self.writeToFile(self.dateDict.keys(), \
        os.path.join(os.path.dirname(target), "dateTags.csv"))
        self.writeToFile(self.relationDict.keys(), \
        os.path.join(os.path.dirname(target), "relationTags.csv"))
        
    def exportTagLists(self, target):
        pFile = open(target, 'w+')
        pickle.dump([self.subjectDict.keys(), self.typeDict.keys(),\
        self.ppnIdDict.keys(), self.langDict.keys(), self.dateDict.keys(),\
        self.relationDict.keys()], pFile)
        pFile.close()
        
    def writeToFile(self, contentList, target):
        with open(target, "w") as f:
            for item in contentList:
                f.write(item + "\n")
            

if __name__=="__main__":
    handler = MetaHandler("./metaHandler.log")
    handler.createMetaDicts("./econStor_meta/")
    handler.exportMetaDicts("./metadata.pickle")
    handler.exportTagLists("./tags.pickle")
