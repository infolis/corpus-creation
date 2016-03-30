# -*- coding: utf-8 -*-

import json
import os
import random
import cPickle as pickle
import sys
import shutil
import CreateLinks

class CorpusCreator():
    """Class for creating a subcorpus of the given corpus. 
    Features: 
    1. retrieve list of documents having specified metadata tags
    2. create random sample of fixed size 
    3. create symbolic links to documents (metadata or pdf) at specified location
    """

    def __init__(self, jsonCommand):
        self.config = self.loadJson(jsonCommand)
        self.metadata = self.loadMetadata()
        
    def loadJson(self, jsonCommand):
        return json.load(open(jsonCommand, "r"))
         
    def selectRandomFiles(self, filenames, n):
        """Create a sample of n randomly selected filenames."""
        if len(filenames) < n:
            print "Warning: source set is smaller than desired sample."
            print "Returning source set."
            return filenames
        selectedFilenames = set([])
        # random choice may choose the same file multiple times
        # thus, do not perform choice operation n times but instead perform
        # operation until n filenames are selected
        while len(selectedFilenames) < n:
            selectedFilenames.add(random.choice(filenames))
        return selectedFilenames
        
    def sample(self, filenames):
        """Create a sample specified size."""
        return self.selectRandomFiles(filenames, int(self.config.get("sample").get("size")))
        
    def createLinks(self, filenames):
        """Create symbolic links to the specified filenames"""
        return CreateLinks.create(self.config.get("createLinks").get("source"), filenames, self.config.get("createLinks").get("target"))      
    
    def getValues(self, element):
        """Return all tags found for element in the metadata"""
        return self.metadata.get(element).keys()
        
    def loadMetadata(self):
        """Unpickle metadata stored in picklePath."""
        pFile = open(self.config.get("picklePath"), "r")
        data = pickle.load(pFile)
        pFile.close()
        return data
    
    def intersect(self, nestedList):
        return list(set.intersection(*map(set, nestedList)))
        
    def union(self, nestedList):
        return list(set.union(*map(set, nestedList)))
    
    def addFilenamesHavingTagPrefix(self, tags, dictionary, matchList):
        tagList = dictionary.keys()
        for tagToSearch in tags:
            tagToSearch = tagToSearch.encode("utf-8")
            if tagToSearch.endswith("*"):
                print "Found prefix query: " + tagToSearch
                for tag in tagList:
                    if tag.startswith(tagToSearch.replace("*","")):
                        print "Found matching tag: " + tag
                        matchList.append(dictionary.get(tag))
        return matchList
        
    def getFilenamesHavingTags(self, tags, dictionary, function):
        matchList = [dictionary.get(tag.encode("utf-8")) for tag in tags if tag.encode("utf-8") in dictionary]
        matchList = self.addFilenamesHavingTagPrefix(tags, dictionary, matchList)
        return function(matchList)
          
    def select(self):
        """Select all filenames having the specified tags or tag prefixes. 
        If intersection flag is set (default), only entries having all specified
        tags are returned. Else, a union of entries having at least one of the 
        tags is returned. Intra: applies to tags inside of one category, 
        inter: applies tags of different categories.
        Example: to use boolean OR for tags in one category (e.g. subject tags) 
        and AND for combination of tags of different categories specify
        "intersectionIntra":"False",
        "intersectionInter":"True".
        """
        matches = []
        function = self.intersect
        if self.config.get("intersectionIntra") == "False":
            function = self.union
            
        toSelect = self.config.get("select")
        for tag in toSelect.keys():
            print "searching for element %s" %tag
            matches.append(self.getFilenamesHavingTags(toSelect.get(tag), self.metadata.get(tag), function))
            
        function = self.intersect
        if self.config.get("intersectionInter") == "False":
            function = self.union
        
        return function(matches)


def usage():
    print "usage: CorpusCreator.py <jsonFile>"
    
    
if __name__=="__main__":
    try:
        creator = CorpusCreator(sys.argv[1])
        selection = creator.select()
        print "Found %d documents" %len(selection)
        sample = selection
        if creator.config.get("sample", False):
            sample = creator.sample(selection)
        if creator.config.get("createLinks", False):
            existingFiles = creator.createLinks(sample)
            try:
                print "Created %d links" %len(existingFiles)
            except TypeError:
                print "Created 0 links" 
        print "Documents in sample:", sample 
        print "Size of sample: %d" %len(sample)
        
    except IndexError:
        usage()
        
