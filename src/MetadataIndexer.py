# -*- coding: utf-8 -*-

import json
import shutil
import os
import xml.etree.ElementTree as ElementTree
import cPickle as pickle
import sys

class MetadataIndexer():
    """Class for parsing bibliographic metadata files. Saves all metadata to 
    an index: a dictionary storing associations between tags (<- keys) and 
    document IDs (<- values).
    Indicies can be loaded and queried using the CorpusCreator class."""
    
    def __init__(self, tagFile, logFile):
        self.tags = self.loadTags(tagFile)
        self.tagDictionaries = {}
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
            key = str(None).encode('utf-8')
        value = value.encode('utf-8')
        values = dictionary.get(key, [])
        values.append(value)
        dictionary[key] = values
        return dictionary
            
    def updateMetaDicts(self, data):
        recordId, metadata = data
        for info in metadata:
            for key in info.keys():
                #key = key.encode('utf-8')
                tagDict = self.tagDictionaries.get(key.encode('utf-8'), {})
                tagDict = self.addToValues(recordId, tagDict, info.get(key))
                self.tagDictionaries[key.encode('utf-8')] = tagDict

    def exportMetaDicts(self, target):
        pFile = open(target, 'w+')
        pickle.dump(self.tagDictionaries, pFile)
        pFile.close()

