# -*- coding: utf-8 -*-

import json
import shutil
import os
import xml.etree.ElementTree as ElementTree
import cPickle as pickle
import sys

class MetadataIndexer():
    """Class for parsing econStor and ssoar metadata and saving it to 
    11 indices storing association between documents and: 
    1. subject tags
    1a: subject_ddc tags
    1b: subject_classoz tags
    1c: subject_thesoz tags
    1d: subect_method tags
    2. type tags
    3. ppn and other id tags
    4. language tags
    5. date tags
    6. relation tags
    7. other tags
    Indicies can be loaded and queried using the CorpusCreator class"""
    
    def __init__(self, tagFile, logFile):
        self.tags = self.loadTags(tagFile)

        self.subjectDict = {}
        self.subjectDict_ddc = {}
        self.subjectDict_classoz = {}
        self.subjectDict_thesoz = {}
        self.subjectDict_methods = {}
        self.typeDict = {}
        self.ppnIdDict = {}
        self.langDict = {}
        self.dateDict = {}
        self.relationDict = {}
        self.miscDict = {}
        
        self.log = logFile

    def loadTags(self, tagFile):
        return json.load(open(tagFile, "r"))
        
    def getId(self, part):
        for attribute in part.getchildren():
            if attribute.tag == self.tags.get("identifier"): 
                return attribute.text.replace(self.tags.get("prefix"), "")\
                .replace("/", "-")

    def getDcInfo(self, metadata):
        raise NotImplementedError("Please implement this method according to the metadata schema.")
        
    def parse(self, filename):
        recordData = {}
        try:
            tree = ElementTree.parse(filename)
            record = tree.getroot()
            for part in record.getchildren():
                if part.tag == self.tags.get("header"): 
                    recordId = self.getId(part)
                    print recordId
                if part.tag == self.tags.get("metadata"):
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
        #todo: loop over entries in tags, store dictionaries in a dictionary ;)
        #todo: what happens if key is not in tags? check
        for info in metadata:
            if self.tags.get("subject") in info:
                self.subjectDict = self.addToValues(recordId, self.subjectDict,\
                info.get(self.tags.get("subject")))
            elif self.tags.get("subject_ddc") in info:
                self.subjectDict_ddc = self.addToValues(recordId, self.subjectDict_ddc,\
                info.get(self.tags.get("subject_ddc")))
            elif self.tags.get("subject_classoz") in info:
                self.subjectDict_classoz = self.addToValues(recordId, self.subjectDict_classoz,\
                info.get(self.tags.get("subject_classoz")))
            elif self.tags.get("subject_thesoz") in info:
                self.subjectDict_thesoz = self.addToValues(recordId, self.subjectDict_thesoz,\
                info.get(self.tags.get("subject_thesoz")))
            elif self.tags.get("subject_methods") in info:
                self.subjectDict_methods = self.addToValues(recordId, self.subjectDict_methods,\
                info.get(self.tags.get("subject_methods")))
            elif self.tags.get("type") in info:
                self.typeDict = self.addToValues(recordId, self.typeDict,\
                info.get(self.tags.get("type")))
            elif self.tags.get("ppnIdTag") in info:
                self.ppnIdDict = self.addToValues(recordId, self.ppnIdDict,\
                info.get(self.tags.get("ppnIdTag")))
            elif self.tags.get("language") in info:
                self.langDict = self.addToValues(recordId, self.langDict,\
                info.get(self.tags.get("language")))
            elif self.tags.get("date") in info:
                self.dateDict = self.addToValues(recordId, self.dateDict,\
                info.get(self.tags.get("date")))
            elif self.tags.get("source") in info:
                self.relationDict = self.addToValues(recordId,\
                self.relationDict, info.get(self.tags.get("source")))
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
            
