# -*- coding: utf-8 -*-

import json
import os
import random
import cPickle as pickle
import sys

class CorpusCreator():
    """Class for creating a subcorpus of the given corpus. 
    Features: 
    1. retrieve list of documents having specified keywords
    2. create sample of fixed size (random or arbitrary sample)
    3. copy corresponding documents (metadata or pdf) to specified location
    """

    def __init__(self, jsonCommand):
        self.config = self.loadJson(jsonCommand)
        self.metadata = self.loadMetadata()
        
    def loadJson(self, jsonCommand):
        return json.load(open(jsonCommand, "r"))
    ##unused
    def copyNFiles(self, target, n):
        """Copy a specified number of n files to target."""
        for filename in os.listdir(self.source)[:n+1]:
            shutil.copy(os.path.join(self.source, filename), target)
    ##unused       
    def copyFiles(self, target, filenames):
        """Copy a list of filenames from corpus to target."""
        for filename in filenames:
            shutil.copy(os.path.join(self.source, filename), target)
    ##unused        
    def selectRandomFiles(self, n):
        """Create a sample of n randomly selected filenames."""
        selectedFilenames = set([])
        filenames = os.listdir(self.source)
        # random choice may choose the same file multiple times
        # thus, do not perform choice operation n times but instead perform
        # operation until n filenames are selected
        while len(selectedFilenames) < size:
            selectedFilenames.add(os.path.join(self.source, random.choice(filenames)))
        return selectedFilenames
    
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
    
    def getFilenamesHavingTags(self, tags, dictionary, function):
        matchList = [dictionary.get(tag.encode("utf-8")) for tag in tags]            
        return function(matchList)
          
    def select(self):
        """Select all filenames having the specified tags. 
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
    print "CorpusCreator.py <jsonFile>"
    
    
if __name__=="__main__":
    try:
        creator = CorpusCreator(sys.argv[1])
    except IndexError:
        usage
    
    print len(creator.select())
        
